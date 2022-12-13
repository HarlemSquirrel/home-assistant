"""Config flow for Vivotek integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries, data_entry_flow
from homeassistant.const import (
    CONF_AUTHENTICATION,
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_SSL,
    CONF_USERNAME,
    CONF_VERIFY_SSL,
    HTTP_BASIC_AUTHENTICATION,
    HTTP_DIGEST_AUTHENTICATION,
)
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .camera import DEFAULT_NAME, DEFAULT_SECURITY_LEVEL, DEFAULT_STREAM_SOURCE
from .const import CONF_FRAMERATE, CONF_SECURITY_LEVEL, CONF_STREAM_PATH, DOMAIN

TITLE = "Vivotek"


class VivotekConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Vivotek."""

    async def _show_setup_form(self, step_id: str) -> FlowResult:
        return self.async_show_form(
            step_id=step_id,
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_IP_ADDRESS): cv.string,
                    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                    vol.Required(CONF_PASSWORD): cv.string,
                    vol.Required(CONF_USERNAME): cv.string,
                    vol.Optional(
                        CONF_AUTHENTICATION, default=HTTP_BASIC_AUTHENTICATION
                    ): vol.In([HTTP_BASIC_AUTHENTICATION, HTTP_DIGEST_AUTHENTICATION]),
                    vol.Optional(CONF_SSL, default=False): cv.boolean,
                    vol.Optional(CONF_VERIFY_SSL, default=True): cv.boolean,
                    vol.Optional(CONF_FRAMERATE, default=2): cv.positive_int,
                    vol.Optional(
                        CONF_SECURITY_LEVEL, default=DEFAULT_SECURITY_LEVEL
                    ): cv.string,
                    vol.Optional(
                        CONF_STREAM_PATH, default=DEFAULT_STREAM_SOURCE
                    ): cv.string,
                }
            ),
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initiated by the user."""

        # Request user input, unless we are preparing discovery flow
        if user_input is None:
            return await self._show_setup_form(step_id="user")

        return self.async_create_entry(
            title=TITLE,
            data=user_input,
        )
