#!/usr/bin/env python3
"""Render a validated story-video-director project through Metaso MiniMax-H3."""

from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


SUBMIT_URL = "https://metaso.cn/api/minimax/v2/video_generation"
QUERY_URL = "https://metaso.cn/api/minimax/v2/query/video_generation?task_id={task_id}"
TERMINAL = {"succeeded", "failed", "cancelled"}


def safe_error_text(value: object) -> str:
    """Keep provider diagnostics useful without persisting accidental secrets."""
    import re

    text = str(value)
    text = re.sub(r"(?i)(authorization\s*[:=]\s*bearer\s+)[^\s\"']+", r"\1[REDACTED]", text)
    text = re.sub(r"\bmk-[A-Za-z0-9_-]{12,}\b", "[REDACTED_API_KEY]", text)
    return text[:4000]


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def fenced_prompt(path: Path) -> str:
    import re

    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"```(?:text)?\s*\n(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if len(blocks) != 1:
        raise SystemExit(f"{path} must contain exactly one fenced prompt block")
    return blocks[0].strip()


MEDIA_TYPES = {"image": "image_url", "video": "video_url", "audio": "audio_url"}
ALLOWED_ROLES = {
    "image": {"first_frame", "last_frame", "reference_image"},
    "video": {"reference_video"},
    "audio": {"reference_audio"},
}


def job_references(job: dict, root: Path) -> list[tuple[dict, Path]]:
    refs = job.get("references", [])
    if not isinstance(refs, list) or not refs:
        raise SystemExit(f"{job.get('id', 'job')}: expected at least one media reference")
    prepared: list[tuple[dict, Path]] = []
    seen_slots: set[int] = set()
    for ref in refs:
        if not isinstance(ref, dict):
            raise SystemExit(f"{job.get('id', 'job')}: every reference must be an object")
        media_type = str(ref.get("type", ""))
        role = str(ref.get("role", ""))
        slot = ref.get("slot")
        if media_type not in MEDIA_TYPES or role not in ALLOWED_ROLES[media_type]:
            raise SystemExit(f"{job.get('id', 'job')}: invalid reference type/role {media_type}/{role}")
        if not isinstance(slot, int) or isinstance(slot, bool) or slot <= 0 or slot in seen_slots:
            raise SystemExit(f"{job.get('id', 'job')}: reference slots must be unique positive integers")
        seen_slots.add(slot)
        path = root / str(ref.get("path", ""))
        if not path.is_file():
            raise SystemExit(f"{job.get('id', 'job')}: reference does not exist: {path}")
        prepared.append((ref, path))
    prepared.sort(key=lambda item: int(item[0]["slot"]))
    slots = [int(item[0]["slot"]) for item in prepared]
    if slots != list(range(1, len(slots) + 1)):
        raise SystemExit(f"{job.get('id', 'job')}: reference slots must be contiguous from 1")
    roles = {str(ref["role"]) for ref, _ in prepared}
    frame_mode = bool(roles & {"first_frame", "last_frame"})
    reference_mode = bool(roles & {"reference_image", "reference_video", "reference_audio"})
    if frame_mode and reference_mode:
        raise SystemExit(f"{job.get('id', 'job')}: frame roles and reference roles are mutually exclusive")
    if frame_mode:
        if sum(role == "first_frame" for role in roles) > 1 or sum(role == "last_frame" for role in roles) > 1:
            raise SystemExit(f"{job.get('id', 'job')}: at most one first_frame and one last_frame")
    else:
        counts = {role: sum(str(ref["role"]) == role for ref, _ in prepared) for role in roles}
        if counts.get("reference_image", 0) > 9:
            raise SystemExit(f"{job.get('id', 'job')}: reference_image limit is 9")
        if counts.get("reference_video", 0) > 3 or counts.get("reference_audio", 0) > 3:
            raise SystemExit(f"{job.get('id', 'job')}: reference video/audio limit is 3 each")
    return prepared


def media_data_url(path: Path, media_type: str) -> str:
    suffix = path.suffix.lower()
    mime_by_suffix = {
        ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
        ".mp4": "video/mp4", ".mov": "video/quicktime", ".mp3": "audio/mpeg", ".wav": "audio/wav",
    }
    mime = mime_by_suffix.get(suffix)
    if not mime:
        raise SystemExit(f"Unsupported local media extension: {path}")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def public_media_url(ref: dict, path: Path, media_type: str) -> str:
    url = ref.get("url")
    if isinstance(url, str) and url.startswith(("https://", "http://")):
        return url
    return media_data_url(path, media_type)


