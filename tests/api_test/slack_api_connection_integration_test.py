from src.api import slack_api_connection
from src.chatbot import cadocs_slack
from src.service import utils
from src.chatbot.cadocs_slack import CadocsSlack
from src.intent_handling.cadocs_intents import CadocsIntents
from service.language_handler import LanguageHandler
import pytest
import requests
from unittest.mock import Mock, patch


class TestSlackAPIConnectionIT:
    
    # This variable is used to set the current language for each test method
    language_handler = LanguageHandler()

    def mock_handle_request(self):
        return "test_value"

    def test_handle_request(self, mocker):

        data_test = {"channel": {"id": 1},
                     "user": {"id": "id_test"},
                     "actions": [{"action_id": "action-yes"}],
                     "message": {"ts": 10}}

        self.language_handler.detect_language("Text in English")

        event = {
            "client_msg_id": "msg_test",
            "user": "user_test",
            "text": "can you detect community smells in this repo https://github.com/tensorflow/ranking ?",
            "bot_id": None,
            "channel": "channel_test"
        }
        payload = {"event": event}

        # Mock the start method of Thread class
        mocker.patch.object(slack_api_connection.threading.Thread,
                            'start', return_value=self.mock_handle_request)

        # Mock the auth_test function of slack_web_client
        mocker.patch.object(slack_api_connection.WebClient,
                            "auth_test", return_value=True)
        # Mock the users_info function of slack_web_client
        mocker.patch.object(slack_api_connection.WebClient, "users_info",
                            return_value={"user": {"id": "id_test"}})
        # Mock the chat_postMessage function of slack_web_client
        mocker.patch.object(slack_api_connection.WebClient,
                            "chat_postMessage", return_value=data_test.get("message"))

        mocker.patch('src.api.slack_api_connection.os.environ.get', side_effect=[
            "CADOCSNLU_URL_PREDICT", "0.55", "CSDETECTOR_URL_GETSMELLS"])

        response_intent_manager = {
            "intent": {
                "intent": {
                    "name": "get_smells",
                    "confidence": 0.8
                }
            },
            "entities": {"url": "https://github.com/tensorflow/ranking"}
        }

        response = {
            "files": [],
            "result": [
                "test",
                "BCE"
            ]
        }

        # Mock the Response objects with a mock dict
        mock_response_intent_manager = Mock(spec=requests.Response)
        mock_response_intent_manager.json.return_value = response_intent_manager
        mock_response_tools = Mock(spec=requests.Response)
        mock_response_tools.json.return_value = response

        # Mock requests.get method
        mocker.patch("api.slack_api_connection.requests.get",
                     side_effect=[mock_response_intent_manager, mock_response_tools])

        # Mock os.environ.get method
        mocker.patch('intent_handling.tools.os.environ.get', side_effect=[
            "CADOCSNLU_URL_PREDICT", "0.55"])

        expected_response = {"message": "true"}
        response = slack_api_connection.handle_request(payload)

        # Assertion
        assert expected_response == response

    def test_handle_request_it(self, mocker):

        data_test = {"channel": {"id": 1},
                     "user": {"id": "id_test"},
                     "actions": [{"action_id": "action-yes"}],
                     "message": {"ts": 10}}

        self.language_handler.detect_language("Testo in Italiano")

        event = {
            "client_msg_id": "msg_test",
            "user": "user_test",
            "text": "puoi rilevare i community smells in questo progetto https://github.com/tensorflow/ranking ?",
            "bot_id": None,
            "channel": "channel_test"
        }
        payload = {"event": event}

        # Mock the start method of Thread class
        mocker.patch.object(slack_api_connection.threading.Thread,
                            'start', return_value=self.mock_handle_request)

        # Mock the auth_test function of slack_web_client
        mocker.patch.object(slack_api_connection.WebClient,
                            "auth_test", return_value=True)
        # Mock the users_info function of slack_web_client
        mocker.patch.object(slack_api_connection.WebClient, "users_info",
                            return_value={"user": {"id": "id_test"}})
        # Mock the chat_postMessage function of slack_web_client
        mocker.patch.object(slack_api_connection.WebClient,
                            "chat_postMessage", return_value=data_test.get("message"))

        mocker.patch('src.api.slack_api_connection.os.environ.get', side_effect=[
            "CADOCSNLU_URL_PREDICT", "0.55", "CSDETECTOR_URL_GETSMELLS"])

        response_intent_manager = {
            "intent": {
                "intent": {
                    "name": "get_smells",
                    "confidence": 0.8
                }
            },
            "entities": {"url": "https://github.com/tensorflow/ranking"}
        }

        response = {
            "files": [],
            "result": [
                "test",
                "BCE"
            ]
        }

        # Mock the Response objects with a mock dict
        mock_response_intent_manager = Mock(spec=requests.Response)
        mock_response_intent_manager.json.return_value = response_intent_manager
        mock_response_tools = Mock(spec=requests.Response)
        mock_response_tools.json.return_value = response

        # Mock requests.get method
        mocker.patch("api.slack_api_connection.requests.get",
                     side_effect=[mock_response_intent_manager, mock_response_tools])

        # Mock os.environ.get method
        mocker.patch('intent_handling.tools.os.environ.get', side_effect=[
            "CADOCSNLU_URL_PREDICT", "0.55"])

        expected_response = {"message": "true"}
        response = slack_api_connection.handle_request(payload)

        # Assertion
        assert expected_response == response
