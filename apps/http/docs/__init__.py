"""
Módulo para cargar y proporcionar documentación de la API.
"""
import json
import os
from pathlib import Path


class ApiDocs:
    """
    Clase para cargar y proporcionar documentación de la API.
    """
    _docs = {}
    
    @classmethod
    def load_docs(cls):
        docs_dir = Path(__file__).parent
        for file in docs_dir.glob('*.json'):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    resource_name = file.stem
                    cls._docs[resource_name] = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar la documentación {file}: {str(e)}")

    @classmethod
    def get_docs(cls, resource, endpoint=None):
        if not cls._docs:
            cls.load_docs()
            
        if resource not in cls._docs:
            return {}
            
        if endpoint:
            return cls._docs[resource].get(endpoint, {})
        else:
            return cls._docs[resource]

# Cargar documentación al iniciar
ApiDocs.load_docs() 