import streamlit as st
import auth
    

@auth.check_is_authenticated
def chat_page():
    st.title("Chat Page")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg['sender'] == "User":
                with st.chat_message("user"):
                    st.markdown(msg['content'])
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg['content'])

    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("Ваше сообщение:", key='user_input')
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        st.session_state.messages.append({"sender": "User", "content": user_input})
        response = f"Бот получил ваше сообщение: {user_input}"
        st.session_state.messages.append({"sender": "Bot", "content": response})
        st.session_state.messages.append({"sender": "Bot", "content": "some random text"})
        st.rerun()

def booking_history_page():
    st.title("Booking History Page")
    
def support_page():
    st.title("Support Page")

@auth.check_is_authenticated
def home_page():
    st.title(f"Главная страница, {auth.controller.get('username')}")

    page_names_to_funcs = {
        "Chat Page": chat_page,
        "Booking Hisroey": booking_history_page,
        "Support Page": support_page
    }
    page_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
    page_names_to_funcs[page_name]()
    if st.button("Выйти"):
        auth.controller.set('username', '')
        st.rerun()

# Функция для отображения экрана профиля
def profile_page():
    st.title(f"User Profile: {st.session_state.username}")

    if st.button("Back"):
        st.session_state.page = "Main"
        st.experimental_rerun()


def main():
    var = auth.controller.get('username')
    if var:
        home_page()
    else:
        auth.login()

if __name__ == "__main__":
    main()