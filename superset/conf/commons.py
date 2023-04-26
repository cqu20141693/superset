import os


def from_env(key: str, default):
    """
    获取系统环境变量
    @param key:
    @param default:
    @return:
    """
    if key in os.environ:
        # Explicitly import config module that is not necessarily in pythonpath; useful
        # for case where app is being executed via pex.
        return os.environ[key]
    else:
        return default


LOGIN_SERVER_URL = from_env('LOGIN_SERVER_URL',
                            'https://witeam.com/login')  # GUC登录接口
CHECK_SERVER_URL = from_env('CHECK_SERVER_URL',
                            'https://witeam.com/api/guc/token/verify/real-time')

USER_INFO_RUL = from_env('USER_INFO_RUL',
                         "https://witema.com/api/guc/current/user-info")

USER_LOGIN_OUT_RUL = from_env('USER_LOGIN_OUT_RUL',
                              "https://witeam.com/api/guc/protocol/oauth2/logout-code")
