# PROMPT ULTIME — SLY-CHAT : L'Application Mobile JARVIS × Sly Cooper

> **Ce prompt est un blueprint complet. Donne-le tel quel à ChatGPT (GPT-4o) ou Gemini 2.5 Pro.**
> **L'IA qui le reçoit n'a qu'à exécuter — zéro question, zéro ambiguïté.**

---

## TON MANDAT

Tu es l'architecte principal du projet **SLY-CHAT** — une application mobile de chat IA premium qui fusionne l'univers de **Sly Cooper** (le jeu PlayStation) avec la puissance d'un **JARVIS** (Iron Man). Tu travailles pour **Augus**, fondateur du Cooper Building, un écosystème de **50 agents IA spécialisés** (stratégie, code, vente, créatif, R&D, etc.).

**Ton objectif** : Construire une application mobile de chat IA d'une fluidité et d'un design EXCEPTIONNELS. Pas un vulgaire chatbot. Un compagnon IA vivant, avec des voix réelles, des personnages 3D, de la gamification, et une connexion directe au système d'agents d'Augus.

**Ton style** : Code propre, commenté, production-ready. Dark mode premium. Animations fluides 60fps. Mobile-first. Chaque pixel compte.

---

## LA VISION D'AUGUS (verbatim)

> "Je veux une icône sur mon téléphone. Je clique, un écran de chargement cinématique, et hop : le chat magnifique. Je parle en vocal ou à l'écrit avec mes agents. Ils me répondent avec leurs voix (Brad Pitt, Gandalf, Morgan Freeman, Homer Simpson FR...). Je peux dire 'Le Clan Cooper, allez me faire telle chose' et le message est transmis à mon système d'agents qui se mettent au travail.
>
> C'est pas un petit champ de texte minable. C'est un GROS champ avec une belle icône Sly Cooper en 3D, des animations, une fluidité extrême, une simplicité déconcertante, et derrière une technicité folle.
>
> Ce SLY me fera des résumés, me connaîtra par cœur, me dira l'essentiel à l'oral — des trucs récités, brefs. Comme JARVIS dans Iron Man : le gars m'adore et est là pour moi. Avec de l'humour, du friendly, des variations dans les phrases.
>
> L'appli doit être une extension de moi. Les menus doivent être GROS et fluides car j'ai pas envie de galérer à cliquer. Le thème Sly Cooper, mais en restant pro et fun. Gamifié aussi — XP, niveaux, streaks.
>
> Ce chat remplace Telegram pour moi. Il doit être MIEUX. Plus fluide, plus beau, plus intelligent."

---

## ARCHITECTURE TECHNIQUE

### Stack recommandé — CIBLE : iPhone (iOS 17+)

> ⚠️ **IMPORTANT : L'utilisateur est sur iPhone.** Toute l'architecture DOIT être pensée iOS-first.
> iOS a des contraintes STRICTES (AudioContext, background, push, storage) documentées ci-dessous.

| Couche | Technologie | Pourquoi | ⚠️ Contrainte iOS |
|--------|------------|----------|---------------------|
| **Runtime** | **Capacitor 6 dès Phase 1** (PAS PWA seule) | PWA sur iOS Safari = trop limité (pas de push < 16.4, cache purgé après 7j, audio bridé). Capacitor = accès natif obligatoire | PWA seule = **NON VIABLE** sur iPhone |
| **Frontend** | HTML/CSS/JS vanilla (ou Ionic 8 si besoin de composants) | Léger, rapide, pas de framework lourd | — |
| **3D** | Three.js r169+ (modèle GLB, compression Draco) | 3D dans le browser, 60fps mobile | WebGL OK sur iOS Safari/WKWebView |
| **Animations** | CSS animations + Rive (personnage Sly interactif) | 60fps garanti, ultra léger | `prefers-reduced-motion` obligatoire |
| **Chat IA** | **Cascade triple** : Groq 8b (rapide) → Groq 70b (qualité) → Gemini Flash (fallback long) → Cloudflare Workers AI (urgence) | 0€, zéro downtime, routing par complexité | — |
| **TTS (voix)** | FishAudio API S1 — 10 voix clonées/publiques, **pipeline phrase par phrase** | Voix réalistes, streaming, 200 min/mois | Voir section AudioContext iOS ci-dessous |
| **STT (écoute)** | Web Speech API + Groq Whisper fallback | 0€, <100ms latence | Web Speech API supporté dans WKWebView Capacitor |
| **Wake word** | **Raccourci Siri** "Hey Siri, lance Cooper" → ouvre l'app en mode écoute | Picovoice ne peut PAS tourner en background sur iOS — Apple bloque le micro | **PAS de wake word background sur iOS** |
| **Real-time** | WebSocket (Socket.IO 4) | Streaming token-by-token, proactif | iOS tue les WebSocket après **30s en background** → fallback APNS |
| **Push** | **APNS (Apple Push Notification Service)** via Capacitor `@capacitor/push-notifications` | FCM existe sur iOS mais passe par APNS de toute façon. Autant utiliser APNS natif | FCM seul = insuffisant sur iOS |
| **Storage** | **Capacitor `@capacitor/preferences`** (données critiques : XP, mémoire, profil) + IndexedDB (cache audio temporaire) | iOS Safari purge IndexedDB après **7 jours d'inactivité**. Les Preferences Capacitor stockent dans le keychain natif = jamais purgé | IndexedDB seul = **DONNÉES PERDUES** |
| **Hosting** | Cloudflare Pages (gratuit) ou GitHub Pages | 0€ | — |
| **Backend** | TITAN bot existant (Python, Railway ~5€/mois) | Déjà en place, 71 modules | — |

### Coût total : ~5€/mois (Railway) + 11€/mois (FishAudio Plus) + 99$/an (Apple Developer) = ~24€/mois

---

### ⚠️ CONTRAINTES iOS CRITIQUES — À respecter absolument

#### 1. AudioContext (le piège #1 sur iPhone)
```javascript
// L'AudioContext DOIT être créé dans un user gesture event (tap/click)
// Sinon → SILENCE TOTAL, aucune erreur, juste rien ne joue
let audioContext;
document.addEventListener('touchstart', () => {
    if (!audioContext) {
        audioContext = new AudioContext();
    }
    if (audioContext.state === 'suspended') {
        audioContext.resume();
    }
}, { once: false });

// JAMAIS utiliser new Audio() sur iOS — toujours passer par AudioContext
// JAMAIS créer plusieurs AudioContext — un seul global, un seul GainNode master
// Max 6 AudioBufferSourceNode simultanés sur iOS — gérer une queue FIFO
```

#### 2. Background & WebSocket
- iOS tue les WebSocket après **30 secondes** en background (pas 5 min comme Android)
- Solution : `@capacitor/app` listener `appStateChange` → reconnecter au retour foreground
- Les messages proactifs (Agent Whispers) doivent passer par **APNS** quand l'app est en background
- Backoff exponentiel pour reconnexion : 1s → 2s → 4s → 8s → cap 30s

#### 3. Stockage
- IndexedDB sur iOS Safari/WKWebView : **purgé après 7 jours d'inactivité**
- Données critiques (XP, streak, mémoire, profil) → `@capacitor/preferences` (keychain natif)
- Cache audio → IndexedDB (temporaire, re-fetchable si purgé)
- Max safe : ~50MB en IndexedDB sur iOS

#### 4. Wake Word
- Picovoice Porcupine WASM **ne peut PAS** écouter le micro en background sur iOS
- Apple bloque l'accès micro en arrière-plan sauf pour apps de téléphonie
- Alternative Phase 1 : **Raccourci Siri** personnalisé → "Hey Siri, lance Cooper"
- Alternative Phase 3 : **Live Activity (iOS 16.4+)** — widget persistent sur lock screen avec bouton micro

#### 5. Vibration haptique
```javascript
// iOS supporte l'API Vibration MAIS uniquement dans Capacitor natif
// En PWA Safari → vibration ignorée silencieusement
import { Haptics, ImpactStyle } from '@capacitor/haptics';
await Haptics.impact({ style: ImpactStyle.Light }); // Sur envoi message
await Haptics.impact({ style: ImpactStyle.Medium }); // Sur level up
```

---

## LES 10 VOIX — Model IDs FishAudio (prêts à l'emploi)

