import pandas
from abc import abstractmethod

class PostgresBase():
    conn_string = None
    port = '5432'
    sslmode = 'allow'  # { required, disable, allow }
    driver = None  # don't use
    conn = None

    @abstractmethod
    def _conn(self):
        pass

    def get_cursor(self):
        conn = self._conn()
        return conn.cursor()

    def fetchAll(self, query):
        self._conn()
        df = pandas.read_sql(query, con=self.conn)
        self.conn.close()
        self.conn.close()
        return df

    def fetchOne(self, query):
        self._conn()
        db = self.conn.cursor()
        db.execute(query)
        rows = db.fetchone()
        if len(rows) > 0:
            return rows[0]
        else:
            return None

    def fetchRow(self, query):
        self._conn()
        db = self.conn.cursor()
        db.execute(query)
        rows = db.fetchone()
        if len(rows) > 0:
            return list(rows)
        else:
            return list()

    def fetchCol(self, query):
        df = self.fetchAll(query)
        return df.iloc[:, 0].tolist()

    def execute(self, script):
        affected_rows = -1
        self._conn()
        cursor = self.conn.cursor()
        cursor.execute(script)

        self.conn.commit()
        affected_rows = cursor.rowcount
        self.conn.close()
        return affected_rows

    def table_exists(self, table_name, schema=None):
        if schema is None:
            cant = self.fetchOne(f"SELECT COUNT(1) FROM information_schema.tables WHERE table_name = '{table_name}' ")
        else:
            cant = self.fetchOne(
                f"SELECT COUNT(1) FROM information_schema.tables WHERE table_name = '{table_name}' AND table_schema='{schema}'")
        return cant > 0

    def close(self):
        self.conn.close()


class PostgresFromClass(PostgresBase):
    conn_string = None
    port = '5432'
    sslmode = 'allow'  # { required, disable, allow }
    driver = None  # don't use
    conn = None

    @property
    @abstractmethod
    def host(self):
        pass

    @property
    @abstractmethod
    def user(self):
        pass

    @property
    @abstractmethod
    def password(self):
        pass

    @property
    @abstractmethod
    def dbname(self):
        pass

    def __init__(self):
        self._conn()

    def _conn(self):
        import psycopg2
        self.conn_string = 'host={} user={} dbname={} password={} port={} sslmode={}'.format(
            self.host, self.user, self.dbname, self.password, str(self.port), self.sslmode
        )
        try:
            self.conn = psycopg2.connect(self.conn_string)
        except psycopg2.OperationalError as e:
            raise Exception("OperationalError, verifique la VPN o su red")
        except Exception as e:
            raise Exception(e)

        return self.conn

    def create_engine(self):
        # TODO deactivate logging 'sqlalchemy.engine'
        from sqlalchemy import create_engine
        return create_engine(
            f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}?sslmode={self.sslmode}')



class PostgresFromString(PostgresBase):
    conn_string = None
    port = '5432'
    sslmode = 'allow'  # { required, disable, allow }
    driver = None  # don't use
    conn = None

    def __init__(self, conn_string):
        self.conn_string = conn_string
        self._conn()

    def _conn(self):
        try:
            import psycopg2
            self.conn = psycopg2.connect(self.conn_string)
        except Exception as e:
            raise Exception(e)
        return self.conn


class PostgresToBigquery(PostgresFromString):
    def to_bigquery(self,
                    source_table,
                    project,
                    dataset,
                    target_table=None,
                    limit=100000,
                    verbose=False,
                    where='',
                    columns='*',
                    disposition='DROP'  # DROP, TRUNCATE, APPEND
                    ):
        from google.cloud import bigquery
        from ipywidgets import IntProgress
        try:
            i = 0
            rows = 0
            max_iterations = 10000

            if verbose: print("Conectando a Postgres\t", end='')
            db = self
            if verbose: print("[OK]")
            total_rows = db.fetchOne(f"SELECT COUNT(1) FROM {source_table} {where}")
            print('total rows:', total_rows)
            f = IntProgress(min=0, max=total_rows)
            display(f)  # display the bar

            # Bigquery connection & target configuration
            table_id = f'`{project}.{dataset}.{target_table}`'
            client_bigquery = bigquery.Client(project=project)
            if target_table is None: target_table = source_table
            if disposition == 'DROP':
                client_bigquery.delete_table(f'{dataset}.{target_table}', not_found_ok=True)
            elif disposition == 'TRUNCATE':
                job_config = bigquery.QueryJobConfig(use_legacy_sql=False)
                query_job = client_bigquery.query(f'''TRUNCATE TABLE {table_id}''',
                                                  job_config=job_config)  # API request
                query_job.result()  # Waits for statement to finish
            elif disposition == 'APPEND':
                pass
            else:
                raise Exception(f"disposition {disposition} nor supported")

            if verbose: print("Copiando datos...", end='')
            while 1:

                if verbose: print(f"EXTRACT PostgreSQL... ", end='')
                sql = f"""SELECT {columns} FROM {source_table} {where} LIMIT {limit} OFFSET {limit * i}"""
                if verbose: print(sql)
                df = db.fetchAll(sql)
                rows = len(df)
                f.value += rows  # signal to increment the progress bar
                if verbose: print("OK")
                if rows > 0:
                    if verbose: print(f"LOAD Bigquery... ", end='')
                    job_config = bigquery.LoadJobConfig(autodetect=True, write_disposition='WRITE_APPEND')
                    client_bigquery.load_table_from_dataframe(df, f"{dataset}.{target_table}", job_config=job_config)
                    if verbose: print(f"OK")
                if rows == 0 or rows < limit:
                    # print("FIN")
                    break
                if i >= max_iterations:
                    break
                i = i + 1
        except Exception as e:
            print('ERROR', e)

# @deprecated
class PostgresSQL(PostgresBase):
    conn_string = None
    port = '5432'
    sslmode = 'allow'  # { required, disable, allow }
    driver = None  # don't use
    conn = None

    @property
    @abstractmethod
    def host(self):
        pass

    @property
    @abstractmethod
    def user(self):
        pass

    @property
    @abstractmethod
    def password(self):
        pass

    @property
    @abstractmethod
    def dbname(self):
        pass

    def __init__(self):
        self._conn()

    def _conn(self):
        import psycopg2
        self.conn_string = 'host={} user={} dbname={} password={} port={} sslmode={}'.format(
            self.host, self.user, self.dbname, self.password, str(self.port), self.sslmode
        )
        try:
            self.conn = psycopg2.connect(self.conn_string)
        except psycopg2.OperationalError as e:
            raise Exception("OperationalError, verifique la VPN o su red")
        except Exception as e:
            raise Exception(e)

        return self.conn

    def create_engine(self):
        # TODO deactivate logging 'sqlalchemy.engine'
        from sqlalchemy import create_engine
        return create_engine(
            f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}?sslmode={self.sslmode}')
