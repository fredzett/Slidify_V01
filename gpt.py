import openai
import streamlit as st
import os
import platform

# QUICK FIX TO SWITCH BETWEEN LOCAL AND REMOTE
processor = platform.processor()
openai.api_key = os.getenv("OPENAI_API_KEY") if processor else st.secrets["api_key"]

#openai.api_key = os.getenv("OPENAI_API_KEY")#st.secrets["api_key"]

llm2model = {"davinci": "text-davinci-003", 
            "curie": "text-curie-001", 
            "babbage": "text-babbage-001",  
            "ada": "text-ada-001"}

def _get_GPT3_prompt(prompt, instructions, **GPT_OPTIONS):
    """Returns a prompt for GPT-3"""
    llm, temperature, max_tokens, top_p, frequency_penalty, presence_penalty = GPT_OPTIONS.values()
    model = llm2model[llm]
    inpt = instructions + "\n" + prompt + "\n"
    answer =  openai.Completion.create(
            model=model,
            prompt=inpt, 
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        ).choices[0].text
    print(answer)
    return answer
