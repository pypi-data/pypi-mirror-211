import numpy as np
import random
def randomint(start, end):
    return np.random.randint(start, end)
def PercentChance(percent):
    return random.uniform(0,100) < percent

def Sort2(sub_li):
    return(sorted(sub_li, key = lambda x: str(x)))  
