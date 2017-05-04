import json
from aiohttp import web
from aiohttp.web import Response
from .spider import dor_spider, get_ele
from .decorator import require_admin_login

api = web.Application()

# ====== async view handlers ======
async def ele_search_api(request):
    dordb = request.app['dordb']
    ele_dict = await dordb.dormitories.find_one()
    dor_dict = ele_dict['meter']

    try:
        json_data = await request.json()
    except json.decoder.JSONDecodeError:
        return Response(body = b'{"error": "post json data error"}',
            content_type = 'application/json', status = 500)
    dor = json_data.get('dor')
    typeit = json_data.get('type')
    _dor = dor_dict.get(dor)
    if _dor is None:
        return Response(body = b'{}',
            content_type = 'application/json', status = 404)
    if typeit == 'light': # 照明电费
        meter = _dor[0]
    elif typeit == 'air': # 空调电费
        if len(_dor) == 1:
            meter = 0
        else: meter = _dor[1]
    rv = await get_ele(meter, dor, typeit)
    if rv:
        return web.json_response(rv)
    else: return Response(body = b'{"msg": "fuck ccnu"}',
        content_type = 'application/json', status = 500)

@require_admin_login
async def ele_store_api(request):
    dordb = request.app['dordb']
    if (await dordb.dormitories.find_one()) is None:
        _meter_index = await dor_spider()
        await dordb['dormitories'].insert_one({'meter': _meter_index})
        return web.json_response({'msg': 'dormitory info stored',
            'dor_dict': _meter_index})
    else:
        return web.json_response({'msg': 'dormitory info already stored'})

@require_admin_login
async def ele_delete_api(request):
    dordb = request.app['dordb']
    if (await dordb.dormitories.find_one()) is None:
        return web.json_response({'msg': 'dormitory info already deleted'})
    else:
        await dordb.drop_collection('dormitories')
        return web.json_response({'msg': 'delete dormitory info'})

# =================================

# ====== url --------- maps  ======
api.router.add_route('POST', '/ele/', ele_search_api, name='ele_search_api')
api.router.add_route('DELETE', '/ele/', ele_delete_api, name='ele_delete_api')
api.router.add_route('GET', '/ele/', ele_store_api, name='ele_store_api')
# =================================
