"""API v1 router.

Routers are loaded one by one; a router that fails to import is logged and
skipped so that the remaining API stays available.
"""

import importlib
import logging

from fastapi import APIRouter

_log = logging.getLogger(__name__)

api_router = APIRouter()

# (module, prefix, tag)
_ROUTERS = [
    ("health", "", "health"),
    ("auth", "/auth", "auth"),
    ("tenants", "", "tenants"),
    ("organizations", "", "organizations"),
    ("profiles", "", "profiles"),
    ("settings", "", "settings"),
    ("notifications", "", "notifications"),
    ("activity", "/activity", "activity"),
    ("content", "", "content"),
    ("ai_providers", "", "ai-providers"),
    ("ai_core", "", "ai-core"),
    ("ai_advanced", "", "ai-advanced"),
    ("integrations", "", "system"),
    ("advanced_features", "", "advanced"),
    ("monetization", "", "monetization"),
    ("security_performance", "", "security"),
    ("api_monitoring", "", "api-monitoring"),
    ("logging_analytics", "", "logging-analytics"),
    ("social_messaging", "", "social-messaging"),
    ("streaming_premium", "", "streaming-premium"),
    ("community_compliance", "", "community-compliance"),
    ("content_quality", "", "content-quality"),
    ("publishing_distribution", "", "publishing-distribution"),
    ("user_management", "", "user-management"),
    ("enterprise_features", "", "enterprise-features"),
    ("analytics_reporting", "", "analytics-reporting"),
    ("platform_completion", "", "platform-completion"),
    ("advanced_platform", "", "advanced-platform"),
    ("ecommerce", "", "ecommerce"),
    ("ecommerce_extended", "", "ecommerce-extended"),
    ("marketing", "", "marketing"),
    ("memberships", "", "memberships"),
    ("courses", "", "courses"),
    ("analytics_admin", "", "analytics-admin"),
    ("news", "/news", "news"),
]

ROUTER_LOAD_FAILURES = {}

for _module, _prefix, _tag in _ROUTERS:
    try:
        _mod = importlib.import_module(f"{__name__}.{_module}")
        api_router.include_router(_mod.router, prefix=_prefix, tags=[_tag])
    except Exception as exc:  # noqa: BLE001 - legacy routers may fail in many ways
        ROUTER_LOAD_FAILURES[_module] = repr(exc)
        _log.warning("router %s failed to load: %r", _module, exc)

__all__ = ["api_router", "ROUTER_LOAD_FAILURES"]
