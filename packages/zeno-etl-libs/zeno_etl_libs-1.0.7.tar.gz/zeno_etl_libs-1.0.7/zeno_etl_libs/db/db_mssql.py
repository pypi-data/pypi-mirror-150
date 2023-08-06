import boto3
import pypyodbc as pyodbc
from zeno_etl_libs.config.common import Config
from zeno_etl_libs.logger import get_logger

logger = get_logger()


def download_private_key_from_s3():
    s3 = boto3.resource('s3')
    file = "id_rsa"
    ssh_pkey_full_path = '/tmp/' + file
    bucket_name = "aws-prod-glue-assets-921939243643-ap-south-1"
    logger.info(f"bucket_name: {bucket_name}")
    logger.info(f"ssh_pkey_full_path: {ssh_pkey_full_path}")
    s3.Bucket(bucket_name).download_file("private/" + file, file)
    logger.info(f"ssh_pkey_full_path downloaded successfully")
    return ssh_pkey_full_path


class MSSql:
    """ MSSQL DB Connection """
    """ implementing singleton design pattern for DB Class """

    def __init__(self, connect_via_tunnel=False):
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.db_secrets = secrets
        self.user = self.db_secrets['WH_MSSQL_USER']
        self.password = self.db_secrets['WH_MSSQL_PASSWORD']
        self.host = self.db_secrets['WH_MSSQL_HOST']
        self.port = self.db_secrets['WH_MSSQL_PORT']
        self.db = self.db_secrets['WH_MSSQL_DATABASE']
        self.connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + self.host + ";DATABASE=" + \
                                 self.db + ";UID=" + self.user + ";PWD=" + self.password + ";TrustServerCertificate=yes"
        # self.url = f"mssql+pymssql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        # TODO: switch on tunnel connect
        self.connect_via_tunnel = False
        self.connection = None
        self.cursor = None
        self.tunnel = None

    def __start_tunnel(self):
        from sshtunnel import SSHTunnelForwarder
        self.tunnel = SSHTunnelForwarder(
            ('workstation.generico.in', 22),
            ssh_username='glue',
            ssh_pkey=download_private_key_from_s3(),
            ssh_private_key_password='',
            remote_bind_address=('wh1.zeno.health', 1433)
        )
        logger.info("Tunnel class ok")
        self.tunnel.start()
        logger.info("Tunnel started")

    def open_connection(self):
        if self.connect_via_tunnel:
            self.__start_tunnel()
        self.connection = pyodbc.connect(self.connection_string)
        # self.connection = pymssql.connect(server='yourserver.database.windows.net', user='yourusername@yourserver',
        #                        password='yourpassword', database='AdventureWorks')
        # self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db,
        #                                   port=int(self.port), connect_timeout=5)

        self.cursor = self.connection.cursor()
        return self.connection

    def connection(self):
        """
        :return: connection to mysql DB using pymysql lib
        """
        return self.open_connection()

    def close(self):
        """
        closes the DB connection
        :return None
        """
        self.connection.close()

        if self.connect_via_tunnel:
            self.tunnel.close()
        print("PostGre DB connection closed successfully!")

    def close_connection(self):
        self.close()
