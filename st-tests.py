import streamlit as st
from deckmaker import make_deck, deck2markdown, markdown2marp
from help import GPT_INSTRUCTION, INFO_MODEL
from time import sleep



deck = "Nothing"

def unpack_header(slide_info) -> list:
    """Unpacks the header from the slide_info dictionary"""
    headers = []
    for key, value in slide_info.items():
        print(value)
        headers.append(value["header"])
    return headers

def show_info(name, text, s=0.5):
    name.empty()
    name.info(text)
    #sleep(s)

def show_warning(name, text, s=0.5):
    name.warning(text)
    sleep(s)
    name.empty()


counter = 0
if "counter" not in st.session_state:
    st.session_state.counter = 0
    st.session_state.slide_info = {}


####################################################
###################### SIDEBAR
st.sidebar.markdown("__Configuration__")
model = st.sidebar.selectbox(label="Model", options=["GPT-3", "ChatGPT"], index=0,help=INFO_MODEL)
with st.sidebar.expander("Instructions"):
    st.text("Test")

instructions = st.sidebar.text_area("Instructions", value=GPT_INSTRUCTION)
if model == "GPT-3":
    llm = st.sidebar.selectbox(label="Language Model", options=["davinci", "curie", "babbage", "ada"])
    temperature = st.sidebar.slider(label="Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    max_tokens = st.sidebar.slider(label="Max tokens", min_value=50, max_value=1000, value=500, step=10)
    top_p = st.sidebar.slider(label="Top p", min_value=0.0, max_value=1.0, value=.5, step=0.1)
    frequency_penalty = st.sidebar.slider(label="Frequency penalty", min_value=0.0, max_value=2.0, value=0.3, step=0.1)
    presence_penalty = st.sidebar.slider(label="Presence penalty", min_value=0.0, max_value=2.0, value=0.5, step=0.1)

    GPT_OPTIONS = {model: llm , "temperature": temperature, "max_tokens": max_tokens, 
                "top_p": top_p, "frequency_penalty": frequency_penalty, "presence_penalty": presence_penalty}

else: 
    GPT_OPTIONS = {}

####################################################
###################### MAIN
warning = st.empty()
st.markdown("# Slide Deck Creator")
st.markdown("## Add a slide")

with st.form(key="slide_form"):
    slide_header = st.text_input(label="Header", value="", placeholder="The t-Test    ")
    prompt = st.text_area(label="What should be on this slide?", value="", height=300, placeholder="Explain in three bullet points what a t-test is!")
    add_slide = st.form_submit_button("Add slide")  
    info = st.empty()

if add_slide:
    info.info("Adding slide...")
    sleep(0.2)
    info.empty()
    counter = st.session_state.counter
    st.session_state.slide_info[counter] = {"header": slide_header, "prompt": prompt}
    st.session_state.counter += 1

with st.expander("Slides in deck", expanded=False):
    all_header = [f"{i + 1} | {h}" for i, h in zip(st.session_state.slide_info.keys(), unpack_header(st.session_state.slide_info))]
    slides = st.multiselect(label="Slides in deck", label_visibility="hidden" ,options=all_header, default=all_header)

#st.write(slides)
#st.write(st.session_state.slide_info)

#### Create slide deck
make = st.button("Make slide deck")

# Info prompt for user to see what is happening
info = st.empty() 


if make:
    if slides == []:
        pass
    else:
        ### Get GPT input per prompt/slide
        slide_idx = [int(s.split("|")[0])-1 for s in slides]
        slide_info = {k: v for k, v in st.session_state.slide_info.items() if k in slide_idx}
        ## Make deck incl. input from GPT
        show_info(info, "Making deck...")
        deck = make_deck(slide_info, instructions, **GPT_OPTIONS)

        # Write deck to markdown
        show_info(info, "Writing markdown...")
        fname = "deck.md"
        deck2markdown(deck, fname)  


        # Convert markdown to html
        show_info(info, "Creating html...")
        markdown2marp(fname)
        info.info("Presentation has been created!")
        info.empty()


