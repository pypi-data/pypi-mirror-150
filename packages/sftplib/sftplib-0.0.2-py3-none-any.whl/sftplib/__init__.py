
from sftplib.ftp import FTPClient
from sftplib.sftp import SFTPClient


def Client(protocol, host, user, password, port=0):
    proto = protocol.strip().lower()
    assert proto in ['ftp', 'sftp'], 'Invalid protocol, options are: SFTP, FTP'
    if proto == 'ftp':
        port = port if port != 0 else 21
        return FTPClient(host, user, password, port)
    else:
        port = port if port != 0 else 22
        return SFTPClient(host, user, password, port)

