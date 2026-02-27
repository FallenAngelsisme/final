"""
進化系統數據配置
Evolution System Data Configuration

使用方式 / How to use:
1. 在這裡定義每個怪獸的進化鏈
2. 設定進化所需等級
3. 指定進化後的圖片路徑
4. 設定能力加成

Evolution Chain Example:
Charmander (Lv.16) -> Charmeleon (Lv.36) -> Charizard
"""

from src.utils.definition import Monster
'''
{
        "name": "Charmander",
        "hp": 60,
        "max_hp": 60,
        "level": 6,
        "sprite_path": "menu_sprites/menusprite7.png",
        "element": "Fire"
      },
{
        "name": "Charmeleon",
        "hp": 60,
        "max_hp": 60,
        "level": 6,
        "sprite_path": "menu_sprites/menusprite8.png",
        "element": "Fire"
      },
{
        "name": "Charizard",
        "hp": 60,
        "max_hp": 60,
        "level": 6,
        "sprite_path": "menu_sprites/menusprite9.png",
        "element": "Fire"
      },
{
        "name": "Rat",
        "hp": 60,
        "max_hp": 60,
        "level": 6,
        "sprite_path": "menu_sprites/menusprite10.png",
        "element": "Grass"
      },
{
        "name": "Rat_snack",
        "hp": 60,
        "max_hp": 60,
        "level": 6,
        "sprite_path": "menu_sprites/menusprite11.png",
        "element": "Grass"
      },
{
        "name": "Pidgey",
        "hp": 60,
        "max_hp": 60,
        "level": 6,
        "sprite_path": "menu_sprites/menusprite12.png",
        "element": "Water"
      },
{
        "name": "Pidgeotto",
        "hp": 60,
        "max_hp": 60,
        "level": 6,
        "sprite_path": "menu_sprites/menusprite13.png",
        "element": "Water"
      },
{
        "name": "Pidgeot",
        "hp": 60,
        "max_hp": 60,
        "level": 6,
        "sprite_path": "menu_sprites/menusprite14.png",
        "element": "Water"
      },
{
        "name": "Bulbasaur",
        "hp": 60,
        "max_hp": 60,
        "level": 6,
        "sprite_path": "menu_sprites/menusprite15.png",
        "element": "Grass"
      },
{
        "name": "Ivysaur",
        "hp": 60,
        "max_hp": 60,
        "level": 6,
        "sprite_path": "menu_sprites/menusprite16.png",
        "element": "Grass"
      }

'''
# ==================== 進化數據表 ====================
# 格式說明:
# "原始名稱": {
#     "to": "進化後名稱",
#     "level": 進化所需等級,
#     "sprite": "進化後圖片路徑",
#     "stat_bonus": {"hp": HP加成, "attack": 攻擊力加成}
# }

EVOLUTION_DATA = {
    # === 皮卡丘進化鏈 ===
    "Pikachu": {
        "to": "Charizard",
        "level": 30,
        "sprite": "menu_sprites/menusprite2.png",
        "stat_bonus": {"hp": 40, "attack": 20}
    },

    "Charizard": {
        "to": "Blastoise",
        "level": 30,
        "sprite": "menu_sprites/menusprite3.png",
        "stat_bonus": {"hp": 40, "attack": 20}
    },
    # === 小火龍進化鏈 ===
    "Charmander": {
        "to": "Charmeleon",
        "level": 16,
        "sprite": "menu_sprites/menusprite8.png",
        "stat_bonus": {"hp": 20, "attack": 10}
    },
    "Charmeleon": {
        "to": "Charizard",
        "level": 36,
        "sprite": "menu_sprites/menusprite9.png",
        "stat_bonus": {"hp": 50, "attack": 30}
    },

    
    # === 妙蛙種子進化鏈 ===
    "Bulbasaur": {
        "to": "Ivysaur",
        "level": 16,
        "sprite": "menu_sprites/menusprite2.png",
        "stat_bonus": {"hp": 22, "attack": 9}
    },
    "Ivysaur": {
        "to": "Venusaur",
        "level": 36,
        "sprite": "menu_sprites/menusprite3.png",
        "stat_bonus": {"hp": 48, "attack": 28}
    },
    
    # === 波波進化鏈 ===
    "Pidgey": {
        "to": "Pidgeotto",
        "level": 18,
        "sprite": "menu_sprites/pidgeotto.png",
        "stat_bonus": {"hp": 15, "attack": 12}
    },
    "Pidgeotto": {
        "to": "Pidgeot",
        "level": 36,
        "sprite": "menu_sprites/pidgeot.png",
        "stat_bonus": {"hp": 35, "attack": 25}
    },
    
    # === 小拉達進化鏈 ===
    "Rattata": {
        "to": "Raticate",
        "level": 20,
        "sprite": "menu_sprites/raticate.png",
        "stat_bonus": {"hp": 30, "attack": 18}
    },
    
    # === 烈雀進化鏈 ===
    "Spearow": {
        "to": "Fearow",
        "level": 20,
        "sprite": "menu_sprites/fearow.png",
        "stat_bonus": {"hp": 28, "attack": 22}
    },
    
    # === 阿柏蛇進化鏈 ===
    "Ekans": {
        "to": "Arbok",
        "level": 22,
        "sprite": "menu_sprites/arbok.png",
        "stat_bonus": {"hp": 32, "attack": 20}
    },
    
    
    
    
}


