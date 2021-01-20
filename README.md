# host: http://106.14.212.56/api2/
## code
> 一般

    200 // 成功

    10001  // 当前选择的库不可为空

    10002  // 登录失败

    10003  // 限制登录

    10004  // 只能post

    10005  // 只能get

    10006  // 没有权限

    10007  // 错误参数

    10008  // 操作失败

> 微信相关

    20001  // code已被使用

    20002  // 授权出错


## 登陆（user）

> 登陆获取 assToken

1. path = login
1. 请求方式 post
1. 数据格式
```
 data = {
    "name":"xxx",
    "password":"xxxx"
 } 
 ```
> 返回
```
{
    "code": 200, 
    "msg": "登录成功",
    "data": {
        "userName": "xxxx",
        "assToken": "xxxx"
    }
}
```




## 查询（query）

> 查询当前可用的库

1. path = dbs
1. 请求方式 get

> 查询当前库的可用表
1. path = tables
1. 请求方式 get
1. 数据格式 params = {db: 'xxx'} / ?db=xxx

> 查询数据
1. path = data
1. 请求方式 post
1. 数据格式
```
data = {
    "db": "xxx",
    "table": "xxx",
    "page": 1,      // 需要传 不需要就不用传 与pageSize 要传都需要传
    "pageSize": 10,
    "remove": [], // 不需要返回的字段
    "order": {  // 需要传 不需要就不用传 
        "orderBy": "xxx",
        "isDesc": -1 / 1
    },
    "jsonMessage": {
        'name': 'cyc', // 并且的关系 
        'age': '/ddd/' // '/需要正则匹配的数据/'      
    },
    "jsonMessage": {
        查或者关系
        $or:[
            {age:{$gte:30}},
            {"name": '/ddd/'}
        ]
        查 并且关系
        $and:[
            {age:{$gte:30}},
            {"name": '/ddd/'}
        ]
        查 in关系
        age:{$in:[25,33]
   }
返回
{
    "code": 200, 
    "msg": "操作成功", 
    "data": {
        "list": [
            { "d": 1, "name": 12, "cc":123}
        ], 
        "count": 1, 
        "page": 1
    }
}
```

## 添加（add）
> 添加数据
1. path = data
1. 请求方式 post
1. 数据格式
```
data = {
    "db": "xxx",
    "table": "xxx",
    "jsonMessage": {
        'name': 'cyc', // 并且的关系 
        'age': 18       
    }
}
返回
{
    "code": 200, 
    "msg": "操作成功", 
    "data": {}
}
```

> 获取阿里oss签名

1. path = sign
1. 请求方式 post
1. 数据格式
```
data = {
   "dir": "xxx"
}
返回
{
    "code": 200, 
    "msg": "获取成功", 
    "data": {
        "accessid": "xxxxxx",
        "host": "xxxx", 
        "policy":"xxxxx",
        "signature": "xxxxx", 
        "expire": 1612345678, 
        "dir": "xxx"
    }
}
```
> 获取别的资源的文章
1. path = article
1. 请求方式 post
1. 数据格式
```
    data = {
        "db": "xxx", // 存到哪个库哪个表
        "table": "xxx",
        "save_db": true / false, // true 为储存数据到指定数据库
        "jsonMessage": {
            'resource': '哪里的数据', // 不指定的话 可以通过url 来确定 如果没找到会拿不到
            'url': '文章的链接'      // csdn/jianshu/juejin/cnblogs/zhihu 
        }
    }
    返回
    {
        "code": 200,
        "msg": "添加成功",
        "data": {
            "content": "html",
            "from": "csdn",
            "from_url": "https://lgdsunday.blog.csdn.net/article/details/110202405",
            "id": "article_0.23429897757484786_csdn_4400"
        }
    }
```

## 修改（update）
1. path = replace
1. 请求方式 post
1. 数据格式
```
data = {
    "db": "xxx",
    "table": "xxx",
    "query": { // 查询 哪条数据
        'name': 'cyc', // 并且的关系 
        'age': '/正则需要匹配的内容/'   
    },
    "jsonMessage": { // 修改哪些 有就修改 没有添加
        'name': 'cyc', // 并且的关系 
        'age': 18       
    }
}
返回
{
    "code": 200, 
    "msg": "修改成功", 
    "data": { // 修改哪些 有就修改 没有添加
        'name': 'cyc', // 并且的关系 
        'age': 18       
    }
}
```

## 删除（dalete）
> 删除单条数据
1. path = deleteone
1. 请求方式 post
1. 数据格式
```
data = {
    "db": "xxx",
    "table": "xxx",
    "isAll": true, // 默认是 true 删除全部匹配 false为删除匹配到的第一个 
    "jsonMessage": { 
        'name': 'cyc', // 并且的关系 
        'age': '/正则需要匹配的内容/'         
    }
}
返回
{
    "code": 200, 
    "msg": "删除成功", 
    "data": 1 // 删除的数量
}
```
> 删除表
1. path = drop
1. 请求方式 post
1. 数据格式
```
data = {
    "db": "xxx",
    "table": "xxx",
}
返回
{
    "code": 200, 
    "msg": "删除成功", 
    "data": 'xxx' // 表名
}
```

## 微信（wechat）
> appid
1. path = appid
1. 请求方式 get

> openid
1. path = openid
1. 请求方式 get
1. 数据格式 code = xxx

> 分享签名
1. path = getsign
1. 请求方式 post

