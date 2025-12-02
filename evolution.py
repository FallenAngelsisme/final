EVOLUTION_DATA = {
    "Pikachu": {
        "to": "Raichu",
        "level": 30,
        "sprite": "menu_sprites/raichu.png",
        "stat_bonus": {"hp": 40, "attack": 20}
    },
    # 你可以繼續擴充其他怪
}

def can_evolve(monster):
    """判斷怪獸是否可進化"""
    if monster.name in EVOLUTION_DATA:
        evo = EVOLUTION_DATA[monster.name]
        return monster.level >= evo["level"]
    return False

def evolve(monster):
    """進化怪獸，回傳進化後的數據"""
    if not can_evolve(monster):
        return None
    
    evo = EVOLUTION_DATA[monster.name]
    old_name = monster.name
    monster.name = evo["to"]
    monster.sprite_path = evo["sprite"]
    monster.max_hp += evo["stat_bonus"].get("hp", 0)
    monster.hp = monster.max_hp
    monster.attack = getattr(monster, "attack", monster.level*2 + 20) + evo["stat_bonus"].get("attack", 0)
    return old_name, monster.name
