from time import sleep
import os

import streamlit as st

from deckmaker import make_deck, deck2markdown, markdown2marp#deck2qmd, make_deck_quarto, markdown2reveal
from help import GPT_INSTRUCTION, INFO_MODEL

st.set_page_config(page_title="The Mechanical McKinsey", page_icon="🤖", initial_sidebar_state="collapsed")

def main_page():
    ##### Incorporate "styles.css" into the app
    with open("styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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
        #name.empty()

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

    with st.sidebar.expander("Model options"):
        if model == "GPT-3":
            llm = st.selectbox(label="Language Model", options=["davinci", "curie", "babbage", "ada"])
            temperature = st.slider(label="Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
            max_tokens = st.slider(label="Max tokens", min_value=50, max_value=1000, value=500, step=10)
            top_p = st.slider(label="Top p", min_value=0.0, max_value=1.0, value=.5, step=0.1)
            frequency_penalty = st.slider(label="Frequency penalty", min_value=0.0, max_value=2.0, value=0.3, step=0.1)
            presence_penalty = st.slider(label="Presence penalty", min_value=0.0, max_value=2.0, value=0.5, step=0.1)

            GPT_OPTIONS = {model: llm , "temperature": temperature, "max_tokens": max_tokens, 
                        "top_p": top_p, "frequency_penalty": frequency_penalty, "presence_penalty": presence_penalty}

        else:
            GPT_OPTIONS = {}
        instructions = st.text_area("Instructions", height=140, value=GPT_INSTRUCTION)

    execute = st.sidebar.selectbox(label="Execute code?", options=["Execute", "Don't execute"], index=1, help="If you select 'Execute', the code will be executed and the output will be shown in the presentation. If you select 'Don't execute', the code will be shown as code in the presentation.")
    execute2bool = {"Execute": True, "Don't execute": False}
    execute = execute2bool[execute]


    ####################################################
    ###################### MAIN
    warning = st.empty()
    #st.markdown("# The Mechanical McKinsey 🤖")
    #st.markdown("Create a slide deck within minutes! 🚀")

    with st.form(key="slide_form", clear_on_submit=True):
        slide_header = st.text_input(label="Slide titel", value="", placeholder="The political system in Germany")
        prompt = st.text_area(label="Content of the slide", value="", height=300, placeholder="Explain the political system in Germany in three bullet points!")
        add_slide = st.form_submit_button("Add slide to deck")  
        info = st.empty()

    if add_slide:

        info.info("Adding slide to deck...")
        sleep(0.2)
        info.empty()
        counter = st.session_state.counter
        st.session_state.slide_info[counter] = {"header": slide_header, "prompt": prompt}
        st.session_state.counter += 1

    with st.expander("Slides in deck", expanded=False):
        all_header = [f"{i + 1} | {h}" for i, h in zip(st.session_state.slide_info.keys(), unpack_header(st.session_state.slide_info))]
        slides = st.multiselect(label="Slides in deck", label_visibility="hidden" ,options=all_header, default=all_header, )
        delete = st.button("Remove selected slides from deck")
        if delete: 
            if slides == []:
                info = st.info("No slides selected!")
                sleep(0.2)
                info.empty()  
            else:
                slide_idx = [int(s.split("|")[0])-1 for s in slides]
                slide_info = {k: v for k, v in st.session_state.slide_info.items() if k not in slide_idx}
                st.session_state.slide_info = slide_info
                st.session_state.counter = len(slide_info)
                info = st.info("Slides removed from deck!")
                sleep(0.2)
                info.empty()


    #### Create slide deck
    make = st.button("Calculate slide deck")


    # Info prompt for user to see what is happening
    info = st.empty() 

    

    if make:
        if slides == []:
            pass
        else:
            if model == "GPT-3":
                ### Get GPT input per prompt/slide
                slide_idx = [int(s.split("|")[0])-1 for s in slides]
                slide_info = {k: v for k, v in st.session_state.slide_info.items() if k in slide_idx}
                ## Make deck incl. input from GPT
                show_info(info, "Making deck...")
                deck = make_deck(slide_info, instructions, **GPT_OPTIONS)#make_deck_quarto(slide_info, instructions, execute,**GPT_OPTIONS) # Includes progress bar
                
                ## Write deck to markdown
                show_info(info, "Writing markdown...")
                fname = "deck.md"#"deck.qmd"
                deck2markdown(deck, fname)#deck2qmd(deck, fname)

                ## Convert markdown to html
                show_info(info, "Creating html...")
                markdown2marp(fname)#markdown2reveal(fname)
                info.success("Presentation has been created!")
                sleep(1)
                info.empty()
                with open("deck.html", 'rb') as f:
                    st.download_button(              #second button
                        label="Download presentation",
                        data=f,
                        file_name="deck.html",
                        mime='application/xhtml+xml',
                    )

            else:
                show_warning(warning, "ChatGPT is not implemented yet")
                sleep(1)
                warning.empty()

def landing_page():

    # Check if deck exists and delete it
    if os.path.exists("deck.qmd"):
        os.unlink("deck.qmd")
    if os.path.exists("deck.html"):
        os.unlink("deck.html")

    text = st.markdown("""
    
# 🤖 The Mechanical McKinsey 

🚀 AI assisted slide draft using GPT-3. 

__All you need is:__
- a topic
- a broad outline or structure of your presentation
    
__How does it work?__ 

1. Enter a slide title :books:

2. Enter what you want to say on the slide :speech_balloon:

3. Add the slide to the deck :thumbsup:

4. Repeat steps 1-3 for all slides :repeat:

5. Select the slides you want to include in the deck :white_check_mark:

6. Click on "Calculate slide deck" :rocket:

Your presentation will be created in the background and open in a new browser tab :tada:

__Choose "Create deck" in the sidebar to get started!__

    
    
    """)
   
pages_dict = {"Instructions": landing_page, "Create deck": main_page}
select_page = st.sidebar.selectbox("Navigation", ["Instructions", "Create deck"])
pages_dict[select_page]()