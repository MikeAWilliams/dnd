import random
from datetime import datetime
from support_types import *

random.seed(datetime.now())

class FairAttackRoler():
    def RoleDamage(self, min, max):
        return random.randint(min, max)
    def RoleAttack(self):
        return random.randint(1,20)


class combat_basic():
    def __init__(self, atk_mod, damage_ranges, attack_roler = FairAttackRoler()):
        self.__atack_mod = atk_mod
        self.__damage_ranges = damage_ranges
        self.__attack_roler = attack_roler
    
    def RoleAttack(self):
        d20 = self.__attack_roler.RoleAttack() 
        return (d20, d20 + self.__atack_mod)
    
    def RoleDamage(self):
        result = {}
        for dmg_type in self.__damage_ranges:
            result[dmg_type.name] = self.__attack_roler.RoleDamage(dmg_type.min, dmg_type.max) + dmg_type.const

        return result
    
    def RoleDamageCritSupliment(self):
        result = {}
        for dmg_type in self.__damage_ranges:
            result[dmg_type.name] = self.__attack_roler.RoleDamage(dmg_type.min, dmg_type.max)

        return result
    
    def RoleDamageCrit(self):
        result = self.RoleDamage()
        supliment = self.RoleDamageCritSupliment()
        for dmg_type in self.__damage_ranges:
            result[dmg_type.name] += supliment[dmg_type.name]
        return result
    
    def RoleCombinedAttack(self, ac, attack_modifier):
        raw1, attack_role1 = self.RoleAttack()
        raw2, attack_role2 = self.RoleAttack()
       
        raw = raw1
        attack_role = attack_role1
        if AttackModifier.ADVANTAGE == attack_modifier:
            attack_role = max(attack_role1, attack_role2)
            raw = max(raw1, raw2)
        if AttackModifier.DISADVANTAGE == attack_modifier:
            attack_role = min(attack_role1, attack_role2)
            raw = min(raw1, raw1)

        if 20 == raw:
            return AttackResult(CritResult.CRIT_SUCCESS, attack_role, self.RoleDamageCrit())
        
        if 1 == raw:
            return AttackResult(CritResult.CRIT_FAIL, attack_role, None)

        if attack_role >= ac:
            return AttackResult(CritResult.NONE, attack_role, self.RoleDamage())
        return AttackResult(CritResult.NONE, attack_role, None)


      