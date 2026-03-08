"""
supabase_client.py — BD unificada para bot de Gmail y bot de WhatsApp.

Esquema de la tabla `citas`:
  - email       TEXT (nullable)
  - phone       TEXT (nullable)
  - event_id    TEXT NOT NULL
  - fecha_cita  TIMESTAMPTZ NOT NULL
  - created_at  TIMESTAMPTZ DEFAULT NOW()

Al menos uno de email o phone debe estar relleno.
"""

import logging
import os
import re
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

MAX_CITAS_ACTIVAS = int(os.environ.get("MAX_CITAS_ACTIVAS", "2"))


def clean_email(raw: str) -> str:
    m = re.search(r'<(.+?)>', raw)
    return m.group(1).strip() if m else raw.strip()


def clean_phone(raw: str) -> str:
    return raw.strip()


def get_supabase():
    from supabase import create_client
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Faltan SUPABASE_URL o SUPABASE_KEY.")
    return create_client(url, key)


def guardar_cita(event_id: str, fecha_cita: datetime,
                 email: str = None, phone: str = None) -> bool:
    try:
        db = get_supabase()
        row = {"event_id": event_id, "fecha_cita": fecha_cita.isoformat()}
        if email:
            row["email"] = clean_email(email)
        if phone:
            row["phone"] = clean_phone(phone)
        db.table("citas").insert(row).execute()
        logger.info(f"💾 Cita guardada | email={email} phone={phone} | {event_id}")
        return True
    except Exception as e:
        logger.error(f"❌ Error guardando cita: {e}")
        return False


def obtener_ultimo_event_id(email: str = None, phone: str = None) -> str | None:
    try:
        db = get_supabase()
        q = db.table("citas").select("event_id").order("created_at", desc=True).limit(1)
        if email:
            q = q.eq("email", clean_email(email))
        elif phone:
            q = q.eq("phone", clean_phone(phone))
        result = q.execute()
        return result.data[0]["event_id"] if result.data else None
    except Exception as e:
        logger.error(f"❌ Error consultando Supabase: {e}")
        return None


def obtener_todas_citas_cliente(email: str = None, phone: str = None) -> list[dict]:
    try:
        db = get_supabase()
        ahora = datetime.now().astimezone().isoformat()
        q = db.table("citas").select("event_id, fecha_cita").gt("fecha_cita", ahora).order("fecha_cita")
        if email:
            q = q.eq("email", clean_email(email))
        elif phone:
            q = q.eq("phone", clean_phone(phone))
        return q.execute().data or []
    except Exception as e:
        logger.error(f"❌ Error obteniendo citas: {e}")
        return []


def contar_citas_futuras(email: str = None, phone: str = None) -> int:
    try:
        db = get_supabase()
        ahora = datetime.now().astimezone().isoformat()
        q = db.table("citas").select("event_id", count="exact").gt("fecha_cita", ahora)
        if email:
            q = q.eq("email", clean_email(email))
        elif phone:
            q = q.eq("phone", clean_phone(phone))
        result = q.execute()
        return result.count if result.count is not None else len(result.data)
    except Exception:
        return 0


def eliminar_cita(event_id: str, email: str = None, phone: str = None) -> bool:
    try:
        db = get_supabase()
        q = db.table("citas").delete().eq("event_id", event_id)
        if email:
            q = q.eq("email", clean_email(email))
        elif phone:
            q = q.eq("phone", clean_phone(phone))
        q.execute()
        logger.info(f"🗑️ Cita eliminada: {event_id}")
        return True
    except Exception as e:
        logger.error(f"❌ Error eliminando cita: {e}")
        return False


def obtener_event_id_por_fecha(fecha: datetime,
                                email: str = None, phone: str = None) -> str | None:
    try:
        db = get_supabase()
        if fecha.hour == 0 and fecha.minute == 0:
            desde = fecha.replace(hour=0, minute=0, second=0).isoformat()
            hasta = fecha.replace(hour=23, minute=59, second=59).isoformat()
        else:
            desde = (fecha - timedelta(hours=2)).isoformat()
            hasta = (fecha + timedelta(hours=2)).isoformat()
        q = (db.table("citas").select("event_id, fecha_cita")
             .gte("fecha_cita", desde).lte("fecha_cita", hasta)
             .order("fecha_cita").limit(1))
        if email:
            q = q.eq("email", clean_email(email))
        elif phone:
            q = q.eq("phone", clean_phone(phone))
        result = q.execute()
        return result.data[0]["event_id"] if result.data else None
    except Exception as e:
        logger.error(f"❌ Error buscando cita por fecha: {e}")
        return None


def obtener_citas_futuras_todas() -> list[dict]:
    try:
        db = get_supabase()
        ahora = datetime.now().astimezone().isoformat()
        result = (
            db.table("citas")
            .select("email, phone, event_id, fecha_cita")
            .gt("fecha_cita", ahora)
            .execute()
        )
        return result.data or []
    except Exception as e:
        logger.error(f"❌ Error obteniendo citas futuras: {e}")
        return []
