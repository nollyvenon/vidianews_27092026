"""Database models.

Each model module is imported independently so that a defect in one legacy
module is logged instead of preventing the whole application from starting.
"""

import importlib
import logging

_log = logging.getLogger(__name__)

_MODULES = [
    "user", "activity_logs", "content", "ai_providers", "ai_core", "ai_advanced",
    "integrations", "advanced_features", "monetization", "security_performance",
    "api_monitoring", "logging_analytics", "social_messaging", "streaming_premium",
    "community_compliance", "content_quality", "publishing_distribution",
    "user_management", "enterprise_features", "analytics_reporting",
    "platform_completion", "advanced_platform", "ecommerce", "ecommerce_extended",
    "marketing", "memberships", "courses", "analytics_admin", "tenants",
    "organizations", "profiles", "settings", "notifications", "rbac", "news",
]

LOAD_FAILURES = {}

for _name in _MODULES:
    try:
        _mod = importlib.import_module(f"{__name__}.{_name}")
    except Exception as exc:  # noqa: BLE001 - legacy modules may fail in many ways
        LOAD_FAILURES[_name] = repr(exc)
        _log.warning("models.%s failed to load: %r", _name, exc)
        continue
    for _attr in getattr(_mod, "__all__", None) or [a for a in vars(_mod) if not a.startswith("_")]:
        globals().setdefault(_attr, getattr(_mod, _attr))
