# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : spiderutils.py
# @Created  : 2020/11/2 6:54 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : request 相关工具包
# -------------------------------------------------------------------------------

import random,enum,json
import requests
from werkzeug.exceptions import HTTPException
from flask import abort,jsonify
from vanaspyhelper.error.RequestError import ProxyTypeNotSupport, RequestResolverError, SendRequestError, \
    ConnectionRefused

__user_agent_remote_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

__user_agent_mobile_list = [
    'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
    "Mozilla/5.0 (Linux; Android 10; ELE-AL00 Build/HUAWEIELE-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1178 MMWEBSDK/200201 Mobile Safari/537.36 MMWEBID/616 MicroMessenger/7.0.12.1620(0x27000C36) Process/tools NetType/4G Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9sk Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045132 Mobile Safari/537.36 MMWEBID/3165 MicroMessenger/7.0.12.1620(0x27000C38) Process/tools NetType/4G Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 10; JSN-AL00a Build/HONORJSN-AL00a; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10)",
    "Mozilla/5.0 (Linux; Android 9; PCDM10 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9)",
    "Mozilla/5.0 (Linux; Android 9; V1816A Build/PKQ1.180819.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9)",
    "Mozilla/5.0 (Linux; U; Android 9; zh-TW; ANE-LX2J Build/HUAWEIANE-LX2J) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.5.1146 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; INE-AL00 Build/HUAWEIINE-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9)",
    "Mozilla/5.0 (Linux; U; Android 10; zh-cn; Redmi K30 Build/QKQ1.190825.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.8.14",
    "Mozilla/5.0 (Linux; Android 10; LIO-AN00 Build/HUAWEILIO-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10) NABar/1.0",
    "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; MI 8 Lite Build/OPM1.171019.019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.10.24",
    "Mozilla/5.0 (Linux; Android 8.0.0; BLN-TL10 Build/HONORBLN-TL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 8.0.0)",
    "Mozilla/5.0 (Linux;Android 10) Chrome/80.0.3987.132 BiliApp/5560400 SearchCraft/3.6.4 (Baidu; P1 10) UCBrowser/12.9.2.1072",
    "Mozilla/5.0 (Linux; Android 7.1.2; vivo X9L Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 7.1.2)",
    "Mozilla/5.0 (Linux; Android 10; LYA-TL00 Build/HUAWEILYA-TL00L; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.3.10 (Baidu; P1 10)",
    "Mozilla/5.0 (Linux; Android 9; BND-TL10 Build/HONORBND-TL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9)",
    "Mozilla/5.0 (Linux; Android 10; Redmi K20 Pro Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10)",
    "Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045131 Mobile Safari/537.36 MMWEBID/5964 MicroMessenger/7.0.12.1620(0x27000C37) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; U; Android 9; zh-cn; PBEM00 Build/PKQ1.190519.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.2 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 10; zh-cn; Redmi K20 Pro Build/QKQ1.190825.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.2 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; vivo X20A Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.2 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; PBET00 Build/PKQ1.190519.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9) NABar/1.0",
    "Mozilla/5.0 (Linux; U; Android 9; zh-cn; MI 6 Build/PKQ1.190118.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.10.14",
    "Mozilla/5.0 (Linux; Android 10; LYA-AL00 Build/HUAWEILYA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.2.2 (Baidu; P1 10) NABar/1.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.12(0x17000c25) NetType/4G Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 10; LIO-AL00 Build/HUAWEILIO-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10)",
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-C7000 Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 8.0.0)",
    "Mozilla/5.0 (Linux; Android 10; SM-G9750 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10)",
    "Mozilla/5.0 (Linux; Android 9; V1901A Build/P00610; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9)",
    "Mozilla/5.0 (Linux; Android 10; MI 9 Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10)",
    "Mozilla/5.0 (Linux; U; Android 9; zh-cn; Redmi Note 8 Build/PKQ1.190616.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.2 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045131 Mobile Safari/537.36 MMWEBID/1885 MicroMessenger/7.0.10.1580(0x27000AFF) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 9; GLK-AL00 Build/HUAWEIGLK-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9)",
    "Mozilla/5.0 (Linux; U; Android 10; zh-CN; VOG-AL00 Build/HUAWEIVOG-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.2.1072 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; PAFM00 Build/PKQ1.190319.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9)",
    "Mozilla/5.0 (Linux; U; Android 9; zh-cn; Mi Note 3 Build/PKQ1.181007.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.10.24",
    "Mozilla/5.0 (Linux; Android 8.0.0; FRD-AL10 Build/HUAWEIFRD-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 8.0.0) NABar/1.0",
    "Mozilla/5.0 (Linux; Android 10; LYA-AL00 Build/HUAWEILYA-AL00L; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.12(0x17000c25) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 6.0; HUAWEI MT7-TL00 Build/HuaweiMT7-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 6.0)",
    "Mozilla/5.0 (Linux; Android 10; MI 8 SE Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.3.10 (Baidu; P1 10)",
    "Mozilla/5.0 (Linux; Android 10; SM-G9750 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10) NABar/1.0",
    "Mozilla/5.0 (Linux; Android 10; MI 8 SE Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10)",
    "Mozilla/5.0 (Linux; Android 7.1.1; MI MAX 2 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045132 Mobile Safari/537.36 V1_AND_SQ_8.3.0_1362_YYB_D QQ/8.3.0.4480 NetType/WIFI WebP/0.3.0 Pixel/1080 StatusBarHeight/67",
    "Mozilla/5.0 (Linux; Android 5.1.1; MIX Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36 MMWEBID/4159 MicroMessenger/7.0.6.1460(0x27000634) Process/tools NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 5.1.1; MIX Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36 MMWEBID/8727 MicroMessenger/7.0.6.1460(0x27000634) Process/tools NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 8.0.0; BAH2-W09 Build/HUAWEIBAH2-W09; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 8.0.0)",
    "Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11s Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 7.1.1)",
    "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; VOG-TL00 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.0.6",
    "Mozilla/5.0 (Linux; Android 9; VTR-AL00 Build/HUAWEIVTR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.3.10 (Baidu; P1 9)",
    "Mozilla/5.0 (Linux; Android 10; LYA-AL00 Build/HUAWEILYA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045132 Mobile Safari/537.36 MMWEBID/8931 MicroMessenger/7.0.12.1620(0x27000C36) Process/tools NetType/4G Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 10; MI CC 9 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.11(0x17000b21) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 7.1.1; ONEPLUS A3000 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36 MicroMessenger/7.1.0.1580(0x27000A32) Process/tools NetType/4G Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 9; vivo X21A Build/PKQ1.180819.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9)",
    "Mozilla/5.0 (Linux; U; Android 10; zh-cn; HLK-AL10 Build/HONORHLK-AL1001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.1 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Lenovo L38041 Build/PKQ1.190127.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1176 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/7747 MicroMessenger/7.0.10.1580(0x27000AFE) Process/toolsmp NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Linux; Android 9; ARS-AL00 Build/HUAWEIARS-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9)",
    "Mozilla/5.0 (Linux; U; Android 9; zh-CN; COR-AL10 Build/HUAWEICOR-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.1.1071 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 9; zh-cn; MI 6X Build/PKQ1.180904.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.8.14",
    "Mozilla/5.0 (Linux; Android 10; TNY-AL00 Build/HUAWEITNY-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10)",
    "Mozilla/5.0 (Linux; Android 9; YAL-AL50 Build/HUAWEIYAL-AL50; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9)",
    "Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 5.1.1) NABar/1.0",
    "Mozilla/5.0 (Linux; U; Android 9; zh-CN; MI 6 Build/PKQ1.190118.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/3.5.1.118 Mobile Safari/537.36/18.18362 SearchCraft/2.8.2 Baidu;P1 10.0 57.0.2987.108 UCBrowser/12.1.4.994 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G9860 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10) NABar/1.0",
    "Mozilla/5.0 (Linux; U; Android 9; zh-cn; Redmi Note 7 Pro Build/PKQ1.181203.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.2 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; HRY-AL00 Build/HONORHRY-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/11.7 baiduboxapp/11.13.8.10 (Baidu; P1 10)",
    "Mozilla/5.0 (Linux; Android 9; MIX 2 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9) NABar/1.0",
]

