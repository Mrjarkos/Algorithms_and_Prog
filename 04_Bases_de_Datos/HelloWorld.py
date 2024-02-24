import psycopg2

def main():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname="your_database_name",
            user="your_username",
            password="your_password",
            host="localhost",  # Change this to your database host
            port=5432,  # Change this to your database port
        )

        # Create a cursor
        cursor = conn.cursor()

        # Execute a simple query
        cursor.execute("SELECT 'Hello, PostgreSQL!'")

        # Fetch the result
        result = cursor.fetchone()
        print(result[0])  # Print the result

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
