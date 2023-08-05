import enum
from functools import reduce
import requests
import re
from dataclasses import dataclass

from typing import Callable, Generic, List, TypeVar, TypedDict, Union

from .config import Config


class HTTPMethods(enum.Enum):
    "GET",
    "OPTIONS",
    "HEAD",
    "POST",
    "PUT",
    "PATCH",
    "DELETE"


class NoUrlException(Exception):
    """
    NoUrlException represents a missing URL
    """

    pass


class ConnectionException(Exception):
    """
    ConnectionException represents a failure in the request
    The request raised an exception
    ConnectionException is not a 4xx response
    """

    pass


class AuthenticationException(Exception):
    """
    AuthenticationException represents a failure to authenticate
    """

    pass


def _get_dict(o: any):
    """
    get_dict attempts to convert objects to dict, nested
    """
    try:
        d = o.__dict__
        for k in d:
            d[k] = _get_dict(d[k])
        return d
    except (Exception):
        return o


T = TypeVar("T")


class InterceptorHandler(Generic[T]):
    handlers: List[T]
    "list containing the interceptors"

    def __init__(self):
        self.handlers = []

    def use(self, interceptor: Union[T, List[T]]) -> None:
        """
        method helper for registering an interceptor
        Parameters
        ----------
        interceptor: function interceptor for requests/responses
        """
        if isinstance(interceptor, list):
            self.handlers = self.handlers + interceptor
        else:
            self.handlers.append(interceptor)


RequestInterceptor = Callable[[requests.Request], requests.Request]
""" REST Request interceptor """
ResponseInterceptor = Callable[[requests.Response], requests.Response]
""" REST Request interceptor """


class Interceptors(TypedDict):
    response: InterceptorHandler[ResponseInterceptor]
    request: InterceptorHandler[RequestInterceptor]


@dataclass
class RestClient:
    """
    RestClient represents a rest client for making api calls
    """

    config: Config
    base_url: str
    _interceptors: Interceptors = None

    def __init__(self, config) -> None:
        self.config = config
        self.base_url = config.host
        self._interceptors = dict(
            request=InterceptorHandler[RequestInterceptor](),
            response=InterceptorHandler[ResponseInterceptor](),
        )

    def rest(
        self,
        path: str,
        method: HTTPMethods = "GET",
        data=None,
        files=None,
        params: dict = None,
        headers: dict = None,
        stream: bool = False,
    ) -> requests.Response:
        """
        rest sends a request
        """
        if not self.base_url:
            raise NoUrlException("Caller has no 'base_url'")
        if not path.startswith("/api/v1/"):
            path = "/api/v1/" + path.strip("/")

        # If the data can be converted to a dict then send
        # it as json, otherwise send it as data.
        json_data = None
        if data and not isinstance(data, bytes):
            json_data = _get_dict(data)
            if json_data:
                data = None
        if params:
            params = _get_dict(params)
        # Create request.
        req = requests.Request(
            method,
            self.base_url.strip("/") + path,
            data=data,
            json=json_data,
            files=files,
            headers=headers,
            params=params,
        )

        req = reduce(lambda d, f: f(d), self._interceptors["request"].handlers, req)
        with requests.Session() as session:
            session.stream = stream
            prepared = req.prepare()
            try:
                res = session.send(prepared)
            except Exception as exc:
                raise ConnectionException("Connection Error: " + self.base_url) from exc

            res = reduce(
                lambda r, f: f(r), self._interceptors["response"].handlers, res
            )

            try:
                res.raise_for_status()
            except Exception as e:
                res.close()
                if res.status_code == 401:
                    raise AuthenticationException("Failed to authenticate")
                raise e

            return res

    def paginate_rest(
        self, path: str, method: str = "get", params: dict = {}, cls=None, max_items=10
    ):
        curr_params = params.copy()
        if "limit" not in curr_params:
            curr_params["limit"] = 10
        done = False
        yield_count = 0
        while not done:
            raw_response = self.rest(
                method=method, path=path, data=None, params=curr_params
            )
            response = raw_response.json()
            for i in response["data"]:
                yield_item = i
                if cls:
                    yield_item = cls(**i)
                yield yield_item
                yield_count += 1
                if yield_count == max_items:
                    return
            try:
                curr_params["next"] = re.sub(
                    r".*next=", "", response["links"]["next"]["href"]
                )
            except:
                done = True


class RestClientInstance:
    interceptors: Interceptors

    def __init__(self, restClient: RestClient) -> None:
        self._restClient = restClient
        self.interceptors = restClient._interceptors
        self.paginate_rest = self._restClient.paginate_rest

    def __call__(self, **all: requests.Request) -> requests.Request:
        return self._restClient.rest(**all)
