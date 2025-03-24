# -*- coding: utf-8 -*-
import struct
import time

from burp import IBurpExtender, IHttpListener
import socket
from urlparse import urlparse, parse_qs  # Jython 2.7 的 URL 解析模块
from java.util.concurrent import Executors

class BurpExtender(IBurpExtender, IHttpListener):

    exclude_url = ['bing.com', "googleapis.com", "google.com", 'baidu.com', 'microsoft.com', 'msn.com', 'nelreports.net', 'azure.com', 'bdstatic.com']
    exclude_suffix = ['js', 'css', 'jpeg', 'gif', 'jpg', 'png', 'pdf', 'rar', 'zip', 'docx', 'doc', 'svg', 'jpeg', 'ico', 'woff', 'woff2', 'ttf', 'otf']

    def __init__(self):
        self.s = None

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        callbacks.setExtensionName("HTTP Request Mirror")
        callbacks.registerHttpListener(self)
        self.executor = Executors.newFixedThreadPool(10)  # 3 个线程的池
        return

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if messageIsRequest:
            javaBytes = messageInfo.getRequest()  # 获取 Java byte 数组
            # 获取请求数据（byte数组）
            requestBytes = bytearray(javaBytes)
            # 打印出请求的url
            helper = self._callbacks.getHelpers()
            analyzedRequest = helper.analyzeRequest(messageInfo)
            url = analyzedRequest.getUrl().toString()
            # self._callbacks.printOutput((url))
            # self._callbacks.printOutput(str(type(url)))
            # self._callbacks.printOutput((u"请求Request URL: " + url))
            # self._callbacks.printOutput((u"Request URL: " + url))

            p_url = url.encode('utf-8')
            # 使用 urlparse 解析 URL
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            path = parsed_url.path
            # 目标url、资源不进行转发
            for ex_url in BurpExtender.exclude_url:
                if ex_url in hostname:
                    # self._callbacks.printOutput("ex_url:" + ex_url)
                    return
            for ex_suffix in BurpExtender.exclude_suffix:
                if ex_suffix in path:
                    # self._callbacks.printOutput("ex_suffix:"+ex_suffix)
                    return
            # 将请求数据发送到本地 Python 服务
            # self.sendToPythonListener(requestBytes)
            self.executor.submit(lambda: self.sendToPythonListener(requestBytes))  # 提交任务

    def get_socks(self):
        host = "127.0.0.1"
        port = 16166  # 修改为你本地 Python 服务监听的端口
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s

    def sendToPythonListener(self, data):
        try:
            s = self.get_socks()
        except Exception as e:
            self._callbacks.printError(("get socks fail: " + str(e)))
            return
        try:
            # self._callbacks.printOutput("data len:" + str(len(data)))
            # 发送数据长度
            s.sendall(struct.pack('!I', len(data)))
            # 发送数据
            s.sendall(data)
        except Exception as e:
            self._callbacks.printError(("send data fail: " + str(e)))
            return
        # 接受客户端返回，然后关闭连接
        s.recv(2)
        s.close()

