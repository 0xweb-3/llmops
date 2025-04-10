import pytest

from pkg.response import HttpCode


class TestAppHandler:
    """app控制器的测试类"""

    # def test_completion(self, client):
    #     resp = client.post("/chat", json={"query": "什么是ai agent？"})
    #     assert resp.status_code == 200
    #     assert resp.json.get("code") == HttpCode.SUCCESS
    #     print("响应内容")

    @pytest.mark.parametrize("query", [None, "什么是ai agent？"])
    def test_completion(self, query, client):
        resp = client.post("/chat", json={"query": query})
        assert resp.status_code == 200
        if query is None:
            assert resp.json.get("code") == HttpCode.VALIDATE_ERROR
        else:
            assert resp.json.get("code") == HttpCode.SUCCESS
        print("响应内容：", resp.json)
