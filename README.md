# Agente Wiki

Agente orientado a ayudar a científicos de datos y analistas a auditar features existentes en modelos de producción, reutilizar conocimiento y proponer nuevas variables para modelos de fraude en entidades financieras.

## Objetivos principales

1. Auditoría y reuso: revisar el catálogo de features actuales y filtrar aquellas que sean relevantes, reutilizables o adaptables para un nuevo caso de uso.
2. Recomendación de nuevas features: a partir de un problema de fraude específico, proponer variables que aún no estén en producción y que aporten alto valor predictivo.
3. Generación de informes: entregar respuestas estructuradas en un formato técnico y profesional.

## Estructura del informe de salida

La respuesta del agente debe seguir esta estructura:

1. Resumen del requerimiento
   - Breve análisis del modelo que se desea construir.
2. Features existentes recomendadas (reuso)
   - Nombre de la feature o variable.
   - Modelo(s) actual(es) donde se utiliza.
   - Descripción y por qué es útil para este nuevo modelo.
3. Recomendación de nuevas features
   - Nombre propuesto para la nueva variable.
   - Lógica o definición sugerida.
   - Justificación analítica frente al fraude objetivo.
4. Próximos pasos
   - Recomendaciones técnicas, como validación de nulos, pruebas de estabilidad o drift.

## Reto

Construir un agente local con LangGraph y ChromaDB permite tener control total de la arquitectura y entender en detalle cómo funcionan los agentes de IA modernos.

El proyecto se desarrollará paso a paso usando LangChain para la gestión de datos y herramientas, y LangGraph para orquestar el flujo de razonamiento del agente siguiendo el patrón ReAct (Razonar y Actuar), manteniendo todo 100% local.

## Estructura del proyecto

```text
agent-wiki/
├── data/
│   └── features_produccion.csv      # Catálogo de features actuales de producción
├── src/
│   ├── __init__.py                  # Permite que src sea un paquete de Python
│   ├── tools.py                     # Herramienta de ChromaDB y búsqueda vectorial
│   └── agent.py                     # Prompt del sistema y grafo de LangGraph
├── .env                             # Variables de entorno (API keys, configuración)
├── .gitignore                      # Archivos a ignorar en Git
├── LICENSE                         # Licencia del proyecto
├── README.md                       # Documentación del proyecto
├── requirements.txt                 # Dependencias del proyecto
├── main.py                          # Punto de entrada del agente
└── .venv                           # Entorno virtual (opcional; puede estar ignorado)
```

## Uso

1. Clona el repositorio.
2. Crea y activa un entorno virtual.
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configura tus variables de entorno en `.env`.
5. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

## Estado

Proyecto inicial en desarrollo.
