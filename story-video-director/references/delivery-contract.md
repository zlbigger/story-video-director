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
├── output/
├── 00-director-brief.md
├── 00-screenplay.md        # required for dialogue-led drama
├── 01-production-timeline.md
├── dialogue-ledger.json    # required when named characters speak
├── project-manifest.json
├── api-jobs.json
└── render-state.json       # created only after API execution
```

The director brief records story interpretation, visual bible, sound world, and intentional assumptions. The timeline records clip duration, narrative function, assets, and transitions.

For dialogue-led drama, `00-screenplay.md` is the human-readable story source and `dialogue-ledger.json` is the exact machine-readable source of truth for words, speaker ownership, timing, addressee, delivery, and on/off-screen status. Every prompt utterance must match the ledger exactly.

## 2. Manifest schema

```json
{
  "version": 1,
  "title": "Project title",
  "target_model": "seedance-2.0",
  "recurring_identities": [
    {"id": "lead", "identity_anchor": "assets/characters/lead.png", "clips": ["clip-01", "clip-02"]}
  ],
  "reference_limits": {"images": 9, "videos": 3, "audios": 3, "total": 12},
  "total_duration_seconds": 24,
  "max_clip_seconds": 15,
  "master_audio": {"path": "assets/audio/master.wav", "duration_seconds": 24, "cut_policy": "beat_or_breath_aligned"},
  "clips": [
    {
      "id": "clip-01",
      "duration_seconds": 10,
      "prompt_file": "prompts/clip-01.md",
      "image_refs": ["assets/characters/lead.png", "assets/shots/shot-01.png"],
      "video_refs": [],
      "audio_refs": [],
      "depends_on": [],
      "continuity": {"continuity_from": "", "continuity_to": "", "opening_state": "", "end_state": ""},
      "reference_labels": [{"label": "<Subject 1>", "path": "assets/characters/lead.png", "relationship": "fully_preserved", "inherit": ["face", "hair"], "exclude": ["sheet grid", "studio background"]}]
    }
  ]
}
```

Use paths relative to the project directory. Total duration must equal the sum of clip durations.

Declare every identity that appears in more than one clip under `recurring_identities`. Each entry requires a stable `id`, an existing `identity_anchor`, and at least two consuming clip IDs. The identity anchor should normally be a visually approved four-view sheet. Shot frames and location images are not valid identity anchors.

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
      "resolution": "768P",
      "prompt_file": "prompts/clip-01.md",
      "references": [
        {"type": "image", "path": "assets/shots/clip-01-first-frame.png", "role": "first_frame", "slot": 1}
      ]
    }
  ]
}
```

The resolution shown is an example: honor the user’s selected resolution and provider-supported values; do not inherit higher-cost settings from example jobs. Before paid submission, report planned clip count, total generated duration, resolution and estimated cost, separately from actual billing.

Do not include provider credentials. A future adapter may translate this manifest into an API request. Keep reference labels and retention relationships aligned with the H3 prompting guide. `master_audio` is required when sound spans clips; it records the one timeline used for assembly, not a per-clip replacement.

For Metaso MiniMax-H3 execution, choose one input mode per job:

- image-to-video: one `first_frame` and optional one `last_frame`;
- multimodal reference: up to nine `reference_image` items and optional `reference_video` / `reference_audio` items.

The two modes are mutually exclusive. Every declared job reference is actually uploaded in ascending `slot` order and corresponds to `@1`, `@2`, and so on in the prompt. Other project assets are not implicitly uploaded.

Prefer multimodal reference mode for recurring-character films. A same-view continuation may upload the preceding approved real end frame as one `reference_image`, then the recurring identity anchors, location plate, important prop, and optional action layout as additional `reference_image` items. Do not switch to `first_frame` merely to preserve continuity when multimodal references are also needed.

The renderer writes non-secret execution state to `render-state.json`, downloaded clips to `output/clips/`, and the merged result to `output/final.mp4`. It must never write authorization headers or API keys.

## 4. Quality checklist

- total duration reported and correct;
- every clip ≤15s;
- reference counts within selected model budget;
- every referenced file exists;
- each prompt contains every required `@filename`;
- every reference has a job and exclusion;
- character name and visible marker appear in relevant beats;
- dialogue language is named;
- dialogue-led work includes a screenplay and valid dialogue ledger;
- every utterance has a unique ID, exact named speaker, addressee, non-overlapping time range, and exact prompt match;
- each speaking beat states speaker mouth movement, listener silence, and unambiguous camera coverage;
- no dialogue braces appear in final-frame instructions or outside canonical utterance lines;
- spoken content fits duration;
- audio policy is explicit;
- multi-clip projects include continuity handoffs and, when applicable, one master audio timeline;
- every H3 reference label has a retention relationship and explicit inherited/excluded attributes;
- final frame is explicit;
- negative prompt exists;
- no generated title or subtitle unless requested;
- key images visually inspected;
- manifest and API jobs parse as valid JSON.
- every executable MiniMax-H3 job uses one valid input mode and stays within its media limits;
- every declared recurring identity has an existing identity anchor and is referenced by its consuming clips;
- paid submission occurs only after explicit user authorization;
- rendered clip files and final output exist before reporting success;
- final duration, frame rate, dimensions, video stream, and audio stream are verified.

## Multi-clip edit contract

For multiple clips, require `02-continuity-plan.md` with one record for every adjacent pair; follow [continuity-and-edit-design.md](continuity-and-edit-design.md). This document holds cut motivation, state/motion handoff, picture and sound strategy, edit points, actual-frame provenance, and boundary QA status. The existing JSON validator does not validate this editorial document: review it explicitly. `depends_on` and continuity metadata do not by themselves implement runtime scheduling or editing. Planned master audio is not automatically mixed by the stock renderer. Use the staged rendering and explicit edit workflow in that guide when needed.

## Prop-dependent scene additions

For fragile manipulation, ignition, breakage or persistent debris, include `prop-state-ledger.json` and `keyframe-plan.md` per `prop-action-continuity.md`. These documents specify object identities, sources, hands, contact, state changes, destinations, floor layouts, temporal reference roles and consumers. The existing structural validator does not validate their physical correctness; audit them and actual footage explicitly.
