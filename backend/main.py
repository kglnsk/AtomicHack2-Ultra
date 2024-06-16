import json
import os
import re
import string
import numpy as np
import openai
from util.ragdb import RAGDB
import faiss
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
import tempfile
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import requests
import pandas as pd 

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-m3')



def load_faiss_index(database):
    ragdb  = RAGDB(database)
    return ragdb


class InputText(BaseModel):
    text: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to truncate strings to 200 characters
def truncate_string(s, max_length=200):
    return s.lstrip().rstrip() if len(s) <= max_length else s[:max_length-3].rstrip().lstrip() + '...'



df = pd.read_excel('questions.xlsx')
df.columns = df.iloc[0]
df = df.iloc[1:]
df['Описание'] = df['Описание'].astype(str)
embeddings = np.load('embs-questions.npy')
faiss_index = faiss.IndexFlatL2(embeddings.shape[1])  
faiss_index.add(embeddings)


client = openai.OpenAI(
    api_key="fba55128c5cf945c1c3e8349d5e86b2d284015f2faf0eab3c0cd46ab4dfef179",
    base_url="https://api.together.xyz/v1",
    )

ragdb = load_faiss_index('RosAtom-2048.ragdb')

def get_relevant_questions(question):
    encoded_question = model.encode(question)
    distances, indices = faiss_index.search(encoded_question.reshape(1, -1), 10)
    retrievals = df.iloc[indices.flatten()[:3]]
    retrieve_df = retrievals[['Описание','Решение']]
    retrieve_df.columns = ['question','answer']
    return retrieve_df



def generate_response(question, ragdb):
    rets = ragdb.get_docs(question)
    metadatas = [list(item.metadata.keys())[0] for item in rets]
    
    # Improved string formatting
    sources_text = ' \n\n '.join([f'REFERENCE {i+1}: {ret.page_content}' for i, ret in enumerate(rets)])
    print(len(sources_text),flush=True)
    promptstring = (
f"Вы - блестящий помощник, который точно отвечает на вопросы на темы связанные с делопроизводством.",
 f"Используя информацию, содержащуюся в перечисленных ССЫЛКАХ после слова ТЕКСТ",
 f"ответьте на вопрос, заданный после слова ВОПРОС."
 f"Структурируйте свой ответ и отвечайте поэтапно. Отвечайте исключительно на русском языке. Рассуждайте, используя в качестве входных информацию, данную в ТЕКСТЕ, если данных для ответа недостаточно, то отвечайте НЕДОСТАТОЧНО ДАННЫХ. При ответе, используя информацию из текста,",
 f"используйте ссылки в квадратных скобках, содержащие номер ИСТОЧНИКА с соответствующей информацией.\n",
 f"<ТЕКСТ>:\n{sources_text}\n</ТЕКСТ>\ВОПРОС:\n{question}",
 )
    response = client.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    messages=[{"role": "user", "content":promptstring}],
    temperature=0.5,
    max_tokens=2048,
    )
    answer = response.choices[0].message.content
        
    return answer,metadatas,rets


@app.post("/api/answer_question/")
async def answer_question(input_data:InputText):
    try:
        q = input_data.text
        answer,metadatas,rets = generate_response(q,ragdb)

        # Clean up: remove the temporary file

        rdf = get_relevant_questions(q)
        rdf = rdf.applymap(truncate_string)
        questions_list = rdf.to_dict(orient='records')
        result = {
            "instruction": answer + f'\n\nИсточник:{metadatas[0]}',
            "questions": questions_list
        }

        return JSONResponse(status_code=200, content=result)

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


