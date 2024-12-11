from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from bson import ObjectId


class MongoDocumentSerializer:
    """
    Clase responsable de serializar documentos de MongoDB,
    convirtiendo ObjectId a cadenas serializables por JSON.
    """
    @staticmethod
    def serialize(document):
        if isinstance(document, list):
            return [MongoDocumentSerializer.serialize(doc) for doc in document]
        if isinstance(document, dict):
            return {
                key: str(value) if isinstance(value, ObjectId) else value
                for key, value in document.items()
            }
        return document


class ObjectIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware que utiliza MongoDocumentSerializer para convertir ObjectId en
    respuestas JSON automáticamente.
    """
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        # Serializar el cuerpo de la respuesta si es JSONResponse
        if isinstance(response, JSONResponse):
            response.media = MongoDocumentSerializer.serialize(response.media)
        return response
