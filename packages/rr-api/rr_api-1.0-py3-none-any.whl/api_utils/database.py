import os
from rankset.common.my_sql import MySqlConnection
from api_utils.constants import General

db_user = os.environ.get('user')
db_password = os.environ.get('password')

if db_user is None:
    db_user = General.DEFAULT_USER

if db_password is None:
    db_password = General.DEFAULT_PASSWORD

conn = MySqlConnection(user=db_user, password=db_password, database=General.DATABASE)
