# apenas feito para evitar resultados muito explícitos
NSFW_SUBSTRINGS = [
    "nipple",
    "areola",
    "breast",
    "boob",
    "tit",
    "cleavage_cutout",
    "penis",
    "cock",
    "dick",
    "phallus",
    "glans",
    "foreskin",
    "erection",
    "vagina",
    "vulva",
    "pussy",
    "labia",
    "clitoris",
    "anus",
    "anal",
    "asshole",
    "butthole",
    "testicle",
    "balls",
    "scrotum",
    "semen",
    "cum",
    "ejacul",
    "sex",
    "fuck",
    "intercourse",
    "penetrat",
    "insertion",
    "masturbat",
    "fingering",
    "handjob",
    "blowjob",
    "fellatio",
    "cunnilingus",
    "anilingus",
    "rimjob",
    "rimming",
    "creampie",
    "gangbang",
    "orgy",
    "threesome",
    "rape",
    "molest",
    "grope",
    "orgasm",
    "squirt",
    "nude",
    "naked",
    "nudity",
    "topless",
    "bottomless",
    "nsfw",
    "hentai",
    "porn",
    "erotic",
    "lewd",
    "uncensor",
    "mosaic_censor",
    "bdsm",
    "bondage",
    "restraint",
    "handcuff",
    "whip",
    "spanking",
    "chastity",
    "ballgag",
    "tentacle",
    "oviposit",
    "inflation",
    "vore",
    "scat",
    "urine",
    "lactation",
    "milking",
    "breast_milk",
    "futanari",
    "futa",
    "bestiality",
    "zoophilia",
    "guro",
    "gore",
    "snuff",
    "incest",
    "netorare",
    "mind_break",
    "mind_control",
    "sex_slave",
    "glory_hole",
    "fisting",
    "object_insertion",
    "dildo",
    "vibrator",
    "sex_toy",
    "strapon",
    "rating:e",
    "rating:q",
    "rating:explicit",
    "rating:questionable",
]

EXCECOES = {
    "glasses",
    "sunglasses",
    "class",
    "brass",
    "assassin",
    "classic",
    "breast_pocket",
}

SAFE_RATINGS = {"", "g", "general", "s", "safe", "sfw"}


def is_safe_tag(tag):
    tag = tag.strip().lower()
    if not tag or tag in EXCECOES:
        return True
    return not any(sub in tag for sub in NSFW_SUBSTRINGS)


def is_safe_query(query):
    tags = str(query).replace(",", " ").split()
    return all(is_safe_tag(tag) for tag in tags)


def is_safe_result(item):
    rating = str(item.get("rating", "")).strip().lower()
    tags = item.get("tags", "")
    return rating in SAFE_RATINGS and is_safe_query(tags)


def filtrar_resultados(resultados):
    return [item for item in resultados if is_safe_result(item)]
