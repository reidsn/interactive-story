class Scene:
    ## Models a scene with a script and two outcome pointers.

    ## Constructs a scene object with script lines and outcomes.
    # @param script a list of script lines
    # @param outcomes a list of outcome pointers
    #
    def __init__(self, script, qtype, question, outcomes, replace):
        self.script = script
        self.qtype = qtype
        self.question = question
        self.outcomes = outcomes
        self.replace = replace

    ## Sets the question type.
    # @param qtype the qyestion type
    #
    def set_qtype(self, qtype):
        self.qtype = qtype

    ## Sets the script.
    # @param script the script
    #
    def set_script(self, script):
        self.script = script

    ## Sets the question.
    # @param question the question
    #
    def set_question(self, question):
        self.question = question

    ## Gets the script.
    # @return the script
    #
    def get_script(self):
        return self.script

    ## Gets the question.
    # @return the question
    #
    def get_question(self):
        return self.question

    ## Gets the replace tags.
    # @return the replace tags
    def get_replace(self):
        return self.replace

    ## Runs the scene.
    # @return the outcome scene to go to
    #
    def run_scene(self):
        for line in self.script:
                print(line)
        if self.qtype != 'random':
            question = input(self.question + '\n')
            print('\n')
        else:
            question = self.question.split(',')
            for i in range(len(question)):
                question[i] = int(question[i])
        return answer(question, self.qtype, self.outcomes)

    def to_string(self):
        return('Script: ' + str(self.script) + '\nType: ' + self.qtype + \
               '\nOutcomes: ' + str(self.outcomes))


        
## Determines what outcome the user answer indicates.
# @param text the user input
# @param qtype the type of question
# @return a boolean indicating which outcome is appropriate
def answer(text, qtype, outcomes):
    if qtype == 'yesno': #judges for yes/no questions
        THRESHOLD_PCT = 0.75
        THRESHOLD_TOTAL = 10
        unknown_words = []
        uncountable_words = []
        ambiguous_words = []

        while (word_dict.get(text) is None) or \
            (sum(word_dict.get(text)) < THRESHOLD_TOTAL) or \
            ((word_dict.get(text)[0]/sum(word_dict.get(text))) < THRESHOLD_PCT and \
            (word_dict.get(text)[1]/sum(word_dict.get(text))) < THRESHOLD_PCT):
            if word_dict.get(text) is None:
                unknown_words.append(text)
            elif sum(word_dict.get(text)) < THRESHOLD_TOTAL:
                uncountable_words.append(text)
            elif (word_dict.get(text)[0]/sum(word_dict.get(text))) < THRESHOLD_PCT and \
                (word_dict.get(text)[1]/sum(word_dict.get(text))) < THRESHOLD_PCT:
                ambiguous_words.append(text)

            text = input("Is that yes or no?")

        counts = word_dict.get(text)
        pos = counts[0] / (counts[0] + counts[1])
        if pos >= THRESHOLD_PCT:
            index = 0
        else:
            index = 1

        if len(unknown_words) > 0:
            for word in unknown_words:
                word_dict[word] = [0,0]
                (word_dict.get(word))[index] = 1
        if len(uncountable_words) > 0:
            for word in uncountable_words:
                (word_dict.get(word))[index] = (word_dict.get(word))[index] + 1
        if len(ambiguous_words) > 0:
            for word in ambiguous_words:
                (word_dict.get(word))[index] = (word_dict.get(word))[index] + 1

        return outcomes[index]
    elif 'input' in qtype: #judges for character data
        if qtype[2] == 'yes':
            replace_inpt(qtype[1], text)
        if len(qtype) == 4:
            scenes.get(qtype[3]).set_qtype(text)
        return outcomes[0]
    elif qtype == 'random': #controls randomly selected question options
        import random
        return random.choices(outcomes, text)[0]
    elif qtype == 'choice':
        while text.upper() not in outcomes:
            text = input('Be clearer! Which option do you pick?')
        return text.upper()
    else: #judges for text matching questions
        if isinstance(qtype, str) and (qtype.lower() in text.lower()):
            return outcomes[0]
        elif isinstance(qtype, list) and (text.lower() in qtype):
            return outcomes[0]
        else:
            return outcomes[1]

def replace_inpt(old, new):
    for key in scenes:
        scene = scenes.get(key)
        replace = scene.get_replace()
        
        if old in replace:
            question = scene.get_question()
            scene.set_question(question.replace(old, new))
            
            script = scene.get_script()
            new_script = script
            for i in range(len(script)):
                new_script[i] = script[i].replace(old, new)
            scene.set_script(new_script)

def main():
    next = 'INTRO'
    while next != 'END':
        next = (scenes.get(next)).run_scene()
    for line in endline:
        print(line)



# Reads in yes/no data from file.
import json
with open("yesno_data.json", "r") as infile:
    word_dict = json.load(infile)
infile.close()

# Reads in and processes scenes from file.
infile = open('holygrail_story.txt', 'r', encoding='utf-8')
scenes_list = infile.read().split('##')
scenes = {}
for i in range(1, len(scenes_list) - 1):
    lines = scenes_list[i].rstrip().split('\n')
    key = lines.pop(0)
    replace = lines.pop(0)
    outcome = lines.pop().split(':')
    qtype = lines.pop()
    if ',' in qtype:
        qtype = qtype.split(',')
    question = lines.pop()
    scene_data = Scene(lines, qtype, question, outcome, replace)
    scenes[key] = scene_data
endline = (scenes_list[len(scenes_list) - 1].split('\n'))[1:]
infile.close()

# Creates player character and runs program.
main()
    
# Writes new yes/no data to file.
with open("yesno_data.json", "w") as outfile:
    json.dump(word_dict, outfile, indent=4)
outfile.close()
