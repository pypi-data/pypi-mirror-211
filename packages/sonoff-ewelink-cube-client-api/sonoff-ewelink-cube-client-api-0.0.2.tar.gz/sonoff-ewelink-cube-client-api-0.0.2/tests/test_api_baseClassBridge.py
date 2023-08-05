import unittest
from unittest.mock import MagicMock, patch
import asyncio

from sonoff_ewelink_cube_client_api.api.baseClassBridge import BaseClassBridge


class TestBaseClassBridge(unittest.TestCase):

    @patch('sonoff_ewelink_cube.api.baseClassBridge.httpRequest')
    @patch('asyncio.sleep')
    @patch('asyncio.gather')
    @patch('asyncio.wait_for')
    def test_getBridgeAT(self, mock_wait_for: MagicMock, mock_gather: MagicMock, mock_sleep: MagicMock, mock_httpRequest: MagicMock):
        async def run_test():
            base_class_bridge = BaseClassBridge()
            timeout = 120000
            interval = 2000

            # Mock response data
            response_data = {'error': 0, 'data': {'token': 'access_token'}}

            # Mock the httpRequest method
            base_class_bridge.httpRequest = mock_httpRequest
            mock_httpRequest.return_value = response_data

            # Mock the asyncio functions
            mock_wait_for.return_value = response_data
            mock_gather.return_value = [response_data]

            # Call the method under test
            result = await base_class_bridge.getBridgeAT(timeout, interval)

            # Assertions
            mock_httpRequest.assert_called_once_with(path='bridge_token_path', method='GET', isNeedAT=False)
            mock_wait_for.assert_called_once_with(mock_gather.return_value, timeout=timeout / 1000)
            mock_gather.assert_called_once_with(mock_httpRequest.return_value, base_class_bridge.interval.clear())
            mock_sleep.assert_called_once_with(interval / 1000)
            self.assertEqual(result, response_data)

        asyncio.run(run_test())

    @patch('sonoff_ewelink_cube.api.baseClassBridge.httpRequest')
    def test_updateBridgeConfig(self, mock_httpRequest: MagicMock):
        async def run_test():
            base_class_bridge = BaseClassBridge()
            volume = 50

            # Mock response data
            response_data = {'error': 0, 'data': {}}

            # Mock the httpRequest method
            base_class_bridge.httpRequest = mock_httpRequest
            mock_httpRequest.return_value = response_data

            # Call the method under test
            result = await base_class_bridge.updateBridgeConfig(volume)

            # Assertions
            mock_httpRequest.assert_called_once_with(path='bridge_config_path', method='PUT', params={'volume': volume})
            self.assertEqual(result, response_data)

        asyncio.run(run_test())

    @patch('sonoff_ewelink_cube.api.baseClassBridge.httpRequest')
    def test_getBridgeInfo(self, mock_httpRequest: MagicMock):
        async def run_test():
            base_class_bridge = BaseClassBridge()

            # Mock response data
            response_data = {'error': 0, 'data': {'gateway_info': 'info'}}

            # Mock the httpRequest method
            base_class_bridge.httpRequest = mock_httpRequest
            mock_httpRequest.return_value = response_data

            # Call the method under test
            result = await base_class_bridge.getBridgeInfo()

            # Assertions
            mock_httpRequest.assert_called_once_with(path='bridge_path', method='GET', isNeedAT=False)
            self.assertEqual(result, response_data)

        asyncio.run(run_test())
import unittest
from unittest.mock import MagicMock, patch
import asyncio

from sonoff_ewelink_cube_client_api.api.baseClassBridge import BaseClassBridge


class TestBaseClassBridge(unittest.TestCase):

    @patch('sonoff_ewelink_cube.api.baseClassBridge.httpRequest')
    @patch('asyncio.sleep')
    @patch('asyncio.gather')
    @patch('asyncio.wait_for')
    def test_getBridgeAT(self, mock_wait_for: MagicMock, mock_gather: MagicMock, mock_sleep: MagicMock, mock_httpRequest: MagicMock):
        async def run_test():
            base_class_bridge = BaseClassBridge()
            timeout = 120000
            interval = 2000

            # Mock response data
            response_data = {'error': 0, 'data': {'token': 'access_token'}}

            # Mock the httpRequest method
            base_class_bridge.httpRequest = mock_httpRequest
            mock_httpRequest.return_value = response_data

            # Mock the asyncio functions
            mock_wait_for.return_value = response_data
            mock_gather.return_value = [response_data]

            # Call the method under test
            result = await base_class_bridge.getBridgeAT(timeout, interval)

            # Assertions
            mock_httpRequest.assert_called_once_with(path='bridge_token_path', method='GET', isNeedAT=False)
            mock_wait_for.assert_called_once_with(mock_gather.return_value, timeout=timeout / 1000)
            mock_gather.assert_called_once_with(mock_httpRequest.return_value, base_class_bridge.interval.clear())
            mock_sleep.assert_called_once_with(interval / 1000)
            self.assertEqual(result, response_data)

        asyncio.run(run_test())

    @patch('sonoff_ewelink_cube.api.baseClassBridge.httpRequest')
    def test_updateBridgeConfig(self, mock_httpRequest: MagicMock):
        async def run_test():
            base_class_bridge = BaseClassBridge()
            volume = 50

            # Mock response data
            response_data = {'error': 0, 'data': {}}

            # Mock the httpRequest method
            base_class_bridge.httpRequest = mock_httpRequest
            mock_httpRequest.return_value = response_data

            # Call the method under test
            result = await base_class_bridge.updateBridgeConfig(volume)

            # Assertions
            mock_httpRequest.assert_called_once_with(path='bridge_config_path', method='PUT', params={'volume': volume})
            self.assertEqual(result, response_data)

        asyncio.run(run_test())

    @patch('sonoff_ewelink_cube.api.baseClassBridge.httpRequest')
    def test_getBridgeInfo(self, mock_httpRequest: MagicMock):
        async def run_test():
            base_class_bridge = BaseClassBridge()

            # Mock response data
            response_data = {'error': 0, 'data': {'gateway_info': 'info'}}

            # Mock the httpRequest method
            base_class_bridge.httpRequest = mock_httpRequest
            mock_httpRequest.return_value = response_data

            # Call the method under test
            result = await base_class_bridge.getBridgeInfo()

            # Assertions
            mock_httpRequest.assert_called_once_with(path='bridge_path', method='GET', isNeedAT=False)
            self.assertEqual(result, response_data)

        asyncio.run(run_test())
