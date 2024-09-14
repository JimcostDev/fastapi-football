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
    

# Función para crear un nuevo equipo
def create_team(team: TeamModel) -> TeamModel:
    try:
        # Conectar a la base de datos usando un contexto 'with'
        with get_database_instance() as db:
            # Acceder a la colección de equipos
            teams_collection = db.teams
            
            # Convertir el modelo TeamModel a un diccionario
            team_dict = team.model_dump(exclude_unset=True) # Excluir los valores no establecidos
            
            # Insertar el nuevo equipo en la colección
            result = teams_collection.insert_one(team_dict)
            
            if result.inserted_id:
                message = {"message": "Equipo creado exitosamente"}
                return message 
            
            return team
    except ValidationError as e:
        # Lanzar una excepción HTTP con código 422 si hay errores de validación
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Error de validación: {str(e)}")
    except Exception as e:
        # Lanzar una excepción HTTP con código 500 si ocurre un error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear el equipo: {str(e)}")