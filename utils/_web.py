import traceback

import numpy as np
from decorator import decorator
from fastapi.responses import JSONResponse


def json_compatible(data):  # sourcery skip: assign-if-exp, reintroduce-else
    if isinstance(data, dict):
        return {k: json_compatible(v) for k, v in data.items()}
    if isinstance(data, bytes):
        return str(data)
    if isinstance(data, np.ndarray):
        return data.tolist()
    return data


def web_try(exception_ret=None):
    @decorator
    def f(func, *args, **kwargs):
        error_code = 200
        ret = None
        msg = ''
        try:
            session = None
            for arg in args:
                ret = func(*args, **kwargs)
        except Exception as e:
            msg = traceback.format_exc()
            if len(e.args) > 0 and isinstance(e.args[0], int):
                error_code = e.args[0]
            else:
                error_code = 400
            print('--------------------------------')
            print('Get Exception in web try :( \n{}\n'.format(msg))
            print('--------------------------------')
            if callable(exception_ret):
                ret = exception_ret()
            else:
                ret = exception_ret
        finally:
            if ret is not None and isinstance(ret, JSONResponse):
                return ret
            return json_compatible({"code": error_code,
                                    "data": ret,
                                    "msg": msg.split('\n')[-2] if msg != '' else msg})

    return f
