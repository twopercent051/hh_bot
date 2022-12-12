import aiohttp
import json


async def tag_corrector(string):
    result = string.replace('<strong>', '<b>').replace('</strong>', '</b>')
    result = result.replace('<p>', '\n').replace('</p>', '\n')
    result = result.replace('<ul>', '').replace('</ul>', '')
    result = result.replace('<li>', '—').replace('</li>', '\n')
    result = result.replace('<br>', '\n').replace('<br />', '')
    result = result.replace('<div>', '').replace('</div>', '')
    return result


async def tag_corrector_test(string):
    result = string.replace('<strong>', '').replace('</strong>', '')
    result = result.replace('<p>', '').replace('</p>', '')
    result = result.replace('<ul>', '').replace('</ul>', '')
    result = result.replace('<li>', '—').replace('</li>', '\n')
    result = result.replace('<br>', '').replace('<br />', '')
    result = result.replace('<div>', '').replace('</div>', '')
    result = result.replace('Обязанности:', '\n<b>Обязанности:</b>\n')
    result = result.replace('Требования:', '\n<b>Требования:</b>\n')
    result = result.replace('Условия:', '\n<b>Условия:</b>\n')
    return result



async def get_vacansy_by_id(id):
    result = dict()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.hh.ru/vacancies/{id}') as resp:
            responce = await resp.read()
        data = json.loads(responce)
        currency_symbols = {'RUR': '₽'}
        result['vac_id'] = id
        result['title'] = data['name']
        if data['salary'] is None:
            result['salary'] = 'Не указана'
        elif data['salary']['to'] is None:
            result['salary'] = f"{data['salary']['from']} {currency_symbols[data['salary']['currency']]}"
        elif data['salary']['from'] == 0:
            result['salary'] = f"До {data['salary']['to']} {currency_symbols[data['salary']['currency']]}"
        else:
            result['salary'] = f"От {data['salary']['from']} до {data['salary']['to']} {currency_symbols[data['salary']['currency']]}"
        result['company'] = data['employer']['name']
        result['city'] = data['area']['name']
        result['experience'] = data['experience']['name']
        result['schedule'] = data['schedule']['name']
        result['employment'] = data['employment']['name']
        desc = data['description']
        result['description'] = await tag_corrector_test(desc)
    return result




async def main_request(field):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.hh.ru/vacancies?text={field}') as resp:
            responce = await resp.read()
        data = json.loads(responce)
        top_3_vac = data['items'][:3]
        result_list = []
        for vac in top_3_vac:
            id = vac['id']
            result = await get_vacansy_by_id(id)
            result_list.append(result)
        return result_list




