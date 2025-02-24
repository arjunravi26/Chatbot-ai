from pipeline.pipeline import Pipeline
import streamlit as st

# Set page configuration as the very first Streamlit command.
st.set_page_config(
    page_title="AI Assistant 🤖",
    page_icon="🤖",
    layout="wide"
)


def load_pipeline():
    return Pipeline()


pipeline = load_pipeline()


def get_response(model_number, query):
    """Generate a response based on the selected model and user query."""
    model_names = ["Gemini", "DeepSeek"]
    if "chat_history" in st.session_state:
        chat_history = st.session_state.chat_history
    else:
        chat_history = []
    response = pipeline.predict(query, model_number, chat_history)
    return f"**{model_names[model_number]} says:** {response}"


def main():
    # Initialize chat history in session state if not already present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --- Sidebar ---
    st.sidebar.title("Options")
    models = ["Gemini", "DeepSeek"]
    selected_model = st.sidebar.selectbox("Select a Model", models)
    model_number = models.index(selected_model)

    if st.sidebar.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.experimental_rerun()

    st.title("AI Assistant")

    # Display existing chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # Initial greeting if no conversation exists
    if not st.session_state.chat_history:
        with st.chat_message("assistant"):
            st.markdown(
                "Hello! Select a model from the sidebar and ask me anything about AI.")

    # Accept user input
    user_input = st.chat_input("Type your message here")
    if user_input:
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input})
        response = get_response(model_number, user_input)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
