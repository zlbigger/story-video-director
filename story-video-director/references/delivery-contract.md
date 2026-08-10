# Delivery contract

## Contents

1. Project structure
2. Manifest schema
3. API jobs
4. Quality checklist

## 1. Project structure

```text
project-name/
├── assets/
├── prompts/
├── 00-director-brief.md
├── 01-production-timeline.md
├── project-manifest.json
└── api-jobs.json
```

The director brief records story interpretation, visual bible, sound world, and intentional assumptions. The timeline records clip duration, narrative function, assets, and transitions.

## 2. Manifest schema

```json
{
  "version": 1,
  "title": "Project title",
  "target_model": "seedance-2.0",
  "reference_limits": {"images": 9, "videos": 3, "audios": 3, "total": 12},
  "total_duration_seconds": 24,
  "max_clip_seconds": 15,
  "clips": [
    {
      "id": "clip-01",
      "duration_seconds": 10,
      "prompt_file": "prompts/clip-01.md",
      "image_refs": ["assets/characters/lead.png", "assets/shots/shot-01.png"],
      "video_refs": [],
      "audio_refs": [],
      "depends_on": []
    }
  ]
}
```

Use paths relative to the project directory. Total duration must equal the sum of clip durations.

`reference_limits` is optional for known defaults and recommended when an interface or API exposes limits that differ from the skill defaults. For Seedance 2.5, record provider-confirmed video, audio, and combined-file ceilings instead of guessing them.

## 3. API jobs

`api-jobs.json` mirrors clip order and adds provider-neutral settings:

```json
{
  "jobs": [
    {
      "id": "clip-01",
      "model": "seedance-2.0",
      "duration_seconds": 10,
      "aspect_ratio": "16:9",
      "fps": 24,
      "prompt_file": "prompts/clip-01.md",
      "references": [
        {"type": "image", "path": "assets/characters/lead.png", "slot": 1}
      ]
    }
  ]
}
```

Do not include provider credentials. A future adapter may translate this manifest into an API request.

## 4. Quality checklist

- total duration reported and correct;
- every clip ≤15s;
- reference counts within selected model budget;
- every referenced file exists;
- each prompt contains every required `@filename`;
- every reference has a job and exclusion;
- character name and visible marker appear in relevant beats;
- dialogue language is named;
- spoken content fits duration;
- audio policy is explicit;
- final frame is explicit;
- negative prompt exists;
- no generated title or subtitle unless requested;
- key images visually inspected;
- manifest and API jobs parse as valid JSON.
