SKILLS = [
    "overall",
    "attack",
    "defence",
    "strength",
    "constitution",
    "ranged",
    "prayer",
    "magic",
    "cooking",
    "woodcutting",
    "fletching",
    "fishing",
    "firemaking",
    "crafting",
    "smithing",
    "mining",
    "herblore",
    "agility",
    "thieving",
    "slayer",
    "farming",
    "runecrafting",
    "hunter",
    "construction",
    "summoning",
    "dungeoneering",
    "divination",
    "invention",
    "archaeology",
]

ACTIVITIES = [
    "bounty hunter",
    "b.h. rogues",
    "dominion tower",
    "the crucible",
    "castle wars games",
    "b.a. attackers",
    "b.a. defenders",
    "b.a. collectors",
    "b.a. healers",
    "duel tournament",
    "mobilising armies",
    "conquest",
    "fist of guthix",
    "gg: athletics",
    "gg: resource race",
    "we2: armadyl lifetime contribution",
    "we2: bandos lifetime contribution",
    "we2: armadyl pvp kills",
    "we2: bandos pvp kills",
    "heist guard level",
    "heist robber level",
    "cfp: 5 game average",
    "af15: cow tipping",
    "af15: rats killed after the miniquest",
    "runescore",
    "clue scrolls easy",
    "clue scrolls medium",
    "clue scrolls hard",
    "clue scrolls elite",
    "clue scrolls master",
]

PLAYER = {
    "name": "",
    "skills": {
        "overall": { "rank": 0, "level": 1, "experience": 0 },
        "attack": { "rank": 0, "level": 1, "experience": 0 },
        "defence": { "rank": 0, "level": 1, "experience": 0 },
        "strength": { "rank": 0, "level": 1, "experience": 0 },
        "constitution": { "rank": 0, "level": 1, "experience": 0 },
        "ranged": { "rank": 0, "level": 1, "experience": 0 },
        "prayer": { "rank": 0, "level": 1, "experience": 0 },
        "magic": { "rank": 0, "level": 1, "experience": 0 },
        "cooking": { "rank": 0, "level": 1, "experience": 0 },
        "woodcutting": { "rank": 0, "level": 1, "experience": 0 },
        "fletching": { "rank": 0, "level": 1, "experience": 0 },
        "fishing": { "rank": 0, "level": 1, "experience": 0 },
        "firemaking": { "rank": 0, "level": 1, "experience": 0 },
        "crafting": { "rank": 0, "level": 1, "experience": 0 },
        "smithing": { "rank": 0, "level": 1, "experience": 0 },
        "mining": { "rank": 0, "level": 1, "experience": 0 },
        "herblore": { "rank": 0, "level": 1, "experience": 0 },
        "agility": { "rank": 0, "level": 1, "experience": 0 },
        "thieving": { "rank": 0, "level": 1, "experience": 0 },
        "slayer": { "rank": 0, "level": 1, "experience": 0 },
        "farming": { "rank": 0, "level": 1, "experience": 0 },
        "runecrafting": { "rank": 0, "level": 1, "experience": 0 },
        "hunter": { "rank": 0, "level": 1, "experience": 0 },
        "construction": { "rank": 0, "level": 1, "experience": 0 },
        "summoning": { "rank": 0, "level": 1, "experience": 0 },
        "dungeoneering": { "rank": 0, "level": 1, "experience": 0 },
        "divination": { "rank": 0, "level": 1, "experience": 0 },
        "invention": { "rank": 0, "level": 1, "experience": 0 },
        "archaeology": { "rank": 0, "level": 1, "experience": 0 },
    },
    "activities": {
        "bounty hunter": { "rank": 0, "score": 0 },
        "b.h. rogues": { "rank": 0, "score": 0 },
        "dominion tower": { "rank": 0, "score": 0 },
        "the crucible": { "rank": 0, "score": 0 },
        "castle wars games": { "rank": 0, "score": 0 },
        "b.a. attackers": { "rank": 0, "score": 0 },
        "b.a. defenders": { "rank": 0, "score": 0 },
        "b.a. collectors": { "rank": 0, "score": 0 },
        "b.a. healers": { "rank": 0, "score": 0 },
        "duel tournament": { "rank": 0, "score": 0 },
        "mobilising armies": { "rank": 0, "score": 0 },
        "conquest": { "rank": 0, "score": 0 },
        "fist of guthix": { "rank": 0, "score": 0 },
        "gg: athletics": { "rank": 0, "score": 0 },
        "gg: resource race": { "rank": 0, "score": 0 },
        "we2: armadyl lifetime contribution": { "rank": 0, "score": 0 },
        "we2: bandos lifetime contribution": { "rank": 0, "score": 0 },
        "we2: armadyl pvp kills": { "rank": 0, "score": 0 },
        "we2: bandos pvp kills": { "rank": 0, "score": 0 },
        "heist guard level": { "rank": 0, "score": 0 },
        "heist robber level": { "rank": 0, "score": 0 },
        "cfp: 5 game average": { "rank": 0, "score": 0 },
        "af15: cow tipping": { "rank": 0, "score": 0 },
        "af15: rats killed after the miniquest": { "rank": 0, "score": 0 },
        "runescore": { "rank": 0, "score": 0 },
        "clue scrolls easy": { "rank": 0, "score": 0 },
        "clue scrolls medium": { "rank": 0, "score": 0 },
        "clue scrolls hard": { "rank": 0, "score": 0 },
        "clue scrolls elite": { "rank": 0, "score": 0 },
        "clue scrolls master": { "rank": 0, "score": 0 },
    }
}

class GECategories:
    MISCELLANEOUS = 0
    AMMO = 1
    ARROWS = 2
    BOLTS = 3
    CONSTRUCTION_MATERIALS = 4
    CONSTRUCTION_PRODUCTS = 5
    COOKING_INGREDIENTS = 6
    COSTUMES = 7
    CRAFTING_MATERIALS = 8
    FAMILIARS = 9
    FARMING_PRODUCE = 10
    FLETCHING_MATERIALS = 11
    FOOD_AND_DRINK = 12
    HERBLORE_MATERIALS = 13
    HUTING_EQUIPMENT = 14
    HUNTING_PRODUCE = 15
    JEWELLERY = 16
    MAGE_ARMOUR = 17 
    MAGE_WEAPONS = 18
    MELEE_ARMOUR_LOW_LEVEL = 19
    MELEE_ARMOUR_MID_LEVEL = 20
    MELEE_ARMOUR_HIGH_LEVEL = 21
    MELEE_WEAPONS_LOW_LEVEL = 22
    MELEE_WEAPONS_MID_LEVEL = 23
    MELEE_WEAPONS_HIGH_LEVEL = 24
    MINING_AND_SMITHING = 25
    POTIONS = 26
    PRAYER_ARMOUR = 27
    PRAYER_MATERIALS = 28
    RANGE_ARMOUR = 29
    RANGE_WEAPONS = 30
    RUNECRAFTING = 31
    RUNES_SPELLS_TELEPORTS = 32
    SEEDS = 33
    SUMMONING_SCROLLS = 34 
    TOOLS_AND_CONTAINERS = 35
    WOODCUTTING_PRODUCTS = 36
    POCKET_ITEMS = 37 
    STONE_SPIRITS = 38
    SALVAGE = 39
    FIREMAKING_PRODUCTS = 40
    ARCHEOLOGY_MATERIALS = 41