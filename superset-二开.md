## superset 二开
[superset-2.1.0](https://github.com/apache/superset/tree/2.1.0)
[superset官网](https://superset.apache.org/)

### superset app

### superset frontend
#### 前端编译打包
```
cd superset
npm ci /yarn -i

npm run build /yarn build :执行打包命令后，会将静态文件都到包到sueprset/static目录下

```
#### 前端自定义图表插件
```
superset 目前已经存在的plugins在superset-frontend/plugins目录下
```
### 开发
``` 
superset 启动流程：
1. app.py create_app()方法会创建FlaskApp应用
2. 通过app.config.from_object(config_module) 导入superset.config文件
3. SupersetAppInitializer.init_app(): 日志初始化，数据库连接初始化 

```


#### 运行环境
##### 获取源码
1. git clone -b 2.1.0 git@github.com:apache/superset.git
##### 打包前端静态资源
1[打包编译前端](####前端编译打包)
##### [安装python环境](https://preset.io/blog/tutorial-contributing-code-to-apache-superset/)
通过创建一个 __main__ 方法创建SupersetApp启动调试
1. 配置虚环境
```
进入superset项目根目录
mkdir venv
# Create a Python virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate
```
2. 安装依赖包
```
superset的依赖包都在requirements目录下


```
#### 用户登陆二开
```markdown
Superset登录模块其实是使用了F.A.B(Flask-AppBuilder的简称)的登录认证框架. 有以下的登录认证方式:

｜AUTH_TYPE｜ value｜	description｜
｜--｜--｜--｜
|0 | AUTH_OID |	Open ID的方式验证, 比如通过gmail, Twitter, FB第三方APP都属于这个范畴|
|1 | AUTH_DB	| 通过用户名密码的方式登录, 登录信息存到数据库|
|2 | AUTH_LDAP |	通过LDAP协议进行登录授权, 感兴趣可以搜一下LDAP协议|
|3 | AUTH_REMOTE_USER |	从web server中获得验证, 该server可以是公司内统一使用的登陆系统|
|4 | AUTH_OAUTH |	superset不支持该配置方法|

superset 的配置信息都在superset/config.py文件中，同时提供了通过配置SUPERSET_CONFIG_PATH
的环境变量，配置自定义的superset配置文件例如：
export SUPERSET_CONFIG_PATH=~/superset/conf/superset_config.py

通过配置AUTH_TYPE = AUTH_REMOTE_USER 对接统一登陆系统
。。。。
```
superset提供了
#### 国际化支持中文二开
1. 国际化资源在superset/translations目录下
``` 
其中的文件夹为各种语言支持，其中以en/zh说明，国际化文件在LC_MESSAGES目录下：
messages.json为前端国际化文件， 
messages.po为后端国际化文件，msgid和msgstr成对出现，多语言需要一致，
后端通过from flask_babel import gettext as __，__(msgid) 获取数据时会自动国际化处理
```
2. 新增资源
#### 权限二开
``` 
内置角色：
Admin拥有所有可能的权限，包括授予或取消其他用户的权限，以及更改其他用户的切片和仪表板。
Alpha用户可以访问所有数据源，但不能授予或撤消其他用户的访问权限。它们也仅限于改变它们拥有的对象。Alpha用户可以添加和更改数据源。
Gamma用户的访问权限有限。它们只能使用来自数据源的数据，这些数据源是通过另一个补充角色授予它们访问权限的。他们只能查看由他们有权访问的数据源生成的切片和仪表板。目前Gamma用户无法更改或添加数据源。我们假设他们大部分是内容消费者，尽管他们可以创建片段和仪表板。
还要注意，当Gamma用户查看仪表板和切片列表视图时，他们将只看到他们有权访问的对象。
sql_lab角色授予对sql lab的访问权限。请注意，虽然默认情况下管理员用户可以访问所有数据库，但Alpha和Gamma用户都需要根据每个数据库授予访问权限。
Public允许已注销的用户访问某些Superset功能是可能的。
通过在superset_config.py中设置PUBLIC_ROLE_LIKE_GAMMA=True，可以向PUBLIC ROLE授予与GAMMA角色相同的权限集。如果要使匿名用户能够查看仪表板，这非常有用。仍然需要对特定数据集进行显式授予，这意味着您需要编辑公共角色并手动将公共数据源添加到该角色。
管理每个数据源访问的Gamma

下面是如何让用户只访问特定的数据集。首先确保访问受限的用户[仅]拥有分配给他们的Gamma角色。其次，创建一个新角色（菜单->安全->角色列表），然后单击+号。

这个新窗口允许您给这个新角色起一个名称，将其属性设置为用户，并在“权限”下拉列表中选择表。要选择要与此角色关联的数据源，只需单击下拉列表并使用typeahead搜索表名。
然后，您可以向Gamma用户确认，他们看到与他们的角色相关的表相关联的对象（仪表板和切片）。
自定义
FAB公开的权限是非常细粒度的，允许很大程度的定制。FAB为创建的每个模型（可以添加、可以删除、可以显示、可以编辑…）以及每个视图自动创建许多权限。除此之外，Superset还可以公开更细粒度的权限，如所有数据源访问权限。
我们不建议更改3个基本角色，因为有一组假设是建立在Superset之上的。虽然你可以创建你自己的角色，并把它们与现有的角色结合起来。
权限
角色由一组权限组成，Superset有许多类别的权限。以下是不同类别的权限：
模型和操作：模型是像Dashboard（仪表板）、Slice（切片）或User（用户）这样的实体。每个模型都有一组固定的权限，如可以can_edit(编辑)、can_show(可以显示)、can_delete(可以删除)、can_list(可以列表)、can_add(可以添加)等等。通过将Dashboard仪表板上的“can_delete可以删除”添加到角色，并将该角色授予用户，此用户将能够删除仪表板。
视图：视图是单独的web页面，如explore视图或SQL Lab视图。授予用户后，他/她将在菜单项中看到该视图，并能够加载该页面。
数据源：为每个数据源创建一个权限。如果用户没有授予“所有数据源”访问权限，则用户将只能查看切片或浏览授予它们的数据源
数据库：授予对数据库的访问权限允许用户访问该数据库中的所有数据源，并允许用户在SQL Lab中查询该数据库，前提是已授予用户特定于SQL Lab的权限
限制对数据源子集的访问
最好的方法可能是给用户Gamma加上一个或多个其他角色，这些角色将增加对特定数据源的访问。我们建议您为每个访问配置文件创建单独的角色。假设您的财务部门的人员可以访问一组数据库和数据源，并且这些权限可以合并到单个角色中。具有此配置文件的用户需要将Gamma 作为对它们可以访问的模型和视图的基础，而Finance角色是对数据对象的权限集合。
一个用户可以有多个角色，因此可以授予财务主管Gamma、Finance，或许还可以授予另一个Executive 角色，该角色收集一组数据源，这些数据源为仪表板供数据，只提供给Executive。当查看其仪表板列表时，此用户将仅看到其有权访问的仪表板列表（基于所赋予的角色和权限）。

最后，superset 设置publict可以匿名访问图表
```
#### 图表插件二开

### 打包
#### 本地打python执行包
#### docker打包
### 部署
#### 虚拟机部署
1. 配置python环境，安装好依赖包
2. 将源码包打包到服务器，启动执行
