RUNEMETRICS_API_ENDPOINTS = {
    "profile": "https://apps.runescape.com/runemetrics/profile/profile?user={username}&activities={activities}",
    "monthly_experience": "https://apps.runescape.com/runemetrics/xp-monthly?searchName={username}&skillid={skill_id}",
    "quests": "https://apps.runescape.com/runemetrics/quests?user={username}"
}

HISCORE_API_ENDPOINTS = {
    "ranking": "https://secure.runescape.com/m=hiscore/ranking.json?table={index}&category={category}&size={size}",
    "normal": "https://secure.runescape.com/m=hiscore/index_lite.ws?player={username}",
    "ironman": "https://secure.runescape.com/m=hiscore_ironman/index_lite.ws?player={username}",
    "hardcore": "https://secure.runescape.com/m=hiscore_hardcore_ironman/index_lite.ws?player={username}",
    "season_ranking": "http://services.runescape.com/m=temp-hiscores/getRankings.json?player={username}",
    "past_season_ranking": "http://services.runescape.com/m=temp-hiscores/getRankings.json?player={username}&status=archived",
    "season_detail": "http://services.runescape.com/m=temp-hiscores/getHiscoreDetails.json",
    "past_season_detail": "http://services.runescape.com/m=temp-hiscores/getHiscoreDetails.json?status=archived",
    "clan_ranking": "http://services.runescape.com/m=clan-hiscores/clanRanking.json",
    "user_clan_ranking": "http://services.runescape.com/c={session_id}/m=clan-hiscores/userClanRanking.json"
}

BESTIARY_API_ENDPOINTS = {
    "get_beast": "http://services.runescape.com/m=itemdb_rs/bestiary/beastData.json?beastid={id}",
    "beast_by_term": "http://services.runescape.com/m=itemdb_rs/bestiary/beastSearch.json?term={term}",
    "beast_by_first_letter": "http://services.runescape.com/m=itemdb_rs/bestiary/bestiaryNames.json?letter={letter}",
    "get_areas": "http://services.runescape.com/m=itemdb_rs/bestiary/areaNames.json",
    "get_beasts_by_area": "http://services.runescape.com/m=itemdb_rs/bestiary/areaBeasts.json?identifier={area}",
    "get_slayer_categories": "http://services.runescape.com/m=itemdb_rs/bestiary/slayerCatNames.json",
    "get_slayer_beasts_by_category_id": "http://services.runescape.com/m=itemdb_rs/bestiary/slayerBeasts.json?identifier={id}",
    "weakness_names": "http://services.runescape.com/m=itemdb_rs/bestiary/weaknessNames.json",
    "beasts_by_weakness_id": "http://services.runescape.com/m=itemdb_rs/bestiary/weaknessBeasts.json?identifier={id}",
    "get_beasts_by_level": "http://services.runescape.com/m=itemdb_rs/bestiary/levelGroup.json?identifier={level_from}-{level_to}"
}

GRAND_EXCHANGE_API_ENDPOINTS = {
    "catalogue": "https://services.runescape.com/m=itemdb_rs/api/catalogue/category.json?category={categoryId}",
    "runedate": "https://secure.runescape.com/m=itemdb_rs/api/info.json",
    "items": " https://services.runescape.com/m=itemdb_rs/api/catalogue/items.json?category={categoryId}&alpha={searchString}&page={page}",
    "item_detail": "https://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item={itemId}",
    "graph": "https://services.runescape.com/m=itemdb_rs/api/graph/{itemId}.json",
}