def request_json(url: str, token: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if payload is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            value = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"Provider HTTP {exc.code}: {safe_error_text(body)}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Provider request failed: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError("Provider returned a non-object response")
    return value


def submit(job: dict, root: Path, token: str) -> str:
    prompt = fenced_prompt(root / str(job["prompt_file"]))
    prepared = job_references(job, root)
    content = [{"type": "text", "text": prompt}]
    for ref, path in prepared:
        media_type = str(ref["type"])
        url_type = MEDIA_TYPES[media_type]
        content.append({"type": url_type, url_type: {"url": public_media_url(ref, path, media_type)}, "role": str(ref["role"])})
    payload = {
        "model": str(job.get("model", "MiniMax-H3")),
        "content": content,
        "resolution": str(job.get("resolution", "2K")),
        "duration": int(job.get("duration_seconds", 5)),
        "ratio": str(job.get("aspect_ratio", "adaptive")),
    }
    result = request_json(SUBMIT_URL, token, payload)
    task_id = result.get("task_id")
    if not task_id:
        raise RuntimeError(f"Provider did not return task_id: {result}")
    return str(task_id)


def query(task_id: str, token: str) -> dict:
    result = request_json(QUERY_URL.format(task_id=task_id), token)
    items = result.get("items", [])
    for item in items if isinstance(items, list) else []:
        if isinstance(item, dict) and str(item.get("id")) == task_id:
            return item
    raise RuntimeError(f"Task {task_id} was not present in provider query response")


def download(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "story-video-director/1"})
    with urllib.request.urlopen(req, timeout=300) as response, path.open("wb") as output:
        shutil.copyfileobj(response, output, length=1024 * 1024)


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def probe_dimensions(path: Path) -> tuple[int, int]:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    stream = json.loads(result.stdout)["streams"][0]
    return int(stream["width"]), int(stream["height"])


def extract_last_frame(source: Path, target: Path) -> None:
    """Replace a planned boundary image with the real preceding clip end frame."""
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg is required for chain_from_previous jobs")
    target.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-y", "-sseof", "-0.08", "-i", str(source),
        "-frames:v", "1", "-update", "1", str(target),
    ])


def has_audio(path: Path) -> bool:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=index", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    return bool(json.loads(result.stdout).get("streams"))


def normalize(source: Path, target: Path, width: int, height: int, fps: int, duration: float) -> None:
    fade_out = max(0.0, duration - 0.03)
    video_filter = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,"
        f"fps={fps},trim=duration={duration},setpts=PTS-STARTPTS"
    )
    audio_filter = f"aresample=48000,atrim=duration={duration},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.03,afade=t=out:st={fade_out}:d=0.03"
    command = ["ffmpeg", "-y", "-i", str(source)]
    if has_audio(source):
        command += ["-vf", video_filter, "-af", audio_filter]
    else:
        command += [
            "-f", "lavfi", "-t", str(duration), "-i", "anullsrc=r=48000:cl=stereo",
            "-filter_complex", f"[0:v]{video_filter}[v];[1:a]{audio_filter}[a]",
            "-map", "[v]", "-map", "[a]",
        ]
    command += [
        "-r", str(fps), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-profile:v", "high", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-shortest", str(target),
    ]
    run(command)


def assemble(root: Path, jobs: list[dict], clip_paths: list[Path], total_duration: float) -> Path:
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("ffmpeg and ffprobe are required for assembly")
    output = root / "output"
    normalized = output / "normalized"
    normalized.mkdir(parents=True, exist_ok=True)
    width, height = probe_dimensions(clip_paths[0])
    fps = int(jobs[0].get("fps", 24))
    parts: list[Path] = []
    for job, source in zip(jobs, clip_paths):
        target = normalized / f"{job['id']}.mp4"
        normalize(source, target, width, height, fps, float(job["duration_seconds"]))
        parts.append(target)
    concat_file = output / "concat.txt"
    concat_file.write_text("".join(f"file '{path.as_posix()}'\n" for path in parts), encoding="utf-8")
    joined = output / "joined.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", "-avoid_negative_ts", "make_zero", str(joined)])
    final = output / "final.mp4"
    run([
        "ffmpeg", "-y", "-i", str(joined), "-filter_complex",
        f"[0:v]trim=duration={total_duration},setpts=PTS-STARTPTS[v];[0:a]atrim=duration={total_duration},asetpts=PTS-STARTPTS[a]",
        "-map", "[v]", "-map", "[a]", "-r", str(fps), "-c:v", "libx264", "-preset", "medium",
        "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(final),
    ])
    return final


