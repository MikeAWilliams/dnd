import collections
from enum import Enum

DamageRange = collections.namedtuple('DamageRange', ['name', 'min', 'max', 'const'])
AttackResult = collections.namedtuple('AttackResult', ['crit', 'role_result', 'damage'])

class AttackModifier(Enum):
    NONE = 0
    ADVANTAGE = 1
    DISADVANTAGE = 2

class CritResult(Enum):
    NONE = 0
    CRIT_SUCCESS = 1
    CRIT_FAIL = 2