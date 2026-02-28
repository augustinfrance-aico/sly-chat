"""
COUNCIL STATE — État du Grand Conseil.
Thread-safe, persistant, isolé.
"""

import json
import logging
import threading
import time
import uuid
from pathlib import Path

log = logging.getLogger("titan.classroom.council")

STATE_DIR = Path(__file__).resolve().parent.parent / "memory"
STATE_FILE = STATE_DIR / "council_state.json"
TRANSCRIPT_FILE = STATE_DIR / "council_transcripts.json"

_lock = threading.Lock()


class CouncilState:
    """État du Grand Conseil — table ronde stratégique."""

    def __init__(self):
        self.active = False
        self.session_id: str = ""
        self.subject: str = ""
        self.seated_agents: list[str] = []
        self.speaking_agent: str | None = None
        self.positions: dict[str, dict] = {}      # agent → {text, conviction, weight}
        self.duels: list[dict] = []                 # [{agent1, agent2, attack1, attack2, ...}]
        self.reverses: list[dict] = []              # [{agent, original, reverse, conviction}]
        self.vote_results: dict | None = None       # {votes, percentages, winner}
        self.report: dict | None = None             # rapport final
        self.started_at: float | None = None

    def start(self, subject: str, agents: list[str]):
        """Démarre un Grand Conseil."""
        with _lock:
            self.active = True
            self.session_id = str(uuid.uuid4())[:8]
            self.subject = subject
            self.seated_agents = agents[:12]
            self.speaking_agent = None
            self.positions = {}
            self.duels = []
            self.reverses = []
            self.vote_results = None
            self.report = None
            self.started_at = time.time()
            log.info(f"Council started: {subject} ({len(agents)} agents)")

    def stop(self):
        """Termine le Conseil et sauvegarde le transcript."""
        with _lock:
            if self.positions:
                self._save_transcript()
            self.active = False
            self.speaking_agent = None
            log.info("Council stopped")

    def set_speaking(self, agent: str | None):
        with _lock:
            self.speaking_agent = agent

    def add_position(self, agent: str, text: str, conviction: int):
        with _lock:
            self.positions[agent] = {
                "text": text,
                "conviction": conviction,
                "ts": time.time(),
            }

    def get_position(self, agent: str) -> str | None:
        p = self.positions.get(agent)
        return p["text"] if p else None

    def get_conviction(self, agent: str) -> int | None:
        p = self.positions.get(agent)
        return p["conviction"] if p else None

    def add_duel(self, a1: str, a2: str, attack1: str, attack2: str, conv1: int, conv2: int):
        with _lock:
            winner = a1 if conv1 >= conv2 else a2
            self.duels.append({
                "agent1": a1, "agent2": a2,
                "attack1": attack1, "attack2": attack2,
                "conv1": conv1, "conv2": conv2,
                "winner": winner,
            })

    def add_reverse(self, agent: str, original: str, reverse: str, conviction: int):
        with _lock:
            self.reverses.append({
                "agent": agent,
                "original": original,
                "reverse": reverse,
                "conviction": conviction,
            })

    def set_vote_results(self, votes: dict, percentages: dict, winner: str):
        with _lock:
            self.vote_results = {
                "votes": votes,
                "percentages": percentages,
                "winner": winner,
            }

    def set_report(self, report: dict):
        with _lock:
            self.report = report

    def to_dict(self) -> dict:
        return {
            "active": self.active,
            "session_id": self.session_id,
            "subject": self.subject,
            "seated_agents": self.seated_agents,
            "speaking_agent": self.speaking_agent,
            "positions": self.positions,
            "duels": self.duels,
            "reverses": self.reverses,
            "vote_results": self.vote_results,
            "report": self.report,
            "started_at": self.started_at,
            "elapsed_s": round(time.time() - self.started_at, 1) if self.started_at else 0,
        }

    def _save_transcript(self):
        """Sauvegarde le transcript du Conseil."""
        try:
            transcripts = []
            if TRANSCRIPT_FILE.exists():
                transcripts = json.loads(TRANSCRIPT_FILE.read_text(encoding="utf-8"))
            transcripts.append({
                "type": "council",
                "session_id": self.session_id,
                "subject": self.subject,
                "agents": self.seated_agents,
                "positions": self.positions,
                "duels": self.duels,
                "reverses": self.reverses,
                "vote": self.vote_results,
                "report": self.report,
                "started_at": self.started_at,
                "ended_at": time.time(),
            })
            transcripts = transcripts[-15:]  # garder 15 derniers
            STATE_DIR.mkdir(exist_ok=True)
            TRANSCRIPT_FILE.write_text(
                json.dumps(transcripts, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            log.info(f"Council transcript saved: {self.session_id}")
        except Exception as e:
            log.error(f"Council transcript save error: {e}")

    def save(self):
        with _lock:
            try:
                STATE_DIR.mkdir(exist_ok=True)
                STATE_FILE.write_text(
                    json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
            except Exception as e:
                log.error(f"Council state save error: {e}")


# Singleton
council_state = CouncilState()
