from pymongo import MongoClient

class MongoConnectionManager:
    """
    Clase para manejar la conexión con MongoDB de manera centralizada.
    Implementa el patrón Singleton para reutilizar la misma conexión.
    """
    _client = None

    @classmethod
    def connect(cls, uri: str, db_name: str):
        if cls._client is None:
            cls._client = MongoClient(uri)
        cls._db = cls._client[db_name]
        return cls._db

    @classmethod
    def get_collection(cls, collection_name: str):
        if cls._db is None:
            raise RuntimeError("Primero debes establecer una conexión con `connect`.")
        return cls._db[collection_name]

    @classmethod
    def close(cls):
        if cls._client is not None:
            cls._client.close()
            cls._client = None
