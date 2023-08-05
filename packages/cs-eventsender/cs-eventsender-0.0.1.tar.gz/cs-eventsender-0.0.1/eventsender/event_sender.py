import logging
import os
import requests
from cs_telegram_bot import TelegramClient


class EventSender:
    def __init__(self, server_url=None, api_key=None):
        self.server_url = server_url or os.getenv("REACT_APP_API_URL")
        if not self.server_url:
            raise ValueError(
                "Server URL is not set. It must be provided during initialization or set in the environment variables.")

        self.api_key = api_key or os.getenv("FLASK_APP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is not set. It must be provided during initialization or set in the environment variables.")

        self.telegram_client = TelegramClient()

    def _send_to_server(self, event_type, data):
        payload = {
            "event_type": event_type,
            "data": data.to_dict()
        }
        headers = {'X-Api-Key': self.api_key}
        response = requests.post(
            f"{self.server_url}/events/send", json=payload, headers=headers)

        if response.status_code != 200:
            logging.error(
                f"Failed to send data to server. Status code: {response.status_code}. Response: {response.text}")
            return False
        return True

    def _send_to_telegram(self, data_type, message):
        try:
            self.telegram_client.send_message(data_type, message)
        except Exception as e:
            logging.error(
                f"Failed to send message to telegram. Exception: {e}")
            return False
        return True

    def send_data(self, status, data):
        if status not in ["new", "update"]:
            raise ValueError(
                "Invalid status. It must be either 'new' or 'update'.")

        data_type = data.__tablename__
        event_type = f"{status}_{data_type}"

        message = data.generate_new_message(
        ) if status == "new" else data.generate_update_message()

        server_success = self._send_to_server(event_type, data)
        telegram_success = self._send_to_telegram(data_type, message)

        return server_success and telegram_success