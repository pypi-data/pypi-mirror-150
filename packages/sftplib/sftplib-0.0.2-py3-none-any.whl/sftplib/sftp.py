import os
import paramiko


from sftplib.exceptions import InvalidConnection


class SFTPClient:
    def __init__(self, host, user, password, port=22):
        self.host = host
        self.user = user
        self.password = password
        self.port = port

        self._transport = None
        self._conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self):
        return f'<SFTPClient({self.host}, {self.user}, xxxx, port = {self.port})>'

    def connect(self):
        try:
            self._transport = paramiko.Transport((self.host, self.port))
            self._transport.connect(None, self.user, self.password)
            self._conn = paramiko.SFTPClient.from_transport(self._transport)
        except:
            raise InvalidConnection(f'Error connecting to SFTP server')

    def close(self):
        if self._transport is not None:
            self._transport.close()

        if self._conn is not None:
            self._conn.close()

    def listdir(self, path):
        return self._conn.listdir(path)

    def chdir(self, path):
        self._conn.chdir(path)

        return True

    def mkdir(self, path):
        self._conn.mkdir(path)

        return True

    def rmdir(self, path):
        self._conn.rmdir(path)

        return True

    def pwd(self):
        return self._conn.getcwd()

    def rename(self, oldpath, newpath):
        self._conn.rename(oldpath, newpath)

        return True

    def delete(self, path):
        self._conn.remove(path)

        return True

    def getfo(self, remotepath, fo, callback=None):
        if callback is not None:
            assert callable(callback), "Callback must to be a function"

        self._conn.getfo(remotepath, fo, callback)

    def get(self, remotepath, localpath, callback=None):
        if callback is not None:
            assert callable(callback), "Callback must to be a function"

        path = os.path.split(localpath)[0]

        if not os.path.exists(path):
            os.mkdir(path)

        self._conn.get(remotepath, localpath, callback=callback)

    def putfo(self, fo, remotepath, callback=None):
        if callback is not None:
            assert callable(callback), "Callback must to be a function"
            
        self._conn.putfo(fo, remotepath, callback)

    def put(self, localpath, remotepath, callback=None):
        if callback is not None:
            assert callable(callback), "Callback must to be a function"

        if not os.path.exists(localpath):
            raise Exception(f'{localpath} does not exists')

        self._conn.put(localpath, remotepath, callback=callback)
