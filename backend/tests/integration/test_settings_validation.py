"""Route tests for settings: every editable field is accepted, persisted and validated"""

import pytest


class TestSettingsValidation:
    async def test_every_notification_field_is_saved_and_returned(self, async_client, org_member):
        update = {
            "email_on_activity": False, "email_on_mention": True, "email_on_message": False, "email_digest": "weekly",
            "push_enabled": True, "push_on_activity": True, "push_on_message": False,
            "inapp_enabled": False, "inapp_sound": True, "dnd_enabled": True,
            "dnd_start_time": "22:30", "dnd_end_time": "07:00",
        }
        saved = await async_client.put("/api/v1/settings/me/notifications", json=update, headers=org_member)
        loaded = await async_client.get("/api/v1/settings/me", headers=org_member)

        assert saved.status_code == 200
        assert loaded.status_code == 200
        notifications = loaded.json()["notifications"]
        for key, value in update.items():
            assert notifications[key] == value

    async def test_do_not_disturb_times_must_be_clock_times(self, async_client, org_member):
        response = await async_client.put(
            "/api/v1/settings/me/notifications", json={"dnd_start_time": "25:00"}, headers=org_member
        )

        assert response.status_code == 422

    async def test_empty_do_not_disturb_time_is_refused_so_the_client_must_send_null(self, async_client, org_member):
        response = await async_client.put(
            "/api/v1/settings/me/notifications", json={"dnd_end_time": ""}, headers=org_member
        )

        assert response.status_code == 422

    async def test_null_do_not_disturb_time_clears_it(self, async_client, org_member):
        await async_client.put("/api/v1/settings/me/notifications", json={"dnd_start_time": "22:00"}, headers=org_member)

        cleared = await async_client.put(
            "/api/v1/settings/me/notifications", json={"dnd_start_time": None}, headers=org_member
        )
        loaded = await async_client.get("/api/v1/settings/me", headers=org_member)

        assert cleared.status_code == 200
        assert loaded.json()["notifications"]["dnd_start_time"] is None

    async def test_unknown_digest_is_refused(self, async_client, org_member):
        response = await async_client.put(
            "/api/v1/settings/me/notifications", json={"email_digest": "hourly"}, headers=org_member
        )

        assert response.status_code == 422

    async def test_every_privacy_field_is_saved_and_returned(self, async_client, org_member):
        update = {
            "profile_visibility": "friends_only", "show_email": True, "show_phone": False, "show_activity": False,
            "show_last_seen": False, "allow_messages": "nobody", "allow_search": False, "allow_analytics": False,
            "allow_marketing_emails": True, "allow_third_party_sharing": True,
        }
        saved = await async_client.put("/api/v1/settings/me/privacy", json=update, headers=org_member)
        loaded = await async_client.get("/api/v1/settings/me", headers=org_member)

        assert saved.status_code == 200
        privacy = loaded.json()["privacy"]
        for key, value in update.items():
            assert privacy[key] == value

    async def test_privacy_choices_outside_the_allowed_values_are_refused(self, async_client, org_member):
        visibility = await async_client.put(
            "/api/v1/settings/me/privacy", json={"profile_visibility": "secret"}, headers=org_member
        )
        messages = await async_client.put(
            "/api/v1/settings/me/privacy", json={"allow_messages": "followers"}, headers=org_member
        )

        assert visibility.status_code == 422
        assert messages.status_code == 422

    async def test_every_display_field_is_saved_and_returned(self, async_client, org_member):
        update = {
            "theme": "dark", "language": "fr", "timezone": "Europe/Paris", "date_format": "DD/MM/YYYY",
            "time_format": "12h", "sidebar_collapsed": True, "compact_mode": True, "animations_enabled": False,
            "font_size": "large",
        }
        saved = await async_client.put("/api/v1/settings/me/display", json=update, headers=org_member)
        loaded = await async_client.get("/api/v1/settings/me", headers=org_member)

        assert saved.status_code == 200
        display = loaded.json()["display"]
        for key, value in update.items():
            assert display[key] == value

    async def test_display_choices_outside_the_allowed_values_are_refused(self, async_client, org_member):
        theme = await async_client.put("/api/v1/settings/me/display", json={"theme": "neon"}, headers=org_member)
        font = await async_client.put("/api/v1/settings/me/display", json={"font_size": "huge"}, headers=org_member)
        language = await async_client.put("/api/v1/settings/me/display", json={"language": "x"}, headers=org_member)

        assert theme.status_code == 422
        assert font.status_code == 422
        assert language.status_code == 422

    async def test_settings_require_a_signed_in_user(self, async_client):
        response = await async_client.get("/api/v1/settings/me")

        assert response.status_code in (401, 403)
