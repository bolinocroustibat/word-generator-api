ALLOW_ORIGINS = [
    "http://localhost",
    "https://adriencarpentier.com",
    "https://word-generator-api.adriencarpentier.com",
]

MYSQL_URL = "mysql://root:root@localhost:8889/words"  # local
# MYSQL_URL = "mysql://localmysqluser:foufoune@localhost/words"# prod

DICTIONNARY_EN_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

ALLOWED_TYPES = ["noun", "verb", "adjective", "adverb"]
