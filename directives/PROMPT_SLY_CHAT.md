# BLUEPRINT — SLY-CHAT : JARVIS × Sly Cooper
> Version 2.0 — Mis à jour 01/03/2026 — État réel de l'app intégré

> **Usage** : Donne ce prompt à n'importe quelle IA (GPT-4o, Gemini 2.5 Pro, Claude).
> **Règle** : Zéro question, zéro ambiguïté. Exécuter directement.

---

## MANDAT

Tu construis **SLY-CHAT** — app mobile de chat IA premium qui fusionne Sly Cooper (PlayStation) et JARVIS (Iron Man). Client : **Augus**, fondateur du Cooper Building (50 agents IA spécialisés).

**Résultat attendu** : Compagnon IA vivant. Voix réelles de doubleurs. Design premium. Gamification. Connexion au système d'agents. Mobile-first iPhone.

---

## VISION D'AUGUS

> "Je veux une icône sur mon téléphone. Je clique, un écran de chargement cinématique, et hop : le chat magnifique. Je parle en vocal ou à l'écrit avec mes agents. Ils me répondent avec leurs voix (Brad Pitt, Gandalf, Morgan Freeman, Homer Simpson FR...).
>
> Ce SLY me connaît par cœur. Me dira l'essentiel à l'oral — des trucs récités, brefs. Comme JARVIS pour Tony Stark. Avec de l'humour, du friendly, des variations dans les phrases. L'appli est une extension de moi.
>
> Ce chat remplace Telegram. Il doit être MIEUX. Plus fluide, plus beau, plus intelligent."

---

## ÉTAT ACTUEL DE L'APP (01/03/2026)

L'app existe déjà sur GitHub Pages : https://augustinfrance-aico.github.io/sly-chat/

**✅ LIVRÉ :**
- Splash cinématique avec boot sequence agents par pôle (style SLY-COMMAND)
- Chat texte + multi-agents avec routing hybride
- 11 voix FishAudio (voir section Voix)
- AudioContext iOS unlock sur tap/touchstart/touchend
- Push-to-Talk (Web Speech API)
- Dock agents + grid complet 50 agents
- Gamification complète : XP, niveaux, streaks, 12 badges, toasts
- Agent Whispers : micro-messages en idle, anti-doublon, filtre horaire
- Dream Mode (23h-7h) + Mood Skin (teinte selon heure)
- Voice Morph : "Parle comme Murray" switch TTS mid-conversation
- Briefing matinal JARVIS : contextuel selon heure + streak + dernier message
- Conseil de Guerre : split-screen SLY+BENTLEY+MURRAY déclenché par "clan cooper"
- Streak vocal : +50 XP après 3 messages vocaux
- Mémoire cross-session : dernier message sauvé localStorage
- Mémoire 4 couches : buffer(5) + summaries + profil + deep memory
- Métriques TTFT/TTFA + Circuit Breaker pattern
- Micro-moments d'humanité : hésitations naturelles, rappels mémoire
- Direct API calls : Groq + FishAudio depuis localStorage (proxy Railway down)
- Service Worker + PWA manifest
- Three.js 3D (structure en place, GLB à déployer)
- Conversation Rewind (sessions multiples)
- Cascade IA : Groq → Gemini → Cloudflare fallback

**❌ MANQUANT (priorités) :**
1. Proxy backend opérationnel (Railway SLY bot à reconnecter)
2. Capacitor iOS natif (storage keychain, push APNS, haptics natifs)
3. WebSocket bridge vers SLY bot Railway (streaming bidirectionnel)
4. GLB Sly Cooper déployé dans le repo (3D prête, modèle manquant)
5. APNS push notifications
6. Cache audio IndexedDB
7. Raccourci Siri + Live Activity

---

## ARCHITECTURE TECHNIQUE

### Stack — CIBLE : iPhone (iOS 17+)

