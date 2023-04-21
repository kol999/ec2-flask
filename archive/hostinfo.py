import socket

def get_info():
    hostname = socket.gethostname() 
    ip_address = socket.gethostbyname(hostname)
    msg = f"hostname: {hostname}\n ip_address: {ip_address}" 
    #msg = f"hostname: {hostname}\nIpaddress : {ipaddress}" 
    print(msg)
    return msg 

