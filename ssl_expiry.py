# modified from Lucas Roelser <roesler.lucas@gmail.com>
# Modified from serverlesscode.com/post/ssl-expiration-alerts-with-lambda/

import datetime
import fileinput
import logging
import os
import socket
import ssl
import time

def ssl_expiry_datetime(hostname: str, port: int) -> datetime.datetime:
    # r'...' ignores escape sequences
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )

    conn.connect((hostname, port))
    time.sleep(0.1)
    ssl_info = conn.getpeercert()
    # parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