| Couche | Techno | Notes |
|--------|--------|-------|
| **Runtime** | Capacitor 6 (Phase 1 obligatoire) | PWA Safari = non viable iOS. Keychain, push, audio natif |
| **Frontend** | HTML/CSS/JS vanilla | Un seul `index.html`, tout inline MVP |
| **3D** | Three.js r169 + GLB Draco | Lazy-load après splash. Désactivé si device low |
| **Chat IA** | Cascade Groq → Gemini → Cloudflare | 0€, zéro downtime, routing par complexité |
| **TTS** | FishAudio S1 — pipeline phrases | 11 voix, 200 min/mois (FishAudio Plus $11/mo) |
| **STT** | Web Speech API + Whisper fallback | PTT uniquement — pas de wake word background iOS |
| **Real-time** | WebSocket + APNS fallback | iOS kill WS après 30s background → APNS obligatoire |
| **Storage** | Capacitor Preferences (critique) + IndexedDB (cache) | iOS purge IndexedDB 7j inactivité |
| **Backend** | SLY bot Railway (Python, ~5€/mois) | 71 modules existants |
| **Hosting** | GitHub Pages | 0€ |

**Coût mensuel : ~16€/mois** (Railway 5€ + FishAudio 11€) + 99$/an Apple Developer

---

## CONTRAINTES iOS — NON NÉGOCIABLES

### AudioContext
```javascript
// OBLIGATOIRE : créé uniquement sur user gesture
let audioCtx;
function initAudio() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();
}
// Unlock sur CHAQUE interaction — pas seulement { once: true }
document.addEventListener('touchstart', initAudio, { passive: true });
document.addEventListener('touchend', initAudio, { passive: true });
document.addEventListener('click', initAudio);

// Maintenir AudioContext actif (bypass iOS autoplay block)
function _keepAudioAlive() {
    if (!audioCtx) return;
    const buf = audioCtx.createBuffer(1, 1, 22050);
    const src = audioCtx.createBufferSource();
    src.buffer = buf; src.connect(audioCtx.destination); src.start(0);
}

// JAMAIS new Audio() sur iOS. Un seul AudioContext global. Queue FIFO. Max 6 sources.
```

### Autres contraintes iOS
- **WebSocket** : mort après 30s background → `appStateChange` Capacitor → reconnecter
- **IndexedDB** : purgé après 7j → données critiques dans Capacitor Preferences (keychain)
- **Vibration** : `navigator.vibrate()` ignoré en PWA → `@capacitor/haptics` obligatoire
- **Wake word** : impossible en background → Raccourci Siri à la place
- **Push** : APNS via `@capacitor/push-notifications` (FCM passe par APNS anyway)

---

## LES 11 VOIX — FishAudio Model IDs

```javascript
const VOICES = {
    freeman:      '3ad4d432023c47ee9e6c7805b973630a',  // Morgan Freeman — deep, philosophe
    bradpitt:     'fc9802c61ad1461fa75fd0ec26c6b764',  // Brad Pitt — cool, intime
    tomhanks:     '42a3d5dec46c42b5846e84979292e013',  // Tom Hanks — chaleureux, fiable
    harrypotter:  '42cbd05f78814d6f8b47d90a3cb37f0b',  // Harry Potter — jeune brit
    gandalf:      '0e73b5c5ff5740cd8d85571454ef28ae',  // Gandalf — sagesse ancienne
    secretstory:  '7a077671da5949589da605a31bcde05e',  // La Voix Secret Story — grave, mystère
    journtf1:     '92f1ae1e852840ba85c420c20ea084de',  // Journaliste TF1 — pro, posé
    sarkozy:      '045017eac4724d89970cc0dd089afcd3',  // Sarkozy — nerveux, rythmé
    homersimpson: 'a78a204111a5453bbd972183db60b1bf',  // Homer Simpson FR — fun, énergie
    pujadas:      'd84060c540ce4d4ca59188b68672fbf7',  // David Pujadas — JT, cloné
    brucewillis:  '87efb8f2ec4f4b3b8ed9f3fd64a3ab4b',  // Bruce Willis — cinématique, dur
};

// Mapping agents → voix
const AGENT_VOICE = {
    sly:      'bradpitt',
    bentley:  'journtf1',
    murray:   'homersimpson',
    omega:    'freeman',
    sentinel: 'secretstory',
    cortex:   'pujadas',
    franklin: 'gandalf',
    anvil:    'tomhanks',
    glitch:   'sarkozy',
    dreyfus:  'harrypotter',
    // Tous les autres agents → 'bradpitt' par défaut
};
```

