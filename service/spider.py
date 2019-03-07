import os
import html
import aiohttp
import asyncio
from bs4 import BeautifulSoup

html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'htmls'))
ele_url = "http://202.114.38.46/SelectPage.aspx/SerBindTabDate"
new_ele_url = "http://jnb.ccnu.edu.cn/weixin/example/demo/search.php"
none_data = {
    'dor': "%s",
    'degree': {
        'remain': "",
        'before': "",
        'current': ""
    },
    'ele': {
        '_ele': "",
        'remain': "",
        'before': "",
        'current': ""
    }
}
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
}

async def dor_spider():
    _meter_index = {}
    for dirs, subdirs, files in os.walk(html_path):
        for file in files:
            file_path = os.path.join(html_path, file)
            soup = BeautifulSoup(open(file_path), 'lxml')
            options = soup.find('tr', id='MeterDiv').find_all('option')
            _key_value = []
            for option in options:
                if file[0] not in ['d', 's', 'x', 'y', 'n', 'c']:
                    # 国交
                    building = file[0]
                    key = option.get('value').split('*')[-2]
                    if '国' not in key:
                        if (("空调" in key) or ("照明" in key)):
                            key = u'国' + building + '-' + key[:-2]
                        else: key = u'国' + building + '-' + key
                elif file[0] == 'c':
                    # 产宿
                    key = option.get('value').split('*')[-2][:-2]
                    if '-' in key:
                        _key = key.split('-')
                        if len(_key[-1]) == 1:
                            _key[-1] = "0"+_key[-1]
                        key = (_key[0][0]+_key[0][-1]) + '-' + _key[1][:-1] + _key[-1]
                elif file[0] == 's':
                    # 南湖
                    # 南湖有的寝室没有空调(((ﾟДﾟ;)))
                    key = option.get('value').split('*')[-2]
                    if (("空调" in key) or ("照明" in key)):
                        key = key[:-2]
                else:
                    # 其他寝室
                    key = option.get('value').split('*')[-2][:-2]  # dor
                    if "新增" in key:
                        key = key.replace(u"新增", "")
                    elif "新" in key:
                        key = key.replace(u"新", "")
                value = option.get('value').split('*')[0]          # meter
                if key in _meter_index.keys():
                    _meter_index[key].append(value)
                else:
                    _meter_index[key] = [value]
        return _meter_index

async def get_old_ele(meter, dor, typeit):
    """
    -> 旧电费接口爬虫
    """
    post_data = {
            "nodeInText": "%s*Meter" % meter,
            "PartList": "",
            "SelectPart": 1}
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True), headers=headers) as session:
        async with session.post(ele_url, data=post_data, timeout=5) as resp:
            content = await resp.json()
            main_html = content.get('d').split('|')[1].replace('', '')
            parse_html = html.unescape(main_html)
            html = '<html><body>' + parse_html + '</body></html>'
            soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
            divMeterTopBox = soup.find('div', id='divMeterTopBox')
            divMeterTopBoxtrs = divMeterTopBox.tr.next_siblings

            _tr_dict = {}; _key = 0
            for tr in divMeterTopBoxtrs:
                _key += 1
                _tr_dict.update({str(_key): tr})

            _ele = float(_tr_dict['4'].td.next_sibling.text[:-1])

            if typeit == 'light':
                ele_remain = float(divMeterTopBox.find('td', id='tdSYValue').text[:-1])
                degree_remain = "%.2f" % (ele_remain / _ele)
            elif typeit == 'air':
                degree_remain = float(divMeterTopBox.find('td', id='tdSYValue').text[:-1])
                ele_remain = "%.2f" % (degree_remain * _ele)

            ele_before = _tr_dict['2'].td.next_sibling.text.split('：')[1][:-2]
            ele_current = _tr_dict['3'].td.next_sibling.text.split('：')[1][:-2]

            degree_before = _tr_dict['2'].td.next_sibling.text.split('(')[0][:-3]
            degree_current = _tr_dict['3'].td.next_sibling.text.split('(')[0][:-3]

            return {
                'dor': dor,
                'degree': {
                     'remain': degree_remain,
                     'before': degree_before,
                     'current': degree_current,
                },
                'ele': {
                     '_ele': _ele,
                     'remain': ele_remain,
                     'before': ele_before,
                     'current': ele_current,
                }
            }

async def get_new_ele(meter, dor, typeit):
    """
    -> 新电费接口爬虫
    """
    # set cookie
    cookies = {'ammeterid': meter}
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True), \
        headers=headers, cookies=cookies) as session:
        async with session.get(new_ele_url, timeout=12) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

            all_p = soup.find_all("p")
            all_p.insert(0, "fccnu")
            _ele = float(all_p[5].strings.__next__()[:-2])

            degree_current = ""
            for ch in all_p[4].strings.__next__():
                try:
                    int(ch); degree_current += ch
                except ValueError:
                    if ch == '.': degree_current += '.'
            degree_before = ""
            for ch in all_p[3].strings.__next__():
                try:
                    int(ch); degree_before += ch
                except ValueError:
                    if ch == '.': degree_before += '.'

            ele_before = ""
            for ch in list(all_p[3].strings)[1]:
                try:
                    int(ch); ele_before += ch
                except ValueError:
                    if ch == '.': ele_before += '.'
            ele_current = ""
            for ch in list(all_p[4].strings)[1]:
                try:
                    int(ch); ele_current += ch
                except ValueError:
                    if ch == '.': ele_current += ch

            if typeit == 'light':
                ele_remain = float(all_p[7].strings.__next__()[:-2])
                degree_remain = "%.2f" % (ele_remain / _ele)
            elif typeit == 'air':
                degree_remain = float(all_p[7].strings.__next__()[:-4])
                ele_remain = "%.2f" % (degree_remain * _ele)

            return {
                'dor': dor,
                '_ele': _ele,
                'degree': {
                    'remain': degree_remain,
                    'before': degree_before,
                    'current': degree_current,
                },
                'ele': {
                    'remain': ele_remain,
                    'before': ele_before,
                    'current': ele_current
                }
            }   

async def get_ele(meter, dor, typeit):
    if meter == 0:
        return none_data % dor
    try:
        return await get_old_ele(meter, dor, typeit)
    except aiohttp.client_exceptions.ClientResponseError:
        try:
            return await get_new_ele(meter, dor, typeit)
        except asyncio.TimeoutError:
            return None
