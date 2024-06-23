from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from ..models import Team, UpdateTeam

router = APIRouter()

@router.post("/", response_model=Team)
async def create_team(team: Team):
    result = await team.insert()
    return result

@router.get("/", response_model=List[Team])
async def get_teams():
    result = await Team.find_all().to_list()
    return result

@router.get("/{code_name}", response_model=Team)
async def get_team(code_name: str):
    result = await Team.find(Team.code_name == code_name).first_or_none()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with code name {code_name} not found"
        )
    return result

@router.patch("/{code_name}", response_model=Team)
async def update_team(code_name: str, team_update: UpdateTeam):
    team = await Team.find(Team.code_name == code_name).first_or_none()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Team {code_name} not found"
        )

    updated_team = team_update.model_dump(exclude_unset=True)
    await team.update({"$set": updated_team})

    final_code_name = team_update.code_name if team_update.code_name is not None else code_name
    updated_team = await Team.find_one(Team.code_name == final_code_name)

    return updated_team

@router.delete("/{code_name}")
async def delete_team(code_name: str):
    delete_result = await Team.find_one(Team.code_name == code_name).delete()

    if delete_result is not None:
        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Team {code_name} not found")
