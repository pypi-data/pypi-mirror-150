from __future__ import annotations

import pytest

import coredis
from coredis import PureToken, ResponseError
from tests.conftest import targets


@targets(
    "redis_basic",
    "redis_basic_raw",
    "redis_basic_resp3",
    "redis_basic_raw_resp3",
    "keydb",
)
@pytest.mark.asyncio()
class TestConnection:
    async def test_ping(self, client, _s):
        resp = await client.ping()
        assert resp == _s("PONG")

    async def test_ping_custom_message(self, client, _s):
        resp = await client.ping(message="PANG")
        assert resp == _s("PANG")

    async def test_echo(self, client, _s):
        assert await client.echo("foo bar") == _s("foo bar")

    async def test_client_id(self, client, _s):
        id_ = await client.client_id()
        assert isinstance(id_, int)

    @pytest.mark.min_server_version("6.2.0")
    async def test_client_info(self, client, _s):
        info = await client.client_info()
        assert isinstance(info, dict)
        assert "addr" in info

    async def test_client_reply(self, client, _s):
        assert await client.client_reply(PureToken.ON)

    @pytest.mark.min_server_version("6.2.0")
    async def test_client_trackinginfo_no_tracking(self, client, _s):
        info = await client.client_trackinginfo()
        assert info[_s("flags")] == {_s("off")}

    @pytest.mark.min_server_version("6.2.0")
    async def test_client_trackinginfo_tracking_set(self, client, _s):
        resp = await client.client_tracking(PureToken.ON)
        assert resp
        info = await client.client_trackinginfo()
        assert info[_s("flags")] == {_s("on")}

    async def test_client_list(self, client, _s):
        clients = await client.client_list()
        assert isinstance(clients[0], dict)
        assert "addr" in clients[0]

    @pytest.mark.min_server_version("6.2.0")
    async def test_client_list_with_specific_ids(self, client, _s):
        clients = await client.client_list()
        ids = [c["id"] for c in clients]
        assert ids
        refetch = await client.client_list(identifiers=ids)
        assert sorted(k["addr"] for k in refetch) == sorted(k["addr"] for k in clients)

    async def test_client_kill_fail(self, client, _s):
        with pytest.raises(ResponseError):
            await client.client_kill(ip_port="1.1.1.1:9999")

    async def test_client_kill_filter(self, client, _s):
        resp = await client.client_kill(type_=PureToken.NORMAL)
        assert resp > 0

    async def test_client_kill_filter_skip_me(self, client, _s):
        resp = await client.client_kill(type_=PureToken.NORMAL, skipme=True)
        assert resp > 0

    async def test_client_list_after_client_setname(self, client, _s):
        await client.client_setname("cl=i=ent")
        clients = await client.client_list()
        assert "cl=i=ent" in [c["name"] for c in clients]

    async def test_client_getname(self, client, _s):
        assert await client.client_getname() is None

    async def test_client_setname(self, client, _s):
        assert await client.client_setname("redis_py_test")
        assert await client.client_getname() == _s("redis_py_test")

    async def test_client_pause(self, client, event_loop):
        key = "key_should_expire"
        another_client = coredis.Redis(loop=event_loop)
        await client.set(key, "1", px=100)
        assert await client.client_pause(100)
        res = await another_client.get(key)
        assert not res

    @pytest.mark.min_server_version("6.2.0")
    async def test_select(self, client, _s):
        assert (await client.client_info())["db"] == 0
        assert await client.select(1)
        assert (await client.client_info())["db"] == 1

    @pytest.mark.min_server_version("6.2.0")
    async def test_reset(self, client, _s):
        assert (await client.client_info())["db"] == 0
        assert await client.select(1)
        assert (await client.client_info())["db"] == 1
        await client.reset()
        assert (await client.client_info())["db"] == 0
