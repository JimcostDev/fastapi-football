from fastapi import HTTPException, status
from pydantic import ValidationError
from database.conn_db import get_database_instance
from database.models.team_model import TeamModel
from utils.utils import convert_object_id_to_str


# Función para obtener la lista de equipos
def get_teams(league_name: str = None) -> TeamModel:
    try:
        # Conectar a la base de datos usando un contexto 'with'
        with get_database_instance() as db:
            # Acceder a la colección de equipos
            teams_collection = db.teams
            
            # Definir un filtro para la liga 'Premier League' o vacío para obtener todos los equipos
            filter = {}
            if league_name:
                filter = {"league": league_name}

            # Ejecutar la consulta y ordenar los resultados por nombre (ascendente)
            teams_cursor  = teams_collection.find(filter).sort("name", 1)
            
            # Convertir el cursor de MongoDB a una lista de diccionarios
            teams_list = list(teams_cursor)
            
            # Utilizar la función genérica para convertir '_id' en 'id' y mapear al modelo TeamModel
            teams = convert_object_id_to_str(teams_list, TeamModel)
             
            if teams:
                return teams
            else:
                None
    except Exception as e:
        # Lanzar una excepción HTTP con código 500 si ocurre un error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener los equipos: {str(e)}")