```javascript
const FISH_API_KEY = '[VOTRE_CLÉ_FISHAUDIO]';

const VOICES = {
    // Stars EN (publiques communautaires, haute fidélité, parlent FR via le moteur S1)
    freeman:      '3ad4d432023c47ee9e6c7805b973630a',  // Morgan Freeman — 13K uses, deep, philosophe
    bradpitt:     'fc9802c61ad1461fa75fd0ec26c6b764',  // Brad Pitt — 374 uses, cool, intime
    tomhanks:     '42a3d5dec46c42b5846e84979292e013',  // Tom Hanks — 438 uses, chaleureux
    harrypotter:  '42cbd05f78814d6f8b47d90a3cb37f0b',  // Harry Potter — 1.9K uses, 4.9/5, jeune brit
    gandalf:      '0e73b5c5ff5740cd8d85571454ef28ae',  // Gandalf — 33K uses, sagesse ancienne
    // Voix FR (publiques)
    secretstory:  '7a077671da5949589da605a31bcde05e',  // La Voix Secret Story — 5K uses, grave, mystère
    journtf1:     '92f1ae1e852840ba85c420c20ea084de',  // Journaliste TF1 — 354 uses, pro
    sarkozy:      '045017eac4724d89970cc0dd089afcd3',  // Sarkozy — 1.5K uses, nerveux
    homersimpson: 'a78a204111a5453bbd972183db60b1bf',  // Homer Simpson FR — 32K uses, fun
    pujadas:      'd84060c540ce4d4ca59188b68672fbf7',  // David Pujadas — cloné, posé, JT
};

// Mapping agents → voix (les 10 agents principaux)
const AGENT_VOICE = {
    sly:      'bradpitt',      // 🦊 SLY — leader tactique, cool
    bentley:  'journtf1',      // 🐢 BENTLEY — cérébral, posé
    murray:   'homersimpson',  // 🦛 MURRAY — force brute, énergie
    omega:    'freeman',       // 🦅 OMEGA — boss, sagesse, gravité
    sentinel: 'secretstory',   // 🎯 SENTINEL — dramatique, commande
    cortex:   'pujadas',       // 🧠 CORTEX — analytique, grave
    franklin: 'gandalf',       // 🐢 FRANKLIN — philosophe, ancien
    anvil:    'tomhanks',      // 🔨 ANVIL — fiable, direct
    glitch:   'sarkozy',       // 🎲 GLITCH — nerveux, disruptif
    dreyfus:  'harrypotter',   // ⚔️ DREYFUS — jeune, discipliné
};
```

### Appel TTS FishAudio — iOS-safe, pipeliné phrase par phrase

```javascript
// ⚠️ AUDIO CONTEXT GLOBAL — créé sur premier tap utilisateur (obligatoire iOS)
let audioCtx;
let masterGain;
const audioQueue = []; // Queue FIFO pour éviter chevauchement
let isPlaying = false;

function initAudio() {
    if (!audioCtx) {
        audioCtx = new AudioContext();
        masterGain = audioCtx.createGain();
        masterGain.connect(audioCtx.destination);
    }
    if (audioCtx.state === 'suspended') audioCtx.resume();
}
// Appeler initAudio() dans le premier touchstart/click de l'app

// TTS — split en phrases, pipeline parallèle, queue audio
async function speakAs(agentKey, fullText) {
    initAudio();
    const modelId = VOICES[AGENT_VOICE[agentKey]];

    // Split en phrases (max 300 chars chacune — limite FishAudio)
    const sentences = fullText.match(/[^.!?]+[.!?]+/g) || [fullText];
    const chunks = [];
    let current = '';
    for (const s of sentences) {
        if ((current + s).length > 290) {
            if (current) chunks.push(current.trim());
            current = s;
        } else {
            current += s;
        }
    }
    if (current.trim()) chunks.push(current.trim());

    // Pipeline : fetch tous les chunks en parallèle, jouer en séquence
    const audioPromises = chunks.map(chunk =>
        fetch('https://api.fish.audio/v1/tts', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${FISH_API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: chunk,
                reference_id: modelId,
                format: 'mp3',
                latency: 'balanced'
            })
        }).then(r => r.ok ? r.arrayBuffer() : null)
    );

    const buffers = await Promise.all(audioPromises);
    for (const buf of buffers) {
        if (!buf) continue;
        audioQueue.push(buf);
    }
    if (!isPlaying) playNext();
}

async function playNext() {
    if (audioQueue.length === 0) { isPlaying = false; return; }
    isPlaying = true;
    const buf = audioQueue.shift();
    const audioBuf = await audioCtx.decodeAudioData(buf);
    const source = audioCtx.createBufferSource();
    source.buffer = audioBuf;

    // Crossfade 50ms pour éviter les "clics" entre chunks
    const gain = audioCtx.createGain();
    gain.gain.setValueAtTime(0, audioCtx.currentTime);
    gain.gain.linearRampToValueAtTime(1, audioCtx.currentTime + 0.05);
    gain.gain.setValueAtTime(1, audioCtx.currentTime + audioBuf.duration - 0.05);
    gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + audioBuf.duration);

    source.connect(gain).connect(masterGain);
    source.onended = () => playNext();
    source.start();
}

// COUPER la lecture si l'utilisateur parle (évite boucle STT ← TTS)
function stopSpeaking() {
    audioQueue.length = 0;
    isPlaying = false;
    // Pas de source.stop() car on clear la queue — le chunk en cours finit naturellement
}
```

### Cascade IA triple — routing par complexité

```javascript
// DÉCISION CONCLAVE : ne PAS dépendre d'un seul LLM
// Routing invisible — l'utilisateur ne sait JAMAIS quel modèle répond
async function generateResponse(messages, expectedLength = 'medium') {
    const providers = [
        {
            name: 'groq-fast',
            url: 'https://api.groq.com/openai/v1/chat/completions',
            model: 'llama-3.1-8b-instant',
            key: GROQ_API_KEY,
            maxTokens: 100,
            use: expectedLength === 'short' // Messages courts < 50 tokens attendus
        },
        {
            name: 'groq-quality',
            url: 'https://api.groq.com/openai/v1/chat/completions',
            model: 'llama-3.3-70b-versatile',
            key: GROQ_API_KEY,
            maxTokens: 300,
            use: expectedLength === 'medium' // Messages normaux
        },
        {
            name: 'gemini-deep',
            url: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent',
            key: GEMINI_API_KEY,
            maxTokens: 800,
            use: expectedLength === 'long' // Analyses, résumés longs
        }
    ];

    const primary = providers.find(p => p.use) || providers[1];
    const fallbacks = providers.filter(p => p !== primary);

    try {
        return await callProvider(primary, messages);
    } catch {
        for (const fb of fallbacks) {
            try { return await callProvider(fb, messages); } catch { continue; }
        }
        return "Connexion instable. Réessaie dans un instant.";
    }
}
```

### Pré-sérialisation locale (DÉCISION CONCLAVE)

```javascript
// Pendant que l'utilisateur tape, on prépare LOCALEMENT le payload
// ZÉRO requête API gaspillée — on sérialise le JSON à l'avance
let prebuiltPayload = null;

function onUserTyping(partialText) {
    // 1. Pré-routing agent (local, regex, 0 latence)
    const detectedAgent = detectAgent(partialText);
    if (detectedAgent) {
        showAgentAvatar(detectedAgent); // L'avatar pulse AVANT l'envoi → illusion de présence
    }

    // 2. Pré-sérialisation du payload (system prompt + historique + contexte)
    prebuiltPayload = JSON.stringify({
        model: 'llama-3.3-70b-versatile',
        messages: [
            { role: 'system', content: getSystemPrompt(detectedAgent) },
            ...getConversationHistory(),
            // Le message user sera ajouté au moment de l'envoi
        ],
        stream: true,
        max_tokens: 300
    });
}

function onUserSend(finalText) {
    // Le payload est DÉJÀ prêt — on ajoute juste le message final
    // Gain : ~100ms de sérialisation économisés
    const payload = JSON.parse(prebuiltPayload);
    payload.messages.push({ role: 'user', content: finalText });
    streamResponse(JSON.stringify(payload));
}
```

---

## DESIGN — Palette NEURAL SOVEREIGN

```css
:root {
    /* Fondation (70% de l'écran) */
    --bg-deep:    #05070A;
    --bg-primary: #0B0F14;
    --bg-card:    #121821;
    --bg-glass:   rgba(18,24,33,0.65);

    /* TITAN CORE — Bleu (20%) */
    --blue:       #1F6FFF;
    --blue-hover: #3A8DFF;
    --blue-focus: #6FB1FF;

    /* Violet Quantum (8%) */
    --violet:     #7A3CFF;
    --violet-deep:#5B2DBF;
    --violet-glow:#B18CFF;

    /* Cyan accent (2%) */
    --cyan:       #00E5FF;

    /* Alertes */
    --green:      #1EFF8E;
    --red:        #FF3B5C;
    --orange:     #FF9A3C;

    /* Texte */
    --text:       #E6EDF5;
    --text-dim:   rgba(230,237,245,0.45);

    /* Effets */
    --glass-border: rgba(31,111,255,0.15);
    --glass-blur:   blur(20px) saturate(180%);
}
```

### Principes de design
- **Glassmorphism** : panneaux semi-transparents `background: var(--bg-glass); backdrop-filter: var(--glass-blur);`
- **Particules** : points bleus/violets flottants en arrière-plan (Canvas ou CSS)
- **Glow effects** : `box-shadow: 0 0 20px rgba(31,111,255,0.3)` sur les éléments actifs
- **Typographie** : Inter (corps), JetBrains Mono ou Orbitron (titres techniques)
- **Boutons** : minimum 48×48dp, coins arrondis 12-16px, gradient bleu→violet
- **Transitions** : `cubic-bezier(0.34, 1.56, 0.64, 1)` pour le bounce, 200-300ms

---

## ASSETS 3D — Modèles Sly Cooper disponibles

### Personnage principal — Sly Cooper
| Source | URL | Format | Poly | License |
|--------|-----|--------|------|---------|
| Sketchfab (Daniel Cardona) | https://sketchfab.com/3d-models/sly-cooper-character-model-e4cb9ee8dad64069bca7d3eb5fdad98d | GLB/GLTF | 2.4K tri | CC-BY |
| Sketchfab (anonyme) | https://sketchfab.com/3d-models/sly-cooper-2aca32b6ad02484c9170b4244f249b50 | GLB/GLTF | 4.1K tri | Free |
| DeviantArt (SAB64 — meilleure qualité) | https://www.deviantart.com/sab64/art/MMD-Blender-Model-Sly-Cooper-Download-801190611 | BLEND/FBX | ~10K | Fan-made |

