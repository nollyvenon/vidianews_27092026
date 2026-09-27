"""API Monitoring & Testing endpoints: Modules 41-45"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.models.api_monitoring import *
from app.services.api_monitoring_service import *
from app.core.auth import get_current_user

router = APIRouter(prefix="/api/v1", tags=["api-monitoring"])


# ==================== MODULE 41: API VERSIONING ====================

@router.post("/versions/endpoint")
async def create_endpoint_version(endpoint: str, version: str, db: AsyncSession = Depends(get_db)):
    service = APIVersionService(db)
    ep = await service.create_endpoint_version(endpoint, version, {})
    return {"id": ep.id, "endpoint": ep.endpoint, "version": ep.version}


@router.get("/versions/{endpoint}")
async def get_endpoint_versions(endpoint: str, db: AsyncSession = Depends(get_db)):
    service = APIVersionService(db)
    ep = await service.get_endpoint_version(endpoint, "v1")
    if not ep:
        return {"error": "Endpoint not found"}
    return {"endpoint": ep.endpoint, "version": ep.version, "deprecated": ep.deprecated}


# ==================== MODULE 42: GRAPHQL ====================

@router.post("/graphql/query")
async def register_graphql_query(name: str, query_string: str, db: AsyncSession = Depends(get_db)):
    service = GraphQLService(db)
    query = await service.register_query(name, query_string, {})
    return {"id": query.id, "name": query.name}


@router.get("/graphql/queries")
async def get_graphql_queries(db: AsyncSession = Depends(get_db)):
    service = GraphQLService(db)
    queries = await service.get_all_queries()
    return [{"id": q.id, "name": q.name, "execution_count": q.execution_count} for q in queries]


@router.post("/graphql/execute")
async def execute_graphql(query_id: int, db: AsyncSession = Depends(get_db)):
    service = GraphQLService(db)
    await service.record_query_execution(query_id, 25.5)
    return {"executed": True}


# ==================== MODULE 43: WEBHOOKS ====================

@router.post("/webhooks/register")
async def register_webhook(url: str, event_type: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = WebhookService(db)
    webhook = await service.register_webhook(user["id"], url, event_type)
    return {"id": webhook.id, "url": webhook.url, "event_type": webhook.event_type}


@router.get("/webhooks")
async def get_webhooks(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = WebhookService(db)
    webhooks = await service.get_user_webhooks(user["id"])
    return [{"id": w.id, "url": w.url, "status": w.status} for w in webhooks]


@router.post("/webhooks/{webhook_id}/event")
async def record_webhook_event(webhook_id: int, event_type: str, db: AsyncSession = Depends(get_db)):
    service = WebhookService(db)
    event = await service.record_event(webhook_id, event_type, {})
    return {"id": event.id, "webhook_id": webhook_id}


# ==================== MODULE 44: TESTING ====================

@router.post("/testing/suite")
async def create_test_suite(name: str, test_count: int, db: AsyncSession = Depends(get_db)):
    service = TestingService(db)
    suite = await service.create_test_suite(name, test_count)
    return {"id": suite.id, "name": suite.name, "test_count": suite.test_count}


@router.post("/testing/result")
async def record_test_result(suite_id: int, test_name: str, status: str, db: AsyncSession = Depends(get_db)):
    service = TestingService(db)
    result = await service.record_test_result(suite_id, test_name, status, 150.5)
    return {"id": result.id, "test_name": result.test_name, "status": result.status}


@router.put("/testing/suite/{suite_id}/stats")
async def update_suite_stats(suite_id: int, passed: int, failed: int, coverage: float, db: AsyncSession = Depends(get_db)):
    service = TestingService(db)
    await service.update_suite_stats(suite_id, passed, failed, coverage)
    return {"updated": True}


# ==================== MODULE 45: MONITORING ====================

@router.post("/monitoring/metric")
async def record_metric(metric_type: str, value: float, db: AsyncSession = Depends(get_db)):
    service = MonitoringService(db)
    metric = await service.record_metric(metric_type, value)
    return {"id": metric.id, "metric_type": metric.metric_type, "value": metric.value}


@router.post("/monitoring/alert")
async def create_alert(metric_type: str, severity: str, threshold: float, current: float, message: str, db: AsyncSession = Depends(get_db)):
    service = MonitoringService(db)
    alert = await service.create_alert(metric_type, severity, threshold, current, message)
    return {"id": alert.id, "severity": alert.severity}


@router.get("/monitoring/alerts")
async def get_alerts(db: AsyncSession = Depends(get_db)):
    service = MonitoringService(db)
    alerts = await service.get_alerts()
    return [{"id": a.id, "severity": a.severity, "message": a.message} for a in alerts]


@router.put("/monitoring/alert/{alert_id}/resolve")
async def resolve_alert(alert_id: int, db: AsyncSession = Depends(get_db)):
    service = MonitoringService(db)
    await service.resolve_alert(alert_id)
    return {"resolved": True}


@router.post("/monitoring/health")
async def record_health_check(service_name: str, status: str, response_time_ms: float, db: AsyncSession = Depends(get_db)):
    service_obj = MonitoringService(db)
    check = await service_obj.record_health_check(service_name, status, response_time_ms)
    return {"id": check.id, "service": service_name, "status": status}
