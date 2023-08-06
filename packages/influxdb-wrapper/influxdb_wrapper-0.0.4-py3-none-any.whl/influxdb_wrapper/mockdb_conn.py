from .db_conn import DBConn, DBExceptionNotOpen
from datetime import datetime
from copy import deepcopy


class InfluxMockDBConn(DBConn):
    def __init__(self):
        super().__init__()
        self.db_tables = None

    def openConn(self, params, autocommit=True):
        self.db_tables = {}

    def closeConn(self):
        self.conn.close()

    def insert(self, table, rows):
        if self.db_tables is None:
            raise DBExceptionNotOpen('Database not opened')

        points = deepcopy(rows)
        for point in points:
            point["measurement"] = table
            if 'time' not in point or not point['time']:
                point['time'] = datetime.utcnow()
        self.db_tables[table] = points

    def select(self, table_name: str, tags_conds: tuple, order_by: str = None, order_asc: bool = True, limit: int = 0):
        if self.db_tables is None:
            raise DBExceptionNotOpen('Database not opened')

        result = []
        table = self.db_tables[table_name]
        for row in table:
            fullfills = True
            for cond in tags_conds:
                if row['tags'][cond[0]] != cond[1]:
                    fullfills = False
                    break

            if fullfills:
                # influx returns everything in plain (no tags or fields subdicts)
                result_row = {}
                result_row['time'] = row['time']
                for tag, value in row['tags'].items():
                    result_row[tag] = value
                for field, value in row['fields'].items():
                    result_row[field] = value
                result.append(result_row)

        # Sort if needed
        if order_by is not None:
            result.sort(reverse=not order_asc, key=lambda x: x[order_by])

        # Limit if needed
        result = result[0:limit]

        return result


    def getLock(self, lockname):
        raise

    def releaseLock(self, lockname):
        raise
