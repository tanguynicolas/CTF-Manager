from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, status, responses
from fastapi.responses import Response

from ..models import Team, ValidateFlag
from ..config import kafka_settings

if kafka_settings.enable is True:
    from .producer import produce_flag

router = APIRouter()

@router.post("/flag/")
async def validate_flag(code_name: str, flag: ValidateFlag):
    team = await Team.find(Team.code_name == code_name).first_or_none()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Team {code_name} not found"
        )

    if team.flags:
        for team_flag in team.flags:
            if team_flag.value == flag.value:
                if not team_flag.found:
                    team_flag.found = True
                    team_flag.found_at = datetime.now()
                    await team.save()

                    if kafka_settings.enable is True:
                        print("Produce flag to Kafka")
                        await produce_flag(
                            name=team.name,
                            code_name=team.code_name,
                            flag=team_flag.name,
                            tags=team_flag.tags
                        )

                    return Response(content="Well done! C'était le bon flag ! :D", status_code=status.HTTP_200_OK)
                else:
                    return Response(content=f"You believed it. Le flag a déjà été trouvé à {team_flag.found_at}", status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="There is no flag for your team. Please contact CTF organizers."
        )
    
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Invalid flag. Bien tenté... mais non !"
    )
