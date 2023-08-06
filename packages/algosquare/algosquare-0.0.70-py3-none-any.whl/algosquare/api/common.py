import io
import requests

from .api import api_put

def upload_dataframe(namespace, df):
    with io.BytesIO() as f:
        df.to_csv(f, index=False)
        response = api_put('api/scratchpad', json=dict(filename = f'{namespace}.csv'))
        requests.put(response['url'], data=f.getvalue())
        return response['key']