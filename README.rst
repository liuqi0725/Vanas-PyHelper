VanasPyHelper
======

**DISCLAIMER** 该项目是针对 Vanas 项目的一个 Python 帮助工具包。主要作用是为给 Vanas 的各个微服务中提供通用类的帮助。可能存在 BUG，我会不定期更新。如果将其用于您的生产项目，对您项目造成任何损失，我将不承担任何责任。


软件架构 :

- Python3.8

安装 :

$ pip install git+https://github.com/liuqi0725/Vanas-PyHelper


功能说明 :

- request: do_get,do_post 封装
- request: 获取代理,设置 header 的封装
- request: 下载文件封装
- response: success_json, failure_json 的封装
- response: render_json 返回 Flask Response 对象封装
- request,response 常见异常封装
- logging: logging 统一封装
- vana-token: 对 Vanas-Token-Manager 的获取、验证做了封装 https://github.com/liuqi0725/Vanas-Token-Manager
- vana-token: route 装饰器，可以指定本地验证规则，各微服务通过本地缓存快速验证，减少token-manager server 的交互
- file: 常用函数封装
- crypto: 对 AES,DES 进行了封装
- conf: 对读写 yaml、ini 文件进行封装
