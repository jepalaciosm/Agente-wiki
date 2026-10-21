from src.agent import agent_executor
from src.reporting import generar_reporte_html

def run_agent():
    print("--- Inicializando agent-wiki ---")
    print("==================================================")
    print("🤖 Bienvenido a agent-wiki (Gerencia Analítica de Fraudes)")
    print("==================================================")
    print("Escribe la idea o el objetivo del nuevo modelo de fraude que deseas crear.")
    # print("Ejemplo: 'Necesito un modelo para detectar fraude en créditos de consumo rápido en la app móvil.'\n")
    
    # Capturar la idea directamente desde la consola (input del usuario)
    query_usuario = input("👉 Ingresa la idea de tu nuevo modelo: ")
    
    if not query_usuario.strip():
        print("La consulta no puede estar vacía.")
        return

    mensaje_usuario = f"""
Quiero diseñar features para un modelo de detección de fraude.

Tema o caso de uso descrito por el usuario:
{query_usuario}

Analiza este caso y:
1. Resume el tipo de fraude, el comportamiento que se busca detectar y el contexto disponible.
2. Consulta el catálogo de producción con la herramienta buscar_features_produccion y recomienda las features existentes que sean reutilizables o adaptables. Explica por qué son pertinentes.
3. Propón features nuevas que cubran vacíos del catálogo y estén vinculadas al caso descrito; evita repetir features existentes con otro nombre.
4. Para cada feature nueva, especifica su nombre, lógica de cálculo, entidad o nivel de agregación, ventana temporal, datos requeridos y justificación frente al fraude.
5. Señala los supuestos y riesgos que deben validarse, como disponibilidad de datos, fuga de información, sesgo y estabilidad temporal.

Responde en español, con recomendaciones concretas y priorizadas. No afirmes que existen datos o features si no están confirmados en el catálogo; indica claramente cualquier supuesto.
"""

    print("Enviando consulta al agente...")
    response = agent_executor.invoke({
        "messages": [("user", mensaje_usuario)]
    })

    # Imprimir la respuesta final del agente
    print("==================================================")
    print("\n[INFORME GENERADO POR AGENT-WIKI]:\n")
    print("==================================================")
    contenido_informe = response["messages"][-1].content
    print(contenido_informe)

    ruta_reporte = generar_reporte_html.invoke({"contenido": contenido_informe})
    print(f"\nReporte HTML guardado en: {ruta_reporte}")

if __name__ == "__main__":
    run_agent()