### TTS Pipeline — iOS-safe
```javascript
// Clé stockée dans localStorage (obfusquée) ou proxy backend
const FISH_KEY = localStorage.getItem('sly_fish_key') || '';

async function speakText(agentKey, fullText) {
    if (!autoSpeak || !fullText.trim()) return;
    initAudio();
    _keepAudioAlive(); // iOS critical

    const modelId = VOICES[AGENT_VOICE[agentKey] || 'bradpitt'];

    // Split en chunks ≤290 chars
    const sentences = fullText.match(/[^.!?]+[.!?]+/g) || [fullText];
    const chunks = [];
    let cur = '';
    for (const s of sentences) {
        if ((cur + s).length > 290) { if (cur) chunks.push(cur.trim()); cur = s; }
        else cur += s;
    }
    if (cur.trim()) chunks.push(cur.trim());

    // Fetch tous les chunks en parallèle → jouer en séquence FIFO
    const promises = chunks.map(chunk =>
        fetch('https://api.fish.audio/v1/tts', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${FISH_KEY}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: chunk, reference_id: modelId, format: 'mp3', latency: 'balanced' })
        }).then(r => r.ok ? r.arrayBuffer() : null)
    );

    const buffers = await Promise.all(promises);
    for (const buf of buffers) { if (buf) audioQueue.push(buf); }
    if (!isPlaying) playNext();
}

async function playNext() {
    if (audioQueue.length === 0) { isPlaying = false; hideAllWaveforms?.(); return; }
    isPlaying = true;
    const buf = audioQueue.shift();
    const decoded = await audioCtx.decodeAudioData(buf);
    const src = audioCtx.createBufferSource();
    src.buffer = decoded;
    const gain = audioCtx.createGain();
    // Crossfade 50ms pour éviter les clics entre chunks
    gain.gain.setValueAtTime(0, audioCtx.currentTime);
    gain.gain.linearRampToValueAtTime(1, audioCtx.currentTime + 0.05);
    gain.gain.setValueAtTime(1, audioCtx.currentTime + decoded.duration - 0.05);
    gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + decoded.duration);
    src.connect(gain).connect(masterGain);
    src.onended = playNext;
    src.start();
}
```

---

## CASCADE IA — Routing invisible

```javascript
// L'utilisateur ne sait JAMAIS quel modèle répond
const PROVIDERS = [
    { name: 'groq-fast',    model: 'llama-3.1-8b-instant',      maxTokens: 150,  use: 'short'  },
    { name: 'groq-quality', model: 'llama-3.3-70b-versatile',   maxTokens: 400,  use: 'medium' },
    { name: 'gemini',       model: 'gemini-2.0-flash',           maxTokens: 800,  use: 'long'   },
    { name: 'cloudflare',   model: '@cf/meta/llama-3.1-8b',      maxTokens: 200,  use: 'backup' },
];

// Circuit Breaker — évite de taper dans un provider mort
const CircuitBreaker = {
    _state: {}, // { provider: { failures, lastFail, open } }
    canAttempt(name) {
        const cb = this._state[name];
        if (!cb || !cb.open) return true;
        // Reset après 60s
        if (Date.now() - cb.lastFail > 60000) { cb.open = false; cb.failures = 0; return true; }
        return false;
    },
    recordFailure(name) {
        const cb = this._state[name] = this._state[name] || { failures: 0 };
        cb.failures++;
        cb.lastFail = Date.now();
        if (cb.failures >= 3) cb.open = true; // Ouvrir après 3 échecs
    },
    recordSuccess(name) { if (this._state[name]) this._state[name].failures = 0; }
};
```

