# Agente IA — Gmail + WhatsApp

Proyecto unificado con dos bots de IA que comparten la misma base de datos Supabase.

## Estructura

```
├── email_agent.py          # Bot de Gmail
├── bot_was.py              # Bot de WhatsApp
├── whatsapp_agent.py       # Runner del bot de WhatsApp (GitHub Actions)
├── supabase_client.py      # BD compartida (email + phone)
├── calendar_client.py      # Google Calendar (usado por Gmail bot)
├── pdf_context.py          # Carga PDF de documentación
├── documentacion_empresa.pdf
├── schema.sql              # Schema unificado de Supabase
├── requirements.txt
└── .github/workflows/
    ├── email-agent.yml     # Cron Gmail (cada 5 min)
    └── whatsapp.yml        # Cron WhatsApp (cada 1 min)
```

## Secrets de GitHub necesarios

| Secret | Descripción |
|--------|-------------|
| `GROQ_API_KEY` | API key de Groq |
| `GMAIL_CREDENTIALS_JSON` | Token OAuth de Google |
| `SUPABASE_URL` | URL del proyecto Supabase |
| `SUPABASE_KEY` | Anon Key de Supabase (empieza por eyJ...) |
| `GOOGLE_CALENDAR_ID` | ID del calendario (primary) |
| `COMPANY_NAME` | Nombre de la empresa |
| `CONTACT_INFO` | Email/teléfono de contacto para escalaciones |
| `EVENT_DURATION_MINUTES` | Duración de cita en minutos (ej: 60) |
| `MAX_CITAS_ACTIVAS` | Máximo de citas por cliente (ej: 2) |
| `TWILIO_ACCOUNT_SID` | Account SID de Twilio |
| `TWILIO_AUTH_TOKEN` | Auth Token de Twilio |
| `TWILIO_WHATSAPP_NUM` | Número Twilio (ej: whatsapp:+14155238886) |

## Base de datos

Ejecuta `schema.sql` en el SQL Editor de Supabase para crear la tabla unificada.
