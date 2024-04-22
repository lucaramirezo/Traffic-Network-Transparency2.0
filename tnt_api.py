from fastapi import FastAPI, HTTPException
from my_connector import MySQLConnector
from pydantic import BaseModel
import nest_asyncio
import uvicorn
from typing import Optional

app = FastAPI()
# Crear una instancia del conector
connector = MySQLConnector(host="localhost", user="root", password="root", database="TNT")

# Conectar a la base de datos
connector.connect()
# EJEMPLO PETICIÓN SIN PARÁMETROS
@app.get("/distritos")
def read_distritos():
    query = "SELECT nombre_distrito FROM Distritos"
    try:
        distritos = connector.fetch_data(query)
        if not distritos:
            raise HTTPException(status_code=404, detail="No se han encontrado distritos")
        return {"Distritos": [distrito[0] for distrito in distritos]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# EJEMPLO PETICIÓN CON PARÁMETROS
@app.get("/distritos/{codigo_distrito}")
def read_distritos_param(codigo_distrito: int):
    query = "SELECT nombre_distrito FROM Distritos WHERE codigo_distrito = %s"
    try:
        distrito = connector.fetch_data(query, [codigo_distrito])
        if not distrito:
            raise HTTPException(status_code=404, detail="No se ha encontrado un distrito")
        return {"Distrito": distrito[0][0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#
#EJEMPLO INSERCIÓN
#
class RadarInsert(BaseModel):
    id: int
    ubicacion: str
    carretera: str
    punto_kilometrico: float
    sentido: Optional[str] = None
    tipo: Optional[str] = None
    longitud: Optional[float] = None
    latitud: Optional[float] = None
    coordenadas: Optional[str] = None
    cod_distrito: Optional[int] = None

@app.post("/radares")
def insert_radar(radar_insert: RadarInsert):
    query = """
    INSERT INTO RadaresFijos
    (id, ubicacion, carretera, punto_kilometrico, sentido, tipo, longitud, latitud, coordenadas, cod_distrito)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (
        radar_insert.id, radar_insert.ubicacion, radar_insert.carretera,
        radar_insert.punto_kilometrico, radar_insert.sentido, radar_insert.tipo,
        radar_insert.longitud, radar_insert.latitud, radar_insert.coordenadas,
        radar_insert.cod_distrito
    )
    connector.execute(query, data)
    connector.commit()
    new_radar_id = radar_insert.id # Obtener el ID del radar recién insertado
    connector.close()


    return {"message": "Radar insertado con éxito", "radar_id": new_radar_id}
#
#EJEMPLO BORRADO
#
class AccidenteDelete(BaseModel):
    num_expediente: str
    fecha: Optional[str] = None
    hora: Optional[str] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    codigo_distrito: Optional[int] = None
    tipo_accidente: Optional[str] = None
    coordenada_x_utm: Optional[float] = None
    coordenada_y_utm: Optional[float] = None
    positivo_alcohol: Optional[bool] = None
    positivo_droga: Optional[bool] = None
    fugado: Optional[bool] = None

# Define la función para borrar accidentes
@app.delete("/borrar_accidente")
def borrar_accidente(accidente_delete: AccidenteDelete):
    try:
        query = """
        DELETE FROM Accidentes WHERE num_expediente = %s
        """
        connector.execute(query, accidente_delete.num_expediente)
        connector.commit()
        connector.close()

        return {"message": f"Se ha eliminado el accidente con número de expediente: {accidente_delete.num_expediente}"}
    except Exception as e:
        return {"message": f"Error al eliminar el accidente: {str(e)}"}


#
# EJEMPLO ACTUALIZACION
#
class PersonaInvolucradaUpdate(BaseModel):
    num_expediente: str
    tipo_vehiculo: str
    tipo_persona: str
    rango_edad: str
    sexo: str
    codigo_lesividad: int
    numero_pasajeros: int

# Route to update the column
@app.put("/personas_involucradas/{persona_id}")
def update_persona_involucrada(persona_id: str, persona_update: PersonaInvolucradaUpdate):
    try:
        query = """
        UPDATE PersonasInvolucradas
        SET num_expediente = %s, tipo_vehiculo = %s, tipo_persona = %s,
            rango_edad = %s, sexo = %s, codigo_lesividad = %s, numero_pasajeros = %s
        WHERE uuid = %s
        """
        data = (
            persona_update.num_expediente, persona_update.tipo_vehiculo,
            persona_update.tipo_persona, persona_update.rango_edad,
            persona_update.sexo, persona_update.codigo_lesividad,
            persona_update.numero_pasajeros, persona_id
        )
        connector.execute(query, data)
        connector.commit()  # Save the changes to the database
        affected_rows = connector.rowcount
        connector.close()

        if affected_rows == 0:
            raise HTTPException(status_code=404, detail="Persona involucrada not found")

        return {"message": f"Persona involucrada with uuid {persona_id} updated successfully"}
    except Exception as e:
        return {"message": f"Error updating persona involucrada: {str(e)}"}

nest_asyncio.apply()

if __name__ == "__main__":
    #nest_asyncio.apply()
    #uvicorn.run(app)
    uvicorn.run(app, host="127.0.0.1", port=18000)
#%%

#%%
