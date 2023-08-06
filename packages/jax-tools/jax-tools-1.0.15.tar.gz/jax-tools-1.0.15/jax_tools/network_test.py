# -*- coding: utf-8 -*-
"""
Check if the target IP and port is open
"""
import socket
import sys
from ping3 import ping


def check_icmp_connectivity(ip):
    """
    Check if the target IP is reachable
    Args:
        ip(str): IP address or hostname

    Returns:

    """
    try:
        # Use ping3 to check if the target IP is reachable
        if ping(ip):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def check_connectivity(ip, port):
    """
    检查目标IP和端口是否可以连接
    Args:
        ip: 目标IP
        port:  目标端口

    Returns:
        True if the port is open
        False if the port is closed or the connection is refused
    """
    s = None
    network_unreachable = 'Network is unreachable'
    result_dict = {
        35: 'The port is closed',
        61: 'Connection refused, firewall restrictions may be set on the target port',
        111: 'Connection refused',
        113: 'No route to host',
        101: network_unreachable,
        110: 'Connection timed out',
        10035: network_unreachable,
        10061: 'Connection refused',
        10060: 'Connection timed out',
        10051: network_unreachable,
        10065: 'No route to host',
        10064: 'Host is down',
        10013: 'Permission denied',
        10049: 'Can\'t assign requested address'
    }
    try:
        # 创建一个socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)  # 设置超时时间（单位：秒）
        if isinstance(port, str):
            try:
                port = int(port)
                if port < 0 or port > 65535:
                    print("The port must be between 0 and 65535")
                    sys.exit(1)
            except ValueError:
                print("The port must be a number")
                sys.exit(1)
        # 尝试连接到目标IP和端口
        result = s.connect_ex((ip, port))
        if result == 0:
            print("Connection success")
            result = True
        elif result in result_dict.keys():
            if check_icmp_connectivity(ip):
                print("Connection error: ", result_dict[result])
            else:
                print("Connection error: ", result_dict[result], "and ping not work")
            result = False
        else:
            print("Connection error：", result)
            result = False
    except socket.error as e:
        print("Connection error：", e)
        result = False
    finally:
        if s:
            s.close()
    return result


def main():
    """
    Main function
    Returns:

    """
    if len(sys.argv) == 3:
        target_ip = sys.argv[1]
        target_port = int(sys.argv[2])
        check_connectivity(target_ip, target_port)
    else:
        print("Usage: nd <TargetIP> <TargetPort>")



