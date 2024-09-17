from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, dict):
            # Convert dict with list to string
            for key in response.data:
                if type(response.data.get(key)).__name__ == "list" or type(response.data.get(key)).__name__ == "tuple":
                    response.data[key] = response.data[key][0]
            # change 'detail' to 'msg'
            if response.data.get('detail'):
                response.data['msg'] = response.data.get('detail')
                del response.data['detail']
            response.data['success'] = False
        elif isinstance(response.data, list):
            error = response.data[0]
            if isinstance(error, ErrorDetail):
                response.data = dict({
                    'msg': str(error)
                })

    return response
