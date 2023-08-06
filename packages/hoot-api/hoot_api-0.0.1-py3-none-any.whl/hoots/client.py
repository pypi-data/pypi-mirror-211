from enum import Enum
from typing import List, Optional

import requests
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


class ChannelType(Enum):
    FACEBOOK = "facebook"
    VIBER = "viber"


class IAccountWebhook(BaseModel):
    accountWebhookId: str
    url: str
    verificationSignature: Optional[str] = None


class IAccount(BaseModel):
    accountId: str
    name: str
    channelIds: Optional[List[str]] = None
    creationTimestampSinceEpochInMillis: Optional[int] = None
    email: Optional[str] = None
    keyId: Optional[str] = None
    accountWebhook: Optional[IAccountWebhook] = None


class IAccountKey(BaseModel):
    accountKeyId: str
    key: str
    creationTimestampSinceEpochInMillis: Optional[int] = None
    expirationTimestampSinceEpochInMillis: Optional[int] = None


class IViberConfiguration(BaseModel):
    authToken: str
    name: str
    avatar: str


class IChannel(BaseModel):
    channelId: str
    channelType: ChannelType
    configuration: IViberConfiguration


class ICreateAccountRequest(BaseModel):
    name: str
    email: Optional[str] = None
    organizationId: str


class ICreateChannelRequest(BaseModel):
    channelType: ChannelType
    configuration: IViberConfiguration


class ICreateOrganizationRequest(BaseModel):
    name: str
    email: Optional[str] = None


class ICreateWebhookRequest(BaseModel):
    url: str


class IOrganization(BaseModel):
    organizationId: str
    name: str
    email: Optional[str] = None
    creationTimestampSinceEpochInMillis: Optional[int] = None


class IHootAccountSecret(BaseModel):
    accountId: str
    apiKey: str


class IHootClientOptions(BaseModel):
    apiUrl: Optional[str] = None
    adminSecretKey: Optional[str] = None
    accountSecret: Optional[IHootAccountSecret] = None


class ISendMessageRequest(BaseModel):
    accountId: str
    channelId: str
    activities: List[dict]


class ISendMessage(BaseModel):
    messageId: str
    channelId: str
    status: str


class HootClient:

    DEFAULT_REQUEST_TIMEOUT_IN_SECS = 10
    DEFAULT_API_URL = ""

    def __init__(self, options: IHootClientOptions):
        self.api_url = options.apiUrl or HootClient.DEFAULT_API_URL
        self.account_secret = options.accountSecret
        self.admin_secret = options.adminSecretKey

    def account(self, account_id: str) -> IAccount:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        response = requests.get(
            f"{self.api_url}/account/{account_id}", headers=headers,
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return IAccount(**(response.json()["data"]))

    def api_key(self, account_id: str, api_key_id: str) -> IAccountKey:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        response = requests.get(
            f"{self.api_url}/account/{account_id}/api_key/{api_key_id}", headers=headers,
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return IAccountKey(**(response.json()["data"]))

    def channel(self, account_id: str, channel_id: str) -> IChannel:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        response = requests.get(
            f"{self.api_url}/account/{account_id}/channel/{channel_id}", headers=headers,
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return IChannel(**(response.json()["data"]))

    def create_account(self, request: ICreateAccountRequest) -> IAccount:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        response = requests.post(
            f"{self.api_url}/account", headers=headers, json=request.dict(),
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return IAccount(**(response.json()["data"]))

    def create_account_webhook(
            self, account_id: str, request: ICreateWebhookRequest) -> IAccountWebhook:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        response = requests.post(
            f"{self.api_url}/account/{account_id}/webhook", headers=headers, json=request.dict(),
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return IAccountWebhook(**(response.json()["data"]))

    def create_channel(self, account_id: str, request: ICreateChannelRequest) -> IChannel:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        response = requests.post(
            f"{self.api_url}/account/{account_id}/channel", headers=headers, json=request.dict(),
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return IChannel(**(response.json()["data"]))

    def create_api_key(self, account_id: str) -> IAccountKey:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        response = requests.post(
            f"{self.api_url}/account/{account_id}/api_key", headers=headers,
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return IAccountKey(**(response.json()["data"]))

    def create_organization(self, request: ICreateOrganizationRequest) -> IOrganization:
        headers = self._request_headers_with_admin_secret()
        response = requests.post(
            f"{self.api_url}/organization", headers=headers, json=request.dict(),
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return IOrganization(**(response.json()["data"]))

    def organization(self, organization_id: str) -> IOrganization:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        response = requests.get(
            f"{self.api_url}/organization/{organization_id}", headers=headers,
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return IOrganization(**(response.json()["data"]))

    def remove_account(self, account_id: str) -> None:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        requests.delete(
            f"{self.api_url}/account/{account_id}", headers=headers,
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)

    def remove_api_key(self, account_id: str, api_key_id: str) -> None:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        requests.delete(
            f"{self.api_url}/account/{account_id}/api_key/{api_key_id}", headers=headers,
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)

    def remove_channel(self, account_id: str, channel_id: str) -> None:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        requests.delete(
            f"{self.api_url}/account/{account_id}/channel/{channel_id}", headers=headers,
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)

    def remove_organization(self, organization_id: str) -> None:
        headers = self._request_headers_with_admin_secret()
        requests.delete(
            f"{self.api_url}/organization/{organization_id}", headers=headers,
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)

    def remove_webhook(self, account_id: str, webhook_id: str) -> None:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        requests.delete(
            f"{self.api_url}/account/{account_id}/webhook/{webhook_id}", headers=headers,
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)

    def update_admin_secret(self, admin_secret: str) -> None:
        self.admin_secret = admin_secret

    def update_account_secret(self, account_secret: IHootAccountSecret) -> None:
        self.account_secret = account_secret

    def webhook(self, account_id: str) -> IAccountWebhook:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        response = requests.get(
            f"{self.api_url}/account/{account_id}/webhook", headers=headers,
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return IAccountWebhook(**(response.json()["data"]))

    def send_message(self, request: ISendMessageRequest) -> ISendMessage:
        headers = self._request_headers_with_admin_secret_or_account_api_key()
        response = requests.post(
            f"{self.api_url}/message/send", headers=headers, json=request.dict(),
            timeout=HootClient.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return ISendMessage(**(response.json()["data"]))

    def _request_headers_with_admin_secret(self) -> dict:
        if not self.admin_secret:
            raise Exception(
                "admin secret key is required to create / remove an organization")
        return {
            "Content-Type": "application/json",
            "X-Hoot-Admin-Secret": self.admin_secret
        }

    def _request_headers_with_admin_secret_or_account_api_key(self) -> dict:
        if not self.admin_secret and not self.account_secret:
            raise Exception(
                "admin secret key or account secret is required to get an organization")
        headers = {"Content-Type": "application/json"}
        if self.admin_secret:
            headers["X-Hoot-Admin-Secret"] = self.admin_secret
        if self.account_secret:
            headers["X-Hoot-Account-Id"] = self.account_secret.accountId
            headers["X-Hoot-Api-Key"] = self.account_secret.apiKey
        return headers
