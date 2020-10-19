import numpy as np
import copy
from queue import PriorityQueue
import time
import random

class node:
    def __init__(self, state, target, depth, w_g=0., father=None):
        pass

    def cal_dis(self):
        pass

    def cal_cost(self):
        pass

    def __lt__(self, other):
        pass

class solver:
    def __init__(self, init_state, target_state, w_g=0.):
        pass

    def set_state(self, init_state, target_state):
        pass

    def set_w_g(self, w_g):
        pass

    def move(self, current_state):
        pass

    def solve(self):
        pass

    def reverse(self, end_node):
        pass

    def is_sovable_33(self, ini, tar):
        pass

    @staticmethod
    def get_state_id(state):
        pass


def get_random_init(m, n, steps):
    pass

