class BaseEntities:
    @staticmethod
    def countries():
        return "select * from wyscout.countries;"

    @staticmethod
    def competitions(country_id: int):
        return f"select * from wyscout.competitions where country_id = {country_id};"

    @staticmethod
    def teams(competition_id: int):
        return f"select competition_id, id, name from wyscout.teams where competition_id = {competition_id};"

    @staticmethod
    def players(team_id: int):
        return f"select distinct team_id, player_id, player_name from player_object where team_id = {team_id};"


class Players:
    @staticmethod
    def players_filter(object_id: int, data_type: int):
        """  Returns all players by data type "
            - **current player team id **: 1
            - **country id **: 2
        """
        if data_type == 1:
            where_field = 'team_id'
        elif data_type == 2:
            where_field = 'country_id'
        else:
            return
        return f"select distinct player_id, player_name from wyscout.player_object where {where_field} = {object_id};"

    @staticmethod
    def overview(player_id: int):
        return f"select overview_object from wyscout.player_object where player_id = {player_id} limit 1;"

    @staticmethod
    def stats(player_id: int, required_stats: list):
        required_stat = str(required_stats).replace('[', '(').replace(']', ')')
        return "select distinct stat_name, " \
               "cast(sum(stat_value) / (select count(distinct event_id) from player_statistics " \
               f"where object_id = {player_id}) as decimal(10,2)) as stat_value " \
               f"from wyscout.player_statistics where object_id = {player_id} " \
               f"and stat_name in {required_stat} group by stat_name order by stat_name asc;"

    @staticmethod
    def count_of_games(player_id: int):
        return f"select count(distinct event_id) from player_statistics where object_id = {player_id};"

    @staticmethod
    def position(player_id: int):
        return f"select stat_value from player_statistics where object_id = {player_id} " \
               "and stat_name = 'positions' order by date desc limit 1;"
