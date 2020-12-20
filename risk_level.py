from enum import Enum


class RiskLevel(Enum):
    NO_RISK = 0
    UNIMPORTANT_RISK = 1
    VERY_LITTLE_RISK = 2
    LITTLE_RISK = 3
    VERY_LOW_RISK = 4
    LOW_RISK = 5
    MEDIUM_RISK = 6
    LARGE_RISK = 7
    HIGH_RISK = 8
    VERY_DANGEROUS = 9