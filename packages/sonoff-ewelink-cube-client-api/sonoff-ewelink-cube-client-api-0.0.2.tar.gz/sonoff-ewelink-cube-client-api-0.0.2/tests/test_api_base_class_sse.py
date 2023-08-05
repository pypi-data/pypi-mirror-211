import asyncio
import aiohttp
from typing import Dict, Any, Optional
from unittest.mock import AsyncMock, MagicMock
from sonoff_ewelink_cube_client_api import IHostClass

# Tesztesetek a BaseClassSse osztályra
class TestBaseClassSse:
    async def test_init_sse_without_ip(self):
        base_sse = IHostClass(ip='127.0.0.1')
        base_sse.ip = None
        base_sse.at = "access_token"

        result = await base_sse.init_sse()

        assert result == {"error": 1000, "msg": "ip is needed", "data": {}}

    async def test_init_sse_without_at(self):
        base_sse = IHostClass(ip='127.0.0.1')
        base_sse.ip = "127.0.0.1"
        base_sse.at = None

        result = await base_sse.init_sse()

        assert result == {"error": 1000, "msg": "at is needed", "data": {}}

    async def test_handle_event_with_valid_event_data(self):
        base_sse = IHostClass(ip='127.0.0.1')
        base_sse.handle_event = MagicMock()

        await base_sse.handle_event("event_name", '{"key": "value"}')

        base_sse.handle_event.assert_called_with("event_name", '{"key": "value"}')

    async def test_handle_event_with_invalid_event_data(self):
        base_sse = IHostClass(ip='127.0.0.1')
        base_sse.handle_event = MagicMock()

        await base_sse.handle_event("event_name", 'invalid_json')

        base_sse.handle_event.assert_not_called()

    def test_mount_sse_func(self):
        base_sse = IHostClass(ip='127.0.0.1')
        base_sse.event = MagicMock()

        handler = MagicMock()
        handler.onopen = MagicMock()
        handler.onerror = MagicMock()
        handler.onAddDevice = MagicMock()
        handler.onUpdateDeviceState = MagicMock()
        handler.onUpdateDeviceInfo = MagicMock()
        handler.onUpdateDeviceOnline = MagicMock()
        handler.onDeleteDevice = MagicMock()

        result = base_sse.mount_sse_func(handler)

        base_sse.event.on_open.assert_called_with(handler.onopen)
        base_sse.event.on_error.assert_called_with(handler.onerror)
        base_sse.event.register_event_listener.assert_any_call('device#v1#addDevice', handler.onAddDevice)
        base_sse.event.register_event_listener.assert_any_call('device#v1#updateDeviceState', handler.onUpdateDeviceState)
        base_sse.event.register_event_listener.assert_any_call('device#v1#updateDeviceInfo', handler.onUpdateDeviceInfo)
        base_sse.event.register_event_listener.assert_any_call('device#v1#updateDeviceOnline', handler.onUpdateDeviceOnline)
        base_sse.event.register_event_listener.assert_any_call('device#v1#deleteDevice', handler.onDeleteDevice)

        assert result is None

    def test_unmount_sse_func(self):
        base_sse = IHostClass(ip='127.0.0.1')
        base_sse.event = MagicMock()

        base_sse.unmount_sse_func()

        base_sse.event.remove_event_listener.assert_any_call('device#v1#addDevice')
        base_sse.event.remove_event_listener.assert_any_call('device#v1#updateDeviceState')
        base_sse.event.remove_event_listener.assert_any_call('device#v1#updateDeviceInfo')
        base_sse.event.remove_event_listener.assert_any_call('device#v1#updateDeviceOnline')
        base_sse.event.remove_event_listener.assert_any_call('device#v1#deleteDevice')
        base_sse.event.close.assert_called_once()

# Aszinkron tesztek futtatása
asyncio.run(TestBaseClassSse.test_init_sse_without_ip())
asyncio.run(TestBaseClassSse.test_init_sse_without_at())
asyncio.run(TestBaseClassSse.test_handle_event_with_valid_event_data())
asyncio.run(TestBaseClassSse.test_handle_event_with_invalid_event_data())
asyncio.run(TestBaseClassSse.test_mount_sse_func())
asyncio.run(TestBaseClassSse.test_unmount_sse_func())
