import pandas as pd
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.tools import tool

# 1. Cargar el CSV de features de producción
# Asegúrate de tener un CSV de ejemplo en tu entorno
csv_path = Path(__file__).resolve().parents[1] / "data" / "features_produccion.csv"
df = pd.read_csv(csv_path)

# 2. Convertir cada fila en un texto enriquecido para que el embedding capture el contexto
texts = []
metadatas = []
for _, row in df.iterrows():
    text = (
        f"Feature: {row['feature_name']} | "
        f"Modelo Actual: {row['modelo_actual']} | "
        f"Tipo: {row['tipo']} | "
        f"Descripción: {row['descripcion']}"
    )
    texts.append(text)
    metadatas.append({"feature_name": row["feature_name"], "modelo": row["modelo_actual"]})

# 3. Usar embeddings multilingües desde Ollama, sin descargar modelos de Hugging Face
embeddings = OllamaEmbeddings(model="qwen3-embedding:0.6b")

# 4. Crear la base de datos vectorial en memoria con Chroma
vectorstore = Chroma.from_texts(
    texts=texts,
    embedding=embeddings,
    metadatas=metadatas,
    collection_name="fraud_features_wiki"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 5. Definir la Tool que usará el Agente
@tool
def buscar_features_produccion(query: str) -> str:
    """
    Busca en el catálogo de producción de la gerencia de fraudes características (features) 
    existentes que sean similares, reutilizables o complementarias para un nuevo modelo.
    Utiliza esta herramienta cuando necesites proponer reuso de código o variables.
    """
    docs = retriever.invoke(query)
    if not docs:
        return "No se encontraron features similares en la base de datos actual."
    
    resultados = "\n\n".join([f"- {doc.page_content}" for doc in docs])
    return f"Features encontradas en producción:\n{resultados}"