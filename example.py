from LocalServer import ProxyServer


def handle_func(raw_request):
    print(raw_request)


if __name__ == '__main__':

    myPS = ProxyServer()

    # 设置处理函数
    myPS.set_handle_func(handle_func)

    # 启动服务
    # myPS.start_server("127.0.0.1", 7894)
    myPS.start_server()

