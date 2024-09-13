# Importaciones necesarias de FastAPI, HTTPException, 
from fastapi import FastAPI, HTTPException
from pathlib import Path


# Crear una instancia de la aplicación FastAPI
app = FastAPI(title="JimcostDev Football API",
    description="API para obtener información de equipos de fútbol",
    version="0.1.0",)

# Función para cargar rutas dinámicamente
def load_routes(app):
    routes_directory = Path(__file__).parent / "routes"

    for route_file in routes_directory.glob("*.py"):
        if route_file.name != "__init__.py":
            module = __import__(f"routes.{route_file.stem}", fromlist=["router"])
            app.include_router(module.router)

# Cargar rutas
load_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
