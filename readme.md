# FastAPI Football API

API básica desarrollada con FastAPI para obtener información sobre equipos de fútbol (nombre, liga y país). Este proyecto es ideal para aprender y practicar los fundamentos de FastAPI, incluyendo creación de endpoints, manejo de dependencias y uso de un servidor de desarrollo.

## Instrucciones de Uso

1. **Clona este repositorio** ejecutando el siguiente comando:

    ```bash
    git clone https://github.com/JimcostDev/fastapi-football.git
    ```

2. **Crea y activa tu entorno virtual**:

    - Crea un entorno virtual:

        ```bash
        python -m venv venv
        ```

    - Activa el entorno virtual:

        - En **Windows**:

            ```bash
            venv\Scripts\activate
            ```

        - En **macOS y Linux**:

            ```bash
            source venv/bin/activate
            ```

3. **Instala las dependencias requeridas**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Ejecute el servidor con:**
    ```bash
    fastapi dev main.py # mode dev
    fastapi run # mode prod
    ```
5. **Actualizar versión de FastAPI**:
 ```bash
    pip install --upgrade fastapi
 ```
 ### Puedes  instalar las dependecias individualmente con:
```bash
    pip install "fastapi[standard]"
    pip install pymongo
```