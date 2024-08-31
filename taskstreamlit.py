import streamlit as st
import mysql.connector
import pandas as pd

# Establish MySQL Connection
con = mysql.connector.connect(host="localhost", user="root", password="root", database="py")
cursor = con.cursor()

# Sidebar Navigator
rad = st.sidebar.radio("Navigator", ["Register", "Login", "User Details"])

# Register Section
if rad == "Register":
    st.title("Register")
    # User Input Fields
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email_id = st.text_input("Email Id")
    phone_num = st.text_input("Mobile Number")
    user_name = st.text_input("User Name")
    user_password = st.text_input("Password", type="password")
    user_password_reenter = st.text_input("Re-enter Password", type="password")
    button = st.button("Submit")

    if button:
        if user_password == user_password_reenter:
            # Insert into Database
            qry = "INSERT INTO Pythontask (first_name, last_name, email_id, phone_num, user_name, user_password) VALUES (%s, %s, %s, %s, %s, %s)"
            user = (first_name, last_name, email_id, phone_num, user_name, user_password)
            cursor.execute(qry, user)
            con.commit()
            st.success("Registration successful!")
        else:
            st.error("Passwords do not match")

# Login Section
if rad == "Login":
    st.title("Login")
    user_name = st.text_input("User Name")
    user_password = st.text_input("Password", type="password")
    button = st.button("Login")

    if button:
        login_query = "SELECT * FROM Pythontask WHERE user_name = %s AND user_password = %s"
        user_data = (user_name, user_password)
        cursor.execute(login_query, user_data)
        result = cursor.fetchone()
        if result:
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")

# User Details Section
if rad == "User Details":
    st.title("User Details")
    user_details_query = "SELECT id, first_name, last_name, email_id, phone_num FROM Pythontask"
    cursor.execute(user_details_query)
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=["ID", "First Name", "Last Name", "Email ID", "Phone Number"])
    st.write(df)

# Close MySQL Connection
con.close()