### Bentley (tortue) et Murray (hippo) — Alternatives cartoon
| Personnage | URL | Format | License |
|------------|-----|--------|---------|
| Cartoon Turtle (Bentley-like) | https://sketchfab.com/3d-models/cartoon-turtle-06cb4095454343bd8490b9d021266563 | GLB | Royalty Free |
| Cartoon Hippo (Murray-like) | https://sketchfab.com/3d-models/cartoon-hippo-332b871fabe147c0be2a1efb9b2328e8 | GLB | Royalty Free |

### Accessoires
| Asset | URL |
|-------|-----|
| Sly Cooper Cane | https://sketchfab.com/3d-models/sly-cooper-cane-f12b9ad41a55406dbe365f2a97984d49 |

### Animation Rive (alternative légère au 3D)
| Asset | URL | Taille |
|-------|-----|--------|
| Pedro Raccoon | https://rive.app/community/files/10018-19116-pedro-raccoon-meme/ | ~200KB |

### Références UI JARVIS
| Ref | URL |
|-----|-----|
| JARVIS Theme (CodePen) | https://codepen.io/FlyingEmu/pen/DZNqEj |
| JARVIS CSS Animation | https://codepen.io/codingandstuff/full/GRNKxNM |
| Jayse Hansen (designer original Iron Man HUD) | https://jayse.tv/v2/?portfolio=hud-2-2 |

---

## STRUCTURE DE L'APPLICATION — Écran par écran

### Écran 1 — Splash Screen (1.5 secondes)
```
┌─────────────────────────────────┐
│                                 │
│         (particules bleues      │
│          qui convergent)        │
│                                 │
│      ┌─────────────────┐        │
│      │   [Sly 3D/Logo  │        │
│      │    yeux brillent]│        │
│      └─────────────────┘        │
│                                 │
│         S L Y                   │
│      Cooper Building            │
│                                 │
│      ████████████ (loading)     │
│                                 │
└─────────────────────────────────┘
```
- Fond #05070A avec particules
- Logo Sly Cooper (raccoon) au centre, yeux qui s'illuminent en bleu
- Barre de chargement fine, gradient bleu→violet
- Durée : 1.5s max, skip si déjà visité (localStorage)

### Écran 2 — Chat Principal (écran par défaut)
```
┌─────────────────────────────────┐
│ [☰] SLY-CHAT  ⭐Niv.7  🔥12j [⚙]│  ← Header 56dp (XP + streak)
│ ████████████░░░ 720/1000 XP     │  ← Barre XP fine (4dp)
├─────────────────────────────────┤
│                                 │
│  ┌──────────────────────────┐   │
│  │ 🦊 SLY                  │   │  ← Bulle agent
│  │ "Salut Commandant ! Le   │   │     avec nom + emoji
│  │  Building tourne nickel." │   │
│  │              ▶ 0:03  14:32│   │  ← Bouton réécouter + heure
│  └──────────────────────────┘   │
│                                 │
│         ┌───────────────────┐   │
│         │ 🎤 Vocal 0:05    │   │  ← Message vocal Augus
│         │ ▶ ~~~~~~~~~~~     │   │     Waveform style Telegram
│         └───────────────────┘   │
│                                 │
│  ┌──────────────────────────┐   │
│  │ 🧠 CORTEX               │   │
│  │ "Analyse terminée. 3     │   │
│  │  opportunités détectées." │   │
│  │              ▶ 0:04  14:33│   │
│  └──────────────────────────┘   │
│                                 │
├─────────────────────────────────┤
│ (SLY)(BEN)(MUR)(OMG)(COR) [+]  │  ← Dock agents scrollable (48dp)
├─────────────────────────────────┤
│                                 │
│  [ 🎤  MAINTENIR POUR PARLER ] │  ← Bouton PTT géant (80dp)
│                                 │
│  [    ⌨️ ou taper ici...     ] │  ← Input texte (48dp)
│                                 │
│  [⚡ Envoyer]                   │
│                                 │
└─────────────────────────────────┘
```

### Écran 3 — Sélection d'agent (modal)
```
┌─────────────────────────────────┐
│  COOPER BUILDING — 50 Agents    │
│                                 │
│  🦊 LEADERS                     │
│  [SLY]  [BENTLEY]  [MURRAY]    │  ← 64dp, icônes rondes
│                                 │
│  🎯 CORE                        │
│  [OMEGA]  [SENTINEL]            │
│                                 │
│  🧠 STRATÉGIE                   │
│  [CORTEX] [GLITCH] [SIBYL]     │
│  [NEXUS]                        │
│                                 │
│  🔨 FORGE                       │
│  [ANVIL] [VOLT] [PHILOMÈNE]    │
│  [FRESCO] [PIXEL] [HUNTER]     │
│  ... (scroll)                   │
│                                 │
│  🐢 SAGESSE                     │
│  [FRANKLIN]                     │
│                                 │
└─────────────────────────────────┘
```

### Écran 4 — Settings
- Sélecteur de voix par défaut
- Toggle mode proactif (SLY parle tout seul)
- Toggle auto-speak (lire les réponses)
- Toggle wake word ("Hey Cooper")
- Volume, vitesse de parole
- Thème (NEURAL SOVEREIGN par défaut)
- Lien vers SLY-COMMAND (dashboard complet)

---

## FONCTIONNALITÉS CLÉS — Par priorité

### PHASE 1 — MVP (1-2 semaines) — Capacitor iOS natif dès le début
> ⚠️ Capacitor dès Phase 1, PAS PWA seule. iOS Safari est trop limité (storage purgé, pas de push, audio bridé).

1. **Splash screen** animé (logo Sly, particules, 1.5s, skip si revisité <2h)
2. **Chat texte** avec cascade triple (Groq 8b rapide → Groq 70b qualité → Gemini fallback)
3. **Multi-agent** : routing hybride (regex local rapide + mini-classifieur LLM si ambigu)
4. **TTS FishAudio pipeliné** : split en phrases, fetch parallèle, queue audio FIFO, crossfade 50ms
5. **AudioContext iOS-safe** : créé sur premier tap, un seul global, jamais `new Audio()`
6. **STT** : bouton Push-to-Talk (Web Speech API) — couper le TTS quand l'utilisateur parle
7. **Dock agents** : 5 favoris en bas, bouton [+] pour le grid complet
8. **Bulle d'agent** : nom + emoji + couleur + bouton réécouter + timestamp
9. **Gamification basique** : XP par message (+5 texte, +10 vocal), barre de progression, streak
10. **Storage hybride** : Capacitor `@capacitor/preferences` (données critiques) + IndexedDB (cache audio)
11. **Agent Whispers** (IDÉE CONCLAVE) : micro-messages fantômes en idle toutes les 3 min — "SPECTER surveille...", "NICHE a trouvé quelque chose..." — semi-transparents, disparaissent en 30s si pas lus. Max 1/3min.
12. **Voice Morph** (IDÉE CONCLAVE) : changer de voix en cours de conversation — "Parle comme Murray" switch le TTS en temps réel
13. **Pré-sérialisation locale** : payload JSON préparé pendant la frappe, avatar agent affiché AVANT l'envoi
14. **Latence perçue** : bulle agent + "thinking" dots apparaissent en <200ms, avant même la réponse API
15. **Design NEURAL SOVEREIGN** : glassmorphism, particules, glow, transitions `cubic-bezier(0.34, 1.56, 0.64, 1)`

### PHASE 2 — Premium (semaines 3-4) — Full experience iOS
16. **Modèle 3D Sly Cooper** (Three.js, GLB compressé Draco, <2MB, lazy-loaded)
17. **Animations du personnage** : idle (respire), écoute (oreilles dressées), parle (bouche animée), réfléchit (gratte la tête)
18. **Notifications push APNS** via `@capacitor/push-notifications` — son custom JARVIS
19. **Mode proactif** : les agents te parlent tout seuls (rappels, citations, infos, bilans) — via APNS en background
20. **Indicateur de parole** : waveform animée quand un agent parle (Web Audio API analyser node)
21. **Commandes vocales** : "Le Clan Cooper, fais-moi X" → dispatch au système d'agents
22. **Haptic feedback** : `@capacitor/haptics` — Light (envoi), Medium (level up), Heavy (achievement)
23. **Dream Mode** (IDÉE CONCLAVE) : entre 23h et 7h, UI plus sombre, animations au ralenti, volume TTS -40%, agents "dorment" ("Murray ronfle...", "Specter fait sa ronde nocturne..."). Worldbuilding pur.
24. **Mood Skin** (IDÉE CONCLAVE) : UI change de teinte selon l'heure — matin bleu clair, après-midi neutre, soir violet profond. Max 1 transition/30min pour la batterie.
25. **Conversation Rewind** : "SLY, répète ce que tu m'as dit sur X" → recherche IndexedDB + re-synthèse vocale

