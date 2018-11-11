"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
Note this program will only work on http://www.codeskulptor.org/
"""

# Used to increase the timeout, if necessary
#import user45_ez2W1rKafq_3 as score_test
import codeskulptor
codeskulptor.set_timeout(20)

DICE = (1,2,3,4,5,6)
def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    roll = {}
    
    for dice in hand:
        roll[dice] = roll.get(dice, 0) + dice
        
    max_dice = None
    max_val = 0
    
    for dice, val in roll.items():
        if max_dice == None:
            max_dice = dice
            max_val = val
        elif val > max_val:
            max_dice = dice
            max_val = val
            
    return max_val


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    die = [num + 1 for num in range(num_die_sides)]
    outcomes = gen_all_sequences(die, num_free_dice)
    
    total = 0
    n_cases = 0
    for num in outcomes:
        hand = held_dice + num
        total = total + score(hand)
        n_cases = n_cases + 1
    
    return total / float(n_cases)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
   
    power_set = set([()])
    
    for roll in hand:
        temp_set = set(power_set)
        for subset in power_set:
            new_subset = list(subset)
            new_subset.append(roll)
            temp_set.add(tuple(new_subset))
        power_set = temp_set
    
    return power_set

            
def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    
    all_holds = gen_all_holds(hand)
    hand_length = len(hand)

    max_val = 0
    max_held = None
    
    for held_dice in all_holds:
        free_dice = hand_length - len(held_dice) 
        held_val = expected_value(held_dice, num_die_sides, free_dice)
        
        if(held_val >= max_val):
            max_val = held_val
            max_held = held_dice
  
    return (max_val, max_held)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
#score_test.run_suite(score) 
