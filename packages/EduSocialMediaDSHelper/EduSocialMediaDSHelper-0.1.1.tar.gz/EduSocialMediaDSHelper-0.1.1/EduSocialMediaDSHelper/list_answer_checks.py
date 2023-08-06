# %%
# Likely needed imports
import numpy as np




# %%
# Function to return the big numbers list
def create_big_numbers_list():
    big_numbers_list = [i for i in range(1000)]
    big_numbers_list[90] = 900
    big_numbers_list[345] = 200
    big_numbers_list[505] = 606
    big_numbers_list[786] = 323
    return big_numbers_list




# %%
# Function to return the strange phobias list
def create_strange_phobias_list():
    strange_phobias_list = [
        'Arachibutyrophobia'
        , 'Nomophobia'
        , 'Arithmophobia'
        , 'Plutophobia'
        , 'Xanthophobia'
        , 'Ablutophobia'
        , 'Octophobia'
        , 'Optophobia'
        , 'Globophobia'
        , 'Hippopotomonstrosesquippedaliophobia'
        , 'Ephebiphobia'
        , 'Omphalophobia'
        , 'Linonophobia'
        , 'Pogonophobia'
        , 'Chaetophobia'
        , 'Vestiphobia'
        , 'Ergophobia'
        , 'Decidophobia'
        , 'Eisoptrophobia'
        , 'Deipnophobia'
        , 'Phobophobia'
        , 'Nomophobia'
        ]
    return strange_phobias_list




# %%
# The main set of function checks separated by number
# Check the sum of the big numbers list
def list_check_1(x):
    if x == sum(create_big_numbers_list()):
        print('True')
    else:
        print('False')

def list_check_2(x):
    if x == min(create_big_numbers_list()):
        print('True')
    else:
        print('False')

def list_check_3(x):
    if x == max(create_big_numbers_list()):
        print('True')
    else:
        print('False')

def list_check_4(x):
    if x == len(create_big_numbers_list()):
        print('True')
    else:
        print('False')

def list_check_5(x):
    if x == sum(create_big_numbers_list())/len(create_big_numbers_list()):
        print('True')
    else:
        print('False')

def list_check_6(x):
    if x == create_strange_phobias_list()[0]:
        print('True')
    else:
        print('False')

def list_check_7(x):
    if x == create_strange_phobias_list().index('Globophobia'):
        print('True')
    else:
        print('False')

def list_check_8(x):
    if x == create_big_numbers_list()[0:10]:
        print('True')
    else:
        print('False')

def list_check_9(x):
    if x == ['Ablutophobia', 'Arachibutyrophobia', 'Arithmophobia']:
        print('True')
    else:
        print('False')

def list_check_10(x):
    if x == [0, 2, 4]:
        print('True')
    else:
        print('False')

def list_check_11(x):
    if x == 'Nomophobia':
        print('True')
    else:
        print('False')

def list_check_12(x):
    if x == False:
        print('Correct!')
    else:
        print('Nope!')




# %%
# Function to check the bonus
def list_check_bonus(bad_idxs, bad_values):
    bad_idxs_list = [90, 345, 505, 786]
    bad_values_list = [900, 200, 606, 323]
    if (bad_idxs == bad_idxs_list) and (bad_values == bad_values_list):
        print('True')
    else:
        print('False')