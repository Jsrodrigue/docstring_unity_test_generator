from pathlib import Path
import hashlib
import pickle
from typing import List, Tuple
from src.core_base.code.code_model import CodeItem
from openai import OpenAI
import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calcula similitud coseno entre dos vectores."""
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)


class RAGManager:
    """
    Manager para RAG de proyectos Python usando CodeItem y embeddings.
    Permite crear, guardar, cargar y consultar bases vectoriales por proyecto.
    """

    def __init__(self, project_path: Path, embedding_model: str = "text-embedding-3-small"):
        self.project_path = project_path.resolve()
        self.embedding_model = embedding_model
        self.client = OpenAI()
        self.db_path = Path(".rag_db") / self._hash_path(project_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.embeddings_file = self.db_path / "embeddings.pkl"
        self.items_embeddings: List[Tuple[CodeItem, List[float]]] = []

    def _hash_path(self, path: Path) -> str:
        """Genera hash único para la ruta del proyecto."""
        return hashlib.sha1(str(path.resolve()).encode()).hexdigest()

    def build(self, code_items: List[CodeItem]):
        """Genera embeddings para todos los CodeItem y guarda la base."""
        texts = [f"{item.imports}\n{item.source}\n{item.docstring}" for item in code_items]
        embeddings = [
            self.client.embeddings.create(input=text, model=self.embedding_model).data[0].embedding
            for text in texts
        ]
        self.items_embeddings = list(zip(code_items, embeddings))
        self._save()
        print(f"[RAG] Base construida con {len(code_items)} items en {self.db_path}")

    def _save(self):
        """Guarda la base vectorial en disco."""
        with open(self.embeddings_file, "wb") as f:
            pickle.dump(self.items_embeddings, f)

    def load(self):
        """Carga la base vectorial desde disco."""
        if self.embeddings_file.exists():
            with open(self.embeddings_file, "rb") as f:
                self.items_embeddings = pickle.load(f)
            print(f"[RAG] Base cargada con {len(self.items_embeddings)} items")
        else:
            print("[RAG] No hay base guardada. Build primero.")

    def query(self, query_text: str, top_k: int = 5) -> List[CodeItem]:
        """Devuelve los CodeItem más relevantes para la query."""
        if not self.items_embeddings:
            raise ValueError("Base vacía. Debes build o load primero.")

        query_emb = self.client.embeddings.create(input=query_text, model=self.embedding_model).data[0].embedding

        # Ordenar por similitud (menor distancia = más relevante)
        scored = [
            (item, cosine_similarity(query_emb, emb))
            for item, emb in self.items_embeddings
        ]
        # Ahora mayor similitud = más relevante
        scored.sort(key=lambda x: x[1], reverse=True)

        top_items = [item for item, _ in scored[:top_k]]
        return top_items


if __name__ == "__main__":
    # --- Crear CodeItems de prueba ---
    item1 = CodeItem(
        name="foo",
        type="function",
        source="def foo(): return 'foo'",
        docstring="Función foo",
        file_path=Path("example1.py"),
        imports=["import os"]
    )
    item2 = CodeItem(
        name="bar",
        type="function",
        source="def bar(): return 'bar'",
        docstring="Función bar",
        file_path=Path("example2.py"),
        imports=["import sys"]
    )

    code_items = [item1, item2]

    # --- Inicializar RAG ---
    rag = RAGManager(project_path=Path("."))

    # --- Construir base ---
    print("🔹 Construyendo base RAG...")
    rag.build(code_items)

    # --- Cargar base desde disco ---
    print("🔹 Cargando base RAG desde disco...")
    rag.load()

    # --- Consulta de prueba ---
    query = "quiero la función foo"
    print(f"🔹 Consultando con: '{query}'")
    results = rag.query(query, top_k=2)

    print("Resultados top:")
    for r in results:
        print("-", r.name, "-", r.file_path)
