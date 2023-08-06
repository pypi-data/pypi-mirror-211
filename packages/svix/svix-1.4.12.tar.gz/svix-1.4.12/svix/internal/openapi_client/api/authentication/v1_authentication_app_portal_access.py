import random
from http import HTTPStatus
from time import sleep
from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...models.app_portal_access_in import AppPortalAccessIn
from ...models.app_portal_access_out import AppPortalAccessOut
from ...models.http_error import HttpError
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Unset


def _get_kwargs(
    app_id: str,
    *,
    client: AuthenticatedClient,
    json_body: AppPortalAccessIn,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/auth/app-portal-access/{app_id}/".format(client.base_url, app_id=app_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(idempotency_key, Unset):
        headers["idempotency-key"] = idempotency_key

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> AppPortalAccessOut:
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise HttpError(response.json(), response.status_code)
    if response.status_code == HTTPStatus.FORBIDDEN:
        raise HttpError(response.json(), response.status_code)
    if response.status_code == HTTPStatus.NOT_FOUND:
        raise HttpError(response.json(), response.status_code)
    if response.status_code == HTTPStatus.CONFLICT:
        raise HttpError(response.json(), response.status_code)
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        raise HTTPValidationError(response.json(), response.status_code)
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        raise HttpError(response.json(), response.status_code)
    response_200 = AppPortalAccessOut.from_dict(response.json())

    return response_200


sleep_time = 0.05
num_retries = 3


def sync_detailed(
    app_id: str,
    *,
    client: AuthenticatedClient,
    json_body: AppPortalAccessIn,
    idempotency_key: Union[Unset, str] = UNSET,
) -> AppPortalAccessOut:
    """Get Consumer App Portal Access

     Use this function to get magic links (and authentication codes) for connecting your users to the
    Consumer Application Portal.

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        idempotency_key (Union[Unset, str]):
        json_body (AppPortalAccessIn):

    Returns:
        AppPortalAccessOut
    """

    kwargs = _get_kwargs(
        app_id=app_id,
        client=client,
        json_body=json_body,
        idempotency_key=idempotency_key,
    )

    kwargs["headers"] = {"svix-req-id": f"{random.getrandbits(32)}", **kwargs["headers"]}

    retry_count = 0
    for retry in range(num_retries):
        response = httpx.request(
            verify=client.verify_ssl,
            **kwargs,
        )
        if response.status_code >= 500 and retry < num_retries:
            retry_count += 1
            kwargs["headers"]["svix-retry-count"] = str(retry_count)
            sleep(sleep_time)
            sleep_time * 2
        else:
            break

    return _parse_response(response=response)


def sync(
    app_id: str,
    *,
    client: AuthenticatedClient,
    json_body: AppPortalAccessIn,
    idempotency_key: Union[Unset, str] = UNSET,
) -> AppPortalAccessOut:
    """Get Consumer App Portal Access

     Use this function to get magic links (and authentication codes) for connecting your users to the
    Consumer Application Portal.

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        idempotency_key (Union[Unset, str]):
        json_body (AppPortalAccessIn):

    Returns:
        AppPortalAccessOut
    """

    return sync_detailed(
        app_id=app_id,
        client=client,
        json_body=json_body,
        idempotency_key=idempotency_key,
    )


async def asyncio_detailed(
    app_id: str,
    *,
    client: AuthenticatedClient,
    json_body: AppPortalAccessIn,
    idempotency_key: Union[Unset, str] = UNSET,
) -> AppPortalAccessOut:
    """Get Consumer App Portal Access

     Use this function to get magic links (and authentication codes) for connecting your users to the
    Consumer Application Portal.

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        idempotency_key (Union[Unset, str]):
        json_body (AppPortalAccessIn):

    Returns:
        AppPortalAccessOut
    """

    kwargs = _get_kwargs(
        app_id=app_id,
        client=client,
        json_body=json_body,
        idempotency_key=idempotency_key,
    )

    kwargs["headers"] = {"svix-req-id": f"{random.getrandbits(32)}", **kwargs["headers"]}

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        retry_count = 0
        for retry in range(num_retries):
            response = await _client.request(**kwargs)
            if response.status_code >= 500 and retry < num_retries:
                retry_count += 1
                kwargs["headers"]["svix-retry-count"] = str(retry_count)
                sleep(sleep_time)
                sleep_time * 2
            else:
                break

    return _parse_response(response=response)


async def asyncio(
    app_id: str,
    *,
    client: AuthenticatedClient,
    json_body: AppPortalAccessIn,
    idempotency_key: Union[Unset, str] = UNSET,
) -> AppPortalAccessOut:
    """Get Consumer App Portal Access

     Use this function to get magic links (and authentication codes) for connecting your users to the
    Consumer Application Portal.

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        idempotency_key (Union[Unset, str]):
        json_body (AppPortalAccessIn):

    Returns:
        AppPortalAccessOut
    """

    return await asyncio_detailed(
        app_id=app_id,
        client=client,
        json_body=json_body,
        idempotency_key=idempotency_key,
    )
