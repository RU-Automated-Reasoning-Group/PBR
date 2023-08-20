import torch
import torch.nn as nn

from karel.dsl import *
from karel.robot import KarelRobot


ACTION_INDEX = [0, 1, 2, 3, 4]
ACTION_NAME = [
    'move',
    'turn_right',
    'turn_left',
    'pick_marker',
    'put_marker'
]


# make your life easier first
class SimpleProgram:
    def __init__(self):
        self.cond_while = k_cond(negation=False, cond=k_cond_without_not('front_is_clear'))
        self.cond_if = k_cond(negation=False, cond=k_cond_without_not('markers_present'))
        self.stmts_while = []
        self.stmts_if = []

    def append_while(self, action):
        assert isinstance(action, k_action)
        self.stmts_while.append(action)

    def append_if(self, action):
        assert isinstance(action, k_action)
        self.stmts_if.append(action)

    # NOTE: there is no restart if

    def restart_while(self, robot):
        
        r = 0.0
        
        while robot.execute_single_cond(self.cond_while) and not robot.no_fuel():
            
            if robot.execute_single_cond(self.cond_if) and not robot.no_fuel():
                for s in self.stmts_if:
                    if not robot.no_fuel():
                        r = robot.execute_single_action(s)
                        if r == 1:
                            return r

            for s in self.stmts_while:
                if not robot.no_fuel():
                    r = robot.execute_single_action(s)
                    if r == 1:
                        return r

        return r

    def print(self, prefix=''):

        p_str = prefix + 'DEF run (m WHILE (front_is_clear) (w '
        
        # also, print lazily
        if self.stmts_if:
            p_str += 'IF (markers_present) (i '
            for s in self.stmts_if:
                p_str += str(s)
                p_str += ' '
            p_str += 'i) '

        for s in self.stmts_while:
            p_str += str(s)
            p_str += ' '
        p_str += 'w)'
        p_str += ' m)'
        
        print(p_str)