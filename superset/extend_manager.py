import requests
from flask import session, abort, redirect, request
from flask_appbuilder.api import expose
from flask_babel import refresh, gettext, _
from flask_login import logout_user, login_user
from requests import Response

from superset import SupersetSecurityManager

from flask_appbuilder.security.views import AuthRemoteUserView
import logging

from superset.conf.commons import USER_LOGIN_OUT_RUL, LOGIN_SERVER_URL, \
    CHECK_SERVER_URL, USER_INFO_RUL

logger = logging.getLogger(__name__)


class ExtendAuthRemoteUserView(AuthRemoteUserView):
    # 需继承config.py中AUTH_TYPE值相对应的父类
    login_template = 'appbuilder/general/security/login_my.html'
    title = "superset login"

    default_view = "index"

    @expose("langs/<string:locale>")
    def index(self, locale):
        """
        切换语言
        @param locale:
        @return:
        """
        if locale not in self.appbuilder.bm.languages:
            abort(404, description="Locale not supported.")
        session["locale"] = locale
        refresh()
        self.update_redirect()
        return redirect("/dashboard/list")

    @expose("/logout/", methods=['GET', 'POST'])
    def logout(self):
        token = request.args.get('token')
        headers = {'Authorization': token}
        result = requests.get(url=USER_LOGIN_OUT_RUL, headers=headers)
        logger.info("user logout,", result)
        logout_user()
        home = gettext("Home")

        hostmsg = _("The hostname provided can't be resolved.")
        return redirect(LOGIN_SERVER_URL)

    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        token = request.headers.get("Authorization")
        lang = request.args.get('lang')  # 语言代码 zh-CN|en-US
        theme = request.args.get('theme')  # 主题 dark | light

        # 添加admin
        admin = request.headers.get("admin")
        if not token:
            token = request.args.get("Authorization")
        if not token:
            return redirect(LOGIN_SERVER_URL)
        else:
            logger.info('Auth Info: lang=%s theme=%s token=%s', lang, theme, token)
            manager = self.appbuilder.sm
            headers = {'Authorization': "Bearer %s" % token}
            result: Response = requests.get(url=CHECK_SERVER_URL, headers=headers)

            if result.status_code != 200 or not result.content or not result.json().get(
                "result", False):
                logger.info("token check failed,", result)
                return redirect(LOGIN_SERVER_URL)
            result = requests.get(url=USER_INFO_RUL, headers=headers)
            if result.status_code != 200:
                logger.info("get user failed,", result)
                return redirect(LOGIN_SERVER_URL)
            if not result.content:
                return redirect(LOGIN_SERVER_URL)
            user_info = result.json()["result"]
            logger.info("login user=%s", user_info)
            if not admin:
                user_name = user_info.get("username", None)
                user_id = user_info.get("id", None) + '@cc.com'
                if user_name is None:
                    user_name = user_info.get("name", "public")
                # 查找用户
                user = manager.find_user(email=user_id)
                if not user:
                    user = manager.find_user(username=user_name)
                    if not user:
                        # if admin_role in user_info["roles"]:
                        role_admin = self.appbuilder.sm.find_role('Admin')
                        user = manager.add_user(user_name, user_name, "",
                                                user_id, role_admin,
                                                password=user_name)
                        logger.info("add user", user)
                    else:
                        user.email = user_id
                        manager.update_user(user)
                if user.username != user_name:
                    user.username = user_name
                    manager.update_user(user)
                logger.info("login %s %s", login_user(user, remember=False),
                            user.username)
                if lang not in self.appbuilder.bm.languages:
                    abort(404, description="Locale not supported.")
                session["locale"] = lang
                refresh()
                self.update_redirect()
                return redirect("/dashboard/list")
            return self.admin_login(manager)

    def admin_login(self, manager):
        # 可以内置一个admin用户，用于管理
        username = "admin"
        user = manager.find_user(username=username)
        login_user(user, remember=False)
        return redirect(self.appbuilder.get_url_for_index)


class ExtendUserManager(SupersetSecurityManager):
    authremoteuserview = ExtendAuthRemoteUserView