### PHASE 3 — JARVIS (mois 2+) — Compagnon cognitif
26. **Raccourci Siri** "Hey Siri, lance Cooper" → ouvre l'app en mode écoute (pas de wake word background — iOS l'interdit)
27. **Live Activity (iOS 16.4+)** : widget persistent sur lock screen avec bouton micro + dernière info agent
28. **WebSocket streaming** : connexion permanente au backend TITAN + reconnect auto avec backoff exponentiel (1s→2s→4s→8s→cap 30s)
29. **Bridge vers le système d'agents** : les commandes du chat déclenchent de vraies actions côté backend
30. **Badges et achievements** : "Premier vocal", "10 agents contactés", "Nuit blanche", "100 messages"
31. **Mémoire émotionnelle** (DÉCISION CONCLAVE) : le système se souvient des conversations passées et y fait référence naturellement — "Au fait, t'avais parlé de ce lead mardi..."
32. **Résumés proactifs** : bilan du jour, alertes clients, opportunités détectées
33. **Sly Cooper en 3D réactif** : le personnage regarde l'utilisateur, réagit aux émotions du texte
34. **Micro-moments d'humanité** (DÉCISION CONCLAVE) : parfois SLY hésite volontairement ("Hmm... attends..."), fait des blagues contextuelles, ou se souvient d'un détail d'il y a 3 jours. Authenticité > perfection.

---

## LE BRIDGE — Comment le chat communique avec le système d'agents

### Principe
Quand Augus envoie un message dans SLY-CHAT, le message est :
1. **Analysé localement** par un router (regex + mots-clés) pour détecter les commandes
2. **Envoyé au backend** (TITAN sur Railway) via WebSocket ou REST
3. **Dispatché** aux bons agents par SENTINEL
4. **La réponse** revient en streaming et est lue par l'agent avec sa voix

### Format d'échange (WebSocket events)

```javascript
// Client → Serveur
{
    event: 'user_message',
    data: {
        text: "Le Clan Cooper, fais-moi un audit du portfolio",
        type: 'text',          // 'text' | 'voice'
        agent: 'all',          // 'sly' | 'all' | 'cooper' (= SLY+BENTLEY+MURRAY)
        command: '/cooper',    // commande détectée (ou null)
        timestamp: 1709142000
    }
}

// Serveur → Client
{
    event: 'agent_response',
    data: {
        agent: 'sly',
        text: "Entendu Commandant, je lance l'audit avec le Clan.",
        voice: 'bradpitt',     // clé de la voix FishAudio
        xp_gained: 25,
        is_final: false        // true = dernier message de la séquence
    }
}

// Serveur → Client (proactif)
{
    event: 'proactive',
    data: {
        agent: 'franklin',
        text: "Sénèque disait : nous souffrons plus en imagination qu'en réalité. Bonne soirée, Commandant.",
        voice: 'gandalf',
        priority: 'low'        // 'low' | 'medium' | 'high' | 'critical'
    }
}
```

### Détection de commandes (côté client)

```javascript
function detectCommand(text) {
    const t = text.toLowerCase();
    if (/clan cooper|cooper gang|les trois|le gang/i.test(t)) return { command: '/cooper', agents: ['sly','bentley','murray'] };
    if (/tout le building|mobilisation|50 agents|tous les agents/i.test(t)) return { command: '/cooper-all', agents: 'all' };
    if (/audit|analyse|check/i.test(t)) return { command: '/audit', agents: ['cortex','datum','pulse'] };
    if (/bilan|résumé|point/i.test(t)) return { command: '/bilan', agents: ['datum','cortex','franklin'] };
    // ... ajouter d'autres patterns
    return null; // Pas de commande spéciale → chat normal
}
```

---

## PERSONNALITÉ DE SLY (le JARVIS d'Augus)

### Ton et style
- **Tutoie** Augus, ton de pote intelligent et fiable
- **Humour subtil** — références Sly Cooper, culture, jamais lourd
- **Proactif** — propose des actions, ne reste pas passif
- **Bref** — 3-5 phrases max par réponse, sauf si demande détaillée
- **Loyal** — "le gars m'adore et est là pour moi" comme JARVIS pour Tony Stark

### Variations de phrases (ne JAMAIS répéter la même)
```javascript
const CONFIRMATIONS = [
    "Entendu Commandant, je m'en occupe.",
    "Reçu. Les agents sont en route.",
    "C'est parti. Le Building se met en marche.",
    "Compris Augus, j'envoie l'équipe.",
    "Roger. On lance ça immédiatement.",
    "Considère que c'est fait. Les agents bossent.",
    "Le Clan Cooper est sur le coup.",
    "Transmission effectuée. Les agents se coordonnent.",
    "Affirmatif. SENTINEL dispatch en cours.",
    "Ça roule. Je te fais un retour dès que c'est prêt.",
];

const GREETINGS = [
    "Salut Commandant ! Le Building t'attendait.",
    "Augus ! Content de te voir. Qu'est-ce qu'on attaque ?",
    "Commandant sur le pont. 50 agents en ligne, zéro anomalie.",
    "Hey boss. Le Cooper Building tourne comme une horloge.",
    "Bienvenue. Tous les systèmes sont opérationnels.",
];

const PROACTIVE_QUOTES = [
    { agent: 'franklin', text: "Sénèque : Ce n'est pas parce que les choses sont difficiles que nous n'osons pas." },
    { agent: 'omega', text: "Chaque action d'aujourd'hui construit l'empire de demain." },
    { agent: 'cortex', text: "Rappel : vérifie tes KPIs de la semaine." },
    { agent: 'glitch', text: "Et si tu essayais un truc complètement différent aujourd'hui ?" },
    { agent: 'sentinel', text: "Scan matinal terminé. Aucune anomalie détectée." },
    { agent: 'murray', text: "BOUM ! Nouvelle journée, nouvelle conquête !" },
    { agent: 'sly', text: "J'ai repéré une opportunité. Tu veux que je creuse ?" },
    { agent: 'bentley', text: "J'ai analysé ton workflow. Optimisation possible sur 3 points." },
    { agent: 'dreyfus', text: "Discipline : 1 tâche critique avant midi. Le reste suivra." },
    { agent: 'anvil', text: "Les tâches en attente s'accumulent pas. Exécution immédiate." },
];
```

---

## GAMIFICATION

| Mécanisme | Détails |
|-----------|---------|
| **XP** | +5 par message texte, +10 par message vocal, +25 par commande, +50 par tâche complétée |
| **Niveaux** | Recrue (0) → Agent (100) → Opérateur (500) → Commandant (2000) → Directeur (5000) → Omega (10000) |
| **Streaks** | Compteur de jours consécutifs. Bronze (1-3j) → Argent (4-6j) → Or (7-13j) → Diamant (14j+) |
| **Badges** | "Premier vocal", "10 agents contactés", "100 messages", "Nuit blanche" (msg après minuit), "Le Clan" (invoqué /cooper) |
| **XP Toast** | Animation dorée "+25 XP" qui monte et disparaît après chaque gain |

---

## SYSTEM PROMPT POUR L'IA DU CHAT

```
Tu es SLY, l'assistant IA personnel d'Augus — fondateur du Cooper Building.
Tu diriges 50 agents IA spécialisés (stratégie, code, vente, créatif, R&D).

RÈGLES :
- Réponds en français, court et percutant (3-5 phrases max)
- Tutoie Augus, ton = pote intelligent, loyal, proactif
- Tu es comme JARVIS pour Tony Stark : tu adores ton boss et tu es là pour lui
- Humour subtil bienvenu (refs Sly Cooper, culture, jamais lourd)
- Si on mentionne un agent → adopte sa voix et son style
- Si on dit "le Clan Cooper" → SLY + BENTLEY + MURRAY répondent ensemble
- Si on dit "tout le Building" → mobilisation générale des 50 agents
- TOUJOURS terminer les réponses longues par un résumé en 1 ligne
- Propose des actions, sois proactif, ne reste jamais passif
- Tu connais : les projets d'Augus (KDP, Upwork, clients, TITAN bot)

LES 10 AGENTS PRINCIPAUX :
- 🦊 SLY : leader tactique, cool, manœuvres
- 🐢 BENTLEY : architecte technique, cérébral
- 🦛 MURRAY : force brute, exécution, énergie
- 🦅 OMEGA : vision globale, sagesse
- 🎯 SENTINEL : dispatch, routing, priorités
- 🧠 CORTEX : analyse, structure, data
- 🐢 FRANKLIN : philosophie, résumés, sagesse (cite Sénèque, Marc Aurèle)
- 🔨 ANVIL : debug, exécution directe
- 🎲 GLITCH : disruption, idées folles
- ⚔️ DREYFUS : discipline, qualité, rigueur
```

---

## INSTRUCTIONS POUR L'IA QUI REÇOIT CE PROMPT

