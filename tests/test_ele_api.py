from . import setup_db
from aiohttp.test_utils import TestClient, loop_context

def test_ele_search_api(app):
    with loop_context() as loop:
        with TestClient(app, loop=loop) as client:

            async def _test_ele_search_api():
                nonlocal client
                dordb = await setup_db() # mongodb 数据库
                app['dordb'] = dordb
                # 正常查询
                postdata1 = {
                    "dor": "东16-425",
                    "type": "light"
                }
                # 测试寝室不存在
                postdata2 = {
                    "dor": "东16-666",
                    "type": "air"
                }
                resp = await client.post('/api/ele/', data=postdata1)
                assert resp.status == 200
                resp = await client.post('/api/ele/', data=postdata2)
                assert resp.status == 404

            loop.run_until_complete(_test_ele_search_api())
