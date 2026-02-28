"""
CLASSROOM STATE — État global de la salle de classe.
Thread-safe, persistant, isolé du reste de TITAN.
"""

import json
import logging
import threading
import time
from pathlib import Path

log = logging.getLogger("titan.classroom.state")

# Persistence
STATE_DIR = Path(__file__).resolve().parent.parent / "memory"
STATE_FILE = STATE_DIR / "classroom_state.json"
TRANSCRIPT_FILE = STATE_DIR / "classroom_transcripts.json"

_lock = threading.Lock()


class ClassroomState:
    """État immutable-ish de la salle de classe."""

    def __init__(self):
        self.active = False
        self.mode = "free"  # free | interrogation | debate
        self.subject = ""
        self.seated_agents: list[str] = []
        self.speaking_agent: str | None = None
        self.queue: list[str] = []  # agents en attente de parole
        self.messages: list[dict] = []  # historique du débat en cours
        self.turn_count = 0
        self.max_turns = 20
        self.max_agents = 12
        self.president: str = "OMEGA"  # modérateur en mode débat
        self.started_at: float | None = None
        self.paused = False

    def start(self, subject: str = "", mode: str = "free", agents: list[str] | None = None):
        """Démarre une session classroom."""
        with _lock:
            self.active = True
            self.mode = mode
            self.subject = subject
            self.speaking_agent = None
            self.queue = []
            self.messages = []
            self.turn_count = 0
            self.paused = False
            self.started_at = time.time()
            if agents:
                self.seated_agents = agents[:self.max_agents]
            log.info(f"Classroom started: mode={mode}, subject={subject}, agents={len(self.seated_agents)}")

    def stop(self):
        """Arrête la session."""
        with _lock:
            if self.messages:
                self._save_transcript()
            self.active = False
            self.speaking_agent = None
            self.queue = []
            self.subject = ""
            self.started_at = None
            log.info("Classroom stopped")

    def add_message(self, agent: str, text: str, role: str = "agent"):
        """Ajoute un message au débat."""
        with _lock:
            msg = {
                "agent": agent,
                "text": text,
                "role": role,  # agent | user | system
                "ts": time.time(),
                "turn": self.turn_count,
            }
            self.messages.append(msg)
            self.turn_count += 1

    def set_speaking(self, agent: str | None):
        """Change l'agent qui parle."""
        with _lock:
            self.speaking_agent = agent

    def next_in_queue(self) -> str | None:
        """Retourne le prochain agent dans la queue."""
        with _lock:
            if self.queue:
                return self.queue.pop(0)
            return None

    def is_over_limit(self) -> bool:
        """Vérifie si on a dépassé la limite de tours."""
        return self.turn_count >= self.max_turns

    def to_dict(self) -> dict:
        """Export pour API."""
        return {
            "active": self.active,
            "mode": self.mode,
            "subject": self.subject,
            "seated_agents": self.seated_agents,
            "speaking_agent": self.speaking_agent,
            "queue": self.queue,
            "messages": self.messages[-50:],  # max 50 derniers
            "turn_count": self.turn_count,
            "max_turns": self.max_turns,
            "max_agents": self.max_agents,
            "president": self.president,
            "paused": self.paused,
            "started_at": self.started_at,
            "elapsed_s": round(time.time() - self.started_at, 1) if self.started_at else 0,
        }

    def _save_transcript(self):
        """Sauvegarde le transcript de la session."""
        try:
            transcripts = []
            if TRANSCRIPT_FILE.exists():
                transcripts = json.loads(TRANSCRIPT_FILE.read_text(encoding="utf-8"))
            transcripts.append({
                "subject": self.subject,
                "mode": self.mode,
                "agents": self.seated_agents,
                "messages": self.messages,
                "turns": self.turn_count,
                "started_at": self.started_at,
                "ended_at": time.time(),
            })
            # Garder les 20 derniers transcripts
            transcripts = transcripts[-20:]
            TRANSCRIPT_FILE.write_text(
                json.dumps(transcripts, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            log.info(f"Transcript saved: {self.turn_count} turns, {len(self.messages)} messages")
        except Exception as e:
            log.error(f"Error saving transcript: {e}")

    def save(self):
        """Persiste l'état courant."""
        with _lock:
            try:
                STATE_FILE.write_text(
                    json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
            except Exception as e:
                log.error(f"Error saving state: {e}")


# Singleton
state = ClassroomState()
