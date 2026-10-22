"""Services module.

Services are imported from their own modules (e.g. app.services.auth_service);
this package no longer eagerly imports every service so one broken legacy
module cannot prevent unrelated ones (such as app.services.news) from loading.
"""
