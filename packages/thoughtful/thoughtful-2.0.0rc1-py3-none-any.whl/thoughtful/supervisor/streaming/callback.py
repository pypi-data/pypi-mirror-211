from __future__ import annotations

import datetime
import logging
from dataclasses import dataclass

import jwt
import requests
from requests.auth import AuthBase

from thoughtful.supervisor.manifest import Manifest
from thoughtful.supervisor.reporting.status import Status
from thoughtful.supervisor.reporting.step_report import StepReport
from thoughtful.supervisor.streaming.payloads import ArtifactsUploadedPayload
from thoughtful.supervisor.streaming.payloads import BotManifestStreamingPayload
from thoughtful.supervisor.streaming.payloads import StatusChangePayload
from thoughtful.supervisor.streaming.payloads import StepReportStreamingPayload
from thoughtful.supervisor.streaming.payloads import StreamingPayload

logger = logging.getLogger(__name__)

POST_TIMEOUT_SECONDS = 10

class Token:
    """A JWT token."""
    def __init__(self, encoded_value: str, algorithm="HS256"):
        self.encoded_value = encoded_value

        decoded_values = jwt.decode(
            jwt=self.encoded_value,
            algorithms=[algorithm],
            options={"verify_signature": False},
        )
        self.expires_at = datetime.datetime.fromtimestamp(decoded_values["exp"])
        self.issued_at = datetime.datetime.fromtimestamp(decoded_values["iat"])

    def __str__(self):
        return self.encoded_value

    @property
    def is_expired(self, expiry_margin: float = 0.1) -> bool:
        """
        Returns True if the token is expired or will expire soon.

        expiry_margin: A float between 0 and 1. For example, if set to 0.1, the
            token will be considered expired if it will expire within 10% of its
            total lifetime.
        """
        now = datetime.datetime.now()
        if now >= self.expires_at:
            return True

        time_to_expire_seconds = (
            self.expires_at - self.issued_at).total_seconds()
        expiry_threshold = time_to_expire_seconds * expiry_margin
        will_expire_soon = abs(time_to_expire_seconds) <= expiry_threshold
        if will_expire_soon:
            return True

        return False


@dataclass
class JWTAuth(AuthBase):
    access_token: Token
    refresh_token: Token
    refresh_url: str

    def __call__(self, r: requests.Request) -> requests.Request:
        self.refresh()
        r.headers["Authorization"] = f"Bearer {self.access_token}"
        return r

    def refresh(self) -> None:
        if not self.access_token.is_expired:
            return

        logger.info("Access token expired, refreshing")
        response = requests.post(
            self.refresh_url,
            json={
                "refreshToken": str(self.refresh_token),
            },
            timeout=POST_TIMEOUT_SECONDS,
        )

        if not response.ok:
            logging.warning("Could not refresh JWT token!")
            logging.warning(f"Received response {response.status_code}: {response.text}")
            return

        logging.info("Successfully refreshed JWT token")
        new_values = response.json()
        self.access_token = Token(new_values["accessToken"])
        self.refresh_token = Token(new_values["refreshToken"])

class StreamingCallback(requests.Session):

    def __init__(
        self, run_id: str, callback_url: str, access_token: str,
        refresh_token: str, refresh_url: str,
    ):
        super().__init__()
        self.run_id = run_id
        self.callback_url = callback_url
        self.auth: JWTAuth = JWTAuth(
            access_token=Token(access_token) if access_token else None,
            refresh_token=Token(refresh_token) if refresh_token else None,
            refresh_url=refresh_url,
        )

    def post(self, payload: StreamingPayload, **kwargs):
        message_json = payload.__json__()

        try:
            logger.info("Posting streaming message")
            logger.info("URL: %s", self.callback_url)
            logger.info("Payload: %s", message_json)
            response = super().post(
                self.callback_url, json=message_json, timeout=POST_TIMEOUT_SECONDS,
                **kwargs
            )
        except Exception:
            # A failed stream message shouldn't break a bot, so catch any possible
            # exception and log it
            logger.exception("Could not post step payload to endpoint")
            return

        logger.info(
            f"Received response: ({response.status_code}): {response.text}")

        return response

    def post_step_update(self, report: StepReport):
        logger.info(
            f"Posting step update id={report.step_id} status={report.status}")
        return self.post(StepReportStreamingPayload(report, self.run_id))

    def post_manifest(self, manifest: Manifest):
        return self.post(BotManifestStreamingPayload(manifest, self.run_id))

    def post_artifacts_uploaded(self, output_uri: str):
        return self.post(
            ArtifactsUploadedPayload(
                run_id=self.run_id, output_artifacts_uri=output_uri
            )
        )

    def post_status_change(self, status: Status):
        return self.post(StatusChangePayload(run_id=self.run_id, status=status))


if __name__ == "__main__":
    at = "xxxxxx"
    rt = "yyyyyy"
    _id = "1"
    url = "https://YOUR_URL_ID.execute-api.us-east-1.amazonaws.com/STAGE/webhooks/users-processes-updates/jwt"
    ref_ur = "https://YOUR_URL_ID.execute-api.us-east-1.amazonaws.com/STAGE/refresh-token"

    callback = StreamingCallback(
        run_id=_id,
        callback_url=url,
        access_token=at,
        refresh_token=rt,
        refresh_url=ref_ur,
    )
    callback.post_status_change(Status.SUCCEEDED)