def get_user_agent_remote(user_agent:list=None):
    """
    获取 [终端] User-Agent 随机获取一个
    :param user_agent: 自定义 user_agent list  默认 None ，从系统内置的 user_agent 中随机选择一个
    :return:
    """

    if user_agent is not None:
        return random.choice(user_agent)

    return random.choice(__user_agent_remote_list)

def get_user_agent_mobile(user_agent:list=None):
    """
    获取 [手机] User-Agent 随机获取一个
    :param user_agent: 自定义 user_agent list  默认 None ，从系统内置的 user_agent 中随机选择一个
    :return:
    """

    if user_agent is not None:
        return random.choice(user_agent)
    return random.choice(__user_agent_mobile_list)

def build_proxies(ip:str="127.0.0.1", port:int=1080 , type:str="http"):
    """
    创建代理配置
    :param ip: 代理 ip 默认 127.0.0.1
    :param port:  代理端口， 默认 1080
    :param type:  代理类型， 默认 http,  备选项 socks5 。  https 启用代理均会添加
    :return:
    """
    proxies = {}

    if type.lower() == 'socks5':
        proxies['http'] = 'socks5://{}:{}'.format(ip,port)
        proxies['https'] = 'socks5://{}:{}'.format(ip,port)
    elif type.lower() == 'http':
        proxies['http'] = 'http://{}:{}'.format(ip,port)
        proxies['https'] = 'https://{}:{}'.format(ip,port)
    else:
        raise ProxyTypeNotSupport(type)

    return proxies


