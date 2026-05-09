# from langchain_openai import ChatOpenAI
# from Augmentation.Augmented import build_prompt

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0
# )

# def generate_answer(query, docs):

#     context = "\n\n".join(
#         [doc.page_content for doc in docs]
#     )

#     prompt = build_prompt(context, query)

#     response = llm.invoke(prompt)

#     return response.content

#from transformers import pipeline
from src.config.Settings import GROQ_API_KEY
from src.Augmentation.Augmented import build_prompt
from langchain_groq import ChatGroq
# Load free HuggingFace model
# pipe = pipeline(
#     "text-generation",
#     model="mistralai/Mistral-7B-Instruct-v0.2",
#     max_new_tokens=256,
#     temperature=0.3
# )
llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0.6,
    api_key=GROQ_API_KEY
)

def generate_answer(query, docs):

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = build_prompt(context, query)

    response = llm.invoke(prompt)

    return response.content