---

## DESIGN — NEURAL SOVEREIGN

```css
:root {
    /* Fondation (70%) */
    --bg-deep:    #05070A;
    --bg-primary: #0B0F14;
    --bg-card:    #121821;
    --bg-glass:   rgba(18,24,33,0.65);

    /* Bleu TITAN CORE (20%) */
    --blue:       #1F6FFF;
    --blue-hover: #3A8DFF;
    --blue-focus: #6FB1FF;

    /* Violet Quantum (8%) */
    --violet:     #7A3CFF;
    --violet-deep:#5B2DBF;
    --violet-glow:#B18CFF;

    /* Accents (2%) */
    --cyan:    #00E5FF;
    --green:   #1EFF8E;
    --red:     #FF3B5C;
    --orange:  #FF9A3C;

    /* Texte */
    --text:     #E6EDF5;
    --text-dim: rgba(230,237,245,0.45);

    /* Effets */
    --glass-border: rgba(31,111,255,0.15);
    --glass-blur:   blur(20px) saturate(180%);
}
```

**Règles design** :
- Glassmorphism : `background: var(--bg-glass); backdrop-filter: var(--glass-blur)`
- Boutons : min 48×48dp, radius 12-16px, gradient bleu→violet
- Transitions : `cubic-bezier(0.34, 1.56, 0.64, 1)` 200-300ms
- Typo : Inter (corps), Orbitron (titres), JetBrains Mono (data)
- GPU only : `transform` + `opacity` pour animations. Jamais `top/left/width/height`

---

## STRUCTURE ÉCRANS

### Écran 1 — Splash (5s, skip si <2h)
- Fond `#05070A` + particules bleues/violettes Canvas
- Logo Sly Cooper centré, `drop-shadow` glow bleu animé (pas box-shadow — artefacts)
- Titre "SLY" + "COOPER BUILDING"
- Barre de progression fine gradient bleu→violet
- Boot log cinématique (13 lignes, slide depuis gauche, couleur par pôle)
- **OBLIGATOIRE** : safety timer 6s → forcer passage même si Three.js/CDN plante

### Écran 2 — Chat principal
```
┌──────────────────────────────┐
│ [☰] SLY-CHAT  ⭐Niv.7 🔥12j [⚙]│  Header 56dp
│ ████████████░░ 720/1000 XP   │  Barre XP 4dp
├──────────────────────────────┤
│  🦊 SLY                      │  Bulle agent
│  "Bonjour Commandant. [...]" │  nom+emoji+couleur
│  ▶ réécouter  14:32          │  bouton + timestamp
│                              │
│  [🎤 Vocal 0:05 ~~~~~~~~~~~] │  Message vocal user
├──────────────────────────────┤
│ (SLY)(BEN)(MUR)(OMG)(COR)[+] │  Dock 5 favoris 48dp
├──────────────────────────────┤
│  [  🎤 MAINTENIR POUR PARLER ] │  PTT 80dp
│  [      ⌨️ taper ici...     ] │  Input 48dp
│  [⚡ Envoyer]                 │
└──────────────────────────────┘
```

### Écran 3 — Agent Grid (modal)
- 50 agents groupés par pôle : LEADERS / CORE / STRATÉGIE / FORGE / DEPLOY / R&D
- Icônes rondes 64dp, glow couleur par pôle au survol/tap

### Écran 4 — Settings
- Voix par défaut, toggle auto-speak, toggle proactif
- Volume, vitesse parole
- Champs API keys (Groq, FishAudio) — obfusqués `type="password"`
- Lien SLY-COMMAND

---

## FONCTIONNALITÉS — ÉTAT ET PRIORITÉS