def do_get(url:str, headers:dict , proxies:dict=None, stream:bool=False, timeout:int=60):
    """
    发送 GET 请求
    :param url: 请求 url
    :param headers:  请求头
    :param proxies: 代理配置 默认 None ，可用 build_proxies() 创建代理配置
    :param stream: 是否采用流方式读取 默认 False
    :param timeout: 超时时间 单位：秒 默认 60
    :return:
    """

    try:
        # s = requests.session()
        # s.headers = headers
        # s.keep_alive = False
        if proxies is not None:
            # s.proxies = proxies
            response = requests.get(url, headers=headers, proxies=proxies, stream=stream,timeout=timeout)
        else:
            response = requests.get(url, headers=headers, stream=stream, timeout=timeout)

        # status != 200 抛出异常
        response.raise_for_status()

        return response
    except requests.exceptions.ConnectionError:
        raise ConnectionRefused()
    except Exception:
        raise RequestResolverError(url=url)

def do_post(url:str, headers:dict , proxies:dict=None, stream:bool=False, timeout:int=60):
    """
    发送 POST 请求
    :param url: 请求 url
    :param headers:  请求头
    :param proxies: 代理配置 默认 None ，可用 build_proxies() 创建代理配置
    :param stream: 是否采用流方式读取 默认 False
    :param timeout: 超时时间 单位：秒 默认 60
    :return:
    """

    try:
        if proxies is not None:
            response = requests.post(url, headers=headers, proxies=proxies, stream=stream,timeout=timeout)
        else:
            response = requests.post(url, headers=headers, stream=stream, timeout=timeout)

        # status != 200 抛出异常
        response.raise_for_status()

        return response

    except requests.exceptions.ConnectionError:
        raise ConnectionRefused()
    except Exception:
        raise RequestResolverError(url=url)

def request_json(url, data:dict=None, client_id:str=None, access_token:str=None, method:str="POST"):
    """
    发送 json 请求
    :param url:
    :param data:
    :param client_id: 每个客户端独有
    :param access_token: 访问 token 从 Vanas-token-manager 获取
    :return:
    """
    headers = {
        "Content-Type": "application/json",
        "access_token": access_token,
        "client_id": client_id,
    }

    try:
        response = None
        if method == "POST":
            if data is not None:
                data = json.dumps(data)
            response = requests.post(url, headers=headers, data=data)
        elif method == "GET":
            response = requests.get(url, headers=headers)

        response.raise_for_status()
        if response is not None:
            return response.json()
    except Exception as e:
        raise SendRequestError(url,e)

