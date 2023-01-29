# Interactive Story

Welcome to Interactive Story, a lightweight infrastructure to run text-based narrative games!

The system currently supports two ways to play: a classic text adventure interface on the command line and a graphical interface using Streamlit.

## Running the Game

To run an Interactive Story, all you need is a JSON file with the story and the run script of your choice. You can find example story JSON files in [stories](https://github.com/sarahnr42/interactive-story/blob/master/stories).

### Command Line

For the command line version of Interactive Story, ensure you have the `interactive_story.py` script and the `classifier` and `vectorizer` in the `model` folder.

To run the story, use the command `python3 interactive_story.py {story file path}`, and the story will run in your terminal.

### Streamlit

For the command line version of Interactive Story, ensure you have installed Streamlit from `requirements.py`.

To run the story, use the command `streamlit run streamlit_app.py {story file path}`, and the story will run in a local server using your web browser.

You can also run `streamlit run streamlit_app.py` and upload the story JSON directly to the webpage.

## Writing a Story

You can write your own custom stories to run with Interactive Story. You can find examples of the story format in [stories](https://github.com/sarahnr42/interactive-story/blob/master/stories).

A story JSON file in a nested dictionary of scene dictionaries. The key of the first scene in the story should be `intro` and the key of the last scene should be `end`. An example of a short three scene story is as follows.

```
{
    "intro": {
        "human_readable": "Introduction",
        "scene": "Welcome to the story!",
        "qytpe": "none",
        "next": "first_scene"
    },
    "first_scene": {
        "human_readable": "The First Scene",
        "scene": "Do you want to go to the last scene?",
        "qtype": "yes_no",
        "yes": "end",
        "no": "intro"
    },
    "end": {
        "scene": "The End!"
    }
}
```

Each scene can have the following parameters:

| Parameter      | Required                                                      | Description                                                                                                                                            |
| -------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| scene          | yes                                                           | The text to display for this scene. If you do not want to display any text, put an empty string.                                                       |
| qtype          | yes, if this scene connects forward to another scene          | The question type of this scene (see [Question Types](#question-types) below). Do not include if this scene does not connect forward to another scene. |
| human_readable | yes, if you want this scene to show up in the history options | How this scene will appear in the history dropdown. Do not include to omit scene from history dropdown.                                                |
| add_to_bag     | no                                                            | A text description of an item to add to the player's inventory when they reach this scene.                                                             |
| image          | no                                                            | Path to an image to show in the Streamlit version.                                                                                                     |

### Question Types

There are seven question types available in Interactive Story and some have parameters specific to them.

#### Yes/No

The `yes_no` question type is the most basic question type in Interactive Story. Use this for scenes where you prompt the user with a yes or no question.

The unique parameters for the `yes_no` question type are:

| Parameter | Required | Description                                            |
| --------- | -------- | ------------------------------------------------------ |
| yes       | yes      | The key of the scene to go to if the user answers yes. |
| no        | no       | The key of the scene to go to if the user answers no.  |

A `yes_no` scene looks like this:
```
"example_scene": {
    "human_readable": "Example Scene",
    "scene": "This is an example scene.\nDo you want to continue?",
    "qtype": "yes_no",
    "yes": "yes_scene",
    "no": "no_scene"
}
```

#### Choice

The `choice` question type allows for a broader range of choice options. Use this for scenes where you prompt the user with a multiple choice question, where each choice leads to a different next scene.

The unique parameter for the `choice` question type is:

| Parameter | Required | Description                                            |
| --------- | -------- | ------------------------------------------------------ |
| choices   | yes      | A list of the choices for the user to pick from.       |

> **_NOTE:_** The lowercased version of each option will be interpreted as the key of the scene it leads to.
> 
> For example, for an option in a choices list called 'Castle', the key of the scene that option leads to should be 'castle'.

A `choice` scene looks like this:
```
{
    "example_scene": {
        "human_readable": "Example Scene",
        "scene": "This is an example scene.\nWhich scene do you want to continue to?",
        "qtype": "choice",
        "choices": ['One', 'Two', 'Three']
    },
    "one": {
        "human_readable": "One",
        "scene": "This is scene one.",
        "qtype": "none",
        "next": "example_scene"
    },
    ...
}
```

#### Input

The `input` question type allows you to collect text input from the user. Use this for scenes where you prompt the user for information that you want to use later in the story or show in the inventory.

The unique parameters for the `input` question type are:

| Parameter | Required | Description                                                     |
| --------- | -------- | --------------------------------------------------------------- |
| input     | yes      | The key to save the user input under in the inventory.          |
| next      | yes      | The key of the next scene to go to after the user enters input. |

> **_TIP:_** If you want to dynamically use user input in the story text, you can do so using {} syntax in the `scene` parameter.
>
> For example, if you have collected the user's name with the input parameter `name`, it is now in the system's inventory as `{'name': 'Bob'}`. You can now have a future scene with the parameter `{'scene': 'Nice to meet you {name}!'}`, and it will display to the user as `Nice to meet you Bob!`.

An `input` scene looks like this:
```
{
    "example_scene": {
        "human_readable": "Example Scene",
        "scene": "This is an example scene.\nWhat is your name?",
        "qtype": "input",
        "input": "name",
        "next": "say_name"
    },
    "say_name": {
        "human_readable": "Say Name",
        "scene": "Hello, {name}! Let's go back to the beginning.",
        "qtype": "none",
        "next": "example_scene"
    }
}
```

#### Knowledge Check

The `knowledge_check` question type allows you to check the user's knowledge. Use this for scenes where you prompt the user to respond with something they previously input into the game in an `input` scene.

The unique parameters for the `knowledge_check` question type are:

| Parameter | Required | Description                                              |
| --------- | -------- | -------------------------------------------------------- |
| info      | yes      | The key that the answer is saved under in the inventory. |
| correct   | yes      | The key of the scene to go to if the user is correct.    |
| wrong     | yes      | The key of the scene to go to if the user is incorrect.  |

A `knowledge_check` scene looks like this:
```
"example_scene": {
    "human_readable": "Example Scene",
    "scene": "This is an example scene.\nWhat is your name?",
    "qtype": "knowledge_check",
    "info": "name",
    "correct": "correct_scene",
    "wrong": "wrong_scene"
}
```

#### Contains

The `contains` question type allows you to check the user's knowledge. Use this for scenes where the answer must contain one of a list of keywords.

The unique parameters for the `contains` question type are:

| Parameter    | Required | Description                                                             |
| ------------ | -------- | ----------------------------------------------------------------------- |
| keywords     | yes      | A list of keywords, where at least one must appear in the user answer.  |
| contains     | yes      | The key of the scene to go to if the answer contains a keyword.         |
| not_contains | yes      | The key of the scene to go to if the answer does not contain a keyword. |

A `contains` scene looks like this:
```
"example_scene": {
    "human_readable": "Example Scene",
    "scene": "This is an example scene.\nWhat is in a BLT?",
    "qtype": "contains",
    "keywords": ["bacon", "lettuce", "tomato"],
    "contains": "correct_scene",
    "not_contains": "wrong_scene"
}
```

#### Random

The `random` question type allows you to randomize which scene comes next. Use this for scenes where you do not require user input, but will randomly determine the next scene.

The unique parameters for the `random` question type are:

| Parameter | Required | Description                                                                                                                                                                                                 |
| --------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| options   | yes      | A list of scene keys for the randomizer to choose from.                                                                                                                                                     |
| weights   | yes      | A list of integer weights for how likely each option is to be chosen. The higher the number, the more likely the option will be chosen. If you want all options to be equally likely, set all weights to 1. |

> **_NOTE:_** While you can include `scene` text for a `random` scene, it may not display in the Streamlit version, as the page will automatically reload as soon as a random option is chosen.

A `random` scene looks like this:
```
"example_scene": {
    "human_readable": "Example Scene",
    "scene": "",
    "qtype": "random",
    "options": ["scene_1", "scene_2", "scene_3"],
    "weights": [1, 3, 1]
}
```

#### None

The `none` question type allows you to present a scene without a user response. Use this for scenes where you want to present information to the user, but do not require user input to move to the next scene.

The unique parameters for the `none` question type are:

| Parameter | Required | Description                         |
| --------- | -------- | ----------------------------------- |
| next      | yes      | The key of the next scene to go to. |

A `none` scene looks like this:
```
"example_scene": {
    "human_readable": "Example Scene",
    "scene": "This is an example scene.",
    "qtype": "none",
    "next": "next_scene"
}
```