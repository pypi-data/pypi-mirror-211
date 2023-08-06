import random
from http import HTTPStatus
from time import sleep
from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_error import HttpError
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Unset


def _get_kwargs(
    event_type_name: str,
    *,
    client: AuthenticatedClient,
    expunge: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/api/v1/event-type/{event_type_name}/".format(client.base_url, event_type_name=event_type_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["expunge"] = expunge

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> None:
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
    response_204 = None
    return response_204


sleep_time = 0.05
num_retries = 3


def sync_detailed(
    event_type_name: str,
    *,
    client: AuthenticatedClient,
    expunge: Union[Unset, None, bool] = False,
) -> None:
    """Delete Event Type

     Archive an event type.

    Endpoints already configured to filter on an event type will continue to do so after archival.
    However, new messages can not be sent with it and endpoints can not filter on it.
    An event type can be unarchived with the
    [create operation](#operation/create_event_type_api_v1_event_type__post).

    Args:
        event_type_name (str): The event type's name Example: user.signup.
        expunge (Union[Unset, None, bool]):

    Returns:
        None
    """

    kwargs = _get_kwargs(
        event_type_name=event_type_name,
        client=client,
        expunge=expunge,
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
    event_type_name: str,
    *,
    client: AuthenticatedClient,
    expunge: Union[Unset, None, bool] = False,
) -> None:
    """Delete Event Type

     Archive an event type.

    Endpoints already configured to filter on an event type will continue to do so after archival.
    However, new messages can not be sent with it and endpoints can not filter on it.
    An event type can be unarchived with the
    [create operation](#operation/create_event_type_api_v1_event_type__post).

    Args:
        event_type_name (str): The event type's name Example: user.signup.
        expunge (Union[Unset, None, bool]):

    Returns:
        None
    """

    return sync_detailed(
        event_type_name=event_type_name,
        client=client,
        expunge=expunge,
    )


async def asyncio_detailed(
    event_type_name: str,
    *,
    client: AuthenticatedClient,
    expunge: Union[Unset, None, bool] = False,
) -> None:
    """Delete Event Type

     Archive an event type.

    Endpoints already configured to filter on an event type will continue to do so after archival.
    However, new messages can not be sent with it and endpoints can not filter on it.
    An event type can be unarchived with the
    [create operation](#operation/create_event_type_api_v1_event_type__post).

    Args:
        event_type_name (str): The event type's name Example: user.signup.
        expunge (Union[Unset, None, bool]):

    Returns:
        None
    """

    kwargs = _get_kwargs(
        event_type_name=event_type_name,
        client=client,
        expunge=expunge,
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
    event_type_name: str,
    *,
    client: AuthenticatedClient,
    expunge: Union[Unset, None, bool] = False,
) -> None:
    """Delete Event Type

     Archive an event type.

    Endpoints already configured to filter on an event type will continue to do so after archival.
    However, new messages can not be sent with it and endpoints can not filter on it.
    An event type can be unarchived with the
    [create operation](#operation/create_event_type_api_v1_event_type__post).

    Args:
        event_type_name (str): The event type's name Example: user.signup.
        expunge (Union[Unset, None, bool]):

    Returns:
        None
    """

    return await asyncio_detailed(
        event_type_name=event_type_name,
        client=client,
        expunge=expunge,
    )