def request_form(url, data:dict , client_id:str=None, access_token:str=None):
    """
    发送 form 表单请求
    :param url:
    :param data:
    :return: json
    """
    try:
        headers = {
            "access_token": access_token,
            "client_id": client_id,
        }

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        if response is not None:
            return response.json()
    except Exception as e:
        raise SendRequestError(url , e)


def E400(desc, code=400):
    """
    未知错误处理，并抛出到 error_handling 中
    :param desc: 错误信息
    :param code: 错误编码 默认 400
    :return:
    """
    exc = HTTPException()
    if isinstance(code,enum.Enum):
        exc.status_code = code.value
    else:
        exc.status_code = code
    exc.description = desc
    return error_handling(exc)

def error_handling(error):
    """
    统一错误处理
    :param error:
    :return: response
    """
    if isinstance(error, HTTPException):
        # 4xx ,5xx 错误
        result = json_res_failure(error.description , error.status_code , str(error))
    else:
        # 500 错误
        description = abort(500).mapping.description
        result = json_res_failure(description , 500 ,trace=str(error))

    # resp = jsonify(result)
    # resp.status_code = result['code']
    return render_json(result)

def render_json(jsonData):
    """
    提供给外部调用，返回 response
    :param jsonData: json 数据
    :return:
    """
    resp = jsonify(jsonData)
    if 'status_code' in jsonData:
        resp.status_code = jsonData['status_code']
    else:
        resp.status_code = 200
    return resp

def json_res_failure(desc:str,code,trace:str=""):
    """
    错误 json
    :param desc:
    :param code:
    :param trace:
    :return:
    """
    if isinstance(code,enum.Enum):
        code = code.value
    return __json_res(False,desc=desc,error_code=code , trace=trace)

def json_res_success(data:dict=None):
    """
    成功 json
    :param data:
    :return:
    """
    return __json_res(True,data=data)


def __json_res(success:bool,data:dict={},desc:str="",error_code:int=400, trace:str=""):
    """
    创建 api 通用 json 返回值
    :param desc: 说明 默认 None
    :param data: 返回数据 默认 None
    :param success: 成功与否
    :param error_code: 错误编码 默认 400
    :param trace: 错误信息 默认 None
    :return:
    """

    int_success = int(success)

    if success :
        result = {'success': int_success, 'data':data, 'description': desc}
    else:
        result = {'success': int_success, 'code': error_code, 'description': desc , 'trace': trace}

    return result


def vanas_get_token(client_id:str, client_secret_key:str,
                    url:str="https://token.35liuqi.com/oauth/token",
                    grant_type:str="client_credentials")->dict:
    """
    vanas 获取 token
    :param client_id: 客户端 id，固定值，由研发人员签发
    :param client_secret: 客户端 secret，由研发人员签发
    :param url:
    :param grant_type: client_credentials 或 password 推荐 client_credentials
    :return: 根据服务端 doc 返回
    """
    import time
    from vanaspyhelper.util.common import md5

    timestamp = int(time.time())
    signature = md5(client_secret_key + str(timestamp)).lower()
    data = {'grant_type': grant_type, 'client_id': client_id, 'signature': signature, "timestamp": timestamp}
    return request_json(url, data)

def vanas_verify_token(access_token:str ,
                       client_id:str ,
                       url="https://token.35liuqi.com/verify_token")->dict:
    """
    vanas 验证 token
    :param access_token: token
    :param client_id: 客户端 id，固定值，由研发人员签发
    :param url:
    :return: 根据服务端 doc 返回
    """
    data = {'access_token': access_token, 'client_id': client_id}
    return request_json(url,data,client_id,access_token)