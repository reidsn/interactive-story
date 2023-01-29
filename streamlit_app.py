"""Streamlit implementation of Interactive Story"""
import streamlit as st
import json
import random
import sys

# Load story.
story = None
if len(sys.argv) == 1:
    file = st.file_uploader('Upload your file here:', type=["json"])
    if file:
        story = json.load(file)
else:
    filename = sys.argv[1]
    story = json.load(open(filename))

# Set starting key.
STARTING_KEY = "intro"

# Instantiate session state keys.
if 'key' not in st.session_state:
    st.session_state.key = STARTING_KEY
if 'inventory' not in st.session_state or st.session_state.key == "intro":
    st.session_state.inventory = dict()
if 'history' not in st.session_state or st.session_state.key == "intro":
    st.session_state.history = []

# Define callback functions.
def save_input(item):
    # For 'input' qtype, save input to inventory.
    st.session_state.inventory[item] = st.session_state.input

def button_click(option):
    # For 'yes_no' and 'none' qtypes, set next scene key to option.
    st.session_state.key = scene.get(option, "error")

def select_choice():
    # For 'choice' qtype, use user selection to move to next scene.
    st.session_state.key = st.session_state.choice.lower()

def knowledge_check(info, correct, wrong):
    # For 'knowledge_check' qtype, check input against answer in inventory.
    if st.session_state.knowledge.lower() == st.session_state.inventory[info].lower():
        st.session_state.key = correct
    else:
        st.session_state.key = wrong

def contains(keywords, correct, wrong):
    # For 'contains' qtype, check for keywords in user input.
    if any(i in st.session_state.contains.lower() for i in keywords):
        st.session_state.key = correct
    else:
        st.session_state.key = wrong

def go_to_history(history_readable, history_keys):
    key = history_keys[history_readable.index(st.session_state.history_select)]

    # Set scene key and revise history.
    st.session_state.key = key
    st.session_state.history = st.session_state.history[:st.session_state.history.index(key)]

# Set expander and dropdown for story history.
with st.expander("History"):
    # Create readable history list and scene key list.
    history_readable = [story[i]["human_readable"] for i in st.session_state.history if story[i].get("human_readable")]
    history_keys = [i for i in st.session_state.history if story[i].get("human_readable")]

    st.selectbox(
        label="Choose A Scene To Jump To",
        options=history_readable,
        key="history_select",
        on_change=go_to_history,
        args=(history_readable, history_keys)
    )

# Set expander to display player info from inventory.
with st.expander("Player Info"):
    # Filter out inventory items from future scenes (if user went back in story history).
    held_items = [i[0] for i in st.session_state.inventory.get("inventory", []) if i[1] in st.session_state.history]
    for name, item in st.session_state.inventory.items():
        if name == "inventory":
            st.text(f"{name}: {held_items}")
        else:
            st.text(f"{name}: {item}")

st.markdown("---")

if story:
    # Get scene info.
    scene = story.get(st.session_state.key, story["error"])

    # Handle history update.
    st.session_state.history.append(st.session_state.key)

    # Add add_to_bag item to user inventory['inventory'].
    if scene.get("add_to_bag"):
        bag = st.session_state.inventory.get("inventory", set())
        bag.add((scene["add_to_bag"], st.session_state.key))
        st.session_state.inventory["inventory"] = bag

    # Display scene text.
    st.markdown(scene["scene"].replace('\n', '  \n').format(**st.session_state.inventory))

    # Process scene display by scene qtype and process user response with callback functions.
    if scene.get("qtype") == "input":
        st.text_input(
            label="Enter Your Answer",
            key="input",
            on_change=save_input,
            args=(scene["input"],)
        )
        st.session_state.key = scene.get("next", "error")
    elif scene.get("qtype") == "yes_no":
        yes, no, space = st.columns([1, 1, 12])
        with yes:
            st.button("Yes", on_click=button_click, args=("yes",))
        with no:
            st.button("No", on_click=button_click, args=("no",))
    elif scene.get("qtype") == "none":
        st.button("Continue", on_click=button_click, args=("next",))
    elif scene.get("qtype") == "choice":
        st.selectbox(
            label="Select Your Answer",
            options=scene["choices"],
            key="choice",
            on_change=select_choice
        )
    elif scene.get("qtype") == "knowledge_check":
        st.text_input(
            label="Enter Your Answer",
            key="knowledge",
            on_change=knowledge_check,
            args=(scene["info"], scene["correct"], scene["wrong"])
        )
    elif scene.get("qtype") == "contains":
        st.text_input(
            label="Enter Your Answer",
            key="contains",
            on_change=contains,
            args=(scene["keywords"], scene["contains"], scene["not_contains"])
        )
    elif scene.get("qtype") == "random":
        st.session_state.key = random.choices(scene["options"], scene["weights"])[0]
        st.experimental_rerun()

    # Display scene image.
    if scene.get("image"):
        st.image(scene["image"])
