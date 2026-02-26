# DECISION LOG — Mémoire Technique Immortelle

> Chaque décision d'architecture, chaque choix technique, chaque bug résolu.
> Format strict : lisible en 5 secondes.

---

## Format

```
### [DATE] — [TITRE]
- **Contexte** : pourquoi
- **Choix** : quoi
- **Alternative** : rejeté et pourquoi
- **Impact** : fichiers
```

---

## Entrées

### 2026-02-26 — Cascade Groq 6 modèles TITAN
- **Contexte** : Coût 0€ obligatoire, fallback IA robuste
- **Choix** : llama-3.3-70b > maverick > scout > kimi-k2 > qwen3-32b > llama-3.1-8b + Gemini
- **Alternative** : OpenAI payant — rejeté coût
- **Impact** : execution/titan/ai_client.py, config.py

### 2026-02-26 — Polling Telegram vs Webhook
- **Contexte** : Simplicité déploiement Railway
- **Choix** : Polling — pas de SSL/endpoint public nécessaire
- **Alternative** : Webhook — plus perf mais config complexe
- **Impact** : execution/titan/main.py

### 2026-02-26 — Anti-doublon set message_id
- **Contexte** : Doublons Telegram = réponses multiples
- **Choix** : Set Python (max 500, purge 200)
- **Alternative** : SQLite — over-engineered
- **Impact** : execution/titan/brain.py

### 2026-02-26 — Restructuration 30 agents
- **Contexte** : 25 agents avec doublons et zones floues
- **Choix** : Fusion (DREYFUS→SPARTAN, FLEMMARD→ZEN, VERSO→ZARA) + création SENTINEL/PULSE/LIMPIDE
- **Alternative** : Garder 25 bruts — manquait dispatch
- **Impact** : personnalites/*.md, agents/agent_profiles.py

### 2026-02-26 — Architecture Tri-Pôle R→F→D
- **Contexte** : Agents isolés sans circulation
- **Choix** : 3 pôles + OMEGA-CORE + boucle perpétuelle
- **Alternative** : Hiérarchie plate — perd la spécialisation
- **Impact** : directives/TRI_POLE.md, CASTING.md

### 2026-02-26 — Exosquelette Cognitif 3 Quick Wins
- **Contexte** : 10 systèmes possibles, priorisation nécessaire
- **Choix** : Decision Log + Reflector Engine + Bug Prédictif
- **Alternative** : Flow God / Agent Futur — R&D future
- **Impact** : memory/decision_log.md, .claude/hooks/