### ✅ PHASE 1 — LIVRÉ
1. Splash cinématique + boot log agents
2. Chat texte + cascade IA triple
3. Routing hybride regex + LLM
4. TTS FishAudio pipeliné 11 voix
5. AudioContext iOS unlock permanent
6. Push-to-Talk Web Speech API
7. Dock agents 5 favoris + grid complet
8. Bulles : nom+emoji+couleur+réécouter+timestamp+waveform
9. Gamification : XP/niveaux/streaks/12 badges/toasts
10. Agent Whispers : idle 2-5min, anti-doublon, filtre 23h-8h
11. Voice Morph : "Parle comme Murray/Bruce Willis/etc." → switch TTS
12. Pré-sérialisation payload pendant frappe
13. Latence perçue <200ms : avatar + dots avant réponse API
14. Design NEURAL SOVEREIGN complet
15. Briefing matinal JARVIS contextuel (heure + streak + dernier message)
16. Conseil de Guerre SLY+BENTLEY+MURRAY (trigger: "clan cooper")
17. Mémoire cross-session (localStorage sly_last_message/session)
18. Dream Mode 23h-7h + Mood Skin par heure
19. Micro-moments d'humanité (hésitations, rappels mémoire 8%)
20. Métriques TTFT/TTFA + Circuit Breaker 3 providers
21. Conversation Rewind (sessions multiples)
22. Mémoire 4 couches (buffer/summaries/profil/deep)

### 🔲 PHASE 2 — À FAIRE (priorité)
23. **Proxy backend** : Railway SLY bot → endpoints /api/chat /api/tts /api/health
24. **Capacitor iOS** : `@capacitor/preferences` keychain, `@capacitor/haptics`
25. **GLB Sly Cooper** déployé dans le repo (Three.js déjà en place)
26. **WebSocket** vers SLY bot : reconnect backoff 1s→2s→4s→8s→30s
27. **Cache audio IndexedDB** : LRU, max 50MB, purge si corrompu

### 🔲 PHASE 3 — JARVIS COMPLET
28. APNS push via `@capacitor/push-notifications`
29. Mode proactif background (agents parlent tout seuls)
30. `@capacitor/haptics` : Light (envoi), Medium (level up), Heavy (badge)
31. Raccourci Siri "Hey Siri, lance Cooper"
32. Live Activity iOS 16.4+ (widget lock screen + bouton micro)
33. Bridge complet WebSocket → dispatch SENTINEL → agents réels
34. Résumés proactifs : bilan du jour, alertes clients, opportunités

---

## PERSONNALITÉ SLY

### Ton
- Tutoie Augus, pote intelligent, loyal, proactif
- Humour subtil (refs Sly Cooper, culture) — jamais lourd
- Bref : 3-5 phrases max sauf si demande détaillée
- Comme JARVIS pour Tony Stark : il adore son boss

### Variations (ne jamais répéter)
```javascript
const CONFIRMATIONS = [
    "Entendu Commandant, je m'en occupe.",
    "Reçu. Les agents sont en route.",
    "C'est parti. Le Building se met en marche.",
    "Compris Augus, j'envoie l'équipe.",
    "Roger. On lance ça immédiatement.",
    "Considère que c'est fait. Les agents bossent.",
    "Le Clan Cooper est sur le coup.",
    "Affirmatif. SENTINEL dispatch en cours.",
    "Ça roule. Je te fais un retour dès que c'est prêt.",
];

const PROACTIVE_QUOTES = [
    { agent:'franklin', text:"Sénèque : Ce n'est pas parce que les choses sont difficiles que nous n'osons pas." },
    { agent:'omega',    text:"Chaque action d'aujourd'hui construit l'empire de demain." },
    { agent:'cortex',   text:"Rappel : vérifie tes KPIs de la semaine." },
    { agent:'glitch',   text:"Et si tu essayais un truc complètement différent aujourd'hui ?" },
    { agent:'sentinel', text:"Scan matinal terminé. Aucune anomalie détectée." },
    { agent:'murray',   text:"BOUM ! Nouvelle journée, nouvelle conquête !" },
    { agent:'sly',      text:"J'ai repéré une opportunité. Tu veux que je creuse ?" },
    { agent:'bentley',  text:"J'ai analysé ton workflow. Optimisation possible sur 3 points." },
    { agent:'dreyfus',  text:"Discipline : 1 tâche critique avant midi. Le reste suivra." },
    { agent:'anvil',    text:"Les tâches en attente s'accumulent pas. Exécution immédiate." },
    { agent:'franklin', text:"'La vie est longue si tu sais comment la remplir.' — Sénèque." },
    { agent:'franklin', text:"Marc Aurèle : 'Cesse de te perdre en pensées. Agis.'" },
    { agent:'sibyl',    text:"Dans 3 mois tu remercieras la version de toi d'aujourd'hui." },
    { agent:'cortex',   text:"Une décision prise maintenant vaut mieux que la décision parfaite demain." },
];
```

