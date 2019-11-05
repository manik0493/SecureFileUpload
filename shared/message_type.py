class MessageType(object):
    NORMAL = 0
    TERMINATE = 2
    ERROR = -1

    AUTH = 10
    AUTH_ACK = 11
    AUTH_REQ = 12
    AUTH_FIN = 13

    UPLOAD = 20
    UPLOAD_REQ = 21
    DOWNLOAD = 30
    DOWNLOAD_REQ = 31