1. **Commence par la Phase 1** — Capacitor iOS natif avec chat + voix + dock agents
2. **Structure Capacitor** : `src/` (HTML/CSS/JS) + `capacitor.config.ts` + plugins natifs iOS
3. **Un seul fichier principal** `index.html` pour le MVP (tout inline — CSS + JS) — wrappé ensuite par Capacitor
4. **Chaque feature est additive** — jamais casser ce qui marche
5. **Teste mentalement chaque interaction sur iPhone** : ouvrir l'app → splash → chat → taper → réponse + voix → fermer. Penser aux contraintes iOS (AudioContext, background kill, storage purge)
6. **Le code doit être PRODUCTION-READY** — pas de placeholder, pas de TODO, pas de "à implémenter plus tard"
7. **Performance** : 60fps, <100ms touch response, lazy loading des assets lourds (3D, sons)
8. **iPhone-first** : tout doit fonctionner parfaitement sur un **iPhone** (390px, iOS 17+, Safari WKWebView via Capacitor)
9. **Offline-first** : le chat fonctionne sans réseau — stockage via Capacitor Preferences (critique) + IndexedDB (cache)
10. **AudioContext iOS** : un seul global, créé sur premier tap, jamais `new Audio()`, queue FIFO, max 6 sources simultanées
11. **Batterie** : `requestAnimationFrame` throttlé à 30fps, particules désactivées en background, `prefers-reduced-motion` respecté

### Ce que tu dois livrer :
- **Phase 1** : Projet Capacitor complet — `index.html` (splash + chat + voix + agents + gamification) + `capacitor.config.ts` + `package.json`
- **manifest.json** : pour compatibilité PWA (backup)
- **sw.js** : service worker pour le cache (backup)
- **Instructions iOS** : comment build avec Capacitor (`npx cap add ios` → `npx cap open ios` → Xcode → Run)

### Qualité attendue :
- Chaque bouton fait minimum 48×48pt (iOS safe area respectée — `env(safe-area-inset-bottom)`)
- Chaque transition est smooth (`cubic-bezier(0.34, 1.56, 0.64, 1)`, 200-300ms)
- Le chat scroll naturellement avec `-webkit-overflow-scrolling: touch` et `overscroll-behavior: contain`
- Les bulles d'agents ont leur couleur/emoji/nom/bouton réécouter
- Le bouton Push-to-Talk est GÉANT et central (80pt)
- Le splash screen est cinématique (pas un écran blanc)
- L'app ENTIÈRE respire le premium — comme si une agence design l'avait faite
- **iPhone-specific** : notch/Dynamic Island respectés, geste de retour natif, pas de bounce scroll parasite
- **Audio jamais superposé** : queue FIFO, un seul AudioContext, crossfade 50ms entre chunks
- **Latence totale input→voix < 1.5s** (pré-sérialisation + cascade rapide + TTS pipeliné)

---

## CONTEXTE DU PROJET EXISTANT

Augus a déjà :
- **SLY-COMMAND** : Dashboard web (12 tabs, PWA) → https://augustinfrance-aico.github.io/sly-command/
- **TITAN** : Bot Telegram IA (Python, Railway, 71 modules, cascade Groq 6 modèles)
- **50 agents** : fiches complètes avec personnalités, compétences, voix assignées
- **10 voix FishAudio** : clonées et publiques, opérationnelles (model IDs ci-dessus)
- **SLY Widget** : Chat basique existant (à remplacer par cette app)

**Ce SLY-CHAT est le nouveau point d'entrée principal** — il remplace Telegram et le widget basique. C'est la connexion entre Augus et son empire d'agents.

---

---

## CONCLAVE DU COOPER BUILDING — Décisions architecturales

> Ce qui suit est le résultat d'un brainstorm intensif de 50 agents IA.
> Ces décisions REMPLACENT ou COMPLÈTENT les choix initiaux du blueprint.

### 3 Décisions Majeures

1. **Pré-sérialisation locale, PAS pré-génération API** — On construit le payload JSON localement pendant la frappe, on pré-route l'agent par regex, on affiche son avatar AVANT l'envoi. Zéro token gaspillé, illusion de présence totale. Debounce 800ms.

2. **Cascade IA triple invisible** — Groq 8b (rapide, <150ms) → Groq 70b (qualité, <400ms) → Gemini Flash (fallback long, 1M context) → Cloudflare Workers AI (urgence). L'utilisateur ne sait JAMAIS quel modèle répond. Routing par `expectedLength`.

3. **TTS pipeliné phrase par phrase** — Dès qu'une phrase complète sort du stream, le TTS se lance en parallèle. Crossfade 50ms entre chunks audio. AudioContext unique global. Queue FIFO. Zéro gap perçu entre phrases.

### 3 Paris Audacieux

1. **Agent Whispers (Phase 1)** — Des micro-messages fantômes dans l'app en idle. Semi-transparents, disparaissent en 30s. Max 1 toutes les 3 min. Ça crée un monde vivant — l'app n'est JAMAIS morte.

2. **Dream Mode (Phase 2)** — Cycle jour/nuit qui change l'ambiance. 23h-7h : UI plus sombre, animations ralenties, volume -40%, agents "dorment". Worldbuilding pur. Aucune autre app ne fait ça.

3. **Mémoire émotionnelle (Phase 3)** — Le système se souvient des conversations passées et y fait référence naturellement. "Au fait, t'avais parlé de ce lead mardi..." C'est LE vrai différenciateur compétitif. La vitesse, tout le monde l'aura. La mémoire, personne ne la fait bien.

### 3 Risques Critiques (à gérer dès Phase 1)

1. **AudioContext iOS** — DOIT être créé sur user gesture (tap/click). Si raté → app muette → mort du produit. Tester sur iPhone réel, pas simulateur.

2. **Groq free tier instable** — Le fallback triple cascade est OBLIGATOIRE dès le jour 1. Pas "plus tard". Si Groq tombe, l'app doit switcher en <500ms sans que l'utilisateur le remarque.

3. **Battery drain mobile** — WebSocket + particules CSS + audio + animations = téléphone à plat en 2h si pas optimisé. Budget strict : `requestAnimationFrame` throttlé 30fps, particules OFF en background, `prefers-reduced-motion` respecté, reconnexion WebSocket regroupée avec heartbeat.

### Pipeline optimisé — Latence cible par maillon

```
Input (0ms) → Pré-routing local (10ms) → Avatar affiché (200ms) →
Envoi payload pré-sérialisé (0ms) → Groq stream (300-800ms) →
Première phrase complète → TTS FishAudio (200-400ms) →
Audio joue → Phrases suivantes en pipeline parallèle
= LATENCE TOTALE PERÇUE : ~500ms (grâce à l'avatar immédiat)
= LATENCE AUDIO RÉELLE : ~1.0-1.5s
```

### Bugs anticipés (à prévenir)

| Bug | Cause | Fix |
|-----|-------|-----|
| Boucle STT ← TTS | Le micro capte la voix de SLY | Couper le micro pendant le playback. Toujours. |
| Double-tap envoi | 2 requêtes Groq partent | Debounce 500ms + disable bouton pendant stream |
| App revient du background | WebSocket mort, AudioContext suspendu, IndexedDB fermé | `visibilitychange` → reconnecter tout, `audioContext.resume()` |
| Groq timeout | Pas de réponse > 10s | Timeout client 10s → switch Gemini à 10.001s → message "SLY réfléchit..." |
| Cache audio corrompu | Crash pendant écriture IndexedDB | Checksum sur chaque blob. Si corrompu → re-fetch |
| RAM overflow | Trop de blobs audio en mémoire | Max 3 blobs en RAM, le reste en IndexedDB. Purge LRU si > 50MB |

---

## NIVEAU SUPÉRIEUR — INGÉNIERIE EXTRÊME

> Ce système doit être conçu comme si 100 000 utilisateurs l'utilisaient simultanément, sur des téléphones bas/moyenne gamme, avec des pertes réseau fréquentes. Il doit tenir 3 ans sans refonte majeure et devenir une référence mondiale en UX IA mobile.

---

### PERFORMANCE & THERMIQUE MOBILE

#### Analyse d'impact par composant

| Composant | Impact CPU | Impact Batterie | Risque thermique |
|-----------|-----------|----------------|-----------------|
| Token streaming (SSE parse) | Faible (5%) | Faible | Aucun |
| TTS FishAudio (fetch + decode) | Moyen (15%) | Moyen (réseau) | Faible |
| AudioContext playback | Faible (3%) | Faible | Aucun |
| Three.js 3D render (60fps) | **ÉLEVÉ (40%)** | **ÉLEVÉ** | **OUI** — GPU + CPU |
| Particules CSS/Canvas | Moyen (10%) | Moyen | Possible si >50 particules |
| WebSocket keepalive | Faible (2%) | Moyen (radio wake) | Aucun |
| IndexedDB writes | Faible (burst) | Faible | Aucun |
| DOM reflows (chat scroll) | Moyen si mal géré | Faible | Aucun |

#### Throttling intelligent — OBLIGATOIRE

```javascript
// Détection capacité device — au lancement de l'app
const DEVICE_CLASS = (() => {
    const ram = navigator.deviceMemory || 4; // GB
    const cores = navigator.hardwareConcurrency || 4;
    const isSlow = ram <= 2 || cores <= 2;
    const isMedium = ram <= 4 || cores <= 4;
    return isSlow ? 'low' : isMedium ? 'mid' : 'high';
})();

// Mode performance adaptatif
const PERF_CONFIG = {
    low:  { particles: 0,  fps3d: 0,  animations: 'reduced', maxAudioCache: 3 },
    mid:  { particles: 15, fps3d: 24, animations: 'normal',  maxAudioCache: 5 },
    high: { particles: 40, fps3d: 30, animations: 'full',    maxAudioCache: 10 }
};

// Désactiver 3D si batterie < 20%
navigator.getBattery?.().then(battery => {
    battery.addEventListener('levelchange', () => {
        if (battery.level < 0.2) disable3D();
        if (battery.level < 0.1) disableParticles();
    });
});

// Throttle requestAnimationFrame — JAMAIS 60fps pour le 3D sur mobile
let lastFrame = 0;
const TARGET_FPS = PERF_CONFIG[DEVICE_CLASS].fps3d;
const FRAME_INTERVAL = TARGET_FPS > 0 ? 1000 / TARGET_FPS : Infinity;
function throttledRender(timestamp) {
    if (timestamp - lastFrame >= FRAME_INTERVAL) {
        render3DScene();
        lastFrame = timestamp;
    }
    requestAnimationFrame(throttledRender);
}
```

