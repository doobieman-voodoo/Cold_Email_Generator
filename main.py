import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import sys
print(sys.executable)
from chain import Chain
from portfolio import Portfolio
from utils import cleaned_text

def create_streamlit_app(llm, portfolio, cleaned_text):
    st.title("Cold Mail Generator")
    url_input = st.text_input("Enter a URL: ", value = "https://careers.nike.com/senior-data-engineer-global-converse-itc/job/R-81660")
    submit_button = st.button("submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = cleaned_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language = 'markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")
            
if __name__ == '__main__':
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout = 'wide', page_title='Cold Email Generator', page_icon = "📧")
    create_streamlit_app(chain, portfolio, cleaned_text)