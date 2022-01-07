import requests
import pandas as pd

def get_data():
    headers = {
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryDL6BnKhhwEMlMs6p',
    }
    data = '------WebKitFormBoundaryDL6BnKhhwEMlMs6p\nContent-Disposition: form-data; name="query"\n\nquery stores($filter: StoreFilterInputType, $pagingInfo: InputBatch!) {\n  stores(filter: $filter, pagingInfo: $pagingInfo) {\n    limit\n    offset\n    count\n    items {\n      id\n      filial_id\n      title\n      premium\n      slug\n      filialType\n      city {\n        ...CityBaseFragment\n        __typename\n      }\n      workingHours {\n        start\n        end\n        __typename\n      }\n      location {\n        ...LocationBaseFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CityBaseFragment on City {\n  id\n  title\n  __typename\n}\n\nfragment LocationBaseFragment on Location {\n  lat\n  lng\n  __typename\n}\n\n------WebKitFormBoundaryDL6BnKhhwEMlMs6p\nContent-Disposition: form-data; name="variables"\n\n{"filter":{"filialId":null,"cityId":null,"start":null,"end":null,"hasCertificate":null,"servicesIds":null},"pagingInfo":{"limit":0,"offset":0},"ids":["OPENED"]}\n------WebKitFormBoundaryDL6BnKhhwEMlMs6p\nContent-Disposition: form-data; name="debugName"\n\n""\n------WebKitFormBoundaryDL6BnKhhwEMlMs6p\nContent-Disposition: form-data; name="operationName"\n\n"stores"\n------WebKitFormBoundaryDL6BnKhhwEMlMs6p--\n'
    response = requests.post("https://silpo.ua/graphql", headers=headers, data=data).json()
    data = response.get('data', {}).get('stores').get('items')
    good_data = []
    for store in data:
        item = {}
        item['_id'] = store.get('filial_id')
        item['address'] = store.get('title')
        item['premium'] = store.get('premium')
        item['type'] = store.get('filialType')
        item['city'] = store.get('city', {}).get('title')
        item['work_time'] = store.get('workingHours', {}).get('start') + '-' + store.get('workingHours', {}).get('end')
        item['x'] = float(store.get('location', {}).get('lng'))
        item['y'] = float(store.get('location', {}).get('lat'))
        good_data.append(item)

    return good_data

def pd_data():
    good_data=get_data()
    df = pd.DataFrame(good_data)
    df['brand_name'] ='Сільпо'
    df['holding_name']='Fozzy Group'
    return df

