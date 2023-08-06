import random
from http import HTTPStatus
from time import sleep
from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_error import HttpError
from ...models.http_validation_error import HTTPValidationError
from ...models.one_time_token_in import OneTimeTokenIn
from ...models.one_time_token_out import OneTimeTokenOut
from ...types import UNSET, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: OneTimeTokenIn,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/auth/one-time-token/".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> OneTimeTokenOut:
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
    response_200 = OneTimeTokenOut.from_dict(response.json())

    return response_200


sleep_time = 0.05
num_retries = 3


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: OneTimeTokenIn,
    idempotency_key: Union[Unset, str] = UNSET,
) -> OneTimeTokenOut:
    """Exchange One Time Token

     This is a one time token

    Args:
        idempotency_key (Union[Unset, str]):
        json_body (OneTimeTokenIn):

    Returns:
        OneTimeTokenOut
    """

    kwargs = _get_kwargs(
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
    *,
    client: AuthenticatedClient,
    json_body: OneTimeTokenIn,
    idempotency_key: Union[Unset, str] = UNSET,
) -> OneTimeTokenOut:
    """Exchange One Time Token

     This is a one time token

    Args:
        idempotency_key (Union[Unset, str]):
        json_body (OneTimeTokenIn):

    Returns:
        OneTimeTokenOut
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        idempotency_key=idempotency_key,
    )


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: OneTimeTokenIn,
    idempotency_key: Union[Unset, str] = UNSET,
) -> OneTimeTokenOut:
    """Exchange One Time Token

     This is a one time token

    Args:
        idempotency_key (Union[Unset, str]):
        json_body (OneTimeTokenIn):

    Returns:
        OneTimeTokenOut
    """

    kwargs = _get_kwargs(
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
    *,
    client: AuthenticatedClient,
    json_body: OneTimeTokenIn,
    idempotency_key: Union[Unset, str] = UNSET,
) -> OneTimeTokenOut:
    """Exchange One Time Token

     This is a one time token

    Args:
        idempotency_key (Union[Unset, str]):
        json_body (OneTimeTokenIn):

    Returns:
        OneTimeTokenOut
    """

    return await asyncio_detailed(
        client=client,
        json_body=json_body,
        idempotency_key=idempotency_key,
    )
