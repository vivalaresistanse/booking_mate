
import streamlit as st
import streamlit_cookies_controller
import sqlite3
import os
path = os.getenv("DB_PATH")
controller = streamlit_cookies_controller.CookieController()

def check_is_authenticated(func):
    def wrapper(*args, **kwargs):
        if controller.get('username'):
            return func(*args, **kwargs)
        return login()
    return wrapper


def get_user_credentials(username, password):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    cursor.execute("SELECT username, password FROM users WHERE username = ? AND password = ?",(username, password))
    user = cursor.fetchone()
    connection.close()
    if user:
        controller.set("username", user[0])
        return user[0],user[1]
    return None, None

def login():
    input_username = st.text_input("Username")
    input_password = st.text_input("Password", type="password")

    if st.button("Login"):
        name, hashed_password = get_user_credentials(input_username, input_password)
        st.session_state['username'] = name
        print(name, hashed_password)    

        if name and hashed_password:
            st.write(f'Welcome *{name}*')
        else:
            st.error("Username not found")
        st.rerun()