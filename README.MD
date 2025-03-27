# Burp流量镜像工具

## 使用方法
### 1、环境配置
~~~
1、将 "jython-2.7.3.jar" 文件配置到Burp的python环境中
2、将 "BurpPlugin.py" 文件作为扩展添加到Burp中
~~~

### 2、运行
~~~
python example.py

注意：先启动本地 example.py，再重新打开Burp中的插件
~~~

## 文件说明
~~~
这个工具主要用于将burp代理的http流量镜像一份到本地，以便用于其它安全测试

BurpPlugin.py       // 文件为burp插件（需要配合当前目录下的jypython使用）
jython-2.7.3.jar    // 用于配置burp的jython环境
LocalServer.py      // 文件接收burp传递的HTTP流量，并可以接收处理函数
~~~

## 配置说明
~~~
burp与本地服务使用的默认端口为：16166

如果需要更改端口:
1、自行修改 BurpPlugin.py 中的端口，然后添加到burp的插件中
2、在 myPS.start_server() 中指定ip与端口（见example.py）
~~~

## Q&S
~~~
1、在服务端做了一定的域名过滤，因此可能有些流量没有传到本地
~~~