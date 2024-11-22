from pydantic import BaseModel, Field

class TeamModel(BaseModel):
    id: str = Field(..., description="ID del equipo", alias="_id")  # Alias para recibir _id de MongoDB
    name: str = Field(..., description="Nombre del equipo")
    league: str = Field(..., description="Liga del equipo")
    country: str = Field(..., description="País del equipo")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "65cb8d4b73c22307b9a89b1d",  # Este será el _id convertido
                "name": "Real Madrid",
                "league": "La Liga",
                "country": "Spain"
            }
        }
        populate_by_name = True  # Permitir la población por el nombre del campo (id en lugar de _id)

class TeamCreateUpdateModel(BaseModel):
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