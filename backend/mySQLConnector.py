import mysql.connector
from timeout_decorator import timeout, TimeoutError as TDTimeoutError
from config import MASTER_A_CONFIG, MASTER_B_CONFIG
import threading

class MySQLConnector:
    def __init__(self):
        # Initialize the class with default values
        self.database = MASTER_A_CONFIG.get('database', 'amazon')
        self.masterA_connection = None
        self.masterB_connection = None
        self.current_connection = None
        self.cursor = None
        try:
            self.__before_query()
        except Exception as e:
            print(e)
            exit(1)
            
    # Try connecting to the database with a timeout
    def __connect_with_timeout(self, config):
        try:
            @timeout(3)
            def _connect(config):
                return mysql.connector.connect(**config)

            connection = _connect(config)
            print(f"[OK] Connected to master")
            return connection
        except TDTimeoutError as e:
            print('[ERROR] timeout connecting')
            return None
        except mysql.connector.Error as e_master:
            print(f'[ERROR] connecting to master: {e_master}')
            return None
        except Exception as e:
            return None

    # Try reconnecting to the database with a timeout
    def __reconnect_with_timeout(self, connection): 
        try:
            @timeout(3)
            def _reconnect(connection):
                return connection and connection.reconnect()
            _reconnect(connection)
        except TDTimeoutError as e:
            print('[ERROR] timeout reconnecting')
        except Exception as e:
            print(e)

    # Check if the connection is alive with a timeout
    def __check_connection_with_timeout(self, connection):
        try:
            @timeout(3)
            def _check_connection(connection):
                return  connection and connection.is_connected()
            response =  _check_connection(connection)
            return response
        except TDTimeoutError as e:
            print('[ERROR] timeout checking connection')
            return False
        except Exception as e:
            print(e)
            return False

    # Switch between two database servers (Master A and Master B)
    def __switch_master(self, config, master):
        # Check if there's already a connection and it's alive
        if self.current_connection and self.__check_connection_with_timeout(self.current_connection):
            print(f"[INFO] Already connected to {master}")
            return True
        elif self.current_connection: # Try reconnecting and
            self.__reconnect_with_timeout(self.current_connection)

        # check the connection again
        if self.current_connection and self.__check_connection_with_timeout(self.current_connection):
            print(f"[INFO] Again reconnected to {master}")
            return True
        else:
            # If connection fails, try to establish a new connection
            self.current_connection = self.__connect_with_timeout(config)
            if self.current_connection and self.__check_connection_with_timeout(self.current_connection):
                self.cursor = self.current_connection.cursor()
                print(f"[INFO] Switched to {master}")
                return True
            else:
                print(f"[ERROR] Failed to switch to {master}")

        return False

    # Perform checks and switch to the appropriate server before executing a query
    def __before_query(self):
        if self.current_connection and self.__check_connection_with_timeout(self.current_connection):
            return
        # If there's no existing connection, try switching to Master A.
        if self.__switch_master(MASTER_A_CONFIG, 'masterA'):
            return
        # If switching to Master A fails, try switching to Master B.
        if self.__switch_master(MASTER_B_CONFIG, 'masterB'):
            return
        # If both fail, raise an exception indicating that no master could be connected.
        raise Exception("Unable to connect to any master server")

    # Execute a SQL query
    def execute_query(self, query, values=None):
        try:
            self.__before_query()
            if 'SELECT' in query.upper() or 'DELETE' in query.upper():
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)
        except mysql.connector.Error as e:
            print(f'[ERROR] Executing query: {e}')
            return None
        except Exception as e:
            print(e)
            return None

    # Execute a test query on the database
    def select_test_query(self):
        self.execute_query(f'select * from amazon.user')
        data = self.cursor.fetchall()
        if data and len(data) > 0:
            print(f'[INFO] Successful query.')
        else:
            print(f'[INFO] Failed query')
        
    def insert_user(self, name, email, password):
        try:
            insert_query = f'INSERT INTO {self.database}.user (name, email, password) VALUES (%s, %s, %s)'
            values = (name, email, password)
            self.execute_query(insert_query, values)
            self.current_connection.commit()
            return 'User inserted successfully'
        except mysql.connector.Error as err:
            return f'Error during user insertion: {err}'
        
    def insert_product(self, user_id, name, price, stock, image_url, description, category_id):
        try:
            insert_query = f'INSERT INTO {self.database}.product (user_id, name, price, stock, image_url, description, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            values = (user_id, name, price, stock, image_url, description, category_id)
            self.execute_query(insert_query, values)
            self.current_connection.commit()
            return 'Product inserted successfully'
        except mysql.connector.Error as err:
            return f'Error during product insertion: {err}'

    def update_product(self, user_id, product_id, name, price, stock, image_url, description, category_id):
        try:
            update_query = f'UPDATE {self.database}.product SET name = %s, price = %s, stock = %s, image_url = %s, description = %s, category_id = %s WHERE id = %s and user_id = %s'
            values = (name, price, stock, image_url, description, category_id, product_id, user_id)
            self.execute_query(update_query, values)
            self.current_connection.commit()
            return 'Product updated successfully'
        except mysql.connector.Error as err:
            return f'Error during product update: {err}'

    def select_products(self, user_id):
        try:
            select_query = f'SELECT * FROM {self.database}.product WHERE user_id = {str(user_id)}'
            self.execute_query(select_query)
            products = []
            for row in self.cursor.fetchall():
                product = {field: value for field, value in 
                           zip(['id', 'name', 'price', 'stock', 'image_url', 'description', 'category_id'], row)}
                products.append(product)
            return products
        except mysql.connector.Error as err:
            return f'Error during product selection: {err}'
    
    def select_categories(self):
        try:
            select_query = f'SELECT * FROM {self.database}.category'
            self.execute_query(select_query)
            categories = self.cursor.fetchall()
            categories =  list(map(lambda category: {"id": category[0], "value": category[1]}, categories))
            return categories
        except mysql.connector.Error as err:
            return f'Error during product selection: {err}'
        
    def delete_product_by_id(self, user_id, product_id):
        try:
            delete_query = f'DELETE FROM {self.database}.product WHERE user_id = {str(user_id)} AND id = {str(product_id)}'
            self.execute_query(delete_query)
            self.current_connection.commit()
            return 'Product deleted successfully'
        except mysql.connector.Error as err:
            return f'Error during product deletion: {err}'

        
    def close_connection(self):
        self.cursor.close()
