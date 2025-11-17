import pandas as pd
import mysql.connector
from mysql.connector import Error


def clean_price(price):
    if isinstance(price, str):
        # 移除 '$' 符号、空格和其他可能的货币符号
        return float(price.replace('$', '').replace(' ', '').replace(',', ''))
    return price


def import_rubber_data():
    connection = None
    try:
        # 读取CSV文件并打印列名
        df = pd.read_csv('rubber_data.csv')
        print("DataFrame的列名:", df.columns.tolist())
        print("\n数据预览:")
        print(df.head())

        # 数据库连接配置
        connection = mysql.connector.connect(
            host='localhost',
            database='table_tennis',
            user='root',
            password='123456'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # 创建rubber_data表
            create_table_query = """
            CREATE TABLE IF NOT EXISTS rubber_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                rank_num INT,
                rubber VARCHAR(255),
                speed DECIMAL(3,1),
                spin DECIMAL(3,1),
                control DECIMAL(3,1),
                tacky DECIMAL(3,1),
                weight DECIMAL(3,1),
                sponge_hardness DECIMAL(3,1),
                gears DECIMAL(3,1),
                throw_angle DECIMAL(3,1),
                consistency DECIMAL(3,1),
                durable DECIMAL(3,1),
                overall DECIMAL(3,1),
                ratings INT,
                price DECIMAL(10,2)
            )
            """
            cursor.execute(create_table_query)
            print("表创建成功")

            # 准备插入语句
            insert_query = """
                INSERT INTO rubber_data 
                (rank_num, rubber, speed, spin, control, tacky, weight,
                sponge_hardness, gears, throw_angle, consistency, durable,
                overall, ratings, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # 清理价格数据
            if 'Price' in df.columns:
                df['Price'] = df['Price'].apply(clean_price)
            elif 'price' in df.columns:
                df['price'] = df['price'].apply(clean_price)

            # 转换数据为元组列表
            records = df.values.tolist()

            # 批量插入数据
            cursor.executemany(insert_query, records)

            # 提交事务
            connection.commit()
            print(f"成功插入 {cursor.rowcount} 条记录")

    except Error as e:
        print(f"数据库错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        print(traceback.format_exc())

    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
            print("数据库连接已关闭")


if __name__ == "__main__":
    import_rubber_data()