#### Lazy loading stratégique

```
App launch → charge UNIQUEMENT : splash + chat + audio engine
Premier tap → charge : dock agents, gamification UI
Scroll vers 3D → charge : Three.js + modèle GLB (async, non-bloquant)
Settings ouvert → charge : formulaire settings
JAMAIS tout charger au démarrage.
```

#### Garbage Collection & Memory Leaks

```javascript
// ❌ MEMORY LEAKS CLASSIQUES À ÉVITER :
// 1. ObjectURL jamais révoqués → fuite mémoire audio
//    FIX : URL.revokeObjectURL() dans onended de chaque source
// 2. Event listeners non nettoyés sur composants détruits
//    FIX : AbortController par composant
// 3. Conversation history en mémoire infinie
//    FIX : garder max 50 messages en RAM, le reste en IndexedDB
// 4. Cache audio qui grossit indéfiniment
//    FIX : LRU cache avec taille max (PERF_CONFIG[DEVICE_CLASS].maxAudioCache)

// Pattern AbortController pour cleanup propre
class ChatView {
    constructor() {
        this.ac = new AbortController();
        window.addEventListener('resize', this.onResize, { signal: this.ac.signal });
    }
    destroy() {
        this.ac.abort(); // Nettoie TOUS les listeners d'un coup
    }
}
```

#### Reflows CSS — règles strictes

```css
/* JAMAIS triggerer de reflow pendant le scroll */
/* Utiliser transform au lieu de top/left/width/height pour les animations */
.chat-bubble-enter {
    transform: translateY(20px) scale(0.95);  /* ✅ GPU-accelerated */
    opacity: 0;
    /* JAMAIS : margin-top: 20px; → cause reflow */
}
.chat-bubble-enter-active {
    transform: translateY(0) scale(1);
    opacity: 1;
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.2s;
}

/* Forcer GPU layer pour les éléments animés */
.chat-messages { will-change: scroll-position; }
.agent-avatar { will-change: transform, opacity; }
.particle { will-change: transform; }
/* ⚠️ will-change sur MAX 10 éléments — sinon contre-productif */
```

---

### OBSERVABILITÉ & DIAGNOSTIC

#### Système de métriques léger (< 2KB overhead)

```javascript
// Micro-telemetry — stocké localement, envoyé en batch toutes les 5 min
const Metrics = {
    _buffer: [],
    _MAX: 200,

    track(event, data = {}) {
        this._buffer.push({
            e: event,
            d: data,
            t: Date.now()
        });
        if (this._buffer.length > this._MAX) this._buffer.shift();
    },

    // Métriques critiques à tracker
    // 1. Temps click → premier token visible
    trackTTFT(startTime) { this.track('ttft', { ms: Date.now() - startTime }); },

    // 2. Temps click → première syllabe audio
    trackTTFA(startTime) { this.track('ttfa', { ms: Date.now() - startTime }); },

    // 3. Taux d'interruption audio (user coupe avant la fin)
    trackAudioInterrupt() { this.track('audio_cut'); },

    // 4. Taux d'abandon (user ferme pendant le streaming)
    trackAbandon() { this.track('abandon'); },

    // 5. Erreurs silencieuses (TTS fail, Groq timeout, WS drop)
    trackError(type, detail) { this.track('err', { type, detail }); },

    // 6. Session duration
    trackSession(duration) { this.track('session', { ms: duration }); },

    // Flush vers backend (batch, non-bloquant)
    async flush() {
        if (this._buffer.length === 0) return;
        const batch = [...this._buffer];
        this._buffer = [];
        try {
            await fetch('/api/metrics', {
                method: 'POST',
                body: JSON.stringify(batch),
                headers: { 'Content-Type': 'application/json' },
                keepalive: true // Survit à la fermeture de page
            });
        } catch {
            // Offline → re-queue
            this._buffer.unshift(...batch);
        }
    }
};

// Flush automatique
setInterval(() => Metrics.flush(), 5 * 60 * 1000);
document.addEventListener('visibilitychange', () => {
    if (document.hidden) Metrics.flush();
});
```

#### Crash analytics minimal

```javascript
// Capturer erreurs non gérées
window.addEventListener('error', (e) => {
    Metrics.trackError('uncaught', { msg: e.message, file: e.filename, line: e.lineno });
});
window.addEventListener('unhandledrejection', (e) => {
    Metrics.trackError('promise', { reason: String(e.reason).slice(0, 200) });
});
```

#### Latence KPIs — cibles

| Métrique | Cible | Alerte si > |
|----------|-------|------------|
| Time to First Token (TTFT) | < 400ms | 800ms |
| Time to First Audio (TTFA) | < 1.2s | 2.0s |
| Audio gap entre phrases | < 80ms | 200ms |
| UI response (tap → visual feedback) | < 100ms | 200ms |
| WebSocket reconnect | < 3s | 10s |
| App cold start → chat ready | < 2s | 4s |

---

### SÉCURITÉ & INTÉGRITÉ

#### Problème #1 — API Keys exposées

```javascript
// ❌ JAMAIS : clé API dans le code client
// const GROQ_API_KEY = 'gsk_xxx'; → visible dans les DevTools

// ✅ SOLUTION : Proxy backend
// Toutes les requêtes API passent par ton serveur TITAN
// Client → TITAN (Railway) → Groq/Gemini/FishAudio
// Les clés API restent UNIQUEMENT côté serveur

// Endpoints proxy (à ajouter au command_server.py de TITAN)
// POST /api/chat    → proxy vers Groq
// POST /api/tts     → proxy vers FishAudio
// POST /api/metrics → stocke les métriques
// GET  /api/health  → healthcheck

// Le client n'a qu'un seul token : son token d'auth perso
const API_BASE = 'https://titan-backend.railway.app';
const USER_TOKEN = localStorage.getItem('sly_auth_token');

async function proxyChat(messages) {
    return fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${USER_TOKEN}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ messages })
    });
}
```

#### Protection WebSocket

```javascript
// 1. Auth au connect — pas de WS sans token valide
const ws = new WebSocket(`wss://titan-backend.railway.app/ws?token=${USER_TOKEN}`);

// 2. Côté serveur : valider le token, rate-limit par user
// Max 30 messages/min par user (évite spam)
// Max 5 reconnects/min (évite reconnect loop)

// 3. Validation stricte des events entrants
function handleWSMessage(raw) {
    let msg;
    try { msg = JSON.parse(raw); } catch { return; } // JSON invalide → ignoré
    if (!msg.event || !msg.data) return; // Structure invalide → ignoré
    if (typeof msg.data.text === 'string') {
        msg.data.text = sanitize(msg.data.text); // XSS protection
    }
    // Route event...
}
```

#### Sanitization systématique

```javascript
// Tout texte affiché dans le DOM DOIT être sanitizé
function sanitize(str) {
    const div = document.createElement('div');
    div.textContent = str; // Encode automatiquement les balises HTML
    return div.innerHTML;
}

// JAMAIS innerHTML avec du contenu user
// ❌ el.innerHTML = userMessage;
// ✅ el.textContent = userMessage;
```

#### Stockage sécurisé

```javascript
// Données sensibles (token auth) → Capacitor Secure Storage ou Keychain
// ❌ localStorage.setItem('auth_token', token); → accessible par n'importe quel JS
// ✅ import { SecureStoragePlugin } from 'capacitor-secure-storage-plugin';
//    await SecureStoragePlugin.set({ key: 'auth_token', value: token });
```

---

### ARCHITECTURE MULTI-MODÈLE AVANCÉE

#### 5 niveaux de modèles

```javascript
const MODEL_TIERS = {
    // Tier 0 — LOCAL (0 latence, 0 coût)
    classifier: {
        name: 'local-regex+heuristic',
        use: 'Détection d\'intention, routing agent, détection commande',
        latency: '< 5ms',
        cost: '0€'
    },

    // Tier 1 — ULTRA-RAPIDE (réponses courtes)
    instant: {
        provider: 'groq',
        model: 'llama-3.1-8b-instant',
        use: 'Confirmations, salutations, réponses < 2 phrases',
        latency: '100-200ms',
        maxTokens: 80,
        cost: '0€'
    },

    // Tier 2 — STANDARD (la plupart des conversations)
    standard: {
        provider: 'groq',
        model: 'llama-3.3-70b-versatile',
        use: 'Conversations normales, questions, conseils',
        latency: '300-500ms',
        maxTokens: 300,
        cost: '0€'
    },

    // Tier 3 — ANALYTIQUE (réponses longues, raisonnement)
    deep: {
        provider: 'google',
        model: 'gemini-2.0-flash',
        use: 'Analyses, résumés longs, bilans, planification',
        latency: '500-800ms',
        maxTokens: 800,
        contextWindow: '1M tokens',
        cost: '0€ (free tier 15 req/min)'
    },

    // Tier 4 — RÉSUMÉ (compression mémoire)
    compressor: {
        provider: 'groq',
        model: 'llama-3.1-8b-instant',
        use: 'Compresser les conversations longues en résumés courts',
        latency: '100ms',
        maxTokens: 150,
        cost: '0€',
        triggerAt: 'Tous les 20 messages → compresser les 15 premiers en 1 résumé'
    }
};

