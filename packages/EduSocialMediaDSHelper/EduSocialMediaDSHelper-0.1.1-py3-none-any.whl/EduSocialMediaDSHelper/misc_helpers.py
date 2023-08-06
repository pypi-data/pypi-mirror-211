# %%
# Likely imports for all functions below
import numpy as np
import matplotlib.pyplot as plt
import time



# %%
# Example Likert distributions with various centers and outlier capability
# Returns an array of ints of a given size
def ExLikertDist(size=1000, center=None, outlier=False):

    l_choices = [1, 2, 3, 4, 5]

    if center == 'left':
        l_probs = [0.40, 0.35, 0.15, 0.05, 0.05]
    elif center == 'right':
        l_probs = [0.05, 0.05, 0.15, 0.35, 0.40]
    elif center == 'bimodal':
        l_probs = [0.35, 0.125, 0.05, 0.125, 0.35]
    elif center == 'center':
        l_probs = [0.05, 0.15, 0.60, 0.15, 0.05]
    else:
        l_probs = [0.2, 0.2, 0.2, 0.2, 0.2]

    a = np.random.choice(l_choices, p=l_probs, size=size)

    if outlier:
        a = np.concatenate([a, [8]*int(round(size/100))])

    return a




# %%
# Magic eight ball class for object-oriented activity
class MagicEightBall():

    def __init__(self):

        self.l_choices = [
            'As I see it, yes'
            , 'Ask again later'
            , 'Better not tell you now'
            , 'Cannot predict now'
            , 'Concentrate and ask again'
            , 'Dont count on it'
            , 'It is certain'
            , 'It is decidedly so'
            , 'Most likely'
            , 'What do you think'
            , 'My reply is no'
            , 'My sources say no'
            , 'Why on Earth would you trust the answers of a pool ball?'
            , 'Outlook good'
            , 'Outlook not so good'
            , 'Reply hazy try again'
            , 'Leave me alone, I am tired'
            , 'Signs point to yes'
            , 'Very doubtful'
            , 'Without a doubt'
            , 'Yes'
            , 'Yes, definitely'
            , 'You may rely on it'
            , '...I hate this job. Why do I answer questions all day? Geeze... OH! Sorry there. AHEM, "Your answer is yes"'
            ]

        self.shape = 'round'
        self.color = 'black'
        self.number = 8
        self.size = 'Eh probably like a few inches in diameter?'

    def shake(self):
        print('Why are you shaking me?! Ask me a question')
    
    def answer(self, some_string='Does not matter really'):
        print(np.random.choice(self.l_choices))




# %%
# RobTheRobot class used for object-oriented activity
class RobTheRobot():

    def __init__(self, color=None):

        # Rob may wear different things when he is red
        if np.random.choice([1, 2]) == 1:
            self.red_headgear = 'sombrero'
            self.red_bodygear = 'tuxedo'
        else:
            self.red_headgear = 'snorkel'
            self.red_bodygear = 'cape'           

        # Basic setup
        self.l_all_colors = [
            'red'
            , 'blue'
            , 'green'
            , 'yellow'
            , 'purple'
        ]

        self.d_wearables = {
            'red': {'headgear': self.red_headgear, 'bodygear': self.red_bodygear}
            , 'blue': {'headgear': 'headphones', 'bodygear': 'nothing'}
            , 'green': {'headgear': 'nothing', 'bodygear': 'armor'}
            , 'yellow': {'headgear': 'sombrero', 'bodygear': 'nothing'}
            , 'purple': {'headgear': 'headphones', 'bodygear': 'tuxedo'}
            , 'orange': {'headgear': 'snorkel', 'bodygear': 'cape'}
        }

        # Allows students to specifically pass a color, if not randomly pick one and finish setup
        if color:
            self.color = color
        else:
            self.color = np.random.choice(self.l_all_colors)

        self.headgear = self.d_wearables[self.color]['headgear']
        self.bodygear = self.d_wearables[self.color]['bodygear']

    # Students should provide a function with two arguments (headgear and bodygear) that can guess Rob's color
    # This function checks if the provided function is correct
    def check_answer(self, myfunc=None):

        correct = False

        if myfunc:

            for check_color in self.l_all_colors:
                check_headgear = self.d_wearables[check_color]['headgear']
                check_bodygear = self.d_wearables[check_color]['bodygear']
                answer_color = myfunc(check_headgear, check_bodygear)
                if answer_color != check_color:
                    print(f'Sorry, something went wrong on the color {check_color}.')
                    break
                elif check_color == self.l_all_colors[-1]:
                    correct = True

            if correct:
                print('Awesome, you did it!')

        else:
            print('Provide a function to check your answer!')

        # Note a simple reasonable answer might look like the below
        # def find_robot_color(headgear, bodygear):

        #     if headgear == 'nothing':
        #         color = 'green'
        #     elif bodygear == 'nothing' and headgear == 'headphones':
        #         color = 'blue'
        #     elif bodygear == 'tuxedo' and headgear == 'headphones':
        #         color = 'purple'
        #     elif bodygear == 'nothing' and headgear == 'sombrero':
        #         color = 'yellow'
        #     else:
        #         color = 'red'
            
        #     return color




# %%
# Timer for the function creation activity
def time_me(n_seconds=45):
    start_t = time.time()
    while True:
        time.sleep(1)
        elapsed_seconds = round(time.time() - start_t)
        print('\r' + 'Seconds elapsed: ' + str(elapsed_seconds), end='')
        if elapsed_seconds >= n_seconds:
            print()
            break




# %%
# Check answer function for the pandas sphinx riddle
def riddle_of_the_sphinxes(answer):
    if answer == 3678:
        print('You grab the sphinx maked 640 and inspect it carefully. Upon flipping it over, you notice a secret compartment.')
        print('Inside is a small note with lattitude and longitude coordinates. Congrats! You are about to be rich.')
        print('\n')
        print('You have solved the riddle! For bonus points, come up with your own riddle! But you must show the work to prove that it works!')
    else:
        print('Sorry, no treasure here!')