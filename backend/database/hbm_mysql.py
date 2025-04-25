import time
import os
import mysql.connector.pooling

def get_db_pool():
    """
    创建并返回数据库连接池
    """
    try:
        # 从环境变量中获取 MySQL 连接信息
        local_mysql_url = os.getenv('LOCAL_MYSQL_URL', 'localhost:3306')
        host, port = local_mysql_url.split(':') if ':' in local_mysql_url else (local_mysql_url, '3306')
        
        config = {
            'host': host,
            'port': port,
            'user': os.getenv('MYSQL_USER'),
            'password': os.getenv('MYSQL_PASSWORD'),
            'database': os.getenv('MYSQL_DATABASE'),
            'pool_name': 'hbm_mysql_pool',
            'pool_size': 20
        }
        return mysql.connector.pooling.MySQLConnectionPool(**config)
    except Exception as e:
        print(f"Error creating database connection pool: {e}")
        raise

def get_db_connection(retries=5, delay=5):
    """
    获取数据库连接，支持重试逻辑
    """
    for i in range(retries):
        try:
            pool = get_db_pool()
            return pool.get_connection()
        except mysql.connector.Error as err:
            print(f"Error getting database connection from pool (attempt {i + 1}/{retries}): {err}")
            if i < retries - 1:
                time.sleep(delay)
    raise Exception("无法连接到数据库，请检查数据库服务是否已启动")

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
        connection.rollback()
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
        connection.rollback()
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