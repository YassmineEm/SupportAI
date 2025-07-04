from utils.langchain_client import llm
from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template("""
You are a professional customer support evaluator.
Analyze the following chat transcript and provide constructive feedback:

{transcript}
""")

async def handle_chat_analysis(file):
    content = (await file.read()).decode('utf-8')
    chain = prompt | llm
    feedback = chain.invoke({"transcript": content})
    return {"feedback": feedback}


