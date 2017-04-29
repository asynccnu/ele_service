import os
import json
import base64
import functools
import aiohttp
from aiohttp.web import Response

def require_admin_login(f):
    @functools.wraps(f)
    async def decorator(request, *args, **kwargs):
        authorized = False
        headers = request.headers # .keys()
        req_headers = dict(headers)

        basic_auth_header = req_headers.get('Authorization')
        if basic_auth_header:
            auth_header = basic_auth_header[6:]
            admin, pwd = base64.b64decode(auth_header).decode().split(':')
            if admin == os.getenv('ADMIN') and \
               pwd == os.getenv('ADMINPWD'):
                   authorized = True
            else: return Response(body = b'{}',
                content_type = 'application/json', status = 403)

        if authorized:
            response = await f(request)
            return response
        else:
            return Response(body = b'{}',
            content_type = 'application/json', status = 401)
    return decorator
