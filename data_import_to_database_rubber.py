import pandas as pd
import mysql.connector
from mysql.connector import Error

def clean_price(price):
    if isinstance(price, str):
        # Remove '$' symbol, spaces, and other possible currency symbols
        return float(price.replace('$', '').replace(' ', '').replace(',', ''))
    return price

def import_rubber_data():
    connection = None
    try:
        # Read CSV file and print column names
        df = pd.read_csv('rubber_data.csv')
        print("DataFrame column names:", df.columns.tolist())
        print("\nData preview:")
        print(df.head())

        # Database connection configuration
        connection = mysql.connector.connect(
            host='localhost',
            database='table_tennis',
            user='root',
            password='123456'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Create rubber_data table
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
            print("Table created successfully")

            # Prepare insert statement
            insert_query = """
                INSERT INTO rubber_data 
                (rank_num, rubber, speed, spin, control, tacky, weight,
                sponge_hardness, gears, throw_angle, consistency, durable,
                overall, ratings, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Clean price data
            if 'Price' in df.columns:
                df['Price'] = df['Price'].apply(clean_price)
            elif 'price' in df.columns:
                df['price'] = df['price'].apply(clean_price)

            # Convert data to a list of tuples
            records = df.values.tolist()

            # Batch insert data
            cursor.executemany(insert_query, records)

            # Commit transaction
            connection.commit()
            print(f"Successfully inserted {cursor.rowcount} records")

    except Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        print(traceback.format_exc())

    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed")

if __name__ == "__main__":
    import_rubber_data()
