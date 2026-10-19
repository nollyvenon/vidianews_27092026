"""API Monitoring & Testing endpoints: Modules 41-45"""

from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, Optional
from app.db.session import get_db
from app.models.api_monitoring import *
from app.services.api_monitoring_service import *
from app.services.graphql_explorer import MAX_QUERY_LENGTH, schema_summary
from app.core.security import get_current_user

router = APIRouter(tags=["api-monitoring"])


# ==================== MODULE 41: API VERSIONING ====================

@router.post("/versions/endpoint")
async def create_endpoint_version(endpoint: str, version: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = APIVersionService(db)
    ep = await service.create_endpoint_version(endpoint, version, {})
    return {"id": ep.id, "endpoint": ep.endpoint, "version": ep.version}


def _version_value(value) -> str:
    return value.value if hasattr(value, "value") else str(value)


@router.get("/versions")
async def list_endpoint_versions(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Every registered endpoint version, grouped by endpoint"""
    rows = await APIVersionService(db).list_endpoint_versions()
    return [
        {
            "id": row.id,
            "endpoint": row.endpoint,
            "version": _version_value(row.version),
            "deprecated": bool(row.deprecated),
            "sunset_date": row.sunset_date.isoformat() if row.sunset_date else None,
        }
        for row in rows
    ]


@router.get("/versions/migrations")
async def list_version_migrations(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Planned and completed migrations between API versions"""
    rows = await APIVersionService(db).list_migrations()
    return [
        {
            "id": row.id,
            "old_version": _version_value(row.old_version),
            "new_version": _version_value(row.new_version),
            "status": row.status,
            "executed_at": row.executed_at.isoformat() if row.executed_at else None,
        }
        for row in rows
    ]


@router.get("/versions/{endpoint}")
async def get_endpoint_versions(endpoint: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = APIVersionService(db)
    ep = await service.get_endpoint_version(endpoint, "v1")
    if not ep:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return {"endpoint": ep.endpoint, "version": ep.version, "deprecated": ep.deprecated}


# ==================== MODULE 42: GRAPHQL ====================

class GraphQLQueryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    query_string: str = Field(min_length=1, max_length=MAX_QUERY_LENGTH)


class GraphQLExecuteRequest(BaseModel):
    query_id: int
    variables: Optional[Dict[str, Any]] = None


class GraphQLRunRequest(BaseModel):
    query: str = Field(min_length=1, max_length=MAX_QUERY_LENGTH)
    variables: Optional[Dict[str, Any]] = None


@router.post("/graphql/query", status_code=201)
async def register_graphql_query(request: GraphQLQueryRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Save a query so it appears in the explorer and its executions are measured"""
    service = GraphQLService(db)
    query = await service.register_query(request.name, request.query_string, {})
    return {"id": query.id, "name": query.name}


@router.get("/graphql/queries")
async def get_graphql_queries(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = GraphQLService(db)
    queries = await service.get_all_queries()
    return [
        {
            "id": q.id,
            "name": q.name,
            "query_string": q.query_string,
            "execution_count": q.execution_count or 0,
            "avg_execution_time_ms": round(q.avg_execution_time_ms or 0.0, 3),
        }
        for q in queries
    ]


@router.get("/graphql/schema")
async def get_graphql_schema(current_user: User = Depends(get_current_user)):
    """The types and fields the explorer can query"""
    return {"types": schema_summary()}


@router.post("/graphql/execute")
async def execute_graphql(request: GraphQLExecuteRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Run a saved query and record its measured execution time"""
    service = GraphQLService(db)
    try:
        return await service.execute_stored_query(request.query_id, request.variables)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/graphql/run")
async def run_graphql(request: GraphQLRunRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Run a query typed into the explorer, without saving it"""
    service = GraphQLService(db)
    try:
        return await service.run_ad_hoc(request.query, request.variables)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


# ==================== MODULE 43: WEBHOOKS ====================

@router.post("/webhooks/register")
async def register_webhook(url: str, event_type: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    service = WebhookService(db)
    webhook = await service.register_webhook(user.id, url, event_type)
    return {"id": webhook.id, "url": webhook.url, "event_type": webhook.event_type}


@router.get("/webhooks")
async def get_webhooks(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    service = WebhookService(db)
    webhooks = await service.get_user_webhooks(user.id)
    return [{"id": w.id, "url": w.url, "status": w.status} for w in webhooks]


@router.post("/webhooks/{webhook_id}/event")
async def record_webhook_event(webhook_id: int, event_type: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = WebhookService(db)
    event = await service.record_event(webhook_id, event_type, {})
    return {"id": event.id, "webhook_id": webhook_id}


# ==================== MODULE 44: TESTING ====================

@router.get("/testing/suites")
async def list_test_suites(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Test suites with their most recently recorded results"""
    suites = await TestingService(db).list_test_suites()
    return [
        {
            "id": suite.id,
            "name": suite.name,
            "test_count": suite.test_count or 0,
            "passed": suite.passed or 0,
            "failed": suite.failed or 0,
            "skipped": suite.skipped or 0,
            "coverage_percentage": round(suite.coverage_percentage or 0.0, 1),
            "last_run_at": suite.last_run_at.isoformat() if suite.last_run_at else None,
        }
        for suite in suites
    ]


@router.post("/testing/suite")
async def create_test_suite(name: str, test_count: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = TestingService(db)
    suite = await service.create_test_suite(name, test_count)
    return {"id": suite.id, "name": suite.name, "test_count": suite.test_count}


@router.post("/testing/result")
async def record_test_result(suite_id: int, test_name: str, status: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = TestingService(db)
    result = await service.record_test_result(suite_id, test_name, status, 150.5)
    return {"id": result.id, "test_name": result.test_name, "status": result.status}


@router.put("/testing/suite/{suite_id}/stats")
async def update_suite_stats(suite_id: int, passed: int, failed: int, coverage: float, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = TestingService(db)
    await service.update_suite_stats(suite_id, passed, failed, coverage)
    return {"updated": True}


# ==================== MODULE 45: MONITORING ====================

@router.post("/monitoring/metric")
async def record_metric(metric_type: str, value: float, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = MonitoringService(db)
    metric = await service.record_metric(metric_type, value)
    return {"id": metric.id, "metric_type": metric.metric_type, "value": metric.value}


@router.post("/monitoring/alert")
async def create_alert(metric_type: str, severity: str, threshold: float, current: float, message: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = MonitoringService(db)
    alert = await service.create_alert(metric_type, severity, threshold, current, message)
    return {"id": alert.id, "severity": alert.severity}


@router.get("/monitoring/alerts")
async def get_alerts(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = MonitoringService(db)
    alerts = await service.get_alerts()
    return [{"id": a.id, "severity": a.severity, "message": a.message} for a in alerts]


@router.put("/monitoring/alert/{alert_id}/resolve")
async def resolve_alert(alert_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = MonitoringService(db)
    await service.resolve_alert(alert_id)
    return {"resolved": True}


@router.post("/monitoring/health")
async def record_health_check(service_name: str, status: str, response_time_ms: float, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service_obj = MonitoringService(db)
    check = await service_obj.record_health_check(service_name, status, response_time_ms)
    return {"id": check.id, "service": service_name, "status": status}
