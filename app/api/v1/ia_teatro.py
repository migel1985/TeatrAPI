from flask import Blueprint, jsonify, request
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from models.escenas import create_escena_db, get_escenas_by_capitulo
import os

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
chat_historiales = {}  # Diccionario de historiales por session_id

prompt = ChatPromptTemplate.from_messages([
    ("system", """Eres una experta en teatro amateur. Tu misión es ayudar al usuario a preparar clases y sesiones de teatro. Me vas a hablar como una generación Z con sus frases incomprensibles.
                    Quiero que me des datos contrastados y reales. CONTEXTO ADICIONAL: {extra_context}"""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

ia_teatro_bp = Blueprint('ia_teatro', __name__, url_prefix='/teatrapi')

@ia_teatro_bp.route('/hablar_con_ia', methods=['POST'])
def hablar_con_ia():
    try:
        data = request.get_json()
        mensaje = data.get('mensaje', '').strip()
        descCapitulo = data.get('descCapitulo', '').strip()
        capitulo_id = int(data.get('capitulo_id', 0))  # ← INT para DB
        user_id = data.get('user_id', 0)
        # print("Miguel: Antes del if: ", mensaje)
        # Inicializar historial si no existe
        if capitulo_id not in chat_historiales:
            chat_historiales[capitulo_id] = ChatMessageHistory()
            # print(f"Nuevo historial creado para {capitulo_id}")
        
        llm = ChatGroq(
            model="meta-llama/llama-4-maverick-17b-128e-instruct", 
            temperature=0,
            groq_api_key=GROQ_API_KEY
        )
        
        chain = prompt | llm
        
        def get_memory(session_id):
            if session_id not in chat_historiales:
                chat_historiales[session_id] = ChatMessageHistory()
            return chat_historiales[session_id]
        
        cadena_historial = RunnableWithMessageHistory(
            chain,
            get_memory,  # ← Función explícita, más segura
            input_messages_key="input",
            history_messages_key="history",
        )
        
        
        response = cadena_historial.invoke(
            {"input": mensaje, "extra_context": descCapitulo},
            config={"configurable": {"session_id": capitulo_id}}
        )
        
        ai_response = response.content



        # ✅ NUEVA PARTE: GUARDAR ESCENA EN DB
        
        
        escena = create_escena_db(
            chapter_id=capitulo_id,
            query=mensaje,        # Pregunta limpia del usuario
            response=ai_response, # Respuesta de la IA
            sources=None,         # Opcional para RAG futuro
            obra_id=None       # Relaciona con obra/usuario
        )
        
        print(f"💾 Escena guardada: ID {escena['id']}")
        
        return jsonify({
            'success': True, 
            'respuesta': ai_response,
            'escena_id': escena['id']  # Para frontend si quiere usarlo
        }), 200

        
    except KeyError as e:
        print(f"KeyError - Session no encontrada: {e}")
        return jsonify({'success': False, 'error': f'Sesión {capitulo_id} no encontrada'}), 400
    except Exception as e:
        print(f"Error completo: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500



# ✅ AÑADIR ESTE ENDPOINT arriba del hablar_con_ia
@ia_teatro_bp.route('/escenas/<int:capitulo_id>', methods=['GET'])
def get_escenas(capitulo_id: int):
    try:
        
        escenas = get_escenas_by_capitulo(capitulo_id)
        return jsonify({'success': True, 'escenas': escenas}), 200
    except Exception as e:
        print(f"Error escenas: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500