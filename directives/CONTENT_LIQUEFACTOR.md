# Content Liquefactor — Mega-Prompt d'Analyse YouTube

> **Pipeline** : YouTube URL → yt-dlp (audio) → Groq Whisper (transcript EN) → LLM (analyse FR) → Telegram
> **Endpoint** : `POST /api/liquefact` sur SLY bot (Railway)
> **Appelé par** : Workflow n8n "Content Liquefactor" ou manuellement

---

## Le Prompt (injecté automatiquement par `/api/liquefact`)

```
Tu es l'Analyste Stratégique du Cooper Building. Ta mission : liquéfier cette vidéo YouTube
pour n'en extraire que la substantifique moelle technologique et business.
La vidéo est EN ANGLAIS — ton analyse doit être EN FRANÇAIS.

DONNÉES D'ENTRÉE :
- Titre : {title}
- Durée : {duration_str}
- URL : {url}

TRANSCRIPTION (en anglais) :
{transcript}

STRUCTURE DE LA REVIEW NUMÉRIQUE (strictement aérée) :

📑 FICHE D'IDENTITÉ VIDÉO
Titre : {title}
Durée réelle : {duration_str} | Temps de lecture résumé : 3 min.
Score d'intérêt Business : /10 (potentiel freelance/automatisation)

🎯 LE "CORE" (3 idées forces, en français)
Idée 1 : [Explication concise]
Idée 2 : [Explication concise]
Idée 3 : [Explication concise]

🛠️ L'ARTILLERIE TECHNIQUE (outils/APIs cités)
Format tableau :
| Outil | Fonction Clé | Lien/API mentionnée |

💡 VULGARISATION & LEXIQUE
2 concepts complexes expliqués comme à un enfant (analogie simple, en français).
Ex : "Le RAG, c'est comme donner un livre ouvert à l'IA au lieu de lui demander de réciter de mémoire."

🚀 ACTION FREELANCE (Visibility & Business)
Comment utiliser ces infos pour améliorer la visibilité ou vendre un nouveau service demain ?

🎨 SCHÉMA LOGIQUE
Étapes du processus/automatisation sous forme A → B → C.

⚠️ Si la vidéo dure plus de 1h → segmenter par chapitres thématiques.
⚠️ Toujours répondre EN FRANÇAIS même si la transcription est en anglais.
```

---

## Architecture du Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    n8n Cloud (orchestrateur)                  │
│                                                              │
│  [Trigger]     [HTTP Request]      [Telegram]               │
│  Schedule      POST /api/liquefact  Send Review             │
│  ou Webhook    → SLY bot Railway   → Chat Augus             │
│  15 min        timeout 120s        formaté Markdown          │
└───────┬──────────────┬─────────────────────┬────────────────┘
        │              │                     │
        ▼              ▼                     ▼
   YouTube RSS    SLY Bot Railway       Telegram Bot API
   (nouvelles    ┌──────────────┐
    vidéos)      │ yt-dlp       │
                 │ → audio.mp3  │
                 │ Groq Whisper │
                 │ → transcript │
                 │ Groq/Gemini  │
                 │ → review FR  │
                 └──────────────┘
```

---

## Endpoints Disponibles

### POST `/api/transcribe`
Transcription seule (sans analyse IA).
```json
// Request
{"url": "https://www.youtube.com/watch?v=xxx"}

// Response
{
  "transcript": "Full text...",
  "title": "Video Title",
  "duration_sec": 360,
  "video_id": "xxx",
  "chunks_count": 1,
  "char_count": 5000
}
```

### POST `/api/liquefact`
Pipeline complet : transcription + analyse IA → Review Numérique en français.
```json
// Request
{"url": "https://www.youtube.com/watch?v=xxx"}

// Response
{
  "review": "📑 FICHE D'IDENTITÉ VIDÉO\nTitre: ...\n🎯 LE CORE...",
  "title": "Video Title",
  "url": "https://...",
  "duration_sec": 360,
  "duration_str": "6 min",
  "transcript_chars": 5000,
  "video_id": "xxx"
}
```

---

## Configuration Requise

- `GROQ_API_KEY` dans `.env` (transcription Whisper + analyse LLM)
- `GEMINI_API_KEY` dans `.env` (fallback LLM)
- `yt-dlp` installé (via requirements.txt → Docker auto)
- `ffmpeg` installé (déjà dans le Dockerfile)

## Limites Free Tier

| Ressource | Limite Groq Free |
|-----------|-----------------|
| Audio transcription | 8h/jour (28800 sec) |
| Fichier max | 25 MB |
| Requêtes/min | 20 RPM |
| LLM tokens | Selon modèle |

→ Suffisant pour ~20-30 vidéos de 20 min/jour.

---

## Chaînes YouTube Surveillées

Configurées dans le workflow n8n (`Blueprint/n8n_content_liquefactor.json`) :

| Chaîne | Channel ID | Thème |
|--------|-----------|-------|
| **Nick Saraev** (prioritaire) | `UCbo-KbSjJDG6JWQ_MTZ_rNA` | Automation, Make.com, n8n, business IA |
| AI Jason | `UCbRP3c757lWg9M-U7TyEkXA` | Vulgarisation IA |
| Matt Wolfe | `UC4JX40jDee_tINbkjycV4Sg` | Outils IA, news |
| Fireship | `UCsBjURrPoezykLs9EqgamOA` | Dev + IA, format court |
| Two Minute Papers | `UCnUYZLuoy1rq1aVMwx4piYg` | Recherche IA |
| The AI Advantage | `UCX6OQ3DkcsbYNE6H8uQQuVA` | Outils IA pratiques |

Pour ajouter une chaîne : modifier le node "Liste des chaînes" dans le workflow n8n.
