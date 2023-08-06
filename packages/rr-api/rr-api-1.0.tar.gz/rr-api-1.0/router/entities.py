import api_utils as au
from fastapi import APIRouter


class EntitiesModel(au.base_model.BaseModel):
    """
    Initiate entities model
    """
    pass


router_entities = APIRouter(
    prefix=f"/{au.constants.Routs.ENTITIES}",
    tags=[au.constants.Routs.ENTITIES]
)


@router_entities.get(path=f"/countries", summary="Returns all countries")
async def countries():
    """
    Returns all competitions by country id
    """
    return {au.constants.Keys.DATA_TYPE: au.constants.Keys.COUNTRIES,
            au.constants.Keys.DATA:
                EntitiesModel.Meta.database.get_data(query=au.query.BaseEntities.countries())[0],
            au.constants.Keys.STATUS_CODE: 200}


@router_entities.get(path="/competitions/{country_id}", summary="Returns all competitions by country id")
async def competitions(country_id: int):
    """
        Returns all competitions by country id
        - **country**: The country unique id.
    """
    return {au.constants.Keys.DATA_TYPE: au.constants.Keys.COMPETITIONS,
            au.constants.Keys.DATA:
                EntitiesModel.Meta.database.get_data(
                    query=au.query.BaseEntities.competitions(country_id=country_id))[0],
            au.constants.Keys.STATUS_CODE: 200}


@router_entities.get(path="/teams/{competition_id}", summary="Returns all teams by competition id")
async def teams(competition_id: int):
    """
        Returns all teams by country and competition id"
        - **competition**: The competition unique id.
    """
    return {au.constants.Keys.DATA_TYPE: au.constants.Keys.TEAMS,
            au.constants.Keys.DATA:
                EntitiesModel.Meta.database.get_data(
                    query=au.query.BaseEntities.teams(competition_id=competition_id))[
                    0],
            au.constants.Keys.STATUS_CODE: 200}


@router_entities.get(path="/players/{team_id}",
                     summary="Returns all players by team id")
async def players(team_id: int):
    """
        Returns all players by country, competition and team id
        - **team**: The team unique id.
    """
    return {au.constants.Keys.DATA_TYPE: au.constants.Keys.PLAYERS,
            au.constants.Keys.DATA:
                EntitiesModel.Meta.database.get_data(query=au.query.BaseEntities.players(team_id=team_id))[
                    0], au.constants.Keys.STATUS_CODE: 200}
