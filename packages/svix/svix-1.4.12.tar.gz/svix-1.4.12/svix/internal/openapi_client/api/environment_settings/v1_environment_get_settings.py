import random
from http import HTTPStatus
from time import sleep
from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...models.environment_settings_out import EnvironmentSettingsOut
from ...models.http_error import HttpError
from ...models.http_validation_error import HTTPValidationError


def _get_kwargs(
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/v1/environment/settings/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> EnvironmentSettingsOut:
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
    response_200 = EnvironmentSettingsOut.from_dict(response.json())

    return response_200


sleep_time = 0.05
num_retries = 3


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> EnvironmentSettingsOut:
    """Get Org Settings

     Get the environment's settings

    Returns:
        EnvironmentSettingsOut
    """

    kwargs = _get_kwargs(
        client=client,
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
    *,
    client: AuthenticatedClient,
) -> EnvironmentSettingsOut:
    """Get Org Settings

     Get the environment's settings

    Returns:
        EnvironmentSettingsOut
    """

    return sync_detailed(
        client=client,
    )


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> EnvironmentSettingsOut:
    """Get Org Settings

     Get the environment's settings

    Returns:
        EnvironmentSettingsOut
    """

    kwargs = _get_kwargs(
        client=client,
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
    *,
    client: AuthenticatedClient,
) -> EnvironmentSettingsOut:
    """Get Org Settings

     Get the environment's settings

    Returns:
        EnvironmentSettingsOut
    """

    return await asyncio_detailed(
        client=client,
    )
