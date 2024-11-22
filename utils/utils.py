# convertir _id en id de una lista de documentos
def convert_object_id_to_str_multi(documents: list, model):
    """
    Convierte el campo '_id' en 'id' como string en una lista de documentos y los 
    convierte en instancias del modelo Pydantic que se le pase.

    :param documents: Lista de documentos devueltos por MongoDB
    :param model: Modelo Pydantic al cual mapear los documentos
    :return: Lista de instancias del modelo Pydantic
    """
    # Convertimos '_id' en 'id' y lo pasamos al modelo
    for doc in documents:
        if '_id' in doc:
            doc['id'] = str(doc['_id'])  # Convertir _id a id como string
            del doc['_id']  # Eliminar el campo _id original
    # Retornar una lista de instancias del modelo
    return [model(**doc) for doc in documents if doc]



# convertir _id en id de un solo documento
def convert_object_id_to_str_single(doc, model):
    """
    Convierte el campo '_id' en 'id' como string en un documento y lo convierte en una 
    instancia del modelo Pydantic que se le pase.

    :param doc: Documento devuelto por MongoDB
    :param model: Modelo Pydantic al cual mapear el documento
    :return: Instancia del modelo Pydantic
    """
    if '_id' in doc:
        doc['id'] = str(doc['_id'])  # Convertir _id a id como string
        del doc['_id']  # Eliminar el campo _id
    # Retornar la instancia del modelo
    return model(**doc) if doc else None
