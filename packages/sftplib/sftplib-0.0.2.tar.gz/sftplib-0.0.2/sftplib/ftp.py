import os
from ftplib import FTP


from sftplib.exceptions import InvalidConnection


class FTPClient:
    def __init__(self, host, user, password, port=21):
        self.host = host
        self.user = user
        self.password = password
        self.port = port

        self._transport = None
        self._conn = None

    def __enter__(self):
        self._start_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close_connection()

    def __repr__(self):
        return f'<FTPClient({self.host}, {self.user}, xxxx, port = {self.port})>'

    def _start_connection(self):
        try:
            self._conn = FTP()
            self._conn.connect(self.host, self.port)
            self._conn.login(self.user, self.password)
        except:
            raise InvalidConnection(f'Error connecting to FTP server')

    def _close_connection(self):
        if self._conn is not None:
            self._conn.close()

    def listdir(self, path):
        return self._conn.nlst(path)

    def chdir(self, path):
        self._conn.cwd(path)
        return True

    def mkdir(self, path):
        self._conn.mkd(path)

        return True

    def rmdir(self, path):
        self._conn.rmd(path)

        return True

    def pwd(self):
        self._conn.pwd()

    def rename(self, oldpath, newpath):
        self._conn.rename(oldpath, newpath)

        return True

    def delete(self, path):
        self._conn.delete(path)

        return True

    def getfo(self, remotepath, fo):
        self._conn.retrbinary(f'RETR {remotepath}', fo.write)

    def get(self, remotepath, localpath):
        path = os.path.split(localpath)[0]

        if not os.path.exists(path):
            os.mkdir(path)

        with open(localpath, 'wb') as f:
            self.getfo(remotepath, f)

    def putfo(self, fo, remotepath):
        self._conn.storbinary(f'STOR {remotepath}', fo)
    
    def put(self, localpath, remotepath):
        if not os.path.exists(localpath):
            raise Exception(f'{localpath} does not exists')

        with open(localpath, 'rb') as f:
            self.putfo(f, remotepath)
