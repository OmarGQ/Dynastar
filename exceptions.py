# -*- coding: utf-8 -*-
"""
Created on Thu May 25 10:40:43 2023

@author: kiddra
"""

class Impossible(Exception):
    """Exception raised when an action is impossible to be performed.

    The reason is given as the exception message.
    """
    
class QuitWithoutSaving(SystemExit):
    """Can be raised to exit the game without automatically saving."""