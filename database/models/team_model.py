from pydantic import BaseModel, Field

class TeamModel(BaseModel):
    name: str = Field(..., description="Nombre del equipo")
    league: str = Field(..., description="Liga del equipo")
    country: str = Field(..., description="País del equipo")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Real Madrid",
                "league": "La Liga",
                "country": "Spain"
            }
        }


