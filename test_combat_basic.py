import pytest
from combat_basic import *
from support_types import *

def GenerateAttackRoles(testObject, NUMBER_OF_ROLES):
    result = {}
    for x in range(NUMBER_OF_ROLES):
        raw, atk = testObject.RoleAttack()
        if atk in result:
            result[atk] += 1
        else:
            result[atk] = 1
    return result

def TestAttackRoleRange(roles, dmg_mod):
    for atk in roles:
        assert(atk <= 20 + dmg_mod and atk >= dmg_mod + 1)

def TestAttackRoleDistribution(roles, dmg_mod, NUMBER_OF_ROLES):
    EXPECTED_COUNT_FOR_EACH_VALUE = NUMBER_OF_ROLES / 20  
    min_count = 10000000000000
    max_count = -1
    for x in range(dmg_mod + 1, 20 + dmg_mod + 1):
        val = roles[x]
        if val < min_count:
            min_count = val
        if val > max_count:
            max_count = val 
    assert(max_count <= EXPECTED_COUNT_FOR_EACH_VALUE * 1.10)
    assert(min_count >= EXPECTED_COUNT_FOR_EACH_VALUE * 0.90)

def TestRoleAttack(dmg_mod):
    testObject = combat_basic(dmg_mod, [])
      
    NUMBER_OF_ROLES = 20000 
    roles = GenerateAttackRoles(testObject, NUMBER_OF_ROLES)
    TestAttackRoleRange(roles, dmg_mod)
    TestAttackRoleDistribution(roles, dmg_mod, NUMBER_OF_ROLES)

def GenerateDamageRoles(testobject, NUMBER_OF_ROLES):
    results = []
    for x in range(NUMBER_OF_ROLES):
        results.append(testobject.RoleDamage())
    return results

def TestRoleDamageRange(results, damage_list):
    for role in results:
        for dmg_type in damage_list:
            aResult = role[dmg_type.name]
            assert(None != aResult)
            assert(aResult >= dmg_type.min and aResult <= dmg_type.max)

def BuildDamageRoleDistribution(results, damage_type):
    distribution = {}
    for role in results:
        value = role[damage_type.name]
        if value in distribution:
            distribution[value] += 1
        else:
            distribution[value] = 1
    return distribution

def TestDamageRoleDistributionForType(distribution, dmg_type, NUMBER_OF_ROLES):
    dmg_range = dmg_type.max - dmg_type.min + 1
    expected_count = NUMBER_OF_ROLES / dmg_range 
    
    min_count = 10000000000000
    max_count = -1
    for x in range(dmg_type.min, dmg_type.max + 1):
        val = distribution[x]
        if val < min_count:
            min_count = val
        if val > max_count:
            max_count = val 
    assert(max_count <= expected_count * 1.10)
    assert(min_count >= expected_count * 0.90)


def TestDamageRoleDistribution(results, damage_list, NUMBER_OF_ROLES):
   for dmg_type in damage_list:
       distribution = BuildDamageRoleDistribution(results, dmg_type)
       TestDamageRoleDistributionForType(distribution, dmg_type, NUMBER_OF_ROLES)

class ListAttackRoler():
    def __init__(self, attack_list, damage_list):
        self.__attack_list = attack_list
        self.__attack_index = 0
        self.__damage_list = damage_list
        self.__damage_index = 0
    
    def RoleDamage(self, min, max):
        result = self.__damage_list[self.__damage_index]
        self.__damage_index += 1
        if self.__damage_index == len(self.__damage_list):
            self.__damage_index = 0
        return result

    def RoleAttack(self):
        result = self.__attack_list[self.__attack_index]
        self.__attack_index += 1
        if self.__attack_index == len(self.__attack_list):
            self.__attack_index = 0
        return result

