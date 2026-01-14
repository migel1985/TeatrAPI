from app.core.database import get_db_connection
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import List, Dict, Any


def get_escenas_by_capitulo(capitulo_id: int) -> List[Dict[str, Any]]:
    """Obtiene todas las escenas (Q&A) de un capítulo específico"""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, chapter_id, query, response, sources, obra_id, created_at
                FROM scenes 
                WHERE chapter_id = %s 
                ORDER BY created_at
            """, (capitulo_id,))
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def create_escena_db(
    chapter_id: int, 
    query: str, 
    response: str, 
    sources: str = None, 
    obra_id: int = None
) -> Dict[str, Any]:
    """Crea una nueva escena guardando pregunta y respuesta de la IA"""
    conn = get_db_connection()
    try:
        print("Miguel: obra_id ", obra_id)
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO scenes (chapter_id, query, response, sources, obra_id, created_at)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                RETURNING id, chapter_id, query, response, sources, obra_id, created_at
            """, (chapter_id, query, response, sources, obra_id))
            row = cur.fetchone()
            print(f"✅ Miguel: Escena guardada ID {row['id']} para capítulo {chapter_id}")
            conn.commit()
            return dict(row)
    except Exception as e:
        print(f"❌ Miguel: ERROR creando escena: {str(e)}")
        conn.rollback()
        raise e
    finally:
        conn.close()


def delete_escena_db(escena_id: int) -> bool:
    """Elimina una escena específica"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM scenes WHERE id = %s
            """, (escena_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"❌ Miguel: ERROR eliminando escena: {str(e)}")
        conn.rollback()
        raise e
    finally:
        conn.close()
