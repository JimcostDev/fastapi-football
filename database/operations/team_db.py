from bson import ObjectId
from fastapi import HTTPException, status
from pydantic import ValidationError
from database.conn_db import get_database_instance
from database.models.team_model import TeamModel, TeamCreateUpdateModel
from utils.utils import convert_object_id_to_str_multi, convert_object_id_to_str_single


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
                # Usar la opción 'i' para ignorar mayúsculas y minúsculas
                filter = {"league": {"$regex": league_name, "$options": "i"}} 

            # Ejecutar la consulta y ordenar los resultados por nombre (ascendente)
            teams_cursor  = teams_collection.find(filter).sort("name", 1)
            
            # Convertir el cursor de MongoDB a una lista de diccionarios
            teams_list = list(teams_cursor)
            
            # Utilizar la función genérica para convertir '_id' en 'id' y mapear al modelo TeamModel
            teams = convert_object_id_to_str_multi(teams_list, TeamModel)
             
            if teams:
                return teams
    except Exception as e:
        # Lanzar una excepción HTTP con código 500 si ocurre un error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener los equipos: {str(e)}")
    
# Función para obtener un equipo por ID
def get_team_by_id(team_id: str) -> TeamModel:
    try:
        # Conectar a la base de datos usando un contexto 'with'
        with get_database_instance() as db:
            # Acceder a la colección de equipos
            teams_collection = db.teams
            
            # Buscar un equipo por su ID
            team = teams_collection.find_one({"_id": ObjectId(team_id)})
            if team:
                # Convertir '_id' en 'id' y mapear al modelo TeamModel
                team = convert_object_id_to_str_single(team, TeamModel)
                return team
    except Exception as e:
        # Lanzar una excepción HTTP con código 500 si ocurre un error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener el equipo: {str(e)}")

# Función para obtener un equipo por nombre
def get_team_by_name(team_name: str) -> TeamModel:
    try:
        # Conectar a la base de datos usando un contexto 'with'
        with get_database_instance() as db:
            # Acceder a la colección de equipos
            teams_collection = db.teams
            
            # Buscar un equipo por su nombre (ignorar mayúsculas y minúsculas)
            team = teams_collection.find_one({"name": {"$regex": team_name, "$options": "i"}})
            if team:
                team = convert_object_id_to_str_single(team, TeamModel)
                return team
    except Exception as e:
        # Lanzar una excepción HTTP con código 500 si ocurre un error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener el equipo: {str(e)}")
    

# Función para crear un nuevo equipo
def create_team(team: TeamCreateUpdateModel) -> TeamCreateUpdateModel:
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
    
# Función para actualizar un equipo existente
def update_team(team_id: str, team: TeamCreateUpdateModel) -> TeamCreateUpdateModel:
    try:
        # Conectar a la base de datos usando un contexto 'with'
        with get_database_instance() as db:
            # Acceder a la colección de equipos
            teams_collection = db.teams
            
            # Convertir el modelo TeamModel a un diccionario
            team_dict = team.model_dump(exclude_unset=True) # Excluir los valores no establecidos
            
            existing_team = teams_collection.find_one({"_id": ObjectId(team_id)})
            if existing_team: 
                # Actualizar el equipo en la colección
                result = teams_collection.update_one({"_id": ObjectId(team_id)}, {"$set": team_dict})
                if result.modified_count > 0 and result.matched_count > 0:
                    message = {"message": "Equipo actualizado exitosamente"}
                    return message 
                else:
                    message = {"message": "No se pudo actualizar el equipo, no se encontraron cambios"}
                return team
    except ValidationError as e:
        # Lanzar una excepción HTTP con código 422 si hay errores de validación
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Error de validación: {str(e)}")
    except Exception as e:
        # Lanzar una excepción HTTP con código 500 si ocurre un error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar el equipo: {str(e)}")
    
# Función para eliminar un equipo existente
def delete_team(team_id: str):
    try:
        # Conectar a la base de datos usando un contexto 'with'
        with get_database_instance() as db:
            # Acceder a la colección de equipos
            teams_collection = db.teams
            
            existing_team = teams_collection.find_one({"_id": ObjectId(team_id)})
            if existing_team:
                # Eliminar el equipo de la colección
                result = teams_collection.delete_one({"_id": ObjectId(team_id)})
                if result.deleted_count > 0:
                    message = {"message": "Equipo eliminado exitosamente"}
                    return message
    except Exception as e:
        # Lanzar una excepción HTTP con código 500 si ocurre un error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar el equipo: {str(e)}")