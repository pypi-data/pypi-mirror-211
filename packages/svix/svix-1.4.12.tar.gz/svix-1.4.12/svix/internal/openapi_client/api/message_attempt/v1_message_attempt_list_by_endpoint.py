import datetime
import random
from http import HTTPStatus
from time import sleep
from typing import Any, Dict, List, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_error import HttpError
from ...models.http_validation_error import HTTPValidationError
from ...models.list_response_message_attempt_out import ListResponseMessageAttemptOut
from ...models.message_status import MessageStatus
from ...models.status_code_class import StatusCodeClass
from ...types import UNSET, Unset


def _get_kwargs(
    app_id: str,
    endpoint_id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, MessageStatus] = UNSET,
    status_code_class: Union[Unset, None, StatusCodeClass] = UNSET,
    channel: Union[Unset, None, str] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    event_types: Union[Unset, None, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/app/{app_id}/attempt/endpoint/{endpoint_id}/".format(
        client.base_url, app_id=app_id, endpoint_id=endpoint_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["limit"] = limit

    params["iterator"] = iterator

    json_status: Union[Unset, None, int] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value if status else None

    params["status"] = json_status

    json_status_code_class: Union[Unset, None, int] = UNSET
    if not isinstance(status_code_class, Unset):
        json_status_code_class = status_code_class.value if status_code_class else None

    params["status_code_class"] = json_status_code_class

    params["channel"] = channel

    json_before: Union[Unset, None, str] = UNSET
    if not isinstance(before, Unset):
        json_before = before.isoformat() if before else None

    params["before"] = json_before

    json_after: Union[Unset, None, str] = UNSET
    if not isinstance(after, Unset):
        json_after = after.isoformat() if after else None

    params["after"] = json_after

    json_event_types: Union[Unset, None, List[str]] = UNSET
    if not isinstance(event_types, Unset):
        if event_types is None:
            json_event_types = None
        else:
            json_event_types = event_types

    params["event_types"] = json_event_types

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> ListResponseMessageAttemptOut:
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
    response_200 = ListResponseMessageAttemptOut.from_dict(response.json())

    return response_200


sleep_time = 0.05
num_retries = 3


def sync_detailed(
    app_id: str,
    endpoint_id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, MessageStatus] = UNSET,
    status_code_class: Union[Unset, None, StatusCodeClass] = UNSET,
    channel: Union[Unset, None, str] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    event_types: Union[Unset, None, List[str]] = UNSET,
) -> ListResponseMessageAttemptOut:
    """List Attempts By Endpoint

     List attempts by endpoint id

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        endpoint_id (str): The ep's ID or UID Example: unique-ep-identifier.
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]): The attempt's ID Example:
            atmpt_1srOrx2ZWZBpBUvZwXKQmoEYga2.
        status (Union[Unset, None, MessageStatus]): The sending status of the message:
            - Success = 0
            - Pending = 1
            - Fail = 2
            - Sending = 3
        status_code_class (Union[Unset, None, StatusCodeClass]): The different classes of HTTP
            status codes:
            - CodeNone = 0
            - Code1xx = 100
            - Code2xx = 200
            - Code3xx = 300
            - Code4xx = 400
            - Code5xx = 500
        channel (Union[Unset, None, str]):  Example: project_1337.
        before (Union[Unset, None, datetime.datetime]):
        after (Union[Unset, None, datetime.datetime]):
        event_types (Union[Unset, None, List[str]]):

    Returns:
        ListResponseMessageAttemptOut
    """

    kwargs = _get_kwargs(
        app_id=app_id,
        endpoint_id=endpoint_id,
        client=client,
        limit=limit,
        iterator=iterator,
        status=status,
        status_code_class=status_code_class,
        channel=channel,
        before=before,
        after=after,
        event_types=event_types,
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
    endpoint_id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, MessageStatus] = UNSET,
    status_code_class: Union[Unset, None, StatusCodeClass] = UNSET,
    channel: Union[Unset, None, str] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    event_types: Union[Unset, None, List[str]] = UNSET,
) -> ListResponseMessageAttemptOut:
    """List Attempts By Endpoint

     List attempts by endpoint id

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        endpoint_id (str): The ep's ID or UID Example: unique-ep-identifier.
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]): The attempt's ID Example:
            atmpt_1srOrx2ZWZBpBUvZwXKQmoEYga2.
        status (Union[Unset, None, MessageStatus]): The sending status of the message:
            - Success = 0
            - Pending = 1
            - Fail = 2
            - Sending = 3
        status_code_class (Union[Unset, None, StatusCodeClass]): The different classes of HTTP
            status codes:
            - CodeNone = 0
            - Code1xx = 100
            - Code2xx = 200
            - Code3xx = 300
            - Code4xx = 400
            - Code5xx = 500
        channel (Union[Unset, None, str]):  Example: project_1337.
        before (Union[Unset, None, datetime.datetime]):
        after (Union[Unset, None, datetime.datetime]):
        event_types (Union[Unset, None, List[str]]):

    Returns:
        ListResponseMessageAttemptOut
    """

    return sync_detailed(
        app_id=app_id,
        endpoint_id=endpoint_id,
        client=client,
        limit=limit,
        iterator=iterator,
        status=status,
        status_code_class=status_code_class,
        channel=channel,
        before=before,
        after=after,
        event_types=event_types,
    )


