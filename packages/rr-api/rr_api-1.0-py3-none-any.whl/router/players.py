import api_utils as au
from fastapi import APIRouter


class PlayersModel(au.base_model.BaseModel):
    """
    Initiate entities model
    """
    pass


router_players = APIRouter(
    prefix=f"/{au.constants.Routs.PLAYERS}",
    tags=[au.constants.Routs.PLAYERS]
)


@router_players.get(path="/overview/{player_id}", summary="Returns player overview")
async def overview(player_id: int):
    """
    Returns player overview by unique player_id
    """
    return {au.constants.Keys.DATA_TYPE: au.constants.Keys.OVERVIEW,
            au.constants.Keys.DATA:
                PlayersModel.Meta.database.get_data(query=au.query.Players.overview(player_id=player_id))[0],
            au.constants.Keys.STATUS_CODE: 200}


@router_players.post(path="/stats/{player_id}", summary="Returns player overview")
async def stats(player_id: int, required_stats: list = au.constants.FilterData.DEFAULT_STATS):
    """
    Returns player stays by unique player_id
    """
    return {au.constants.Keys.DATA_TYPE: au.constants.Keys.STATS,
            au.constants.Keys.DATA:
                PlayersModel.Meta.database.get_data(query=au.query.Players.stats(player_id=player_id,
                                                                                 required_stats=required_stats))[0],
            au.constants.Keys.POSITION:
                PlayersModel.Meta.database.get_data(query=au.query.Players.position(player_id=player_id))[0],
            au.constants.Keys.COUNT_OF_GAMES:
                PlayersModel.Meta.database.get_data(query=au.query.Players.count_of_games(player_id=player_id))[0],
            au.constants.Keys.STATUS_CODE: 200}


@router_players.get(path="/filter/{data_type}/{object_id}", summary="Returns all players by data type")
async def compare_players(object_id: int, data_type: int = 1):
    """
        data_type:
        - current player team id: 1
        - country id: 2

        object_id:
        - the main id, need to be unique.
    """
    return {au.constants.Keys.DATA_TYPE: au.constants.Keys.PLAYERS,
            au.constants.Keys.DATA:
                PlayersModel.Meta.database.get_data(
                    query=au.query.Players.players_filter(object_id=object_id, data_type=data_type))[0],
            au.constants.Keys.STATUS_CODE: 200}
