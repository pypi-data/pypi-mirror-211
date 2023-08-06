from enum import Enum

HTTP_CLIENT_TIMEOUT: float = 4.0


sentinel = object()


class EntryConf(int, Enum):
    NM = 1
    NEW = 2
    EXACT = 3
    JUNK = 4
    HA = 5
    DET = 6
    REINIT = 7
    NF = 8


class EntryMood(str, Enum):
    ANGRY = "angry"
    FEAR = "fear"
    NEUTRAL = "neutral"
    SAD = "sad"
    DISGUST = "disgust"
    HAPPY = "happy"
    SURPRISE = "surprise"


class Sex(int, Enum):
    MALE = 0
    FEMALE = 1
