
import os
from dotenv import load_dotenv
load_dotenv()

MAX_CONNECT_TIMEOUT = 3

MASTER_A_CONFIG = {
    'host' : os.getenv('MYSQL_HOST'),
    'database' : os.getenv('MYSQL_DATABASE'),
    'port' : os.getenv('MYSQL_PORT_MASTER_A'),
    'user' : os.getenv('MYSQL_USER_MASTER_A'),
    'password' : os.getenv('MYSQL_PASSWORD_MASTER_A'),
    'auth_plugin' : 'mysql_native_password',
    'connect_timeout' : MAX_CONNECT_TIMEOUT
}


MASTER_B_CONFIG = {
    'host' : os.getenv('MYSQL_HOST'),
    'database' : os.getenv('MYSQL_DATABASE'),
    'port' : os.getenv('MYSQL_PORT_MASTER_B'),
    'user' : os.getenv('MYSQL_USER_MASTER_B'),
    'password' : os.getenv('MYSQL_PASSWORD_MASTER_B'),
    'auth_plugin' : 'mysql_native_password',
    'connect_timeout' : MAX_CONNECT_TIMEOUT
}
