from typing import Optional, List
import secrets
import hashlib
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import ConfigDict, BaseModel, Field, model_validator, field_validator
from beanie import Document, Indexed

class ValidateFlag(BaseModel):
    value: str

    # Remove space from the beginning and the end of value
    @field_validator('value')
    def strip_whitespace(cls, v):
        return v.strip()

class Flag(BaseModel):
    name: str
    order: int
    description: Optional[str] = None
    value: Optional[str] = None
    found: bool = Field(default=False, exclude=True)
    found_at: Optional[datetime] = Field(default=None, exclude=True)
    points: int = 1
    tags: Optional[List[str]] = []

    # Generate random flag when not provided
    @model_validator(mode='before')
    @classmethod
    def set_random_value(cls, values):
        if values.get('value') is None:
            random_bytes = secrets.token_bytes(20)
            hash_object = hashlib.sha256(random_bytes)
            values['value'] = hash_object.hexdigest()
        return values

class UpdateTeam(BaseModel):
    name: Optional[str] = None
    code_name: Optional[str] = None
    description: Optional[str] = None
    flags: Optional[List[Flag]] = None

    @field_validator('flags')
    def check_unique(cls, v):
        if v is None:
            return v
        flag_names = [flag.name for flag in v]
        if len(flag_names) != len(set(flag_names)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate flag name found."
            )
        flag_orders = [flag.order for flag in v]
        if len(flag_orders) != len(set(flag_orders)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate flag order found."
            )
        return v

class Team(Document):
    name: str
    code_name: Indexed(str, unique=True) # type: ignore
    description: Optional[str] = None
    flags: Optional[List[Flag]] = []
    # players: Optional[List[BackLink["Player"]]] = Field(json_schema_extra={"original_field": "team"}) # type: ignore   default_factory=list, 

    @field_validator('flags')
    def check_unique(cls, v):
        if v is None:
            return v
        flag_names = [flag.name for flag in v]
        if len(flag_names) != len(set(flag_names)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate flag name found."
            )
        flag_orders = [flag.order for flag in v]
        if len(flag_orders) != len(set(flag_orders)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate flag order found."
            )
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Les Loups de Wall Street",
                "code_name": "les-loups-de-wall-street",
                "description": "Amiens (France) engineering school team",
                "flags": [
                    {
                        "name": "Kernel Exploit 1",
                        "order": 1
                    },
                    {
                        "name": "SSH Attack 1",
                        "order": 2,
                        "description": "with multiple tags and fixed value",
                        "value": "lemotdepassedeouf",
                        "points": 3,
                        "tags": ["password", "pentest", "hydra", "hard"]
                    }
                ]
            }
        }
    )

    class Settings:
          name = "teams"
