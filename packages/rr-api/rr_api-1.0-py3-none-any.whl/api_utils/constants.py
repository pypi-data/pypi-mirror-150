class General:
    DATABASE = 'wyscout'
    DEFAULT_USER = 'root'
    DEFAULT_PASSWORD = 'password'


class Keys:
    STATUS_CODE = 'status_code'
    DATA_TYPE = 'data_type_name'
    DATA = 'data'
    COUNTRIES = 'countries'
    COMPETITIONS = 'competitions'
    TEAMS = 'teams'
    PLAYERS = 'players'
    OVERVIEW = 'overview'
    STATS = 'stats'
    POSITION = 'position'
    COUNT_OF_GAMES = 'count_of_games'


class Routs:
    ENTITIES = 'entities'
    PLAYERS = 'players'


class FilterData:
    DEFAULT_STATS = ['minutes on field', 'goal', 'xg shot', 'assist', 'pre assist', 'shot assist', 'interception',
                     'yellow cards', 'red cards']
