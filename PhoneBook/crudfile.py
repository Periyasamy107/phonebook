from readfile import *

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
    choice = st.sidebar.radio("", ["Perform CRUD Operations"])

    if choice == "Perform CRUD Operations":
        st.subheader("Perform CRUD Operations:")
        operation = st.selectbox("Select Operation", ["Select Records", "Insert Record", "Update Record", "Delete Record"])

        try:
            if operation == "Select Records":
                condition = st.text_input("Enter WHERE condition (e.g., Name='Doe'):", "")
                if st.button("Execute"):
                    result = select_records_from_db(cursor, condition)
                    st.dataframe(result)

            elif operation == "Insert Record":
                name = st.text_input("Name:", "")
                email = st.text_input("Email:", "")
                phone1 = st.text_input("Phone 1:", "")
                phone2 = st.text_input("Phone 2:", "")

                if st.button("Insert Record"):
                    insert_single_record_into_db(cursor, name, email, phone1, phone2)
                    st.success("Record successfully inserted into the database!")
                connection.commit()
                
            elif operation == "Update Record":
                condition = st.text_input("Enter WHERE condition (e.g., Name='Doe'):", "")
                name = st.text_input("New Name:", "")
                email = st.text_input("New Email:", "")
                phone1 = st.text_input("New Phone 1:", "")
                phone2 = st.text_input("New Phone 2:", "")

                if st.button("Update Record"):
                    update_record_in_db(cursor, condition, name, email, phone1, phone2)
                    st.success("Record successfully updated in the database!")
                connection.commit()

            elif operation == "Delete Record":
                condition = st.text_input("Enter WHERE condition (e.g., Name='Doe'):", "")

                if st.button("Delete Record"):
                    delete_record_from_db(cursor, condition)
                    st.success("Record successfully deleted from the database!")
                connection.commit()

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            # Close the connection
            connection.close()

# CRUD functions

def insert_single_record_into_db(cursor, Name, Email, Phone1, Phone2):
    cursor.execute('''
        INSERT INTO phone_records (Name, Email, Phone1, Phone2)
        VALUES (%s, %s, %s, %s)
    ''', (Name, Email, Phone1, Phone2))

def select_records_from_db(cursor, condition):
    query = 'SELECT * FROM phone_records'
    if condition:
        query += f" WHERE {condition}"
    cursor.execute(query)
    return pd.DataFrame(cursor.fetchall(), columns=['Name', 'Email', 'Phone 1', 'Phone 2'])

def update_record_in_db(cursor, condition, Name, Email, Phone1, Phone2):
    update_query = '''
        UPDATE phone_records
        SET Name = %s, Email = %s, Phone1 = %s, Phone2 = %s
        WHERE {}
    '''.format(condition)
    cursor.execute(update_query, (Name, Email, Phone1, Phone2))

def delete_record_from_db(cursor, condition):
    delete_query = '''
        DELETE FROM phone_records
        WHERE {}
    '''.format(condition)
    cursor.execute(delete_query)

if __name__ == "__main__":
    main()