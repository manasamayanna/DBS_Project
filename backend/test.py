from mySQLConnector import MySQLConnector

mysqlConnector = MySQLConnector()

# Continuously execute a test query and handle exceptions
import time
while True:
    try:
        mysqlConnector.select_test_query()
    except Exception as e:
        print(e)
    print('+' * 30)
    time.sleep(5)
