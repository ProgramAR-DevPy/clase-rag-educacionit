# 🤖 Proyecto RAG Educativo

Un sistema completo de **Retrieval-Augmented Generation (RAG)** diseñado para enseñar conceptos de IA a programadores. Este proyecto combina la potencia de OpenAI GPT con búsqueda semántica para crear un asistente inteligente basado en tus propios documentos.

## 🎯 Objetivos del Proyecto

- **Demostrar** cómo funciona RAG en la práctica
- **Enseñar** los componentes clave de un sistema RAG
- **Proporcionar** una base modificable para proyectos personales
- **Mostrar** mejores prácticas en el desarrollo con IA

## 🚀 Características

### ✨ **Sistema RAG Completo**
- Carga automática de documentos
- Generación de embeddings con OpenAI
- Base de datos vectorial con ChromaDB
- Búsqueda semántica inteligente
- Generación de respuestas contextualizadas

### 🖥️ **Interfaz Dual**
- **Web**: Interfaz interactiva con Streamlit
- **Terminal**: Script de línea de comandos

### 📚 **Documentos de Ejemplo**
- Inteligencia Artificial
- Machine Learning
- Programación en Python

### 🎓 **Material Educativo**
- Documentación completa de RAG
- Explicaciones paso a paso
- Ejemplos prácticos
- Ejercicios para estudiantes

## 📋 Requisitos

### **Sistema**
- Python 3.8 o superior
- Acceso a internet (para OpenAI API)
- 2GB de espacio libre (base de datos vectorial)

### **Clave API**
- Cuenta de OpenAI con créditos disponibles
- Clave API (obtener en [OpenAI Platform](https://platform.openai.com/api-keys))

## 🛠️ Instalación

### **1. Clonar/Descargar el Proyecto**
```bash
git clone <tu-repositorio>
cd clase-rag
```

### **2. Crear Entorno Virtual (Recomendado)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### **3. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **4. Configurar Variables de Entorno**
```bash
# Copiar archivo de ejemplo
cp ejemplo.env .env

# Editar .env y agregar tu clave API
OPENAI_API_KEY=sk-tu_clave_aqui
```

## 🎮 Uso

### **Interfaz Web (Recomendado)**
```bash
streamlit run rag_system.py
```

1. **Abrir** http://localhost:8501 en tu navegador
2. **Configurar** tu clave API en la barra lateral
3. **Cargar** documentos desde la pestaña correspondiente
4. **Crear** la base de datos vectorial
5. **Realizar** consultas y explorar resultados

### **Terminal**
```bash
python run_rag.py
```

Perfecto para pruebas rápidas y demostraciones en vivo.

## 📁 Estructura del Proyecto

```
Clase RAG/
├── 📄 rag_system.py          # Sistema principal con interfaz Streamlit
├── 🖥️ run_rag.py            # Script para terminal
├── 📋 requirements.txt       # Dependencias Python
├── 🔧 ejemplo.env           # Plantilla de variables de entorno
├── 📚 RAG_Explicacion.md    # Documentación completa de RAG
├── 📖 README.md             # Este archivo
└── 📂 documentos/           # Documentos de ejemplo
    ├── inteligencia_artificial.txt
    ├── machine_learning.txt
    └── python_programming.txt
```

## 🔧 Personalización

### **Agregar Tus Documentos**
1. Coloca archivos `.txt` (UTF-8) en `documentos/`
2. Recarga la aplicación
3. Vuelve a crear la base de datos vectorial

### **Modificar Parámetros**
```python
# rag_system.py - línea ~45
self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Tamaño de fragmentos
    chunk_overlap=200,    # Solapamiento
)

# rag_system.py - línea ~38
self.llm = ChatOpenAI(
    temperature=0.7,      # Creatividad (0-1)
    model_name="gpt-3.5-turbo"  # Modelo OpenAI
)
```

## 📊 Costos Estimados

### **OpenAI API**
- **GPT-3.5-turbo**: ~$0.002 por 1K tokens
- **Embeddings**: ~$0.0001 por 1K tokens
- **Consulta típica**: $0.01 - $0.05

### **Ejemplo de Uso**
- 100 consultas ≈ $2-5 USD
- Base de 50 documentos ≈ $1-2 USD (una vez)

## ❓ Preguntas Frecuentes

### **¿Funciona sin internet?**
No, requiere conexión para OpenAI API. Para uso offline, considera modelos locales como Ollama.

### **¿Puedo usar otros modelos de lenguaje?**
Sí, el código es extensible. Puedes integrar Hugging Face, Anthropic Claude, etc.

### **¿Soporta archivos PDF?**
Actualmente solo `.txt`. Como ejercicio, puedes agregar soporte para PDF usando PyPDF2.

### **¿Es seguro para datos sensibles?**
Los datos se envían a OpenAI. Para información confidencial, considera modelos locales.

## 🎓 Para Profesores

### **Objetivos de Aprendizaje**
- Comprender arquitectura RAG
- Experimentar con embeddings vectoriales
- Aprender integración de APIs
- Practicar desarrollo con IA

### **Sugerencias de Clase**
1. **Demo en vivo** con la interfaz web
2. **Explicar** cada componente del código
3. **Comparar** respuestas con/sin RAG
4. **Asignar** ejercicios de personalización

### **Ejercicios Propuestos**
- Adaptar con documentos del curso
- Comparar diferentes modelos de embeddings
- Implementar métricas de evaluación
- Crear API REST para el sistema

## 🎯 Para Estudiantes

### **Antes de Empezar**
1. Lee `RAG_Explicacion.md` completamente
2. Ejecuta el sistema con los documentos ejemplo
3. Experimenta con diferentes consultas

### **Ejercicios Básicos**
1. **Personalización**: Cambia documentos por tu contenido
2. **Parámetros**: Ajusta chunk_size y temperature
3. **Comparación**: Prueba con/sin contexto RAG

### **Proyectos Avanzados**
1. Interfaz de chat conversacional
2. Soporte para múltiples formatos
3. Sistema de evaluación de respuestas
4. Integración con bases de datos

## 🐛 Solución de Problemas

### **Error: "No module named..."**
```bash
pip install -r requirements.txt
```

### **Error: "Invalid API key"**
1. Verifica tu clave en [OpenAI Platform](https://platform.openai.com/api-keys)
2. Asegúrate de tener créditos disponibles
3. Revisa el archivo `.env`

### **Error: "No documents found"**
1. Verifica que hay archivos `.txt` en `documentos/`
2. Asegúrate de que están codificados en UTF-8
3. Revisa la ruta especificada

### **Streamlit no abre automáticamente**
```bash
# Abrir manualmente
http://localhost:8501
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. **Fork** el proyecto
2. **Crea** una rama para tu feature
3. **Commit** tus cambios
4. **Push** a la rama
5. **Abre** un Pull Request

### **Ideas para Contribuir**
- Soporte para más formatos de archivo
- Mejoras en la interfaz de usuario
- Optimizaciones de rendimiento
- Documentación adicional
- Ejemplos de casos de uso

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **OpenAI** por los modelos GPT y embeddings
- **LangChain** por el framework RAG
- **Streamlit** por la interfaz web sencilla
- **ChromaDB** por la base de datos vectorial

---

## 📞 Soporte

¿Tienes preguntas? 

- 📧 **Email**: [tu-email@ejemplo.com]
- 💬 **Discord**: [Tu servidor]
- 📱 **Twitter**: [@tu_usuario]

---

**¡Esperamos que disfrutes aprendiendo sobre RAG!** 🚀 