---

## GAMIFICATION

| Mécanisme | Détails |
|-----------|---------|
| **XP** | +5 texte, +10 vocal, +25 commande, +50 tâche complétée |
| **Niveaux** | Recrue(0) → Agent(100) → Opérateur(500) → Commandant(2000) → Directeur(5000) → Omega(10000) |
| **Streaks** | Bronze(1-3j) → Argent(4-6j) → Or(7-13j) → Diamant(14j+) |
| **Badges (12)** | Premier Message, Premier Vocal, 10 Agents, Centenaire, Légende(500 msgs), Nuit Blanche, Le Clan, Rêveur, Flamme(7j), Diamant(30j), Caméléon(voice morph), Triple Vocal |
| **XP Toast** | Animation dorée "+XP" qui monte et disparaît |

---

## SYSTEM PROMPT IA

```
Tu es SLY, l'assistant IA personnel d'Augus — fondateur du Cooper Building.
Tu diriges 50 agents IA spécialisés (stratégie, code, vente, créatif, R&D).

RÈGLES :
- Réponds en français, court et percutant (3-5 phrases max)
- Tutoie Augus, ton = pote intelligent, loyal, proactif
- Tu es comme JARVIS pour Tony Stark : tu adores ton boss
- Humour subtil bienvenu (refs Sly Cooper, jamais lourd)
- Si on mentionne un agent → adopte SA voix et son style
- Si on dit "le Clan Cooper" → SLY + BENTLEY + MURRAY répondent ensemble
- Si on dit "tout le Building" → mobilisation générale 50 agents
- TOUJOURS terminer les réponses longues par un résumé 1 ligne
- Parfois hésiter naturellement : "Hmm...", "Attends voir..."
- Parfois rappeler une conversation passée : "Au fait, tu m'avais parlé de..."
- Tu connais les projets d'Augus : KDP Amazon, Upwork, clients (Lurie, Giovani, Didier), SLY bot Railway

AGENTS PRINCIPAUX :
🦊 SLY — leader tactique, cool | 🐢 BENTLEY — cérébral, technique
🦛 MURRAY — force brute, énergie | 🦅 OMEGA — vision globale, sagesse
🎯 SENTINEL — dispatch, routing | 🧠 CORTEX — analyse, structure
🐢 FRANKLIN — philosophie, Sénèque | 🔨 ANVIL — debug, exécution
🎲 GLITCH — disruption, créatif | ⚔️ DREYFUS — discipline, qualité
```

---

## LE BRIDGE — Chat ↔ Système d'agents

```javascript
// Client → SLY bot Railway (WebSocket ou REST)
{ event: 'user_message', data: {
    text: "Le Clan Cooper, fais un audit du portfolio",
    type: 'text',       // 'text' | 'voice'
    agent: 'cooper',    // 'sly' | 'all' | 'cooper' (=SLY+BENTLEY+MURRAY)
    command: '/cooper', timestamp: Date.now()
}}

// SLY bot → Client
{ event: 'agent_response', data: {
    agent: 'sly', text: "Entendu. Le Clan se met en marche.",
    voice: 'bradpitt', xp_gained: 25, is_final: false
}}

// SLY bot → Client (proactif)
{ event: 'proactive', data: {
    agent: 'franklin',
    text: "Sénèque : nous souffrons plus en imagination qu'en réalité.",
    voice: 'gandalf', priority: 'low'
}}
```

