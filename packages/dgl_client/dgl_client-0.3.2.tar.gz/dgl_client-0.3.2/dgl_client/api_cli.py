import time
import os
import logging
import json
import requests
import sseclient
import uuid

logger = logging.getLogger(__name__)

import json
from base64 import b64decode, b64encode

def prepare_token(api_key: str, user_id: str , provider_account_id: str, username: str, client="website"):
    token_data = {
        "api_key": api_key,
        "client": client,
        "user_id": user_id,
        "provider_account_id": provider_account_id,
        "username": username
    }

    token = b64encode(json.dumps(token_data).encode())
    return token


def login_check(endp, tok):
    logger.info("Trying to login...")
    username = None
    try:
      response = requests.get(
          f"{endp}/auth/check",
          json={},
          headers={"Authorization": f"Bearer {tok}"},
      )
      response.raise_for_status()
      username = response.json()
    except:
      pass

    return username

def refresh_token(endp, atok, rtok):
    logger.info("Refreshing login token...")
    new_tok = None
    try:
      response = requests.get(
          f"{endp}/auth/refresh",
          json={},
          headers={
              "Refresh": f"{rtok}"
              },
      )
      response.raise_for_status()
      new_tok = response.json()
    except:
      raise
    logger.info("New token is %s"%str(new_tok))

    return new_tok

def ak2token(endp, access_key):
    logger.info("Logging in using access_key...")
    new_tok = None
    try:
      response = requests.post(
          f"{endp}/auth/trusted_login",
          json={},
          headers={
              "TrustedClient": f"{access_key}"
              },
      )
      response.raise_for_status()
      new_tok = response.json()
    except:
      raise
    logger.info("New token is %s"%str(new_tok))

    return new_tok


class APIClient:
    def __init__(self, backend_url, http_client=requests):
        self.backend_url = backend_url
        self.http_client = http_client
        self.auth_headers = None
        self.message_id = None

    def login(self, access_key):
        print(access_key)
        atok = ak2token(self.backend_url, access_key)

        username = login_check(self.backend_url, atok)

        if username:
            logger.info(f"Logged in as {username}")    
            self.auth_headers = {"Authorization": f"Bearer {atok}"}


    def continue_chat(self, chat_id):
        self.chat_id = chat_id
        return self.chat_id

    def create_chat(self):
        response = self.http_client.post(
            f"{self.backend_url}/chats",
            json={},
            headers=self.auth_headers,
        )
        response.raise_for_status()
        self.chat_id = response.json()["id"]
        self.message_id = None
        return self.chat_id

    def get_available_models(self):
        response = self.http_client.get(
            f"{self.backend_url}/configs/model_configs",
            headers=self.auth_headers,
        )
        response.raise_for_status()
        return [model["name"] for model in response.json()]
    
    def get_available_workflows(self):
        response = self.http_client.get(
            f"{self.backend_url}/configs/workflow_configs",
            headers=self.auth_headers,
        )
        response.raise_for_status()
        return [model["name"] for model in response.json()]

    def send_message(self, message, model_config_name, collection=None):
        response = self.http_client.post(
            f"{self.backend_url}/chats/{self.chat_id}/prompter_message",
            json={
                "parent_id": self.message_id,
                "content": message,
                "collection": collection
            },
            headers=self.auth_headers,
        )
        response.raise_for_status()
        prompter_message_id = response.json()["id"]

        response = self.http_client.post(
            f"{self.backend_url}/chats/{self.chat_id}/assistant_message",
            json={
                "parent_id": prompter_message_id,
                "model_config_name": model_config_name,
                "sampling_parameters": {
                    "top_p": 0.95,
                    "top_k": 50,
                    "repetition_penalty": 1.2,
                    "temperature": 1.0,
                },
            },
            headers=self.auth_headers,
        )
        response.raise_for_status()
        self.message_id = response.json()["id"]

        response = self.http_client.get(
            f"{self.backend_url}/chats/{self.chat_id}/messages/{self.message_id}/events",
            stream=True,
            headers={
                "Accept": "text/event-stream",
                **self.auth_headers,
            },
        )
        response.raise_for_status()
        if response.status_code == 204:
            response = self.http_client.get(
                f"{self.backend_url}/chats/{self.chat_id}/messages/{self.message_id}",
                headers=self.auth_headers,
            )
            response.raise_for_status()
            data = response.json()
            yield data["content"]
        else:
            client = sseclient.SSEClient(response)
            events = iter(client.events())
            for event in events:
                if event.event == "error":
                    raise RuntimeError(event.data)
                if event.event == "ping":
                    continue
                try:
                    data = json.loads(event.data)
                except json.JSONDecodeError:
                    raise RuntimeError(f"Failed to decode {event.data=}")
                event_type = data["event_type"]
                if event_type == "token":
                    yield data["text"]
                elif event_type == "message":
                    # full message content, can be ignored here
                    if "message" in data:
                        if "content" in data['message']:
                            yield data['message']["content"]
                        else:
                            _s = data["message"]
                            logger.debug(f"Message event type but no content? {_s=}")                             
                    else:
                        logger.debug(f"Message event type but no message? {data=}")    
                elif event_type == "error":
                    raise RuntimeError(data["error"])
                elif event_type == "pending":
                    logger.debug(f"Message pending. {data=}")
                else:
                    print("UNKNOWN!!!")
                    print(data)


