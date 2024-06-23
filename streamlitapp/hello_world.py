import streamlit as st
import random

st.title("Conference Programme Explorer")

st.write("Hello World")

st.markdown(
    """Welcome to the **Conference Programme Explorer!**

Streamlit is a great tool for building interactive data applications, and amongst
others allows the use of markdown to format text.

In the following commits, or using the different pages of the app, you will see how
to build a simple application to explore the EURO 2024 conference programme. For an up-to-date
version of the programme, check the [conference website](https://euro2024cph.dk/)"""
)


st.write("## Basic input elements")

# Streamlit reloads on every user interaction, and does this from top-to-bottom in the script. This means
# that the random number generated here will be different on every reload.
st.write(f"Random number: {random.randint(0, 100)}")

# Streamlit reloads the page each time the user interacts with the input elements. Hence, this means
# that we can also re-use some of the input provided. For example, we can use the provided text input
# at an earlier stage in the application by collecting it from the `session_state`. Note that the `session_state`
# will be empty at the start of a new browser session.
text_input_value = st.session_state.get("text_input_value", None)
st.write(f"Text input value: {text_input_value}")

# We can capture the input provided by the user in a variable and as such use it later on.
number_input_value = st.number_input("Enter a positive number", value=1, min_value=0, step=1)

# To capture the provided user input and re-use it at other points in the app, we can set the `key` of
# the input element and store the value in the `session_state`.
text_input_return = st.text_input("Enter some text", value=None, key="text_input_value")

st.write(f"Number input value: {number_input_value}")
st.write(f"Text input value: {text_input_return}")
