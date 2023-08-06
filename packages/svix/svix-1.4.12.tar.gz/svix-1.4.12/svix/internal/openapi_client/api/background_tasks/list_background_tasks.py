import random
from http import HTTPStatus
from time import sleep
from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...models.background_task_status import BackgroundTaskStatus
from ...models.background_task_type import BackgroundTaskType
from ...models.http_error import HttpError
from ...models.http_validation_error import HTTPValidationError
from ...models.list_response_background_task_out import ListResponseBackgroundTaskOut
from ...models.ordering import Ordering
from ...types import UNSET, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    status: Union[Unset, None, BackgroundTaskStatus] = UNSET,
    task: Union[Unset, None, BackgroundTaskType] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, Ordering] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/background-task/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_status: Union[Unset, None, str] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value if status else None

    params["status"] = json_status

    json_task: Union[Unset, None, str] = UNSET
    if not isinstance(task, Unset):
        json_task = task.value if task else None

    params["task"] = json_task

    params["limit"] = limit

    params["iterator"] = iterator

    json_order: Union[Unset, None, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value if order else None

    params["order"] = json_order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> ListResponseBackgroundTaskOut:
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
    response_200 = ListResponseBackgroundTaskOut.from_dict(response.json())

    return response_200


sleep_time = 0.05
num_retries = 3


def sync_detailed(
    *,
    client: AuthenticatedClient,
    status: Union[Unset, None, BackgroundTaskStatus] = UNSET,
    task: Union[Unset, None, BackgroundTaskType] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, Ordering] = UNSET,
) -> ListResponseBackgroundTaskOut:
    """List Background Tasks

     List background tasks executed in the past 90 days.

    Args:
        status (Union[Unset, None, BackgroundTaskStatus]):
        task (Union[Unset, None, BackgroundTaskType]):
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]):
        order (Union[Unset, None, Ordering]): Defines the ordering in a listing of results.

    Returns:
        ListResponseBackgroundTaskOut
    """

    kwargs = _get_kwargs(
        client=client,
        status=status,
        task=task,
        limit=limit,
        iterator=iterator,
        order=order,
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
    status: Union[Unset, None, BackgroundTaskStatus] = UNSET,
    task: Union[Unset, None, BackgroundTaskType] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, Ordering] = UNSET,
) -> ListResponseBackgroundTaskOut:
    """List Background Tasks

     List background tasks executed in the past 90 days.

    Args:
        status (Union[Unset, None, BackgroundTaskStatus]):
        task (Union[Unset, None, BackgroundTaskType]):
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]):
        order (Union[Unset, None, Ordering]): Defines the ordering in a listing of results.

    Returns:
        ListResponseBackgroundTaskOut
    """

    return sync_detailed(
        client=client,
        status=status,
        task=task,
        limit=limit,
        iterator=iterator,
        order=order,
    )


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    status: Union[Unset, None, BackgroundTaskStatus] = UNSET,
    task: Union[Unset, None, BackgroundTaskType] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, Ordering] = UNSET,
) -> ListResponseBackgroundTaskOut:
    """List Background Tasks

     List background tasks executed in the past 90 days.

    Args:
        status (Union[Unset, None, BackgroundTaskStatus]):
        task (Union[Unset, None, BackgroundTaskType]):
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]):
        order (Union[Unset, None, Ordering]): Defines the ordering in a listing of results.

    Returns:
        ListResponseBackgroundTaskOut
    """

    kwargs = _get_kwargs(
        client=client,
        status=status,
        task=task,
        limit=limit,
        iterator=iterator,
        order=order,
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
    status: Union[Unset, None, BackgroundTaskStatus] = UNSET,
    task: Union[Unset, None, BackgroundTaskType] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, Ordering] = UNSET,
) -> ListResponseBackgroundTaskOut:
    """List Background Tasks

     List background tasks executed in the past 90 days.

    Args:
        status (Union[Unset, None, BackgroundTaskStatus]):
        task (Union[Unset, None, BackgroundTaskType]):
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]):
        order (Union[Unset, None, Ordering]): Defines the ordering in a listing of results.

    Returns:
        ListResponseBackgroundTaskOut
    """

    return await asyncio_detailed(
        client=client,
        status=status,
        task=task,
        limit=limit,
        iterator=iterator,
        order=order,
    )
