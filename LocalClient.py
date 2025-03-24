import socket
import struct


def start_server(host='127.0.0.1', port=16166):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(10)
    print(f"Listening on {host}:{port}...")

    while True:
        client_socket, addr = server.accept()
        print("处理addr请求：", addr)
        data_len = client_socket.recv(4)
        data_length = struct.unpack('!I', data_len)[0]
        # print("数据长度：", data_length)

        received_data = b""
        while len(received_data) < data_length:
            chunk = client_socket.recv(data_length - len(received_data))
            if not chunk:
                break
            received_data += chunk
        if received_data:
            # 在这里你可以添加对 HTTP 请求数据的处理和安全测试
            # print("收到数据:")
            data = received_data.decode('utf-8', errors='ignore')
            # print(data)
            # print(type(data))

        # 发送一个消息，告知接受完成
        client_socket.send(b"ok")
        client_socket.close()


if __name__ == "__main__":
    start_server()
