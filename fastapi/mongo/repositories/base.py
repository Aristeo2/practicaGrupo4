from pymongo.collection import Collection
from bson import ObjectId
from mongo.middleware.middleware import MongoDocumentSerializer

class BaseRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, data: dict):
        """Inserta un nuevo documento en la colección."""
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def get_by_id(self, document_id: str):
        """Obtiene un documento por su ID y serializa el ObjectId."""
        document = self.collection.find_one({"_id": ObjectId(document_id)})
        return MongoDocumentSerializer.serialize(document) if document else None


    def delete(self, document_id: str):
        """Elimina un documento por su ID."""
        result = self.collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count

    def update(self, document_id: str, data: dict):
        """Actualiza un documento por su ID."""
        result = self.collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": data}
        )
        return result.modified_count

    def list_all(self):
        """Devuelve todos los documentos de la colección con ObjectId serializados."""
        return [MongoDocumentSerializer.serialize(doc) for doc in self.collection.find()]

