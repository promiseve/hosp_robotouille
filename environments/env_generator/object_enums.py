from enum import Enum

class Item(Enum):
    BOTTOMBUN = "bottombun"
    LETTUCE = "lettuce"
    PATTY = "patty"
    TOPBUN = "topbun"
    BREAD = "bread"
    CHEESE = "cheese"
    TOMATO = "tomato"
    ONION = "onion"
    CHICKEN = "chicken"
    MEDICINE = "medicine"
    PULSE_CHECKER = "pulse_checker-equipment"
    AED = "aed"
    CPR_KIT = "cpr_kit"
    VENTILATOR = "ventilator"
    CPR_BOARD = "cpr_board"
    CPR_STOOL = "cpr_stool"
    CPR_VENT = "cpr_vent"
    

class Player(Enum):
    ROBOT = "robot"
    NURSE = "nurse"

class Station(Enum):
    BOARD = "board"
    STOVE = "stove"
    TABLE = "table"
    PATIENT = "patient"
    PATIENT_LEGS = "patient_legs"

def str_to_typed_enum(s):
    """
    Attempts to convert a string into any of the typed enums.
    Args:
        s (str): String to convert.
    
    Raises:
        ValueError: If the string cannot be converted into any of the typed enums.
    
    Returns:
        typed_enum (Enum): Enum of the string.
    """
    for typed_enum in [Item, Player, Station]:
        try:
            return typed_enum(s)
        except ValueError:
            pass
    raise ValueError(f"Could not convert {s} into any of the typed enums.")