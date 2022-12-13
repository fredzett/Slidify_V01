from gpt import _get_GPT3_prompt
import subprocess

def _make_yaml(footer="by ChatGPT"):
    return f"""---
marp: true
theme: custom
paginate: true
size: 16:9
math: mathjax
style: @import url('https://unpkg.com/tailwindcss@^2/dist/utilities.min.css')
footer: {footer}
---
    """

def _make_title_slide(titel="Presentation by AI", subtitel="Pretty cool, huh?"):
    return f"""
<!-- _class: title -->
<!-- _footer: '' -->
<!-- _paginate: false -->
# {titel} 
## {subtitel}
    """

def _make_slide(header, answer):
    return f"""
---
## {header} 
    
{answer}
    
"""

def make_deck(slide_info: dict, instructions, **GPT_OPTIONS) -> str:
    deck = _make_yaml() + _make_title_slide() 
    for key, value in slide_info.items():
        prompt = value["prompt"]
        answer = _get_GPT3_prompt(prompt, instructions, **GPT_OPTIONS)
        deck += _make_slide(value["header"], answer)
    return deck


def deck2markdown(deck: str, fname="deck.md") -> None:
    with open(fname, "w") as f:
            f.write(deck)

def markdown2marp(file):
    
    # Create HTML
    marp_it = f"npx @marp-team/marp-cli@latest --theme custom.css --html {file}"
    
    # Open HTML in Browser
    file = file.split(".")[0] # remove .md
    proc = subprocess.run([marp_it], shell=True, stdout=subprocess.PIPE)
    #subprocess.Popen(['open', f'{file}.html'])
    return proc