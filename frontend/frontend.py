import streamlit as st
import time
import requests

from urllib.parse import quote

from helpers import parse_results, get_llm_response, get_context


def display_ui():
    if query:
        context_title = "Results"
        if generate_llm_response:
            context_title = "Context"
        with st.expander(context_title):
            resos = get_context(query)
            to_write = parse_results(resos)
            st.markdown(to_write, unsafe_allow_html=True)

        if generate_llm_response:
            title = st.empty()
            title.write("Summary - Generating...")
            container = st.container(border=True)
            container.write_stream(get_llm_response(query))
            title.write("Summary")


query = st.text_input("Enter your query", placeholder="Type Here ...")
generate_llm_response = st.checkbox("Generate LLM Response", value=False)
generate_button = st.button("Generate", on_click=display_ui)
