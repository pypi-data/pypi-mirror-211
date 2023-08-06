# %%
# Likely needed imports
import numpy as np




# First question check
def elements_check_1(func):
    assert func('sky') == 3, 'Error on sky input'
    assert func('life') == 1, 'Error on life input'
    assert func('energy') == 1, 'Error on energy input'
    assert func('spirit') == 1, 'Error on spirit input'
    print('Correct, good job!')




# Second question check
def elements_check_2(func):
    assert func('sky', 'sky') == 3, 'Error on sky input' # Sky always gets the bonus
    assert func('sky', 'life') == 3, 'Error on sky input'
    assert func('sky', 'energy') == 3, 'Error on sky input'
    assert func('sky', 'spirit') == 3, 'Error on sky input'
    assert func('life', 'sky') == 1, 'Error on life input'
    assert func('life', 'life') == 1, 'Error on life input'
    assert func('life', 'energy') == 1, 'Error on life input'
    assert func('life', 'spirit') == 2, 'Error on life input' # Life against spirit
    assert func('energy', 'sky') == 1, 'Error on energy input'
    assert func('energy', 'life') == 2, 'Error on energy input' # Energy against life
    assert func('energy', 'energy') == 1, 'Error on energy input'
    assert func('energy', 'spirit') == 1, 'Error on energy input'
    assert func('spirit', 'sky') == 1, 'Error on spirit input'
    assert func('spirit', 'life') == 1, 'Error on spirit input'
    assert func('spirit', 'energy') == 2, 'Error on spirit input' # Spirit against energy
    assert func('spirit', 'spirit') == 1, 'Error on spirit input'
    print('Correct, good job!')




# Third question check
def elements_check_3(func):

    # The correct damage calculation
    def correct_calc(your_element, opponent_element, base_damage=3.145):

        if your_element == 'sky':
            dmg_mult = 3
        elif (your_element == 'spirit') and (opponent_element == 'energy'):
            dmg_mult = 2
        elif (your_element == 'energy') and (opponent_element == 'life'):
            dmg_mult = 2
        elif (your_element == 'life') and (opponent_element == 'spirit'):
            dmg_mult = 2
        else:
            dmg_mult = 1

        final_damage = base_damage * dmg_mult
            
        return round(final_damage, 1)

    # Iterate over all the element combos, asserting using the same number (should get all meaningful mistakes)
    l_e = ['sky', 'life', 'energy', 'spirit']
    for your_e in l_e:
        for opponent_e in l_e:
            assert func(your_e, opponent_e) == correct_calc(your_e, opponent_e, 3.145), f'Error on {your_e} vs {opponent_e}.'

    print('Correct, good job!')
