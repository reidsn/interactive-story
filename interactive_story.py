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
        initial = text
        while (text not in yes) and (text not in no):
            text = input('Be clearer! Is that yes or no?')
        if text in yes:
            if text != initial:
                yes.append(initial)
            return outcomes[0]
        else:
            if text != initial:
                no.append(initial)
            return outcomes[1]
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



# Reads in yes/no data lists from file.
infile = open('answer_lists.txt', 'r', encoding='utf-8')
answer_lists = infile.readlines()
yes = answer_lists[0].strip().split(',')
no = answer_lists[1].strip().split(',')
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
yes_list = ''
no_list = ''
for i in range(len(yes)):
    if i > 0:
        yes[i] = ',' + yes[i]
    yes_list = yes_list + yes[i]
for i in range(len(no)):
    if i > 0:
        no[i] = ',' + no[i]
    no_list = no_list + no[i]

outfile = open('answer_lists.txt', 'w', encoding='utf=8')
outfile.write(yes_list + '\n' + no_list)
outfile.close()
