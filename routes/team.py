# Importaciones necesarias de FastAPI
from fastapi import (
    HTTPException, 
    APIRouter,
    status,
    Query  # Para manejar los query parameters
)

# Importar la función para obtener la instancia de la base de datos
from database.operations.team_db import get_teams

# Crear una instancia de la aplicación FastAPI
router = APIRouter()

# Definir una ruta GET para obtener la lista de equipos
@router.get("/", 
         tags=['teams'],
         summary="Obtener equipos de una liga o todos los equipos",
         description="Obtiene una lista de equipos de una liga (se debe pasar el nombre de liga como parámetro) o todos los equipos. Los equipos se ordenan por nombre.")
async def get_teams_endpoint(league_name: str = Query(None, description="Nombre de la liga para filtrar los equipos")):
    """
    Endpoint para obtener la lista de equipos, filtrando opcionalmente por el nombre de la liga.
    """
    try:
        # Llama a la función get_teams con el parámetro league_name
        teams = get_teams(league_name)
        
        if not teams:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No se pudo encontrar la información de los equipos")
        
        return teams
    
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener los equipos: {str(ex)}")
