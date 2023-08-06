from __future__ import annotations

import dataclasses
import datetime
import re
import shlex
from typing import Pattern

from coredis.typing import (
    AbstractSet,
    ClassVar,
    Dict,
    List,
    Literal,
    Mapping,
    NamedTuple,
    Optional,
    OrderedDict,
    Set,
    StringT,
    Tuple,
    TypedDict,
    Union,
    ValueT,
)

#: Response from `CLIENT INFO <https://redis.io/commands/client-info>`__
#:
#: - ``id``: a unique 64-bit client ID
#: - ``addr``: address/port of the client
#: - ``laddr``: address/port of local address client connected to (bind address)
#: - ``fd``: file descriptor corresponding to the socket
#: - ``name``: the name set by the client with CLIENT SETNAME
#: - ``age``: total duration of the connection in seconds
#: - ``idle``: idle time of the connection in seconds
#: - ``flags``: client flags
#: - ``db``: current database ID
#: - ``sub``: number of channel subscriptions
#: - ``psub``: number of pattern matching subscriptions
#: - ``multi``: number of commands in a MULTI/EXEC context
#: - ``qbuf``: query buffer length (0 means no query pending)
#: - ``qbuf-free``: free space of the query buffer (0 means the buffer is full)
#: - ``argv-mem``: incomplete arguments for the next command (already extracted from query buffer)
#: - ``multi-mem``: memory is used up by buffered multi commands. Added in Redis 7.0
#: - ``obl``: output buffer length
#: - ``oll``: output list length (replies are queued in this list when the buffer is full)
#: - ``omem``: output buffer memory usage
#: - ``tot-mem``: total memory consumed by this client in its various buffers
#: - ``events``: file descriptor events
#: - ``cmd``: last command played
#: - ``user``: the authenticated username of the client
#: - ``redir``: client id of current client tracking redirection
#: - ``resp``: client RESP protocol version. Added in Redis 7.0
ClientInfo = TypedDict(
    "ClientInfo",
    {
        "id": int,
        "addr": str,
        "laddr": str,
        "fd": int,
        "name": str,
        "age": int,
        "idle": int,
        "flags": str,
        "db": int,
        "sub": int,
        "psub": int,
        "multi": int,
        "qbuf": int,
        "qbuf-free": int,
        "argv-mem": int,
        "multi-mem": int,
        "obl": int,
        "oll": int,
        "omem": int,
        "tot-mem": int,
        "events": str,
        "cmd": str,
        "user": str,
        "redir": int,
        "resp": str,
    },
)

#: Script/Function flags
#: See: `<https://redis.io/topics/lua-api#a-namescriptflagsa-script-flags>`__
ScriptFlag = Literal[
    "no-writes",
    "allow-oom",
    "allow-stale",
    "no-cluster",
    b"no-writes",
    b"allow-oom",
    b"allow-stale",
    b"no-cluster",
]


class FunctionDefinition(TypedDict):
    """
    Function definition as returned by `FUNCTION LIST <https://redis.io/commands/function-list>`__
    """

    #: the name of the function
    name: Union[str, bytes]
    #: the description of the function
    description: Union[str, bytes]
    #: function flags
    flags: Set[ScriptFlag]


class LibraryDefinition(TypedDict):
    """
    Library definition as returned by `FUNCTION LIST <https://redis.io/commands/function-list>`__
    """

    #: the name of the library
    name: Union[str, bytes]
    #: the engine used by the library
    engine: Literal["LUA"]
    #: the library's description
    description: Union[str, bytes]
    #: Mapping of function names to functions in the library
    functions: Dict[Union[str, bytes], FunctionDefinition]
    #: The library's source code
    library_code: Optional[Union[str, bytes]]


class ScoredMember(NamedTuple):
    """
    Member of a sorted set
    """

    #: The sorted set member name
    member: Union[str, bytes]
    #: Score of the member
    score: float


class GeoCoordinates(NamedTuple):
    """
    A longitude/latitude pair identifying a location
    """

    #: Longitude
    longitude: float
    #: Latitude
    latitude: float


ScoredMembers = Tuple[ScoredMember, ...]


class GeoSearchResult(NamedTuple):
    """
    Structure of a geo query
    """

    #: Place name
    name: Union[str, bytes]
    #: Distance
    distance: Optional[float]
    #: GeoHash
    geohash: Optional[int]
    #: Lat/Lon
    coordinates: Optional[GeoCoordinates]


#: Definition of a redis command
#: See: `<https://redis.io/topics/key-specs>`__
#:
#: - ``name``: This is the command's name in lowercase
#: - ``arity``: Arity is the number of arguments a command expects.
#: - ``flags``: See `<https://redis.io/commands/command#flags>`__
#: - ``first-key``: This value identifies the position of the command's first key name argumen
#: - ``last-key``: This value identifies the position of the command's last key name argument
#: - ``step``: This value is the step, or increment, between the first key and last key values
#:   where the keys are.
#: - ``acl-categories``: This is an array of simple strings that are the ACL categories to which
#:   the command belongs
#: - ``tips``: Helpful information about the command
#: - ``key-specification``: This is an array consisting of the command's key specifications
#: - ``sub-commands``: This is an array containing all of the command's subcommands, if any
Command = TypedDict(
    "Command",
    {
        "name": str,
        "arity": int,
        "flags": AbstractSet[str],
        "first-key": int,
        "last-key": int,
        "step": int,
        "acl-categories": Optional[AbstractSet[str]],
        "tips": Optional[AbstractSet[str]],
        "key-specifications": Optional[
            AbstractSet[Mapping[str, Union[int, str, Mapping]]]  # type: ignore
        ],
        "sub-commands": Optional[Tuple[str, ...]],
    },
)


