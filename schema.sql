-- Schema unificado para Gmail bot + WhatsApp bot
-- Al menos uno de email o phone debe estar relleno.

CREATE TABLE IF NOT EXISTS citas (
  id          BIGSERIAL PRIMARY KEY,
  email       TEXT,
  phone       TEXT,
  event_id    TEXT NOT NULL,
  fecha_cita  TIMESTAMPTZ NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT check_contacto CHECK (email IS NOT NULL OR phone IS NOT NULL)
);

-- Índices para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_citas_email ON citas(email);
CREATE INDEX IF NOT EXISTS idx_citas_phone ON citas(phone);
CREATE INDEX IF NOT EXISTS idx_citas_fecha ON citas(fecha_cita);

-- Desactivar RLS (el acceso se controla por API key)
ALTER TABLE citas DISABLE ROW LEVEL SECURITY;
