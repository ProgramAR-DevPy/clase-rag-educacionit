import os
import openai
from dotenv import load_dotenv
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader, DirectoryLoader
import streamlit as st

# Cargar variables de entorno
load_dotenv()

class RAGSystem:
    """
    Sistema RAG (Retrieval-Augmented Generation) completo
    
    Este sistema permite:
    1. Cargar documentos de texto
    2. Crear embeddings y almacenarlos en una base de datos vectorial
    3. Realizar búsquedas semánticas
    4. Generar respuestas basadas en el contexto recuperado
    """
    
    def __init__(self, openai_api_key=None):
        """
        Inicializar el sistema RAG
        
        Args:
            openai_api_key (str): Clave API de OpenAI
        """
        # Configurar OpenAI API
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        elif not os.getenv("OPENAI_API_KEY"):
            raise ValueError("Se requiere una clave API de OpenAI")
        
        # Inicializar componentes
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        self.vectorstore = None
        self.qa_chain = None
        
        # Configurar el divisor de texto
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_documents(self, directory_path="./documentos"):
        """
        Cargar documentos desde un directorio
        
        Args:
            directory_path (str): Ruta al directorio con documentos
        
        Returns:
            list: Lista de documentos cargados
        """
        try:
            # Cargar documentos de texto desde el directorio
            loader = DirectoryLoader(
                directory_path, 
                glob="*.txt",
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'}
            )
            documents = loader.load()
            
            if not documents:
                st.warning(f"No se encontraron documentos en {directory_path}")
                return []
            
            # Dividir documentos en chunks
            texts = self.text_splitter.split_documents(documents)
            
            st.success(f"✅ Cargados {len(documents)} documentos, divididos en {len(texts)} fragmentos")
            return texts
            
        except Exception as e:
            st.error(f"Error cargando documentos: {str(e)}")
            return []
    
    def create_vectorstore(self, documents):
        """
        Crear la base de datos vectorial con los documentos
        
        Args:
            documents (list): Lista de documentos procesados
        """
        try:
            if not documents:
                st.error("No hay documentos para procesar")
                return
            
            # Crear base de datos vectorial con ChromaDB
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory="./chroma_db"
            )
            
            # Crear cadena de pregunta-respuesta
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 3}
                ),
                return_source_documents=True
            )
            
            st.success("✅ Base de datos vectorial creada exitosamente")
            
        except Exception as e:
            st.error(f"Error creando vectorstore: {str(e)}")
    
    def query(self, question):
        """
        Realizar una consulta al sistema RAG
        
        Args:
            question (str): Pregunta del usuario
        
        Returns:
            dict: Respuesta y documentos fuente
        """
        if not self.qa_chain:
            return {
                "answer": "❌ El sistema no está inicializado. Por favor, carga los documentos primero.",
                "sources": []
            }
        
        try:
            # Ejecutar la consulta
            result = self.qa_chain({"query": question})
            
            # Extraer fuentes
            sources = []
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    sources.append({
                        "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                        "source": doc.metadata.get("source", "Desconocido")
                    })
            
            return {
                "answer": result["result"],
                "sources": sources
            }
            
        except Exception as e:
            return {
                "answer": f"❌ Error procesando la consulta: {str(e)}",
                "sources": []
            }
    
    def get_similar_documents(self, query, k=3):
        """
        Obtener documentos similares sin generar respuesta
        
        Args:
            query (str): Consulta de búsqueda
            k (int): Número de documentos a retornar
        
        Returns:
            list: Lista de documentos similares
        """
        if not self.vectorstore:
            return []
        
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            return [
                {
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "Desconocido"),
                    "score": "N/A"
                }
                for doc in docs
            ]
        except Exception as e:
            st.error(f"Error en búsqueda de similitud: {str(e)}")
            return []


def main():
    """
    Función principal para la interfaz de Streamlit
    """
    st.set_page_config(
        page_title="Sistema RAG - Demostración",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Sistema RAG - Retrieval-Augmented Generation")
    st.markdown("### Demostración educativa de RAG para programadores")
    
    # Sidebar para configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        openai_key = st.text_input(
            "Clave API OpenAI", 
            type="password",
            help="Ingresa tu clave API de OpenAI"
        )
        
        if st.button("🔄 Reiniciar Sistema"):
            st.rerun()
    
    # Inicializar sistema RAG
    if openai_key:
        try:
            rag_system = RAGSystem(openai_key)
            st.success("✅ Sistema RAG inicializado")
        except Exception as e:
            st.error(f"❌ Error inicializando RAG: {str(e)}")
            return
    else:
        st.warning("⚠️ Ingresa tu clave API de OpenAI en la barra lateral")
        return
    
    # Tabs para diferentes funcionalidades
    tab1, tab2, tab3 = st.tabs(["📄 Cargar Documentos", "❓ Hacer Consultas", "🔍 Búsqueda Semántica"])
    
    with tab1:
        st.header("📄 Cargar y Procesar Documentos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Cargar Documentos")
            directory_path = st.text_input("Directorio de documentos", value="./documentos")
            
            if st.button("📁 Cargar Documentos"):
                with st.spinner("Cargando documentos..."):
                    documents = rag_system.load_documents(directory_path)
                    if documents:
                        st.session_state.documents = documents
        
        with col2:
            st.subheader("Crear Base de Datos Vectorial")
            if st.button("🔨 Crear Vectorstore"):
                if hasattr(st.session_state, 'documents'):
                    with st.spinner("Creando base de datos vectorial..."):
                        rag_system.create_vectorstore(st.session_state.documents)
                        st.session_state.rag_system = rag_system
                else:
                    st.error("Primero carga los documentos")
    
    with tab2:
        st.header("❓ Consultas al Sistema RAG")
        
        if hasattr(st.session_state, 'rag_system'):
            question = st.text_input("Escribe tu pregunta:", placeholder="¿Qué información necesitas?")
            
            if st.button("🚀 Consultar") and question:
                with st.spinner("Procesando consulta..."):
                    result = st.session_state.rag_system.query(question)
                    
                    # Mostrar respuesta
                    st.subheader("📝 Respuesta:")
                    st.write(result["answer"])
                    
                    # Mostrar fuentes
                    if result["sources"]:
                        st.subheader("📚 Fuentes utilizadas:")
                        for i, source in enumerate(result["sources"], 1):
                            with st.expander(f"Fuente {i}: {source['source']}"):
                                st.write(source["content"])
        else:
            st.info("Primero carga y procesa los documentos en la pestaña anterior")
    
    with tab3:
        st.header("🔍 Búsqueda Semántica")
        
        if hasattr(st.session_state, 'rag_system'):
            search_query = st.text_input("Término de búsqueda:", placeholder="Buscar documentos similares...")
            num_results = st.slider("Número de resultados", 1, 10, 3)
            
            if st.button("🔍 Buscar") and search_query:
                docs = st.session_state.rag_system.get_similar_documents(search_query, num_results)
                
                if docs:
                    st.subheader(f"📄 {len(docs)} documentos encontrados:")
                    for i, doc in enumerate(docs, 1):
                        with st.expander(f"Documento {i}"):
                            st.write(f"**Fuente:** {doc['source']}")
                            st.write(doc["content"])
                else:
                    st.info("No se encontraron documentos similares")
        else:
            st.info("Primero carga y procesa los documentos")


if __name__ == "__main__":
    main() 