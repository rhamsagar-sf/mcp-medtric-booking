import os
from typing import Any

import httpx


class ServiceAPIError(RuntimeError):
    pass


class ServiceAPIClient:
    def __init__(self) -> None:
        self.base_url = os.getenv(
            "SERVICE_API_BASE_URL",
            "https://immense-oasis-54700-ed56d04c5f65.herokuapp.com",
        ).rstrip("/")
        self.api_key = os.getenv("SERVICE_API_KEY")
        self.timeout = float(os.getenv("SERVICE_API_TIMEOUT", "20"))

        self.availability_path = os.getenv(
            "SERVICE_API_AVAILABILITY_PATH", "/service-assistant/availability"
        )
        self.booking_path = os.getenv("SERVICE_API_BOOKING_PATH", "/service-visits/book")
        self.reschedule_path = os.getenv(
            "SERVICE_API_RESCHEDULE_PATH", "/service-visits/reschedule"
        )

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            response = httpx.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            body = exc.response.text if exc.response is not None else ""
            raise ServiceAPIError(
                f"API request failed ({exc.response.status_code}): {body}"
            ) from exc
        except httpx.HTTPError as exc:
            raise ServiceAPIError(f"API request error: {exc}") from exc

        try:
            return response.json()
        except ValueError as exc:
            raise ServiceAPIError("API returned non-JSON response") from exc

    def get_service_assistant_availability(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._post(self.availability_path, payload)

    def book_service_visit(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._post(self.booking_path, payload)

    def reschedule_booking(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._post(self.reschedule_path, payload)
