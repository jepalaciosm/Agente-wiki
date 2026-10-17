from src.agent import agent_executor

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
    # Requerimiento de prueba de un usuario simulado
    query_usuario = (
        "Hola agent-wiki, necesito crear un nuevo modelo de Machine Learning "
        "para detectar fraude en {query_usuario} "
        "¿Qué features actuales puedo reutilizar y qué variables nuevas me recomiendas crear?"
    )
    
    # Invocación del grafo de LangGraph
    response = agent_executor.invoke({
        "messages": [("user", query_usuario)]
    })
    
    # Imprimir la respuesta final del agente
    print("==================================================")
    print("\n[INFORME GENERADO POR AGENT-WIKI]:\n")
    print("==================================================")
    print(response["messages"][-1].content)

if __name__ == "__main__":
    run_agent()