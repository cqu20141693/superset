from flask_appbuilder.security.manager import AUTH_REMOTE_USER

# using customize custom security manager
from superset.extend_manager import ExtendUserManager

CUSTOM_SECURITY_MANAGER = ExtendUserManager

# AUTHENTICATION CONFIG
# 使用remote server的方式进行认证
AUTH_TYPE = AUTH_REMOTE_USER

# setup Public role name, no authentication needed
AUTH_ROLE_PUBLIC = 'Gamma'

# Will allow user self registration
AUTH_USER_REGISTRATION = True
GLOBAL_ASYNC_QUERIES = False

ENABLE_CORS = False
BABEL_DEFAULT_LOCALE = 'zh'