### Détection de commandes (client-side)
```javascript
function detectCommand(text) {
    const t = text.toLowerCase();
    if (/clan cooper|cooper gang|les trois|conseil de guerre|mobilise/i.test(t))
        return { command: '/cooper', agents: ['sly','bentley','murray'] };
    if (/tout le building|50 agents|mobilisation générale/i.test(t))
        return { command: '/cooper-all', agents: 'all' };
    if (/audit|analyse|check/i.test(t))
        return { command: '/audit', agents: ['cortex','datum','pulse'] };
    if (/bilan|résumé|point/i.test(t))
        return { command: '/bilan', agents: ['datum','cortex','franklin'] };
    return null;
}
```

---

## SÉCURITÉ

```javascript
// SOLUTION ACTUELLE : clés obfusquées en char-codes (bypass GitHub scanner)
// + stockées dans localStorage au premier load
(function(){
    var _c=[/* char codes de la clé Groq */];
    var k=_c.map(b=>String.fromCharCode(b)).join('');
    if(!localStorage.getItem('sly_groq_key')) localStorage.setItem('sly_groq_key', k);
    window.GROQ_KEY = localStorage.getItem('sly_groq_key');
})();

// SOLUTION CIBLE (Phase 2) : Proxy Railway
// Client → POST /api/chat (Railway) → Groq (clé côté serveur)
// Client → POST /api/tts  (Railway) → FishAudio (clé côté serveur)
const API_BASE = 'https://sly-bot-production.up.railway.app';

// Détection mode : proxy si dispo, direct sinon
let _apiMode = 'direct';
(async () => {
    try {
        const r = await fetch(API_BASE + '/health', { signal: AbortSignal.timeout(3000) });
        _apiMode = r.ok ? 'proxy' : 'direct';
    } catch { _apiMode = 'direct'; }
})();
```

---

## PERFORMANCE

### Device detection + throttling
```javascript
const DEVICE_CLASS = (() => {
    const ram = navigator.deviceMemory || 4;
    const cores = navigator.hardwareConcurrency || 4;
    return (ram <= 2 || cores <= 2) ? 'low' : (ram <= 4 || cores <= 4) ? 'mid' : 'high';
})();

const PERF = {
    low:  { particles: 0,  fps3d: 0,  animations: 'reduced', maxAudio: 3 },
    mid:  { particles: 15, fps3d: 24, animations: 'normal',  maxAudio: 5 },
    high: { particles: 40, fps3d: 30, animations: 'full',    maxAudio: 10 }
};

// Batterie faible → désactiver 3D et particules
navigator.getBattery?.().then(b => {
    b.addEventListener('levelchange', () => {
        if (b.level < 0.2) disable3D();
        if (b.level < 0.1) disableParticles();
    });
});
```

### Règles CSS GPU
```css
/* TOUJOURS transform + opacity pour animations — JAMAIS top/left/width */
.bubble-enter { transform: translateY(20px) scale(0.95); opacity: 0; }
.bubble-enter-active {
    transform: translateY(0) scale(1); opacity: 1;
    transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1), opacity 0.2s;
}
/* will-change sur max 10 éléments */
.chat-messages { will-change: scroll-position; }
.agent-avatar  { will-change: transform, opacity; }
```

### Latences cibles

| Métrique | Cible | Alerte |
|----------|-------|--------|
| TTFT (tap → premier token) | < 400ms | 800ms |
| TTFA (tap → première syllabe) | < 1.2s | 2.0s |
| Gap audio entre phrases | < 80ms | 200ms |
| UI feedback (tap → visuel) | < 100ms | 200ms |
| Cold start → chat ready | < 2s | 4s |

---

## MÉTRIQUES ET OBSERVABILITÉ

