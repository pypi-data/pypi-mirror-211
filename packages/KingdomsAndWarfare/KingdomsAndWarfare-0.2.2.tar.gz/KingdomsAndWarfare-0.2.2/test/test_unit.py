from copy import deepcopy
from pdb import set_trace

from pdb import set_trace

import pytest
from copy import deepcopy

from ..KingdomsAndWarfare.Traits.Trait import Trait
from ..KingdomsAndWarfare.Units.Artillery import Artillery
from ..KingdomsAndWarfare.Units.Cavalry import Cavalry
from ..KingdomsAndWarfare.Units.Infantry import Infantry
from ..KingdomsAndWarfare.Units.Unit import CannotLevelUpError
from ..KingdomsAndWarfare.Units.Unit import CannotUpgradeError
from ..KingdomsAndWarfare.Units.Unit import Unit
from ..KingdomsAndWarfare.Units.UnitFactory import unit_from_dict

# testing the unit class, not to be confused with unit tests...
# ... ok, these are unit tests, too, but still...
def test_unit():
    unit_name = "Splonks Infantry"
    unit_description = "Splonks with swords, mostly."
    splonks = Unit(unit_name, unit_description)

    assert splonks.name == unit_name
    assert splonks.description == unit_description

    magic_resistant = Trait("Magic Resistant", "this unit is resitant to magic")
    splonks.add_trait(magic_resistant)
    test_trait = splonks.traits[0]
    assert test_trait == magic_resistant


def test_levelup():
    splonks = Unit("Splonks Infantry", "Splonks with knives.")
    assert splonks.battles == 0
    assert splonks.experience == Unit.Experience.REGULAR
    splonks.battle()
    assert splonks.battles == 1
    assert splonks.experience == Unit.Experience.VETERAN
    splonks.battle()
    splonks.battle()
    splonks.battle()
    assert splonks.battles == 4
    assert splonks.experience == Unit.Experience.ELITE
    for index in range(4):
        splonks.battle()
    assert splonks.battles == 8
    assert splonks.experience == Unit.Experience.SUPER_ELITE
    with pytest.raises(CannotLevelUpError):
        splonks.level_up()

def test_level_up_undo():
    units = [Infantry("Goldfish Infantry", "Goldfish with lightsabers"), 
             Artillery("Gunslingers", "Slingers who throw guns"), 
             Cavalry("Rhino Cavalry", "Rhinos riding very large horses")]
    for unit in units:
        assert unit.experience == Unit.Experience.REGULAR
        my_clone = deepcopy(unit)
        unit.level_up()
        unit.level_up()
        unit.level_up()
        assert unit.experience == Unit.Experience.SUPER_ELITE
        unit.level_down()
        unit.level_down()
        unit.level_down()
        assert unit.experience == Unit.Experience.REGULAR
        assert my_clone == unit

def test_level_up_undo():
    units = [
        Infantry("Goldfish Infantry", "Goldfish with lightsabers"),
        Artillery("Gunslingers", "Slingers who throw guns"),
        Cavalry("Rhino Cavalry", "Rhinos riding very large horses"),
    ]
    for unit in units:
        assert unit.experience == Unit.Experience.REGULAR
        my_clone = deepcopy(unit)
        unit.level_up()
        unit.level_up()
        unit.level_up()
        assert unit.experience == Unit.Experience.SUPER_ELITE
        unit.level_down()
        unit.level_down()
        unit.level_down()
        assert unit.experience == Unit.Experience.REGULAR
        assert my_clone == unit


def test_levelup_levies():
    splonks = Unit("Splonks levies", "Splonk levies use pumpkins as balaclavas.")
    splonks.experience = Unit.Experience.LEVIES
    with pytest.raises(CannotLevelUpError):
        splonks.level_up()


def test_upgrade_infantry():
    infantry = Unit("Splonks Infantry", "Splonkitude")
    assert infantry.equipment == Unit.Equipment.LIGHT
    infantry.upgrade()
    assert infantry.equipment == Unit.Equipment.MEDIUM
    infantry.upgrade()
    assert infantry.equipment == Unit.Equipment.HEAVY
    infantry.upgrade()
    assert infantry.equipment == Unit.Equipment.SUPER_HEAVY
    with pytest.raises(CannotUpgradeError):
        infantry.upgrade()

def test_upgrade_undo():
    units = [Infantry("Creepy Puppets", "Puppets on magical strings."),
                Artillery("Fish People", "Fish people with squirtguns."),
                Cavalry("Sand People", "Riding Speeder bikes.")]
    for unit in units:
        my_clone = deepcopy(unit)
        assert unit.equipment == Unit.Equipment.LIGHT
        unit.upgrade()
        unit.upgrade()
        unit.upgrade()
        assert unit.equipment == Unit.Equipment.SUPER_HEAVY
        unit.downgrade()
        unit.downgrade()
        unit.downgrade()
        assert unit.equipment == Unit.Equipment.LIGHT
        assert unit == my_clone

def test_upgrade_undo():
    units = [
        Infantry("Creepy Puppets", "Puppets on magical strings."),
        Artillery("Fish People", "Fish people with squirtguns."),
        Cavalry("Sand People", "Riding Speeder bikes."),
    ]
    for unit in units:
        my_clone = deepcopy(unit)
        assert unit.equipment == Unit.Equipment.LIGHT
        unit.upgrade()
        unit.upgrade()
        unit.upgrade()
        assert unit.equipment == Unit.Equipment.SUPER_HEAVY
        unit.downgrade()
        unit.downgrade()
        unit.downgrade()
        assert unit.equipment == Unit.Equipment.LIGHT
        assert unit == my_clone


def test_upgrade_levies():
    levies = Unit("Splonks Levies", "Cucumbers")
    levies.experience = Unit.Experience.LEVIES
    with pytest.raises(CannotUpgradeError):
        levies.upgrade()


def test_typical_use():
    catapult = Infantry("Catapult", "Cats with heavy pulitzer prize trophies.")
    seige_weapon = Trait("Seige Weapon", "These cats will lay seige until given pets.")
    assert catapult.attacks == 1
    assert catapult.attack == 0
    assert catapult.defense == 10
    assert catapult.morale == 0
    assert catapult.command == 0
    assert catapult.experience == Unit.Experience.REGULAR
    assert catapult.equipment == Unit.Equipment.LIGHT
    catapult.add_trait(seige_weapon)
    clone = deepcopy(catapult)
    catapult.upgrade()
    catapult.level_up()
    assert catapult.attacks == 1
    assert catapult.attack == 1
    assert catapult.defense == 12
    assert catapult.command == 1
    assert catapult.experience == Unit.Experience.VETERAN
    assert catapult.equipment == Unit.Equipment.MEDIUM
    saved = catapult.to_dict()
    loaded = unit_from_dict(saved)
    assert loaded.attacks == 1
    assert loaded.attack == 1
    assert loaded.defense == 12
    assert loaded.command == 1
    assert loaded.experience == Unit.Experience.VETERAN
    assert loaded.equipment == Unit.Equipment.MEDIUM
    loaded.upgrade()
    loaded.level_up()
    #infantry leveled up twice to elite, heavy
    assert loaded.attacks == 2
    assert loaded.attack == 2
    assert loaded.defense == 14
    assert loaded.morale == 4
    assert loaded.command == 1
    loaded.level_down()
    loaded.level_down()
    loaded.downgrade()
    loaded.downgrade()
    assert loaded == clone