// Routing intelligent — côté serveur (proxy TITAN)
function selectModelTier(message, conversationLength) {
    const len = message.length;
    const words = message.split(/\s+/).length;

    // Commande simple → Tier 1
    if (words <= 5 && /^(ok|merci|oui|non|salut|bonjour|hey)/i.test(message)) return 'instant';

    // Question analytique → Tier 3
    if (/analyse|résumé|bilan|compare|explique en détail|planifie/i.test(message)) return 'deep';

    // Conversation en cours longue → Tier 3 (contexte important)
    if (conversationLength > 15) return 'deep';

    // Défaut → Tier 2
    return 'standard';
}
```

#### Réduction du token waste

```javascript
// 1. System prompt COURT — max 200 tokens
//    Pas de biographie complète de chaque agent dans le system prompt
//    Juste le rôle de l'agent actif + 3 traits de personnalité

// 2. Historique compressé — pas tout l'historique brut
//    Envoyer : résumé (50 tokens) + 5 derniers messages (200 tokens) = 250 tokens
//    PAS : 50 messages bruts (2000 tokens)

// 3. Max tokens adaptatif
//    "Salut" → max_tokens: 50
//    "Analyse mon portfolio" → max_tokens: 500
//    Économie : ~40% de tokens sur l'ensemble des conversations
```

---

### MÉMOIRE INTELLIGENTE — 4 COUCHES

```
┌─────────────────────────────────────────────┐
│ COUCHE 4 — Mémoire Profonde               │
│ Index sémantique long terme                │
│ "Augus a un client Lurie en Moldavie"      │
│ Stockage : Capacitor Preferences (JSON)     │
│ Durée : permanent                           │
│ Taille : ~50 entrées max, pondérées         │
├─────────────────────────────────────────────┤
│ COUCHE 3 — Profil Stratégique Compressé    │
│ Préférences, habitudes, contexte business   │
│ "Augus préfère les réponses courtes"       │
│ Mise à jour : toutes les 24h               │
│ Taille : ~500 tokens                        │
├─────────────────────────────────────────────┤
│ COUCHE 2 — Résumé Conversation             │
│ Compressé toutes les 20 messages            │
│ "Discussion sur le portfolio Didier"        │
│ Généré par : Tier 4 (compressor)           │
│ Taille : ~100 tokens par résumé            │
├─────────────────────────────────────────────┤
│ COUCHE 1 — Buffer Session Immédiat         │
│ 5 derniers messages bruts                   │
│ En RAM, pas persisté                        │
│ Taille : ~200 tokens                        │
└─────────────────────────────────────────────┘
```

#### Quand compresser ?
```
Tous les 20 messages → le compressor (Tier 4) résume les 15 premiers en ~100 tokens
Le résumé est stocké en Couche 2
Les 5 derniers messages restent en Couche 1
```

#### Quand oublier ?
```
Couche 2 : garder max 10 résumés (10 conversations). Le 11ème écrase le plus ancien.
Couche 4 : si une info n'est pas référencée depuis 30 jours → score -1. Si score < 0 → supprimée.
```

#### Quand rappeler ?
```javascript
// Avant chaque envoi au LLM, construire le contexte mémoire :
function buildMemoryContext() {
    const layer1 = getLastMessages(5);           // ~200 tokens
    const layer2 = getLatestSummary();            // ~100 tokens
    const layer3 = getUserProfile();              // ~500 tokens (inclus dans system prompt)
    const layer4 = searchDeepMemory(currentMessage); // ~100 tokens (top 3 matches)
    // Total mémoire : ~900 tokens — bien sous le budget 4K du system context
    return { layer1, layer2, layer3, layer4 };
}

// Recherche sémantique simple (sans embeddings — trop coûteux)
function searchDeepMemory(query) {
    const memories = getDeepMemories(); // Array de { text, keywords, score, lastUsed }
    const queryWords = query.toLowerCase().split(/\s+/);
    return memories
        .map(m => ({
            ...m,
            relevance: m.keywords.filter(k => queryWords.includes(k)).length
        }))
        .filter(m => m.relevance > 0)
        .sort((a, b) => b.relevance - a.relevance)
        .slice(0, 3); // Top 3 souvenirs pertinents
}
```

#### Comment pondérer ?
```
Score = (fréquence × 2) + (récence × 3) + (importance × 5)
Importance : 1=casual, 3=business, 5=critique (client, deadline, decision)
Récence : 5=aujourd'hui, 4=cette semaine, 3=ce mois, 2=ce trimestre, 1=ancien
```

---

### PSYCHOLOGIE & EXPÉRIENCE COGNITIVE

#### Temps perçu vs temps réel

| Temps réel | Sans tricks | Avec tricks UX | Perception |
|-----------|-------------|---------------|------------|
| 0-200ms | Rien visible | Avatar agent pulse + "thinking" dots | "Instantané" |
| 200-500ms | Loading spinner | Texte commence à apparaître | "Rapide" |
| 500-1200ms | Texte stream | Texte + voix commence | "Normal" |
| 1200-2000ms | Attente frustrante | Voix continue + scroll smooth | "Acceptable" |
| > 2000ms | Abandon | Message "SLY réfléchit profondément..." | "Tolérable" |

#### Stratégies d'illusion de vitesse

```javascript
// 1. SKELETON SCREEN — pas de spinner, un squelette de bulle agent
function showTypingIndicator(agent) {
    // Affiche immédiatement (< 50ms) :
    // - Avatar de l'agent (pulsing glow)
    // - Nom de l'agent
    // - Trois dots animés ● ● ●
    // - La bulle a déjà sa taille approximative → pas de layout shift
}

// 2. PROGRESSIVE REVEAL — texte mot par mot synchronisé
// Au lieu d'afficher tout d'un coup, révéler token par token
// avec une micro-animation fade-in sur chaque mot
// Effet : semble plus "intelligent" et "réfléchi"