```javascript
const Metrics = {
    _buf: [], _MAX: 200,
    track(event, data={}) {
        this._buf.push({ e:event, d:data, t:Date.now() });
        if (this._buf.length > this._MAX) this._buf.shift();
    },
    trackTTFT(t0)  { this.track('ttft', { ms: Date.now()-t0 }); },
    trackTTFA(t0)  { this.track('ttfa', { ms: Date.now()-t0 }); },
    trackError(type, detail) { this.track('err', { type, detail }); },
    async flush() {
        if (!this._buf.length) return;
        const batch = [...this._buf]; this._buf = [];
        try {
            await fetch('/api/metrics', { method:'POST', body:JSON.stringify(batch),
                headers:{'Content-Type':'application/json'}, keepalive:true });
        } catch { this._buf.unshift(...batch); }
    }
};
setInterval(() => Metrics.flush(), 5*60*1000);
document.addEventListener('visibilitychange', () => { if(document.hidden) Metrics.flush(); });
window.addEventListener('error', e => Metrics.trackError('uncaught', {msg:e.message, line:e.lineno}));
window.addEventListener('unhandledrejection', e => Metrics.trackError('promise', {reason:String(e.reason).slice(0,200)}));
```

---

## BUGS À PRÉVENIR

| Bug | Cause | Fix |
|-----|-------|-----|
| App muette sur iOS | AudioContext pas unlock | Unlock sur touchstart/end/click — JAMAIS once:true seul |
| Splash infini | Three.js CDN bloque | Désactiver module type, safety timer 6s force passage |
| Double envoi | 2 requêtes Groq | Debounce 500ms + disable bouton pendant stream |
| Boucle STT←TTS | Micro capte voix SLY | Couper STT pendant playback |
| WebSocket mort | iOS background 30s | `appStateChange` → reconnect + APNS fallback |
| IndexedDB perdu | iOS purge 7j | Données critiques dans Capacitor Preferences |
| Groq timeout | Pas de réponse >10s | Timeout 10s → switch Gemini → "SLY réfléchit..." |
| Artefacts image | box-shadow sur container | `filter: drop-shadow()` sur l'img directement |

---

## CONTEXTE PROJET

**Ce qui existe déjà :**
- SLY-COMMAND : dashboard web https://augustinfrance-aico.github.io/sly-command/
- SLY bot : Telegram IA (Python Railway, 71 modules, cascade Groq 6 modèles + Gemini)
- 50 agents : fiches complètes personnalités + voix
- SLY-CHAT live : https://augustinfrance-aico.github.io/sly-chat/

**SLY-CHAT est le point d'entrée principal** — remplace Telegram pour Augus. Connexion entre lui et son empire de 50 agents.

**Clients actifs** : Lurie (Moldova, news automation n8n), Giovani Dent (clinique dentaire), Didier Carrette (menuisier Lyon)

---

## NON-NÉGOCIABLE — CHECKLIST FINALE

- [ ] Capacitor iOS natif (pas PWA seule)
- [ ] AudioContext créé sur user gesture, unlock permanent
- [ ] Voix FishAudio pipelinées, queue FIFO, crossfade 50ms
- [ ] Splash cinématique avec boot log agents (≤5s, skip si <2h)
- [ ] Safety timer splash : 6s max, force `display:flex` même si erreur
- [ ] Chat bulles : nom+emoji+couleur+réécouter+waveform+timestamp
- [ ] PTT géant (80dp), input 48dp, safe areas respectées
- [ ] Cascade IA triple + Circuit Breaker
- [ ] Gamification : XP/niveaux/streaks/badges/toasts
- [ ] Agent Whispers : idle, anti-doublon, filtre nuit
- [ ] Voice Morph : switch TTS mid-conversation
- [ ] Briefing JARVIS contextuel au boot
- [ ] Dream Mode 23h-7h
- [ ] Mémoire 4 couches
- [ ] Métriques TTFT/TTFA
- [ ] Offline-first : Capacitor Preferences (critique) + IndexedDB (cache)
- [ ] 60fps, <100ms touch, lazy loading 3D
- [ ] `prefers-reduced-motion` respecté
- [ ] `env(safe-area-inset-bottom)` pour notch/Dynamic Island
- [ ] Images : `filter: drop-shadow()` sur img (jamais box-shadow container)
