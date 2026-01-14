# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey  # ← NO LO USES
# from app.core.database import Base  # ← ELIMINA
from app.core.database import get_db_connection
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# SOLO FUNCIONES:
def get_user_capitulos(user_id: int):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select id, usuario_id, titulo, descripcion, created_at, updated_at
                from chapters where usuario_id = %s order by updated_at desc
            """, (user_id,))
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()

def create_capitulo_db(user_id: int, titulo: str = "Nuevo Capítulo", descripcion: str = ""):
    """Crea capítulo con estructura REAL de tabla chapters"""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO chapters (usuario_id, titulo, descripcion, created_at, updated_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING id, titulo, 0 as escenas, updated_at, descripcion
            """, (user_id, titulo, descripcion))
            row = cur.fetchone()
            print(f"✅ Miguel: Fila insertada: {row}")  # DEBUG
            conn.commit()  # ← ¡ESTO FALTABA!
            return row
    except Exception as e:
        print(f"❌ Miguel: ERROR: {str(e)}")
        conn.rollback()  # ← ROLLBACK en error
        raise e  # ← RELANZA para que el frontend lo vea
    finally:
        conn.close()