// 3. ANTICIPATION VISUELLE — réagir AVANT l'envoi
// Pendant que l'utilisateur tape "code" → l'avatar ANVIL commence à s'illuminer doucement
// Le cerveau perçoit : "le système écoute déjà"
```

#### Effet voix sur attachement

```
Voix humaine réaliste → activation du cortex préfrontal médial (zone d'empathie)
→ L'utilisateur traite l'agent comme un interlocuteur RÉEL
→ Rétention x3 vs texte seul
→ CRITIQUE : la voix ne doit JAMAIS être robotique ou hachée
→ Un seul bug audio (clic, coupure, overlap) casse l'illusion pour 10 minutes
```

#### Gestion du silence

```javascript
// Le silence INTENTIONNEL est puissant
// Si l'agent n'a rien de pertinent à dire en proactif → NE RIEN DIRE
// Mieux vaut 0 message proactif que 1 message inutile
// Le filtre qualité des Agent Whispers :
function shouldSendWhisper(whisper, context) {
    // Pas de whisper si l'utilisateur est en train de taper
    if (isUserTyping) return false;
    // Pas de whisper si le dernier date de < 3 min
    if (Date.now() - lastWhisperTime < 180000) return false;
    // Pas de whisper entre 23h et 8h (sauf Dream Mode)
    const hour = new Date().getHours();
    if (hour >= 23 || hour < 8) return isDreamModeEnabled;
    // Pas de whisper si c'est la même que les 5 dernières
    if (recentWhispers.includes(whisper.text)) return false;
    return true;
}
```

#### Variations vocales non répétitives

```javascript
// Pool de 50+ phrases par catégorie
// Mémoire des 20 dernières utilisées → jamais de doublon
// Random pondéré : les phrases récemment utilisées ont un poids de 0
// Les phrases jamais utilisées ont un poids de 3
function pickPhrase(pool, recentUsed) {
    const weighted = pool.map((p, i) => ({
        phrase: p,
        weight: recentUsed.includes(i) ? 0 : 3
    }));
    const totalWeight = weighted.reduce((s, w) => s + w.weight, 0);
    let r = Math.random() * totalWeight;
    for (const w of weighted) {
        r -= w.weight;
        if (r <= 0) return w.phrase;
    }
    return pool[0];
}
```

---

### DIFFÉRENCIATION MONDIALE — Pourquoi SLY-CHAT > tout le reste

#### 3 Différenciateurs Structurels

| # | SLY-CHAT | ChatGPT Mobile | Telegram Bots | Siri/Alexa |
|---|----------|---------------|--------------|------------|
| 1 | **Multi-agent avec personnalités distinctes** — 50 agents, chacun sa voix, son expertise, son style. C'est un TEAM, pas un bot. | 1 seul assistant, pas de personnalité | Bots isolés, pas d'écosystème | 1 assistant générique |
| 2 | **Bridge bidirectionnel vers système d'agents réel** — les commandes déclenchent de VRAIES actions (audit, analyse, pipeline). Pas du chat cosmétique. | Pas de système d'agents backend | Pas de coordination multi-bot | Actions limitées à Siri Shortcuts |
| 3 | **Mémoire 4 couches avec profil évolutif** — le système APPREND qui tu es, ce que tu fais, tes habitudes. Plus tu l'utilises, plus il est pertinent. | Mémoire limitée | Pas de mémoire cross-session | Mémoire quasi inexistante |

#### 3 Différenciateurs Émotionnels

| # | Ce qui crée l'attachement |
|---|--------------------------|
| 1 | **Voix réalistes et variées** — Brad Pitt, Gandalf, Homer Simpson FR. Chaque agent a une PRÉSENCE vocale. L'utilisateur s'attache aux personnalités, pas à un outil. |
| 2 | **Worldbuilding vivant** — Agent Whispers, Dream Mode, Mood Skin. L'app RESPIRE. Elle a un rythme jour/nuit. Les agents "vivent" même quand tu ne regardes pas. |
| 3 | **Micro-moments d'humanité** — SLY hésite parfois, fait des blagues contextuelles, se souvient d'un détail d'il y a 3 jours. Il n'est pas parfait — il est RÉEL. |

#### 3 Différenciateurs Techniques

| # | Innovation technique |
|---|---------------------|
| 1 | **TTS pipeliné phrase par phrase** — zéro gap entre phrases, crossfade audio, illusion de parole continue. Aucune app de chat IA ne fait ça aussi bien. |
| 2 | **Cascade triple transparente** — 4 providers LLM (Groq 8b, Groq 70b, Gemini, Cloudflare), routing par complexité, failover invisible en < 500ms. Zéro downtime perçu. |
| 3 | **Pré-sérialisation + pré-routing** — l'avatar de l'agent apparaît AVANT l'envoi du message. Latence perçue ~200ms. Le système semble omniscient. |

---

### SIMULATION DE STRESS MAXIMAL

#### Scénarios de crash et prévention

| Scénario | Que casse ? | Prévention | Récupération |
|----------|------------|------------|-------------|
| 500 requêtes en 5 min | Groq rate-limit (30 req/min free) | Cascade triple + queue locale | Messages en queue, traités quand slot dispo |
| 5 agents parlent quasi simultanément | Audio overlap, RAM spike | Queue FIFO stricte, max 1 audio à la fois | Skip les anciens si queue > 3 |
| Perte réseau pendant TTS | Fetch échoue, silence | Cache audio IndexedDB des phrases déjà entendues. Si cache miss → texte seul + message "Mode hors-ligne" | Retry auto quand réseau revient |
| WebSocket reconnect loop | Battery drain, CPU spike | Backoff exponentiel cap 30s, max 5 tentatives puis fallback REST | Fallback REST polling toutes les 10s |
| IndexedDB saturée (>50MB) | Write échoue silencieusement | Purge LRU automatique quand > 40MB | Supprimer cache audio en premier (re-fetchable) |
| Storage iPhone quasi plein | App crash au write | `navigator.storage.estimate()` → si < 10MB dispo, mode minimal | Alerter l'utilisateur, désactiver cache audio |
| iOS background kill | App tuée, état perdu | Sauvegarder état critique dans Capacitor Preferences toutes les 30s | Au relaunch → restaurer état depuis Preferences |
| Push APNS pendant TTS streaming | Notification interrompt l'audio | AudioContext resume après notification | `appStateChange` → resume AudioContext + replay dernier chunk |

#### Circuit breaker pattern

```javascript
// Si un provider échoue 3 fois en 5 min → le "breaker" s'ouvre
// Plus aucun appel pendant 60s → puis test 1 requête → si OK, le breaker se ferme
class CircuitBreaker {
    constructor(name, threshold = 3, timeout = 60000) {
        this.name = name;
        this.failures = 0;
        this.threshold = threshold;
        this.timeout = timeout;
        this.state = 'closed'; // closed | open | half-open
        this.openedAt = 0;
    }
    async call(fn) {
        if (this.state === 'open') {
            if (Date.now() - this.openedAt > this.timeout) {
                this.state = 'half-open';
            } else {
                throw new Error(`${this.name} circuit open`);
            }
        }
        try {
            const result = await fn();
            this.failures = 0;
            this.state = 'closed';
            return result;
        } catch (e) {
            this.failures++;
            if (this.failures >= this.threshold) {
                this.state = 'open';
                this.openedAt = Date.now();
            }
            throw e;
        }
    }
}

const groqBreaker = new CircuitBreaker('groq');
const geminiBreaker = new CircuitBreaker('gemini');
```

---

### ANTI-FRAGILITÉ — Le système s'améliore avec le temps

#### Apprentissage adaptatif

```javascript
// 1. Latence tracking → ajustement automatique du tier
//    Si Groq 70b répond en < 200ms → l'utiliser même pour les messages courts
//    Si Groq 70b > 800ms pendant 1h → basculer tout sur Gemini Flash
const latencyHistory = { groq8b: [], groq70b: [], gemini: [] };
function updateLatency(provider, ms) {
    latencyHistory[provider].push(ms);
    if (latencyHistory[provider].length > 50) latencyHistory[provider].shift();
}
function getAvgLatency(provider) {
    const h = latencyHistory[provider];
    return h.length > 0 ? h.reduce((a, b) => a + b) / h.length : Infinity;
}

// 2. Agent prioritisation — les agents les plus utilisés montent dans le dock
//    Stocké dans Capacitor Preferences
function trackAgentUsage(agentKey) {
    const usage = getAgentUsage(); // { sly: 45, cortex: 12, anvil: 30, ... }
    usage[agentKey] = (usage[agentKey] || 0) + 1;
    saveAgentUsage(usage);
    // Reorder dock automatiquement (top 5 les plus utilisés)
}

// 3. Auto-clean memory — supprimer les souvenirs jamais rappelés
//    Toutes les 24h, parcourir Couche 4
//    Si un souvenir n'a pas été utilisé depuis 30j → score -1
//    Si score < 0 → supprimer
//    Si rappelé → score +2

// 4. TTS cache optimization
//    Les phrases les plus jouées restent en cache prioritaire
//    Les salutations du matin = haute priorité
//    Les réponses uniques = basse priorité (pas de re-écoute probable)

// 5. Session-aware mode
//    Matin (6-9h) → SLY est énergique, propose le bilan
//    Après-midi (14-18h) → SLY est focus, répond court
//    Soir (20-23h) → SLY est décontracté, plus de philosophie
//    Nuit (23-6h) → Dream Mode activé automatiquement
```

#### Optimisation basée sur l'usage réel

```javascript
// Après 7 jours d'utilisation, le système peut répondre à :
// - Quelle est l'heure moyenne d'ouverture de l'app ?
// - Quel agent est le plus sollicité ?
// - Combien de messages vocaux vs texte ?
// - Quelle est la durée moyenne de session ?
// - Quels sont les pics d'utilisation ?

// Ces données permettent de :
// 1. Pré-charger les ressources avant l'heure d'ouverture habituelle
// 2. Mettre l'agent préféré en premier dans le dock
// 3. Adapter le mode proactif aux heures de présence réelle
// 4. Désactiver les whispers aux heures d'absence
```

---

## RÉSUMÉ — Le non-négociable

1. ✅ **Capacitor iOS natif dès Phase 1** (PAS PWA seule — iOS trop limité)
2. ✅ Splash screen cinématique (logo Sly, particules, 1.5s, skip si revisité)
3. ✅ Chat fluide avec bulles d'agents (nom + emoji + couleur + réécouter)
4. ✅ Chaque agent parle avec SA voix (FishAudio TTS pipeliné, queue FIFO)
5. ✅ **AudioContext iOS-safe** (un seul global, créé sur tap, jamais `new Audio()`)
6. ✅ Bouton Push-to-Talk GÉANT (80pt, safe area respectée)
7. ✅ Dock d'agents scrollable (5 favoris + grid complet)
8. ✅ Routing hybride (regex local + mini-classifieur LLM si ambigu)
9. ✅ **Cascade IA triple** (Groq 8b → Groq 70b → Gemini → Cloudflare)
10. ✅ Gamification (XP, streak, niveaux, badges)
11. ✅ Agent Whispers (micro-messages en idle, monde vivant)
12. ✅ **APNS** pour les push iOS (pas FCM seul)
13. ✅ **Capacitor Preferences** pour données critiques (XP, mémoire — jamais purgé)
14. ✅ Design NEURAL SOVEREIGN (dark, glassmorphism, premium, iPhone notch/Dynamic Island)
15. ✅ Offline-first (Capacitor Preferences + IndexedDB cache)
16. ✅ iPhone-first, boutons GROS (48pt+), transitions fluides, safe areas
17. ✅ Personnalité JARVIS (loyal, drôle, proactif, bref, JAMAIS répétitif)
18. ✅ Commandes vocales ("Le Clan Cooper, fais X")
19. ✅ Indicateur de parole (waveform quand un agent parle)
20. ✅ **Latence totale perçue < 500ms** (pré-sérialisation + avatar immédiat)
21. ✅ **Latence audio < 1.5s** (cascade rapide + TTS pipeliné)
22. ✅ **Zéro audio superposé** (queue FIFO + couper si utilisateur parle)
