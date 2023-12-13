import pandas as pd
import streamlit as st
import mysql.connector
from mysql.connector import errors


# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Samy@1007',
    'database': 'phonebook',
}

# Streamlit app
def main():
    st.title("Phone Book CRUD Operations")

    # Connect to MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Create phone_records table if not exists
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS phone_records (
            Name VARCHAR(255),
            Email VARCHAR(255),
            Phone1 VARCHAR(20),
            Phone2 VARCHAR(20)
        )
    '''
    cursor.execute(create_table_query)
    connection.commit()

    st.sidebar.header("Options")
    choice = st.sidebar.radio("", ["Upload CSV/JSON"])

    if choice == "Upload CSV/JSON":
        st.subheader("Upload CSV or JSON file:")
        file = st.file_uploader("Choose a file", type=["csv", "json"])

        if file is not None:
            try:
                # Read the file and insert into the database
                if file.type == "text/csv":
                    df = pd.read_csv(file)
                elif file.type == "application/json":
                    df = pd.read_json(file)

                st.dataframe(df)

                if st.button("Save to Database"):
                    insert_records_into_db(cursor, df)
                    st.success("Data successfully saved to the database!")
                connection.commit()

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
            finally:
                # Close the connection
                connection.close()

# CRUD functions
def insert_records_into_db(cursor, df):
    for index, row in df.iterrows():
        cursor.execute('''
            INSERT INTO phone_records (Name, Email, Phone1, Phone2)
            VALUES (%s, %s, %s, %s)
        ''', (row['Name'], row['Email'], row['Phone1'], row['Phone2']))

if __name__=='__main__':
    main() 