async def asyncio_detailed(
    app_id: str,
    endpoint_id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, MessageStatus] = UNSET,
    status_code_class: Union[Unset, None, StatusCodeClass] = UNSET,
    channel: Union[Unset, None, str] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    event_types: Union[Unset, None, List[str]] = UNSET,
) -> ListResponseMessageAttemptOut:
    """List Attempts By Endpoint

     List attempts by endpoint id

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        endpoint_id (str): The ep's ID or UID Example: unique-ep-identifier.
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]): The attempt's ID Example:
            atmpt_1srOrx2ZWZBpBUvZwXKQmoEYga2.
        status (Union[Unset, None, MessageStatus]): The sending status of the message:
            - Success = 0
            - Pending = 1
            - Fail = 2
            - Sending = 3
        status_code_class (Union[Unset, None, StatusCodeClass]): The different classes of HTTP
            status codes:
            - CodeNone = 0
            - Code1xx = 100
            - Code2xx = 200
            - Code3xx = 300
            - Code4xx = 400
            - Code5xx = 500
        channel (Union[Unset, None, str]):  Example: project_1337.
        before (Union[Unset, None, datetime.datetime]):
        after (Union[Unset, None, datetime.datetime]):
        event_types (Union[Unset, None, List[str]]):

    Returns:
        ListResponseMessageAttemptOut
    """

    kwargs = _get_kwargs(
        app_id=app_id,
        endpoint_id=endpoint_id,
        client=client,
        limit=limit,
        iterator=iterator,
        status=status,
        status_code_class=status_code_class,
        channel=channel,
        before=before,
        after=after,
        event_types=event_types,
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
    endpoint_id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, MessageStatus] = UNSET,
    status_code_class: Union[Unset, None, StatusCodeClass] = UNSET,
    channel: Union[Unset, None, str] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    event_types: Union[Unset, None, List[str]] = UNSET,
) -> ListResponseMessageAttemptOut:
    """List Attempts By Endpoint

     List attempts by endpoint id

    Args:
        app_id (str): The app's ID or UID Example: unique-app-identifier.
        endpoint_id (str): The ep's ID or UID Example: unique-ep-identifier.
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]): The attempt's ID Example:
            atmpt_1srOrx2ZWZBpBUvZwXKQmoEYga2.
        status (Union[Unset, None, MessageStatus]): The sending status of the message:
            - Success = 0
            - Pending = 1
            - Fail = 2
            - Sending = 3
        status_code_class (Union[Unset, None, StatusCodeClass]): The different classes of HTTP
            status codes:
            - CodeNone = 0
            - Code1xx = 100
            - Code2xx = 200
            - Code3xx = 300
            - Code4xx = 400
            - Code5xx = 500
        channel (Union[Unset, None, str]):  Example: project_1337.
        before (Union[Unset, None, datetime.datetime]):
        after (Union[Unset, None, datetime.datetime]):
        event_types (Union[Unset, None, List[str]]):

    Returns:
        ListResponseMessageAttemptOut
    """

    return await asyncio_detailed(
        app_id=app_id,
        endpoint_id=endpoint_id,
        client=client,
        limit=limit,
        iterator=iterator,
        status=status,
        status_code_class=status_code_class,
        channel=channel,
        before=before,
        after=after,
        event_types=event_types,
    )
