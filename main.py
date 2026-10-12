from agent import agent_executor

def run_agent():
    print("--- Inicializando agent-wiki ---")
    
    # Requerimiento de prueba de un usuario simulado
    query_usuario = (
        "Hola agent-wiki, necesito crear un nuevo modelo de Machine Learning "
        "para detectar fraude en transacciones de e-commerce mediante tarjetas de crédito "
        "enfocado en compras de alto valor hechas en la madrugada. ¿Qué features actuales "
        "puedo reutilizar y qué variables nuevas me recomiendas crear?"
    )
    
    # Invocación del grafo de LangGraph
    response = agent_executor.invoke({
        "messages": [("user", query_usuario)]
    })
    
    # Imprimir la respuesta final del agente
    print("\n[INFORME GENERADO POR AGENT-WIKI]:\n")
    print(response["messages"][-1].content)

if __name__ == "__main__":
    run_agent()