def save_state(path: Path, state: dict) -> None:
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-assemble", action="store_true")
    parser.add_argument("--poll-seconds", type=int, default=10)
    args = parser.parse_args()

    root = args.project_dir.resolve()
    manifest = read_json(root / "project-manifest.json")
    jobs_doc = read_json(root / "api-jobs.json")
    jobs = jobs_doc.get("jobs", [])
    if not isinstance(jobs, list) or not jobs:
        raise SystemExit("api-jobs.json must contain a non-empty jobs array")

    plan = []
    for job in jobs:
        if not isinstance(job, dict):
            raise SystemExit("Every job must be an object")
        prepared = job_references(job, root)
        fenced_prompt(root / str(job.get("prompt_file", "")))
        duration_value = job.get("duration_seconds", 0)
        if not isinstance(duration_value, int) or isinstance(duration_value, bool) or duration_value < 4 or duration_value > 15:
            raise SystemExit(f"{job.get('id')}: MiniMax-H3 duration_seconds must be an integer in [4, 15]")
        duration = float(duration_value)
        plan.append({"id": job.get("id"), "duration": duration, "resolution": job.get("resolution", "2K"), "references": [{"path": str(path.relative_to(root)), "role": ref["role"], "slot": ref["slot"]} for ref, path in prepared]})

    if args.dry_run:
        print(json.dumps({"project": str(root), "jobs": plan, "will_assemble": not args.no_assemble}, ensure_ascii=False, indent=2))
        return 0

    if jobs_doc.get("submission_enabled") is False or manifest.get("submission_enabled") is False:
        raise SystemExit("Paid submission is disabled for this project. Review authorization and enable a private working copy explicitly; --dry-run remains available.")
    if any(job.get("submission_enabled") is False for job in jobs):
        raise SystemExit("One or more jobs disable paid submission; no jobs were submitted.")
    existing_state_path = root / "render-state.json"
    if existing_state_path.is_file():
        existing_state = read_json(existing_state_path)
        if any(entry.get("task_id") for entry in existing_state.get("jobs", []) if isinstance(entry, dict)):
            raise SystemExit("Existing provider tasks found. Query/download those tasks or prepare reviewed stage projects instead of resubmitting and risking duplicate charges.")

    token = os.environ.get("METASO_API_KEY")
    if not token:
        raise SystemExit("METASO_API_KEY is not set. Obtain a key at https://metaso.cn/minimax-h3 and configure it as an environment variable; never store it in the project.")

    state_path = root / "render-state.json"
    state = {"provider": "metaso-minimax-h3", "jobs": [], "final_output": None}
    clip_paths: list[Path] = []
    output_clips = root / "output" / "clips"
    output_clips.mkdir(parents=True, exist_ok=True)

    try:
        for job in jobs:
            job_id = str(job["id"])
            if job.get("chain_from_previous"):
                if not clip_paths:
                    raise RuntimeError(f"{job_id}: chain_from_previous requires a successful preceding clip")
                refs = job.get("references", [])
                boundary_refs = [
                    ref for ref in refs
                    if isinstance(ref, dict) and ref.get("chain_boundary") is True
                    and ref.get("role") in {"first_frame", "reference_image"}
                ]
                if len(boundary_refs) != 1:
                    raise RuntimeError(
                        f"{job_id}: chain_from_previous requires exactly one first_frame or reference_image with chain_boundary=true"
                    )
                boundary_path = root / str(boundary_refs[0].get("path", ""))
                print(f"Preparing continuity frame for {job_id}...", flush=True)
                extract_last_frame(clip_paths[-1], boundary_path)
            print(f"Submitting {job_id}...", flush=True)
            task_id = submit(job, root, token)
            entry = {"id": job_id, "task_id": task_id, "status": "submitted", "output": None}
            state["jobs"].append(entry)
            save_state(state_path, state)
            while True:
                item = query(task_id, token)
                status = str(item.get("status", "unknown"))
                entry["status"] = status
                entry["estimated_remaining_seconds"] = item.get("estimated_remaining_seconds")
                save_state(state_path, state)
                print(f"{job_id}: {status}", flush=True)
                if status in TERMINAL:
                    break
                time.sleep(max(5, args.poll_seconds))
            if status != "succeeded":
                raise RuntimeError(f"{job_id} ended with status {status}; stopping before later paid jobs")
            content = item.get("content", {})
            url = content.get("url") if isinstance(content, dict) else None
            if not url:
                raise RuntimeError(f"{job_id} succeeded without a download URL")
            clip_path = output_clips / f"{job_id}.mp4"
            download(str(url), clip_path)
            entry["output"] = str(clip_path.relative_to(root))
            entry.pop("estimated_remaining_seconds", None)
            save_state(state_path, state)
            clip_paths.append(clip_path)
    except Exception as exc:
        state["error"] = safe_error_text(exc)
        save_state(state_path, state)
        print(f"ERROR: {safe_error_text(exc)}", file=sys.stderr)
        return 1

    if not args.no_assemble:
        total = float(manifest.get("total_duration_seconds", sum(float(job["duration_seconds"]) for job in jobs)))
        final = assemble(root, jobs, clip_paths, total)
        state["final_output"] = str(final.relative_to(root))
        save_state(state_path, state)
        print(final)
    return 0


if __name__ == "__main__":
    sys.exit(main())
