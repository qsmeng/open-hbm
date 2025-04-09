import mysql.connector
import sys
import os
import logging

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from backend import get_remoto_api_url

def get_db_pool():
    """
    创建并返回数据库连接池
    """
    # url = get_remoto_api_url.get_url_from_env_file('mysql').replace('tcp://', '')
    # host, port = url.split(':', 1)
    host='localhost'
    port='3306'
    try:
        config = {
            'host': os.getenv(host, 'localhost'),
            'port': os.getenv(port, '3306'),
            'user': os.getenv('MYSQL_USER'),
            'password': os.getenv('MYSQL_PASSWORD'),
            'database': os.getenv('MYSQL_DATABASE'),
            'pool_name': 'hbm_mysql_pool',
            'pool_size': 20
        }
        pool = mysql.connector.pooling.MySQLConnectionPool(**config)
        return pool
    except mysql.connector.Error as err:
        print(f"Error creating database pool: {err}")
        raise

def get_db_connection():
    """
    获取数据库连接
    """
    try:
        pool = get_db_pool()
        return pool.get_connection()
    except mysql.connector.Error as err:
        print(f"Error getting database connection from pool: {err}")
        raise

def insert_data(table_name, data):
    """
    插入数据
    """
    try:
        # 获取数据库连接
        with get_db_connection() as connection:
            cursor = connection.cursor()
            # 执行插入语句，使用参数化查询
            placeholders = ", ".join(["%s"] * len(data))
            sql = f"INSERT INTO {table_name} ({', '.join(data.keys())}) VALUES ({placeholders})"
            cursor.execute(sql, list(data.values()))
            connection.commit()
            return cursor.lastrowid
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
        raise  

def upsert_data(table_name, data, unique_keys):
    """
    更新或插入数据
    """
    try:
        # 获取数据库连接
        with get_db_connection() as connection:
            cursor = connection.cursor()
            # 构建插入语句，设置重复时的更新内容
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            update_clause = ", ".join([f"{key}=VALUES({key})" for key in data if key not in unique_keys])

            sql = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE {update_clause}
            """
            cursor.execute(sql, list(data.values()))
            connection.commit()
            return cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Error updating or inserting data: {err}")
        raise


def delete_data(table_name, condition, params):
    """
    删除数据
    """
    try:
        # 获取数据库连接
        with get_db_connection() as connection:
            cursor = connection.cursor()
            # 使用参数化查询来防止 SQL 注入
            sql = f"DELETE FROM {table_name} WHERE {condition}"
            cursor.execute(sql, params)
            connection.commit()
            return cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Error deleting data: {err}")
        raise  

def query_data(table_name, condition, params):
    """
    查询数据
    """
    try:
        # 获取数据库连接
        with get_db_connection() as connection:
            cursor = connection.cursor()
            # 使用参数化查询来防止 SQL 注入
            sql = f"SELECT * FROM {table_name} WHERE {condition}"
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return results
    except mysql.connector.Error as err:
        print(f"Error getting data: {err}")
        raise   

def main():
    try:
        # 获取数据库连接
        with get_db_connection() as connection:
            # 在这里执行数据库操作
            cursor = connection.cursor()
            # 示例查询
            cursor.execute("SELECT 1 FROM dual")
            results = cursor.fetchall()
            for row in results:
                print(row)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()