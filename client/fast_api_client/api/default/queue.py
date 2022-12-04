from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.input_ import Input
from ...models.output import Output
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: Input,
) -> Dict[str, Any]:
    url = "{}/queue".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, Output]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Output.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, Output]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: Input,
) -> Response[Union[HTTPValidationError, Output]]:
    """Queue

     Queue a video ID for processing

    Args:
        json_body (Input):

    Returns:
        Response[Union[HTTPValidationError, Output]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: Input,
) -> Optional[Union[HTTPValidationError, Output]]:
    """Queue

     Queue a video ID for processing

    Args:
        json_body (Input):

    Returns:
        Response[Union[HTTPValidationError, Output]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: Input,
) -> Response[Union[HTTPValidationError, Output]]:
    """Queue

     Queue a video ID for processing

    Args:
        json_body (Input):

    Returns:
        Response[Union[HTTPValidationError, Output]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: Input,
) -> Optional[Union[HTTPValidationError, Output]]:
    """Queue

     Queue a video ID for processing

    Args:
        json_body (Input):

    Returns:
        Response[Union[HTTPValidationError, Output]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
