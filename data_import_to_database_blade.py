import pandas as pd
import mysql.connector
from mysql.connector import Error

def clean_price(price):
    if isinstance(price, str):
        # Remove '$' symbol, spaces, and other possible currency symbols
        return float(price.replace('$', '').replace(' ', '').replace(',', ''))
    return price

def import_blade_data():
    connection = None
    try:
        # Read CSV file
        df = pd.read_csv('blade_data.csv')

        # Print column names for debugging
        print("DataFrame column names:", df.columns.tolist())

        # Check the first few rows of data
        print("\nData preview:")
        print(df.head())

        # Clean price data
        if 'Price' in df.columns:
            df['Price'] = df['Price'].apply(clean_price)
        elif 'price' in df.columns:
            df['price'] = df['price'].apply(clean_price)

        # Database connection configuration
        connection = mysql.connector.connect(
            host='localhost',
            database='table_tennis',
            user='root',
            password='123456'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Prepare insert statement
            insert_query = """
                INSERT INTO blade_data 
                (rank_num, blade, speed, control, stiffness, hardness, 
                consistency, overall, ratings, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

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
    import_blade_data()
