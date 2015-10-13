from collections import namedtuple
from random import random

DEFECT = 'defect'
COOPERATE = 'cooperate'

State = namedtuple('state', ['my_previous_move', 'opponents_previous_move'])
   

def opposite_move(move):
    if move == DEFECT:
        return COOPERATE
    else:
        return DEFECT


def score(my_move, opponents_move):
    if my_move == DEFECT and opponents_move == DEFECT:
        return 1.
    if my_move == COOPERATE and opponents_move == DEFECT:
        return 0.
    if my_move == DEFECT and opponents_move == COOPERATE:
        return 5.
    if my_move == COOPERATE and opponents_move == COOPERATE:
        return 3.

class Pavlov(object):

    def move(self, state):
        if state is None:
            return COOPERATE

        my_move = state.my_previous_move
        opponents_move = state.opponents_previous_move

        if score(my_move, opponents_move) in (1, 0):
            return opposite_move(my_move)
        else:
            return my_move

class TFT(object):

    def move(self, state):
        if state == None:
            return COOPERATE
        return state.opponents_previous_move


class Random(object):

    def __init__(self, p=0.5):
        self.p = p 

    def move(self, state):
        return COOPERATE if self.p <= random() else DEFECT


class AD(object):

    def move(self, state):
        return DEFECT


class AC(object):

    def move(self, state):
        return COOPERATE


class Extortion(object):

    def __init__(self, chi=10):
        self.chi = float(chi)

    def move(self, state):
        if state == None:
            return COOPERATE

        my_move = state.my_previous_move
        opponents_move = state.opponents_previous_move

        if my_move == opponents_move == COOPERATE:
            return COOPERATE if random() < (1. - (2. * self.chi - 2.) / (4. * self.chi + 1.)) else DEFECT
        if my_move == opponents_move == DEFECT:
            return DEFECT
        if my_move == DEFECT and opponents_move == COOPERATE:
            return COOPERATE if random() < ((self.chi + 4.) / (4. * self.chi + 1.)) else DEFECT
        if my_move == COOPERATE and opponents_move == DEFECT:
            return DEFECT

def match(p1, p2, state1=None, state2=None):
    move1, move2 = p1.move(state1), p2.move(state2)
    return (score(move1, move2), State(move1, move2)), \
           (score(move2, move1), State(move2, move1))


def iterated_matches(p1, p2, n_matches=100000):
    state1, state2 = None, None
    total_score1, total_score2 = 0., 0.
    total_matches_thus_far = 0

    for _ in range(n_matches):
        (s1, state1), (s2, state2) = match(p1, p2, state1, state2)
        total_score1 += s1
        total_score2 += s2
        total_matches_thus_far += 1
        #print state1, state2

        if total_matches_thus_far % 100 == 0:
            print
            print "Round: %d" % total_matches_thus_far
            print total_score1 / total_matches_thus_far
            print total_score2 / total_matches_thus_far
            print (total_score1 / total_matches_thus_far - 1.) / (total_score2 / total_matches_thus_far - 1.)

    return total_score1, total_score2




if __name__=='__main__':
    p1 = Extortion()
    p2 = Pavlov()
    iterated_matches(p1, p2)
