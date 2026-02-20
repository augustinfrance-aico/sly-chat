"""
TITAN N8N Module
Create, deploy, manage n8n workflows directly from Telegram.
"""

import json
from datetime import datetime
from typing import Optional

import requests

from ..ai_client import chat as ai_chat
from ..config import N8N_URL, N8N_API_KEY


class TitanN8N:
    """Titan's workflow factory."""

    def __init__(self):
        self.headers = {
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json",
        }

    # === WORKFLOW MANAGEMENT ===

    def list_workflows(self) -> list:
        """List all workflows on n8n."""
        try:
            resp = requests.get(f"{N8N_URL}/api/v1/workflows", headers=self.headers, timeout=10)
            data = resp.json()
            return data.get("data", [])
        except Exception as e:
            return [{"error": str(e)}]

    def get_workflow(self, workflow_id: str) -> dict:
        """Get a specific workflow."""
        try:
            resp = requests.get(f"{N8N_URL}/api/v1/workflows/{workflow_id}", headers=self.headers, timeout=10)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}

    def activate_workflow(self, workflow_id: str) -> dict:
        """Activate a workflow."""
        try:
            resp = requests.patch(
                f"{N8N_URL}/api/v1/workflows/{workflow_id}",
                headers=self.headers,
                json={"active": True},
                timeout=10,
            )
            return resp.json()
        except Exception as e:
            return {"error": str(e)}

    def deactivate_workflow(self, workflow_id: str) -> dict:
        """Deactivate a workflow."""
        try:
            resp = requests.patch(
                f"{N8N_URL}/api/v1/workflows/{workflow_id}",
                headers=self.headers,
                json={"active": False},
                timeout=10,
            )
            return resp.json()
        except Exception as e:
            return {"error": str(e)}

    # === WORKFLOW CREATION ===

    async def create_workflow(self, description: str) -> str:
        """Generate and deploy a workflow from natural language."""
        prompt = f"""Genere un workflow n8n en JSON valide pour cette demande:
"{description}"

Regles:
- JSON valide, pret a importer dans n8n
- Utilise les nodes n8n standards (scheduleTrigger, httpRequest, code, if, googleSheets, gmail, etc.)
- Positionne les nodes correctement (espacement horizontal 200px)
- Ajoute un Error Trigger
- Noms de nodes avec emojis descriptifs
- NE PAS inclure les champs "active", "tags", "pinData"
- NE PAS inclure d'IDs dans les nodes

Reponds UNIQUEMENT avec le JSON, rien d'autre."""

        json_text = ai_chat("Tu es un expert n8n. Tu generes UNIQUEMENT du JSON valide, sans texte.", prompt, 4096)

        # Extract JSON from response
        try:
            # Try to find JSON in the response
            start = json_text.find("{")
            end = json_text.rfind("}") + 1
            if start >= 0 and end > start:
                json_text = json_text[start:end]

            workflow = json.loads(json_text)
        except json.JSONDecodeError as e:
            return f"Erreur parsing JSON: {e}"

        # Clean the workflow
        workflow.pop("active", None)
        workflow.pop("tags", None)
        workflow.pop("pinData", None)
        for node in workflow.get("nodes", []):
            node.pop("id", None)
            if "credentials" in node and not node["credentials"]:
                node.pop("credentials")

        # Deploy to n8n
        try:
            resp = requests.post(
                f"{N8N_URL}/api/v1/workflows",
                headers=self.headers,
                json=workflow,
                timeout=30,
            )

            if resp.status_code == 200:
                result = resp.json()
                wf_id = result.get("id", "?")
                wf_name = result.get("name", "?")
                nodes_count = len(workflow.get("nodes", []))

                return (
                    f"✅ Workflow déployé !\n\n"
                    f"Nom: {wf_name}\n"
                    f"ID: {wf_id}\n"
                    f"Nodes: {nodes_count}\n"
                    f"Status: inactif (active manuellement)\n"
                    f"URL: {N8N_URL}"
                )
            else:
                return f"Erreur déploiement: {resp.status_code} — {resp.text[:200]}"

        except Exception as e:
            return f"Erreur: {e}"

    async def get_status(self) -> str:
        """Get n8n instance status."""
        workflows = self.list_workflows()

        if workflows and isinstance(workflows[0], dict) and "error" in workflows[0]:
            return f"Erreur n8n: {workflows[0]['error']}"

        active = [w for w in workflows if w.get("active")]
        inactive = [w for w in workflows if not w.get("active")]

        lines = [
            f"⚙️ N8N STATUS — {datetime.now().strftime('%d/%m %H:%M')}\n",
            f"Total: {len(workflows)} workflows",
            f"🟢 Actifs: {len(active)}",
            f"⚪ Inactifs: {len(inactive)}",
            f"\nWorkflows actifs:"
        ]

        for w in active:
            lines.append(f"  • {w['name']}")

        if not active:
            lines.append("  (aucun)")

        return "\n".join(lines)
