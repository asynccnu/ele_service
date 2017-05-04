import os
import base64
from . import setup_db
from aiohttp.test_utils import TestClient, loop_context

def test_ele_api(app):
    with loop_context() as loop:
        with TestClient(app, loop=loop) as client:
            
            auth = os.getenv('ADMIN') + ':' + os.getenv('ADMINPWD')
            headers = {'Authorization': 'Basic %s' % base64.b16encode(auth.encode())}

            async def _test_ele_get_api():
                nonlocal client
                dordb = await setup_db() # mongodb 测试数据库
                app['dordb'] = dordb
                resp = await client.get('/api/ele/', headers=headers)
                print(await resp.text())
                assert await resp.text() == "{'msg': 'dormitory info stored'}"
                print(".... ele get api [OK]")

            async def _test_ele_delete_api():
                nonlocal client
                dordb = await setup_db()
                app['dordb'] = dordb
                resp = await client.delete('/api/ele/', headers=headers)
                assert await resp.text() == "{'msg': 'delete dormitory info'}"
                print("... ele delete api [OK]")

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
                print(".... ele search api [OK]")

            loop.run_until_complete(_test_ele_get_api())
            loop.run_until_complete(_test_ele_search_api())
            loop.close()
