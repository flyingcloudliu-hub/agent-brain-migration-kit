#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_context(manifest: dict[str, Any], root: Path) -> list[dict[str, Any]]:
    context_config = manifest.get("context") or {}
    docs = context_config.get("docs") or []
    loaded: list[dict[str, Any]] = []

    for item in docs:
        path = root / str(item.get("path", ""))
        max_chars = int(item.get("max_chars", 4000))
        required = bool(item.get("required", False))
        exists = path.exists() and path.is_file()
        if not exists and required:
            raise FileNotFoundError(f"required context document missing: {path}")
        if not exists:
            loaded.append(
                {
                    "path": str(path),
                    "priority": item.get("priority", "P1"),
                    "exists": False,
                    "text": "",
                }
            )
            continue

        loaded.append(
            {
                "path": str(path),
                "priority": item.get("priority", "P1"),
                "exists": True,
                "text": path.read_text(encoding="utf-8", errors="ignore")[:max_chars],
            }
        )

    return loaded


def fake_primary_backend(router_input: dict[str, Any]) -> dict[str, Any]:
    text = router_input["message"]["text"]
    return {
        "reply": f"Primary backend received: {text}",
        "actions": [],
        "meta": {"backend": "primary", "mode": router_input["config"]["mode"]},
    }


def fake_candidate_backend(router_input: dict[str, Any]) -> dict[str, Any]:
    text = router_input["message"]["text"]
    return {
        "reply": f"Candidate backend would stage and follow up: {text}",
        "actions": [
            {
                "type": "knowledge_stage",
                "payload": {"title": "Demo note", "content": text},
                "confidence": 0.8,
            },
            {
                "type": "progress_update",
                "payload": {"summary": "Create follow-up task"},
                "confidence": 0.72,
            },
        ],
        "meta": {"backend": "candidate", "mode": router_input["config"]["mode"]},
    }


def normalize_actions(result: dict[str, Any], allowed_actions: set[str]) -> dict[str, Any]:
    normalized = []
    for action in result.get("actions") or []:
        if not isinstance(action, dict):
            continue
        if action.get("type") not in allowed_actions:
            continue
        normalized.append(action)
    return {**result, "actions": normalized}


def run_router(manifest: dict[str, Any], request: dict[str, Any], root: Path) -> dict[str, Any]:
    mode = manifest.get("mode", "shadow")
    active_backend = manifest.get("active_backend", "primary")
    allowed_actions = set(manifest.get("allowed_actions") or [])
    router_input = {
        **request,
        "config": {"backend": active_backend, "mode": mode},
        "loaded_context": load_context(manifest, root),
    }

    if mode == "shadow":
        primary = normalize_actions(fake_primary_backend(router_input), allowed_actions)
        candidate_input = {**router_input, "config": {"backend": "candidate", "mode": "shadow"}}
        candidate = normalize_actions(fake_candidate_backend(candidate_input), allowed_actions)
        return {
            "mode": "shadow",
            "result": primary,
            "shadow": {
                "backend": "candidate",
                "result": candidate,
                "note": "shadow result must not trigger side effects",
            },
        }

    if active_backend == "candidate":
        return {
            "mode": mode,
            "result": normalize_actions(fake_candidate_backend(router_input), allowed_actions),
        }

    return {
        "mode": mode,
        "result": normalize_actions(fake_primary_backend(router_input), allowed_actions),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Manifest-driven brain router example")
    parser.add_argument("--manifest", default="manifest.example.json")
    parser.add_argument("--input", default="sample-input.json")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    manifest = load_json(root / args.manifest)
    request = load_json(root / args.input)
    print(json.dumps(run_router(manifest, request, root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

