import streamlit as st

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

# We can capture the input provided by the user in a variable and as such use it later on.
number_input_value = st.number_input("Enter a positive number", value=1, min_value=0, step=1)

text_input_value = st.text_input("Enter some text")

st.write(f"Number input value: {number_input_value}")
st.write(f"Text input value: {text_input_value}")