class TestClass(object):
    def test_RoleAttackZero(self):
        TestRoleAttack(0)
    
    def test_RoleAttackFive(self):
        TestRoleAttack(5)
    
    def test_RoleAttackFiveHundred(self):
        TestRoleAttack(500)

    def test_RoleDamage(self):
        damage_list = []
        damage_list.append(DamageRange('slashing', 1,6,0))
        damage_list.append(DamageRange('bashing', 2,12,0))
        damage_list.append(DamageRange('burning', 31,41,0))
        testObject = combat_basic(0, damage_list)

        NUMBER_OF_ROLES = 20000
        results = GenerateDamageRoles(testObject, NUMBER_OF_ROLES)
        TestRoleDamageRange(results, damage_list)
        TestDamageRoleDistribution(results, damage_list, NUMBER_OF_ROLES)
    
    def test_RoleCombinedAttack_hit(self):
        damage_list = []
        damage_list.append(DamageRange('slashing', 1,11,5))
        damage_list.append(DamageRange('bashing', 2,12,10))
        damage_list.append(DamageRange('burning', 3,15,15))

        test_random_function = ListAttackRoler([10], [10])

        testObject = combat_basic(5, damage_list, test_random_function)
        result = testObject.RoleCombinedAttack(15, AttackModifier.NONE)
        assert(None != result)
        assert(15 == result.role_result)
        assert(result.damage['slashing'] == 15)
        assert(result.damage['bashing'] == 20)
        assert(result.damage['burning'] == 25)

    def test_RoleCombinedAttack_mis(self):
        damage_list = []

        test_random_function = ListAttackRoler([5],[5])

        testObject = combat_basic(5, damage_list, test_random_function)
        result = testObject.RoleCombinedAttack(15, AttackModifier.NONE)
        assert(None != result)
        assert(10 == result.role_result)
        assert(None == result.damage)
    
    def test_RoleCombinedAttack_no_adv(self):
        damage_list = []

        test_random_function = ListAttackRoler([5, 10], [10])

        testObject = combat_basic(0, damage_list, test_random_function)
        result = testObject.RoleCombinedAttack(15, AttackModifier.NONE)
        assert(None != result)
        assert(5 == result.role_result)
    
    def test_RoleCombinedAttack_adv_high_second(self):
        damage_list = []

        test_random_function = ListAttackRoler([5, 10], [10])

        testObject = combat_basic(0, damage_list, test_random_function)
        result = testObject.RoleCombinedAttack(15, AttackModifier.ADVANTAGE)
        assert(None != result)
        assert(10 == result.role_result)
    
    def test_RoleCombinedAttack_adv_high_first(self):
        damage_list = []

        test_random_function = ListAttackRoler([10, 5], [10])

        testObject = combat_basic(0, damage_list, test_random_function)
        result = testObject.RoleCombinedAttack(15, AttackModifier.ADVANTAGE)
        assert(None != result)
        assert(10 == result.role_result)
    
    def test_RoleCombinedAttack_disadv_high_first(self):
        damage_list = []

        test_random_function = ListAttackRoler([10, 5], [10])

        testObject = combat_basic(0, damage_list, test_random_function)
        result = testObject.RoleCombinedAttack(15, AttackModifier.DISADVANTAGE)
        assert(None != result)
        assert(5 == result.role_result)
    
    def test_RoleCombinedAttack_disadv_high_second(self):
        damage_list = []

        test_random_function = ListAttackRoler([5, 10], [10])

        testObject = combat_basic(0, damage_list, test_random_function)
        result = testObject.RoleCombinedAttack(15, AttackModifier.DISADVANTAGE)
        assert(None != result)
        assert(5 == result.role_result)
    
    def test_RoleCombinedAttack_crit(self):
        damage_list = []
        damage_list.append(DamageRange('slashing', 1,11,5))

        test_random_function = ListAttackRoler([20, 10], [5, 4])

        testObject = combat_basic(5, damage_list, test_random_function)
        result = testObject.RoleCombinedAttack(15, AttackModifier.NONE)
        assert(None != result)
        assert(CritResult.CRIT_SUCCESS == result.crit)
        assert(14 == result.damage['slashing'])
    
    def test_RoleCombinedAttack_crit_fail(self):
        damage_list = []
        damage_list.append(DamageRange('slashing', 1,11,5))

        test_random_function = ListAttackRoler([1, 10], [5, 4])

        testObject = combat_basic(5, damage_list, test_random_function)
        result = testObject.RoleCombinedAttack(15, AttackModifier.NONE)
        assert(None != result)
        assert(CritResult.CRIT_FAIL == result.crit)