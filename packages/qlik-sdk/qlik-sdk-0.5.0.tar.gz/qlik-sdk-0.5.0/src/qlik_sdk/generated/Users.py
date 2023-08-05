# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services Grafana 1.0.0-202205031030

from __future__ import annotations
from typing import Iterator, Union
from dataclasses import dataclass, asdict, is_dataclass
import io
import itertools
from ..auth import Auth, Config
from ..listobj import ListObj
from ..rpc import RpcSession


@dataclass
class User:
    """

    Attributes
    ----------
    id: str
    name: str
    subject: str
    tenantId: str
    created: str
      Deprecated. Use `createdAt` instead.
    email: str
      Email is a required field when tenantAdmin creates users with status as 'invited'
    inviteExpiry: float
    lastUpdated: str
      Deprecated. Use `lastUpdatedAt` instead.
    links: object
    locale: str
      Represents the end-user's language tag.
    picture: str
    preferredLocale: str
      Represents the end-user's preferred language tag.
    preferredZoneinfo: str
      Represents the end-user's preferred time zone.
    roles: list[str]
      List of system roles to which the user has been assigned. Only returned when permitted by access control. Deprecated. Use `assignedRoles` instead.
    status: str
    zoneinfo: str
      Represents the end-user's time zone.
    """

    id: str = None
    name: str = None
    subject: str = None
    tenantId: str = None
    created: str = None
    email: str = None
    inviteExpiry: float = None
    lastUpdated: str = None
    links: object = None
    locale: str = None
    picture: str = None
    preferredLocale: str = None
    preferredZoneinfo: str = None
    roles: list[str] = None
    status: str = None
    zoneinfo: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "subject" in kvargs:
            if type(kvargs["subject"]).__name__ is self_.__annotations__["subject"]:
                self_.subject = kvargs["subject"]
            else:
                self_.subject = kvargs["subject"]
        if "tenantId" in kvargs:
            if type(kvargs["tenantId"]).__name__ is self_.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "created" in kvargs:
            if type(kvargs["created"]).__name__ is self_.__annotations__["created"]:
                self_.created = kvargs["created"]
            else:
                self_.created = kvargs["created"]
        if "email" in kvargs:
            if type(kvargs["email"]).__name__ is self_.__annotations__["email"]:
                self_.email = kvargs["email"]
            else:
                self_.email = kvargs["email"]
        if "inviteExpiry" in kvargs:
            if (
                type(kvargs["inviteExpiry"]).__name__
                is self_.__annotations__["inviteExpiry"]
            ):
                self_.inviteExpiry = kvargs["inviteExpiry"]
            else:
                self_.inviteExpiry = kvargs["inviteExpiry"]
        if "lastUpdated" in kvargs:
            if (
                type(kvargs["lastUpdated"]).__name__
                is self_.__annotations__["lastUpdated"]
            ):
                self_.lastUpdated = kvargs["lastUpdated"]
            else:
                self_.lastUpdated = kvargs["lastUpdated"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]
        if "locale" in kvargs:
            if type(kvargs["locale"]).__name__ is self_.__annotations__["locale"]:
                self_.locale = kvargs["locale"]
            else:
                self_.locale = kvargs["locale"]
        if "picture" in kvargs:
            if type(kvargs["picture"]).__name__ is self_.__annotations__["picture"]:
                self_.picture = kvargs["picture"]
            else:
                self_.picture = kvargs["picture"]
        if "preferredLocale" in kvargs:
            if (
                type(kvargs["preferredLocale"]).__name__
                is self_.__annotations__["preferredLocale"]
            ):
                self_.preferredLocale = kvargs["preferredLocale"]
            else:
                self_.preferredLocale = kvargs["preferredLocale"]
        if "preferredZoneinfo" in kvargs:
            if (
                type(kvargs["preferredZoneinfo"]).__name__
                is self_.__annotations__["preferredZoneinfo"]
            ):
                self_.preferredZoneinfo = kvargs["preferredZoneinfo"]
            else:
                self_.preferredZoneinfo = kvargs["preferredZoneinfo"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ is self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        if "status" in kvargs:
            if type(kvargs["status"]).__name__ is self_.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "zoneinfo" in kvargs:
            if type(kvargs["zoneinfo"]).__name__ is self_.__annotations__["zoneinfo"]:
                self_.zoneinfo = kvargs["zoneinfo"]
            else:
                self_.zoneinfo = kvargs["zoneinfo"]

    def delete(self) -> None:
        """
        Deletes a user resource.
        Parameters
        ----------
        """

        self.auth.rest(
            path="/users/{userId}".replace("{userId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patch(self, body: UserPatchSchema) -> None:
        """
        Updates a user resource.
        Parameters
        ----------
        body: UserPatchSchema
        """

        try:
            data = asdict(body)
        except:
            data = body

        self.auth.rest(
            path="/users/{userId}".replace("{userId}", self.id),
            method="PATCH",
            params={},
            data=data,
        )


@dataclass
class Metadata:
    """

    Attributes
    ----------
    valid_roles: list[str]
      List of system roles to which the user can be assigned.
    """

    valid_roles: list[str] = None

    def __init__(self_, **kvargs):
        if "valid_roles" in kvargs:
            if (
                type(kvargs["valid_roles"]).__name__
                is self_.__annotations__["valid_roles"]
            ):
                self_.valid_roles = kvargs["valid_roles"]
            else:
                self_.valid_roles = kvargs["valid_roles"]


@dataclass
class UserCount:
    """

    Attributes
    ----------
    total: float
    """

    total: float = None

    def __init__(self_, **kvargs):
        if "total" in kvargs:
            if type(kvargs["total"]).__name__ is self_.__annotations__["total"]:
                self_.total = kvargs["total"]
            else:
                self_.total = kvargs["total"]


@dataclass
class UserPatch:
    """
    A JSON Patch document as defined in http://tools.ietf.org/html/rfc6902.

    Attributes
    ----------
    op: str
      The operation to be performed.
    path: str
      A JSON Pointer.
    value: Union[str,float,bool,list,object]
      The value to be used for this operation.
    """

    op: str = None
    path: str = None
    value: Union[str, float, bool, list, object] = None

    def __init__(self_, **kvargs):
        if "op" in kvargs:
            if type(kvargs["op"]).__name__ is self_.__annotations__["op"]:
                self_.op = kvargs["op"]
            else:
                self_.op = kvargs["op"]
        if "path" in kvargs:
            if type(kvargs["path"]).__name__ is self_.__annotations__["path"]:
                self_.path = kvargs["path"]
            else:
                self_.path = kvargs["path"]
        if "value" in kvargs:
            if type(kvargs["value"]).__name__ is self_.__annotations__["value"]:
                self_.value = kvargs["value"]
            else:
                self_.value = kvargs["value"]


@dataclass
class UserPatchSchema(dict):
    """
    An array of JSON Patch documents

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        pass


@dataclass
class UserPostSchema:
    """

    Attributes
    ----------
    name: str
    subject: str
    tenantId: str
    email: str
      Email is a required field when tenantAdmin creates users with status as 'invited'
    picture: str
    roles: list[str]
      List of system roles to which the user has been assigned. Only returned when permitted by access control.
    status: str
    """

    name: str = None
    subject: str = None
    tenantId: str = None
    email: str = None
    picture: str = None
    roles: list[str] = None
    status: str = None

    def __init__(self_, **kvargs):
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "subject" in kvargs:
            if type(kvargs["subject"]).__name__ is self_.__annotations__["subject"]:
                self_.subject = kvargs["subject"]
            else:
                self_.subject = kvargs["subject"]
        if "tenantId" in kvargs:
            if type(kvargs["tenantId"]).__name__ is self_.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "email" in kvargs:
            if type(kvargs["email"]).__name__ is self_.__annotations__["email"]:
                self_.email = kvargs["email"]
            else:
                self_.email = kvargs["email"]
        if "picture" in kvargs:
            if type(kvargs["picture"]).__name__ is self_.__annotations__["picture"]:
                self_.picture = kvargs["picture"]
            else:
                self_.picture = kvargs["picture"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ is self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        if "status" in kvargs:
            if type(kvargs["status"]).__name__ is self_.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]


@dataclass
class UsersClass:
    """

    Attributes
    ----------
    data: list[User]
    links: object
    """

    data: list[User] = None
    links: object = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [User(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]


class Users:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_users(self, max_items=10, **queryParams) -> ListObj[User]:
        """
        Retrieves a list of users matching the query.
        tenantId: str
          The tenant ID to filter by. Deprecated. Use the new `filter` parameter to provide a SCIM-syntax filter.

        subject: str
          The subject to filter by. Deprecated. Use the new `filter` parameter to provide a SCIM-syntax filter.

        email: str
          The email to filter by. Deprecated. Use the new `filter` parameter to provide a SCIM-syntax filter.

        status: str
          The status to filter by. Supports multiple values delimited by commas. Deprecated. Use the new `filter` parameter to provide a SCIM-syntax filter.

        role: str
          The role to filter by. Deprecated. Use the new `filter` parameter to provide a SCIM-syntax filter.

        fields: str
          A comma-delimited string of the requested fields per entity. If the 'links' value is omitted, then the entity HATEOAS link will also be omitted.

        limit: float
          The number of user entries to retrieve.

        sort: str
          The field to sort by, with +/- prefix indicating sort order

        sortBy: str
          The user parameter to sort by. Deprecated. Use `sort` instead.

        sortOrder: str
          The sort order, either ascending or descending. Deprecated. Use `sort` instead.

        startingAfter: str
          Get users with IDs that are higher than the target user ID. Cannot be used in conjunction with endingBefore. Deprecated. Use `next` instead.

        endingBefore: str
          Get users with IDs that are lower than the target user ID. Cannot be used in conjunction with startingAfter. Deprecated. Use `prev` instead.

        Parameters
        ----------
        **queryParams
        """

        iter = self.auth.paginate_rest(
            path="/users",
            method="GET",
            params=queryParams,
            cls=User,
            max_items=max_items,
        )
        lst = ListObj()
        i = 0
        while i < min(max_items, 10):
            try:
                lst.append(next(iter))
                i += 1
            except StopIteration:
                break
        lst.iter = itertools.chain(lst, iter)
        return lst

    def create(self, body: UserPostSchema) -> User:
        """
        Creates a user in a given tenant.
        Parameters
        ----------
        body: UserPostSchema
        """

        try:
            data = asdict(body)
        except:
            data = body

        response = self.auth.rest(
            path="/users",
            method="POST",
            params={},
            data=data,
        )
        obj = User(**response.json())
        obj.auth = self.auth
        return obj

    def count(self, **queryParams) -> UserCount:
        """
        Returns the number of users in a given tenant
        tenantId: str
          The tenant ID to filter by.

        Parameters
        ----------
        **queryParams
        """

        response = self.auth.rest(
            path="/users/actions/count",
            method="GET",
            params=queryParams,
            data=None,
        )
        obj = UserCount(**response.json())
        obj.auth = self.auth
        return obj

    def get_me(self) -> any:
        """
        Redirects to retrieve the user resource associated with the JWT claims.
        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/users/me",
            method="GET",
            params={},
            data=None,
        )
        return response.json()

    def get_metadata(self) -> Metadata:
        """
        Returns the metadata with regard to the user configuration.
        Deprecated, use GET /v1/roles instead.
        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/users/metadata",
            method="GET",
            params={},
            data=None,
        )
        obj = Metadata(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, userId: str) -> User:
        """
        Retrieves a user resource.
        Parameters
        ----------
        userId: str
        """

        response = self.auth.rest(
            path="/users/{userId}".replace("{userId}", userId),
            method="GET",
            params={},
            data=None,
        )
        obj = User(**response.json())
        obj.auth = self.auth
        return obj
