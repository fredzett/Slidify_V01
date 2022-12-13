import openai
import streamlit as st

# MAKE SAFE VIA STREAMLIT CONFIG
openai.api_key = st.secrets["api_key"]

llm2model = {"davinci": "text-davinci-003", 
            "curie": "text-curie-001", 
            "babbage": "text-babbage-001", 
            "ada": "text-ada-001"}

def _get_GPT3_prompt(prompt, instructions, **kwargs):
    """Returns a prompt for GPT-3"""
    llm, temperature, max_tokens, top_p, frequency_penalty, presence_penalty = kwargs.values()
    model = llm2model[llm]
    inpt = prompt + "\n" + instructions + "\n"
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
