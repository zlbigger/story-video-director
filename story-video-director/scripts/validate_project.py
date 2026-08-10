#!/usr/bin/env python3
"""Validate a story-video-director delivery package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MODEL_LIMITS = {
    "seedance-2.0": {"images": 9, "videos": 3, "audios": 3, "total": 12},
    # Public/product entry points may expose different 2.5 video, audio, and
    # combined-file ceilings. Only enforce the commonly stated image ceiling
    # unless the project manifest records provider-confirmed overrides.
    "seedance-2.5": {"images": 30, "videos": None, "audios": None, "total": None},
}


def read_json(path: Path, errors: list[str]) -> dict:
    if not path.is_file():
        errors.append(f"missing JSON file: {path.name}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON in {path.name}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.name} must contain a JSON object")
        return {}
    return value


def fenced_blocks(text: str) -> list[str]:
    return re.findall(r"```(?:text)?\s*\n(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)


def chinese_char_count(text: str) -> int:
    return len(re.findall(r"[\u3400-\u9fff]", text))


def validate_project(root: Path) -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []
    summary: dict = {"project": str(root), "clips": 0, "duration": 0}

    if not root.is_dir():
        return [f"project directory does not exist: {root}"], warnings, summary

    manifest = read_json(root / "project-manifest.json", errors)
    jobs_doc = read_json(root / "api-jobs.json", errors)
    clips = manifest.get("clips", [])
    if not isinstance(clips, list) or not clips:
        errors.append("project-manifest.json must contain a non-empty clips array")
        clips = []

    target_model = str(manifest.get("target_model", "seedance-2.0")).lower()
    limits = MODEL_LIMITS.get(target_model)
    if limits is None:
        warnings.append(f"unknown target_model '{target_model}'; using Seedance 2.0 limits")
        limits = dict(MODEL_LIMITS["seedance-2.0"])
    else:
        limits = dict(limits)

    declared_limits = manifest.get("reference_limits", {})
    if declared_limits:
        if not isinstance(declared_limits, dict):
            errors.append("reference_limits must be an object when provided")
        else:
            for key in ("images", "videos", "audios", "total"):
                if key not in declared_limits:
                    continue
                value = declared_limits[key]
                if not isinstance(value, int) or value < 0:
                    errors.append(f"reference_limits.{key} must be a non-negative integer")
                else:
                    limits[key] = value

    max_clip = manifest.get("max_clip_seconds", 15)
    if max_clip != 15:
        warnings.append(f"max_clip_seconds is {max_clip}; this skill requires a 15-second ceiling")

    total = 0.0
    clip_ids: list[str] = []
    for index, clip in enumerate(clips, start=1):
        label = f"clip #{index}"
        if not isinstance(clip, dict):
            errors.append(f"{label} must be an object")
            continue

        clip_id = str(clip.get("id", "")).strip()
        if not clip_id:
            errors.append(f"{label} is missing id")
            clip_id = label
        elif clip_id in clip_ids:
            errors.append(f"duplicate clip id: {clip_id}")
        clip_ids.append(clip_id)
        label = clip_id

        duration = clip.get("duration_seconds")
        if not isinstance(duration, (int, float)) or duration <= 0:
            errors.append(f"{label}: duration_seconds must be positive")
            duration = 0
        elif duration > 15:
            errors.append(f"{label}: duration {duration}s exceeds 15s")
        total += float(duration)

        prompt_rel = clip.get("prompt_file")
        if not isinstance(prompt_rel, str) or not prompt_rel:
            errors.append(f"{label}: missing prompt_file")
            prompt_path = None
            prompt_text = ""
            prompt_body = ""
        else:
            prompt_path = root / prompt_rel
            if not prompt_path.is_file():
                errors.append(f"{label}: prompt file does not exist: {prompt_rel}")
                prompt_text = ""
                prompt_body = ""
            else:
                prompt_text = prompt_path.read_text(encoding="utf-8")
                blocks = fenced_blocks(prompt_text)
                if len(blocks) != 1:
                    errors.append(f"{label}: prompt file must contain exactly one fenced prompt block")
                prompt_body = blocks[0].strip() if blocks else prompt_text.strip()
                if len(prompt_body) > 5000:
                    warnings.append(f"{label}: prompt is {len(prompt_body)} characters; prefer <=5000")
                if not any(term in prompt_body for term in ("最终画面", "最后画面", "Last frame")):
                    errors.append(f"{label}: prompt lacks an explicit final frame")
                if not any(term in prompt_body for term in ("声音", "音效", "无声", "AUDIO")):
                    errors.append(f"{label}: prompt lacks an audio policy")
                if not any(term in prompt_body for term in ("负面提示词", "Negative Prompt")):
                    errors.append(f"{label}: prompt lacks a negative prompt")
                if not any(term in prompt_body for term in ("不要", "不得", "排除")):
                    warnings.append(f"{label}: no visible reference exclusion language found")
                if re.search(r"\b(?:fps|seed|resolution)\b|\d+\s*:\s*\d+", prompt_body, re.I):
                    warnings.append(f"{label}: generation parameters may be inside the model prompt")

                spoken = "".join(re.findall(r"\{([^{}]+)\}", prompt_body))
                spoken_chars = chinese_char_count(spoken)
                if duration and spoken_chars > float(duration) * 4.5:
                    warnings.append(
                        f"{label}: {spoken_chars} Chinese dialogue characters may exceed natural timing for {duration}s"
                    )

        ref_groups = {
            "images": clip.get("image_refs", []),
            "videos": clip.get("video_refs", []),
            "audios": clip.get("audio_refs", []),
        }
        total_refs = 0
        for kind, refs in ref_groups.items():
            if not isinstance(refs, list):
                errors.append(f"{label}: {kind[:-1]}_refs must be an array")
                refs = []
            total_refs += len(refs)
            kind_limit = limits[kind]
            if kind_limit is not None and len(refs) > kind_limit:
                errors.append(f"{label}: {len(refs)} {kind} exceeds {target_model} limit {kind_limit}")
            elif kind_limit is None and len(refs) > 3:
                warnings.append(
                    f"{label}: {len(refs)} {kind}; confirm the current {target_model} provider ceiling"
                )
            for rel in refs:
                if not isinstance(rel, str) or not rel:
                    errors.append(f"{label}: invalid reference path in {kind[:-1]}_refs")
                    continue
                ref_path = root / rel
                if not ref_path.is_file():
                    errors.append(f"{label}: referenced file does not exist: {rel}")
                if prompt_text and f"@{Path(rel).name}" not in prompt_body:
                    errors.append(f"{label}: prompt does not contain inline reference @{Path(rel).name}")
        total_limit = limits["total"]
        if total_limit is not None and total_refs > total_limit:
            errors.append(f"{label}: {total_refs} total references exceeds {target_model} conservative limit {total_limit}")

    declared_total = manifest.get("total_duration_seconds")
    if isinstance(declared_total, (int, float)):
        if abs(float(declared_total) - total) > 0.001:
            errors.append(f"declared total duration {declared_total}s does not equal clip sum {total:g}s")
    else:
        errors.append("project-manifest.json is missing numeric total_duration_seconds")

    jobs = jobs_doc.get("jobs", []) if isinstance(jobs_doc, dict) else []
    if not isinstance(jobs, list):
        errors.append("api-jobs.json jobs must be an array")
        jobs = []
    job_ids = [str(job.get("id", "")) for job in jobs if isinstance(job, dict)]
    if clip_ids and job_ids != clip_ids:
        errors.append("api-jobs.json job order or ids do not match project-manifest clips")

    summary.update({"clips": len(clips), "duration": total, "model": target_model})
    return errors, warnings, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    errors, warnings, summary = validate_project(args.project_dir.resolve())
    if args.as_json:
        print(json.dumps({"ok": not errors, "summary": summary, "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
    else:
        print(f"Project: {summary['project']}")
        print(f"Clips: {summary.get('clips', 0)}  Duration: {summary.get('duration', 0):g}s  Model: {summary.get('model', 'unknown')}")
        for message in warnings:
            print(f"WARNING: {message}")
        for message in errors:
            print(f"ERROR: {message}")
        print("PASS" if not errors else "FAIL")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
