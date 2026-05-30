import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate as pt
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

os.getenv("groq_api_key")

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key = os.getenv("groq_api_key"), model_name="llama-3.3-70b-versatile")
    def extract_jobs(self, cleaned_text):
        prompt_extract = pt.from_template(
            '''
            ### Scraped Text from a Website : 
            {page_data}
            Instructions : 
            Your job is to extract the job postings and return them in a JSON format with the following keys :
            'roles', 'skills', 'descriptions', 'experience'.
            Only return Valid JSON
            ### Valid JSON (NO PREAMBLE):
            '''
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input = {'page_data': cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big, unable to parse jobs.")
        return res if isinstance(res, list) else [res]
    def write_mail(self, job, links):
        prompt_email = pt.from_template(
            '''
            ### JOB DESCRIPTION : 
            {job_description}


            ### INSTRUCTIONS : 
            You are Albert Wesker, Business Executive of Umbrella Corp. Umbrella Corp is an AI and Software consulting Company which has provided several services regarding the integration of automated systems for seamless process of business transaction
            Over our experience, we have empowered numerous enterprises with tailoured solutions fostering skills such as process optmization,
            cost reductions, and heightened overall efficeincy.
            Your Job is to write a cold email to the client regarding the job mentioned above and their capabilities required in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase Umbrella's portfolio : {link_list}

            Remember, you are Albert Wesker, BE at Umbrella Corp. Do not provide a Preamble
            ## EMAIL (NO PREAMBLE): 
            '''
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("groq_api_key"))