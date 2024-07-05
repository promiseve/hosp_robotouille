from enum import Enum

class Station(Enum):
    PATIENT = "patient"
    TABLE = "table"
    AED_STATION = "aed_station"
    CPR_STATION = "cpr_station"
    VENTILATION_STATION = "ventilation_station"

class Item(Enum):
    AED = "aed"
    CPR_KIT = "cpr_kit"
    VENTILATOR = "ventilator"
    MEDICINE = "medicine"
    PULSE_CHECKER = "pulsechecker"

class Player(Enum):
    ROBOT = "robot"
    NURSE = "nurse"

class Predicate(Enum):
    IS_PATIENT = "ispatient"
    IS_TREATABLE = "istreatable"
    IS_TREATED = "istreated"
    IS_DEFIBRILLATED = "isdefibrillated"
    IS_RESUSCITATED = "isresuscitated"
    IS_VENTILATED = "isventilated"
    IS_ROBOT = "isrobot"
    IS_NURSE = "isnurse"
    IS_AED = "isAED"
    IS_CPR_KIT = "isCPR_kit"
    IS_USABLE_FOR_CPR = "isusableforcpr"
    IS_VENTILATOR = "isventilator"
    IS_USABLE_FOR_VENTILATION = "isusableforventilation"
    IS_INGESTABLE = "isingestable"
    IS_INGESTED = "isingested"
    LOC = "loc"
    AT = "at"
    NOTHING = "nothing"
    EMPTY = "empty"
    ON = "on"
    VACANT = "vacant"
    CLEAR = "clear"
    ATOP = "atop"
    HAS = "has"
    SELECTED = "selected"
    CAN_GIVE_MEDICINE = "cangivemedicine"
    CAN_GIVE_AED = "cangiveAED"
    CAN_GIVE_CPR = "cangiveCPR"
    CAN_GIVE_VENT = "cangivevent"
    CAN_MOVE_ITEM = "canmoveitem"
    CAN_MOVE = "canmove"

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