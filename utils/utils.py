def convert_object_id_to_str(documents: list, model):
    """
    Convierte el campo '_id' en 'id' como string en una lista de documentos y los 
    convierte en instancias del modelo Pydantic que se le pase.

    :param documents: Lista de documentos devueltos por MongoDB
    :param model: Modelo Pydantic al cual mapear los documentos
    :return: Lista de instancias del modelo Pydantic
    """
    return [model(**doc, id=str(doc['_id'])) for doc in documents if '_id' in doc]
