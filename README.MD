# Burp流量镜像工具

## 说明
~~~
这个工具主要用于将burp代理的http流量镜像一份到本地，以便用于其它安全测试

BurpPlugin.py       // 文件为burp插件（需要配合当前目录下的jypython使用）
jython-2.7.3.jar    // 用于配置burp的jython环境
LocalClient.py      // 文件用于本地安全分析

后续该项目将扩展为灵活的越权测试工具
~~~

~~~
BurpPlugin.py插件将完整的**HTTP请求**转发至LocalClient.py文件中监听的端口

交互的端口默认设置为：16166

后续将更加完善该工具，目前代解决的问题有：
    1、socket复用问题
    2、LocalClient.py文件中还没有解析HTTP请求和提供后续端口
    3、在完善该项目的基础后，扩展为越权测试工具
~~~