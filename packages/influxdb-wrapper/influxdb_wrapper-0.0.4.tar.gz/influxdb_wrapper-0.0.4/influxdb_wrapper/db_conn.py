from abc import ABC, abstractmethod


class DBOpenException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DBExceptionNotOpen(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DBGetLockException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DBReleaseLockException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DBConn(ABC):

    def __init__(self):
        self.conn = None

    @abstractmethod
    def openConn(self, params, autocommit=True):
        pass

    def getConn(self):
        return self.conn

    def closeConn(self):
        pass

    @abstractmethod
    def insert(self, table, rows):
        pass

    def getLock(self, lockname):
        raise

    def releaseLock(self, lockname):
        raise


def influxdb_factory(db_type: str = 'influx') -> DBConn:
    if db_type == 'influx':
        from .influxdb_conn import InfluxDBConn
        return InfluxDBConn()
    elif db_type == 'mock':
        from .mockdb_conn import InfluxMockDBConn
        return InfluxMockDBConn()
