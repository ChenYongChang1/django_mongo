SUCCESS = 200
NOT_FOUND = 404  # 没有这个路由
REQUIRE_DB = 10001  # 当前选择的库不可为空
LOGIN_ERROR = 10002  # 登录失败
LOGIN_FORBIDDEN = 10003  # 限制登录

ONLY_POST = 10004  # 只能post
ONLY_GET = 10005  # 只能get

NOT_ALLOW = 10006  # 没有权限

BAD_PARAMS = 10007  # 错误参数

ACTION_LOSE = 10008  # 操作失败

HAVE_NO_RESOURCE = 10009  # 还没开发这个资源的选项

CAN_NOT_GET_RESOURCE = 10010  # 未爬取到资源

DONT_MATCH = 10011  # 资源和指定的来源不匹配

NOT_LOGIN = 10012  # 未登录

# 微信相关
OLD_CODE = 20001  # code已被使用

AUTH_ERROR = 20002  # 授权出错
