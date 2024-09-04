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
    CPR_BOARD = "cpr_board"
    VENTILATOR = "ventilator"
    CPR_STOOL = "cpr_stool"
    # syringe in different states
    SYRINGE = "syringe"
    # SYRINGE_TOPRIGHT = "syringe_topright"
    # aeds have very different images, so need different enums
    # AED_ON_TABLE = "aed_on_table"
    # AED_ON_HCW = "aed_on_hcw"
    # # AED_ON_PATIENT = ""
    PUMP = "pump"
    PATIENT = "patient"
    

class Player(Enum):
    ROBOT = "robot"
    NURSE = "nurse"
    R3_FRONT = "r3_front"

class Station(Enum):
    BOARD = "board"
    STOVE = "stove"
    TABLE = "table"
    PATIENT = "patient"
    PATIENT_LEGS = "patient_legs"
    PATIENT_BED_STATION = "patient_bed_station"
    HOSP_CART_LEFT = "hospital_cart_left"
    HOSP_CART_RIGHT = "hospital_cart_right"

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