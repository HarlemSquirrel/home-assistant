"""Tests for Vivotek config flow."""

from unittest.mock import MagicMock, patch

from libpyvivotek import VivotekCamera

from homeassistant.components.vivotek.const import (
    CONF_FRAMERATE,
    CONF_SECURITY_LEVEL,
    CONF_STREAM_PATH,
    DOMAIN,
)
from homeassistant.config_entries import SOURCE_USER
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
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import entity_registry


def mock_camera():
    """Mock Projector."""
    cam = VivotekCamera(host="1.1.1.1", sec_lvl="admin")

    # cam.model_name = MagicMo
    # proj.authenticate = MagicMock()
    # proj.get_manufacturer = MagicMock(return_value="FakeManufacterer")
    # proj.get_product_name = MagicMock(return_value="FakeModel")
    # proj.get_name = MagicMock(return_value="FakeName")
    # proj.get_inputs = MagicMock(return_value=[["DIGITAL", 1], ["VIDEO", 2]])
    # proj.get_power = MagicMock(return_value="off")
    # proj.get_mute = MagicMock(return_value=(True, False))
    # proj.set_power = MagicMock()
    # proj.set_mute = MagicMock()
    # proj.set_input = MagicMock()

    # return proj
    cam.model_name = MagicMock(return_value="FakeModel")
    cam.get_param = MagicMock(return_value="FakeParamVal")

    return cam


async def test_full_user_flow(hass: HomeAssistant) -> None:
    """Test the full user configuration flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result.get("type") == FlowResultType.FORM
    assert result.get("step_id") == SOURCE_USER
    assert "flow_id" in result

    mock_user_input_data = {
        CONF_NAME: "new cam",
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_SSL: True,
        CONF_VERIFY_SSL: True,
        CONF_USERNAME: "someone",
        CONF_PASSWORD: "letmein",
        CONF_SECURITY_LEVEL: "admin",
    }

    # with patch.object(
    #     VivotekCamera, "from_address", timeout=True, return_value=mock_projector()
    # ):
    with patch(
        "libpyvivotek.VivotekCamera", model_name="FakeModel", get_param="FakeParamVal"
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=mock_user_input_data
        )

    assert result.get("type") == FlowResultType.CREATE_ENTRY
    assert result.get("title") == "Vivotek"
    assert result.get("data") == {
        "authentication": "basic",
        "framerate": 2,
        "ip_address": "1.1.1.1",
        "name": "new cam",
        "password": "letmein",
        "security_level": "admin",
        "ssl": True,
        "stream_path": "live.sdp",
        "username": "someone",
        "verify_ssl": True,
    }

    registry = entity_registry.async_get(hass)
    entry = registry.async_get("camera.FakeParamVal")
    assert entry.unique_id == "FakeParamVal"
