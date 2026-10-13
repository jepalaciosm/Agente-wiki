from langchain_ollama import ChatOllama  # O usa langchain_ollama si prefieres local total (ej. ChatOllama(model="llama3"))
from langgraph.prebuilt import create_react_agent
from tools import buscar_features_produccion

# 1. Definir el LLM (Modelo de Lenguaje)
# Si usas Ollama local: from langchain_ollama import ChatOllama; model = ChatOpenAI(model="llama3")
model = ChatOllama(
    model="qwen2.5-coder",  # Reemplaza por el nombre exacto que te dio 'ollama list' si es distinto (ej. qwen2.5-coder:7b)
    temperature=0           # Temperatura baja para que sea preciso y estructurado en sus informes
)

# 2. Registrar las herramientas del agente
tools = [buscar_features_produccion]

# 3. Definir las System Instructions (El prompt de sistema de agent-wiki)
system_prompt = """
Eres agent-wiki, un Ingeniero de Machine Learning Senior y Arquitecto de Datos especializado en la Gerencia Analítica de Fraudes.
Tu trabajo es ayudar a los científicos de datos del equipo cuando necesitan construir un modelo nuevo.

Flujo de trabajo obligatorio:
1. Analiza el objetivo del nuevo modelo que te proporcione el usuario.
2. Utiliza la herramienta `buscar_features_produccion` para consultar qué variables ya existen en producción que sirvan para este caso (fomentando el reuso).
3. Analiza los vacíos y **recomienda variables nuevas** basadas en patrones típicos de fraude (velocidad, geolocalización, agregaciones temporales, etc.).
4. Devuelve un **informe técnico estructurado** con:
   - Resumen del requerimiento.
   - Features Existentes Recomendadas (Reuso).
   - Recomendación de Nuevas Features (Propuestas con lógica sugerida).
   - Próximos pasos técnicos.
"""

# 4. Crear el Agente ReAct utilizando LangGraph
agent_executor = create_react_agent(
    model, 
    tools, 
    state_modifier=system_prompt
)