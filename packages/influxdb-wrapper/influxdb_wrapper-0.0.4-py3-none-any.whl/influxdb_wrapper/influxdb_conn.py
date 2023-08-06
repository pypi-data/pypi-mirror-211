from .db_conn import DBConn, DBOpenException, DBExceptionNotOpen, DBGetLockException, DBReleaseLockException
from datetime import datetime
from influxdb import InfluxDBClient
from copy import deepcopy


class InfluxDBConn(DBConn):
    def __init__(self):
        super().__init__()
        self.conn = None

    def openConn(self, params, autocommit=True):
        host = params['host']
        user = params['user']
        password = params['password']
        bucket = params['bucket']

        self.conn = InfluxDBClient(host=host, username=user, password=password, database=bucket)

    def closeConn(self):
        self.conn.close()

    def insert(self, table, rows):
        if not self.conn:
            raise DBExceptionNotOpen('Database not opened')

        points = deepcopy(rows)
        for point in points:
            point["measurement"] = table
            if 'time' not in point or not point['time']:
                point['time'] = datetime.utcnow()

        self.conn.write_points(points)

    def _get_condition_string(self, condition: tuple):
        ret = ''
        if type(condition[0]) == str:
            ret = "{}='{}'".format(condition[0], condition[1])
        elif type(condition[0]) == int:
            ret = "{}={}".format(condition[0], condition[1])
        return ret

    def select(self, table_name: str, tags_conds: tuple, order_by: str = None, order_asc: bool = True, limit: int = 0):
        conds_string = ""

        if tags_conds:
            conds_string = " WHERE "

            conds_string += self._get_condition_string(tags_conds[0])

            for cond in tags_conds[1:]:
                conds_string += " AND " + self._get_condition_string(cond)

        query = """SELECT * from {table} {conditions}
                ORDER BY {order_by} {direction}
                LIMIT {limit}""".format(table=table_name,
                                        conditions=conds_string,
                                        order_by=order_by,
                                        direction='ASC' if order_asc else 'DESC',
                                        limit=limit)
        result_set = self.conn.query(query)
        points = list(result_set.get_points())

        return points

    def getLock(self, lockname):
        raise

    def releaseLock(self, lockname):
        raise
