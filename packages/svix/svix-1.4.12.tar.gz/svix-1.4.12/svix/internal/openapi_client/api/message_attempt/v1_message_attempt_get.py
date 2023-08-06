import random
from http import HTTPStatus
from time import sleep
from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...models.http_error import HttpError
from ...models.http_validation_error import HTTPValidationError
from ...models.message_attempt_out import MessageAttemptOut


def _get_kwargs(
    app_id: str,
    msg_id: str,
    attempt_id: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/v1/app/{app_id}/msg/{msg_id}/attempt/{attempt_id}/".format(
        client.base_url, app_id=app_id, msg_id=msg_id, attempt_id=attempt_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> MessageAttemptOut:
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
    response_200 = MessageAttemptOut.from_dict(response.json())

    return response_200


sleep_time = 0.05
num_retries = 3


def sync_detailed(
    app_id: str,
    msg_id: str,
    attempt_id: str,
    *,
    client: AuthenticatedClient,
) -> MessageAttemptOut:
    """Get Attempt

     `msg_id`: Use a message id or a message `eventId`

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        msg_id (str): The msg's ID or UID Example: unique-msg-identifier.
        attempt_id (str): The attempt's ID Example: atmpt_1srOrx2ZWZBpBUvZwXKQmoEYga2.

    Returns:
        MessageAttemptOut
    """

    kwargs = _get_kwargs(
        app_id=app_id,
        msg_id=msg_id,
        attempt_id=attempt_id,
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
    app_id: str,
    msg_id: str,
    attempt_id: str,
    *,
    client: AuthenticatedClient,
) -> MessageAttemptOut:
    """Get Attempt

     `msg_id`: Use a message id or a message `eventId`

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        msg_id (str): The msg's ID or UID Example: unique-msg-identifier.
        attempt_id (str): The attempt's ID Example: atmpt_1srOrx2ZWZBpBUvZwXKQmoEYga2.

    Returns:
        MessageAttemptOut
    """

    return sync_detailed(
        app_id=app_id,
        msg_id=msg_id,
        attempt_id=attempt_id,
        client=client,
    )


async def asyncio_detailed(
    app_id: str,
    msg_id: str,
    attempt_id: str,
    *,
    client: AuthenticatedClient,
) -> MessageAttemptOut:
    """Get Attempt

     `msg_id`: Use a message id or a message `eventId`

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        msg_id (str): The msg's ID or UID Example: unique-msg-identifier.
        attempt_id (str): The attempt's ID Example: atmpt_1srOrx2ZWZBpBUvZwXKQmoEYga2.

    Returns:
        MessageAttemptOut
    """

    kwargs = _get_kwargs(
        app_id=app_id,
        msg_id=msg_id,
        attempt_id=attempt_id,
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
    app_id: str,
    msg_id: str,
    attempt_id: str,
    *,
    client: AuthenticatedClient,
) -> MessageAttemptOut:
    """Get Attempt

     `msg_id`: Use a message id or a message `eventId`

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        msg_id (str): The msg's ID or UID Example: unique-msg-identifier.
        attempt_id (str): The attempt's ID Example: atmpt_1srOrx2ZWZBpBUvZwXKQmoEYga2.

    Returns:
        MessageAttemptOut
    """

    return await asyncio_detailed(
        app_id=app_id,
        msg_id=msg_id,
        attempt_id=attempt_id,
        client=client,
    )
