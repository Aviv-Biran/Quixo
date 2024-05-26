import pygame
from Constants import *
import random

class Random_Agent:

    def __init__(self, player: int, env = None) -> None:
        self.player = player
        self.env = env

    def get_player_number(self):
        return self.player
    
    def get_Action(self, state, train = False, events = None):
        actions = self.env.legal_actions(state)
        return random.choice(actions)