class RoleInfo(NamedTuple):
    """
    Redis instance role information
    """

    #:
    role: str
    #:
    offset: Optional[int] = None
    #:
    status: Optional[str] = None
    #:
    slaves: Optional[Tuple[Dict[str, Union[str, int]], ...]] = None
    #:
    masters: Optional[Tuple[str, ...]] = None


class StreamEntry(NamedTuple):
    """
    Structure representing an entry in a redis stream
    """

    identifier: Union[bytes, str]
    field_values: OrderedDict[Union[bytes, str], Union[bytes, str]]


#: Details of a stream
#: See: `<https://redis.io/commands/xinfo-stream>`__
StreamInfo = TypedDict(
    "StreamInfo",
    {
        "first-entry": Optional[StreamEntry],
        "last-entry": Optional[StreamEntry],
        "length": int,
        "radix-tree-keys": int,
        "radix-tree-nodes": int,
        "groups": Union[int, Dict],  # type: ignore
        "last-generated-id": str,
        "max-deleted-entry-id": str,
        "recorded-first-entry-id": str,
        "entries-added": int,
        "entries-read": int,
        "entries": Optional[Tuple[StreamEntry, ...]],
    },
)


class StreamPending(NamedTuple):
    """
    Summary response from
    `XPENDING <https://redis.io/commands/xpending#summary-form-of-xpending>`__
    """

    pending: int
    minimum_identifier: Union[bytes, str]
    maximum_identifier: Union[bytes, str]
    consumers: OrderedDict[Union[bytes, str, int], Union[bytes, str, int]]


class StreamPendingExt(NamedTuple):
    """
    Extended form response from
    `XPENDING <https://redis.io/commands/xpending#extended-form-of-xpending>`__
    """

    identifier: Union[bytes, str]
    consumer: Union[bytes, str]
    idle: int
    delivered: int


#: Response from `SLOWLOG GET <https://redis.io/commands/slowlog-get>`__
class SlowLogInfo(NamedTuple):
    #: A unique progressive identifier for every slow log entry.
    id: int
    #: The unix timestamp at which the logged command was processed.
    start_time: int
    #: The amount of time needed for its execution, in microseconds.
    duration: int
    #: The array composing the arguments of the command.
    command: Tuple[Union[bytes, str], ...]
    #: Client IP address and port
    client_addr: Tuple[Union[bytes, str], int]
    #: Client name
    client_name: str


class LCSMatch(NamedTuple):
    """
    An instance of an LCS match
    """

    #: Start/end offset of the first string
    first: Tuple[int, int]
    #: Start/end offset of the second string
    second: Tuple[int, int]
    #: Length of the match
    length: Optional[int]


class LCSResult(NamedTuple):
    """
    Results from `LCS <https://redis.io/commands/lcs>`__
    """

    #: matches
    matches: Tuple[LCSMatch, ...]
    #: Length of longest match
    length: int


@dataclasses.dataclass
class MonitorResult:
    """
    Details of issued commands received by the client when
    listening with the `MONITOR <https://redis.io/commands/monitor>`__
    command
    """

    #: Time command was received
    time: datetime.datetime
    #: db number
    db: int
    #: (host, port) or path if the server is listening on a unix domain socket
    client_addr: Optional[Union[Tuple[str, int], str]]
    #: The type of the client that send the command
    client_type: Literal["tcp", "unix", "lua"]
    #: The name of the command
    command: str
    #: Arguments passed to the command
    args: Optional[Tuple[str, ...]]

    EXPR: ClassVar[Pattern[str]] = re.compile(r"\[(\d+) (.*?)\] (.*)$")

    @classmethod
    def parse_response_string(cls, response: str) -> MonitorResult:
        command_time, command_data = response.split(" ", 1)
        match = cls.EXPR.match(command_data)
        assert match
        db_id, client_info, command = match.groups()
        command = shlex.split(command)
        client_addr = None
        client_type: Literal["tcp", "unix", "lua"]
        if client_info == "lua":
            client_type = "lua"
        elif client_info.startswith("unix"):
            client_type = "unix"
            client_addr = client_info[5:]
        else:
            host, port = client_info.rsplit(":", 1)
            client_addr = (host, int(port))
            client_type = "tcp"
        return cls(
            time=datetime.datetime.fromtimestamp(float(command_time)),
            db=int(db_id),
            client_addr=client_addr,
            client_type=client_type,
            command=command[0],
            args=tuple(command[1:]),
        )


class ClusterNode(TypedDict):
    host: str
    port: int
    node_id: Optional[str]
    server_type: Optional[Literal["master", "slave"]]


class ClusterNodeDetail(TypedDict):
    id: str
    flags: Tuple[str, ...]
    host: str
    port: int
    master: Optional[str]
    ping_sent: int
    pong_recv: int
    link_state: str
    slots: List[int]
    migrations: List[Dict[str, ValueT]]


class PubSubMessage(TypedDict):
    type: str
    pattern: Optional[StringT]
    channel: StringT
    data: StringT
