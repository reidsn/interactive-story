"""Command line implementation of Interactive Story"""
import json
import pickle
import random
import sys

# Set up state variables.
inventory = dict()
history = []

# Load story.
filename = sys.argv[1]
story = json.load(open(filename))

# Load answer classifier.
with open('model/classifier', 'rb') as picklefile:
    classifier = pickle.load(picklefile)
with open('model/vectorizer', 'rb') as picklefile:
    vectorizer = pickle.load(picklefile)

# Print welcome statement.
print(
    "\nWelcome to the Interactive Story!\n\nType your answer and press enter to move to the next scene, or type " \
    "'quit' to exit the game.\n\nIf you want to go back in the story, type 'back', or 'inventory' to view current "\
    f"character information.{'-' * 79}\n\n"
)

# Run story loop.
key = "intro"
while key != "end":
    # Get scene info.
    scene = story.get(key, story["error"])

    # Handle history update.
    if key == "intro":
        history = []
    history.append(key)

    # Process scene display by scene qtype.
    if scene["qtype"] == "none":
        # For 'none' qtype, display scene text and move on.
        print(f'{scene["scene"]}\n'.format(**inventory))
        key = scene.get("next", "error")
    elif scene["qtype"] == "random":
        # For 'random' qtype, display scene text if filled, then make random choice of next scene from options.
        if scene["scene"]:
            print(f'{scene["scene"]}\n'.format(**inventory))
        key = random.choices(scene["options"], scene["weights"])[0]
    else:
        # For 'choice' qtype, collect choices to display to user.
        choices = f'[{", ".join(scene["choices"])}]\n' if scene["qtype"] == "choice" else ""

        # For all other qtypes, display scene text and collect answer input from user.
        answer = input(f'{scene["scene"]}\n{choices}'.format(**inventory))

        # Classify user input.
        vect = vectorizer.transform([answer.lower()]).toarray()
        label = classifier.predict(vect)[0].lower()

        # Process user input.
        if answer.lower() == "quit":
            # Break loop and end program if user quits.
            break
        elif label == "back":
            # Process user request to go back in story.
            print('-' * 79)

            # Create readable history list and scene key list.
            history_readable = [story[i]["human_readable"] for i in history if story[i].get("human_readable")]
            history_keys = [i for i in history if story[i].get("human_readable")]

            # Gather user choice on scene.
            new_scene = input(f'Please select a scene to return to:\n[{", ".join(history_readable)}]\n').lower()

            # Set scene key and revise history.
            key = history_keys[[i.lower() for i in history_readable].index(new_scene)]
            history = history[:history.index(key)]
        elif label == "inventory":
            # Process user request to view player inventory.
            print('-' * 79)

            # Format inventory and display to user.
            invent_format = '\n'.join([f"{k}: {v}" for k, v in inventory.items()])
            cont = input(
                f"Here's the current game information:\n{invent_format}\nHit Enter to close and continue with " \
                "the story.\n"
            )
        elif scene["qtype"] == "input":
            # For 'input' qtype, save input to inventory.
            inventory[scene["input"]] = answer
            key = scene.get("next", "error")
        elif scene["qtype"] == "yes_no":
            # For 'yes_no' qtype, use classification result to move to next scene.
            key = scene.get(label, "error")
        elif scene["qtype"] == "choice":
            # For 'choice' qtype, use user input to move to next scene.
            if answer.lower() not in [i.lower() for i in scene["choices"]]:
                answer = input("Be clearer! Which option do you pick?\n")
            key = answer.lower()
        elif scene["qtype"] == "knowledge_check":
            # For 'knowledge_check' qtype, check input against answer in inventory.
            if answer.lower() == inventory[scene["info"]].lower():
                key = scene.get("correct", "error")
            else:
                key = scene.get("wrong", "error")
        elif scene["qtype"] == "contains":
            # For 'contains' qtype, check for keywords in user input.
            if any(i in answer.lower() for i in scene["keywords"]):
                key = scene.get("contains", "error")
            else:
                key = scene.get("not_contains", "error")
    print('-' * 79)

    # Add add_to_bag item to user inventory['inventory'].
    if scene.get("add_to_bag"):
        inventory["inventory"] = inventory.get("inventory", []) + [scene["add_to_bag"]]