# ==================== 進化檢查函數 ====================

def can_evolve(monster: Monster) -> bool:
    """
    檢查怪獸是否可以進化
    
    Args:
        monster: 要檢查的怪獸
        
    Returns:
        bool: 是否可以進化
    """
    return monster.name in EVOLUTION_DATA and monster.level >= EVOLUTION_DATA[monster.name]["level"]


def get_evolution_info(monster_name: str) -> dict:
    """
    獲取怪獸的進化資訊
    
    Args:
        monster_name: 怪獸名稱
        
    Returns:
        dict: 進化資訊，如果不存在則返回 None
    """
    return EVOLUTION_DATA.get(monster_name)


def try_evolve(monster: Monster, evolution_data: dict = None) -> str:
    """
    嘗試進化怪獸
    
    Args:
        monster: 要進化的怪獸
        evolution_data: 進化數據（可選，預設使用 EVOLUTION_DATA）
        
    Returns:
        str: 進化訊息，如果無法進化則返回 None
    """
    if evolution_data is None:
        evolution_data = EVOLUTION_DATA
        
    result = monster.evolve(evolution_data)
    if result:
        old_name, new_name = result
        return f"{old_name} evolved into {new_name}!"
    return None


# ==================== 進化鏈查詢 ====================

def get_evolution_chain(monster_name: str) -> list:
    """
    獲取完整的進化鏈
    
    Example:
        get_evolution_chain("Charmander") 
        -> ["Charmander", "Charmeleon", "Charizard"]
    
    Args:
        monster_name: 起始怪獸名稱
        
    Returns:
        list: 完整進化鏈
    """
    chain = [monster_name]
    current = monster_name
    
    while current in EVOLUTION_DATA:
        next_form = EVOLUTION_DATA[current]["to"]
        chain.append(next_form)
        current = next_form
    
    return chain


def get_final_evolution(monster_name: str) -> str:
    """
    獲取最終進化形態
    
    Example:
        get_final_evolution("Charmander") -> "Charizard"
    
    Args:
        monster_name: 怪獸名稱
        
    Returns:
        str: 最終進化形態名稱
    """
    chain = get_evolution_chain(monster_name)
    return chain[-1]


# ==================== 測試用例 ====================

if __name__ == "__main__":
    # 測試進化鏈
    print("=== Evolution Chains ===")
    test_monsters = ["Pikachu", "Charmander", "Squirtle", "Bulbasaur"]
    
    for mon_name in test_monsters:
        chain = get_evolution_chain(mon_name)
        final = get_final_evolution(mon_name)
        print(f"{mon_name}: {' -> '.join(chain)}")
        print(f"Final form: {final}\n")
    
    # 測試進化資訊
    print("=== Evolution Requirements ===")
    for mon_name, evo_data in EVOLUTION_DATA.items():
        print(f"{mon_name} -> {evo_data['to']} (Lv.{evo_data['level']})")
        print(f"  Stats: +{evo_data['stat_bonus']['hp']} HP, +{evo_data['stat_bonus']['attack']} ATK")