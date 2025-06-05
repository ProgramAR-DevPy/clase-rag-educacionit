#!/usr/bin/env python3
"""
Script simple para ejecutar RAG desde línea de comandos
Útil para pruebas rápidas y demostraciones
"""

import os
from dotenv import load_dotenv
from rag_system import RAGSystem

def main():
    """
    Función principal para ejecutar RAG desde terminal
    """
    print("🤖 Sistema RAG - Demostración en Terminal")
    print("=" * 50)
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar clave API
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: No se encontró OPENAI_API_KEY")
        print("Configura tu clave API en el archivo .env")
        return
    
    try:
        # Inicializar sistema RAG
        print("🔧 Inicializando sistema RAG...")
        rag_system = RAGSystem()
        
        # Cargar documentos
        print("📄 Cargando documentos...")
        documents = rag_system.load_documents("./documentos")
        
        if not documents:
            print("❌ No se encontraron documentos en ./documentos")
            return
        
        # Crear base de datos vectorial
        print("🔨 Creando base de datos vectorial...")
        rag_system.create_vectorstore(documents)
        
        print("✅ Sistema listo! Puedes hacer consultas.")
        print("-" * 50)
        
        # Loop de consultas
        while True:
            print("\n💬 Escribe tu pregunta (o 'quit' para salir):")
            question = input("> ").strip()
            
            if question.lower() in ['quit', 'exit', 'salir']:
                print("👋 ¡Hasta luego!")
                break
            
            if not question:
                continue
            
            print("\n🔍 Procesando consulta...")
            result = rag_system.query(question)
            
            # Mostrar respuesta
            print("\n📝 Respuesta:")
            print("-" * 30)
            print(result["answer"])
            
            # Mostrar fuentes
            if result["sources"]:
                print("\n📚 Fuentes utilizadas:")
                print("-" * 30)
                for i, source in enumerate(result["sources"], 1):
                    print(f"{i}. {source['source']}")
                    print(f"   {source['content'][:100]}...")
                    print()
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 