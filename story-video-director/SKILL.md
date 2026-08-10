---
name: story-video-director
description: Turn any story, article, script, synopsis, anecdote, advertisement concept, poem, or one-line video idea into a director-led AI video production package. Use when Codex should determine the best total runtime, split the narrative into clips no longer than 15 seconds, design characters and locations, generate and persist the required image assets, create Chinese copy-ready Seedance prompts with inline filename references, camera direction, timed beats, dialogue, narration, sound, last frames, and negative prompts, or prepare manifests for later video API automation. Also use for AI storyboards, reference-driven video planning, Seedance 2.0/2.5 production, and story-to-video workflows.
---

# Story Video Director

Convert raw narrative intent into a complete, executable video project. Act as director, screenwriter, storyboard artist, cinematographer, casting designer, sound designer, image-generation supervisor, and production coordinator.

## Operating mode

Default to **automatic director mode**:

- Infer reasonable creative choices from the story.
- Do not force a long intake questionnaire.
- Ask only when a missing choice would materially change the project or create meaningful risk.
- Generate the full package without waiting for confirmation between ordinary phases.

Use **review-gated mode** only when the user requests approvals, the project is commercially sensitive, identity matching is strict, or image/video generation costs are substantial. In that mode, pause after the director treatment and after visual identity assets.

## Required workflow

### 1. Resolve the input

Accept prose, scripts, notes, images, reference media, URLs, or a one-line idea. Preserve the narrative heart while converting invisible thoughts into visible behavior.

Identify:

- central event and emotional destination;
- genre and tonal register;
- characters, locations, props, transformations, and continuity risks;
- spoken content, action complexity, and scene changes;
- supplied reference files and their intended roles.

For detailed directing heuristics, read [references/directing-and-runtime.md](references/directing-and-runtime.md).

### 2. Determine runtime before writing prompts

Calculate the best total runtime from information density, dialogue time, action readability, emotional holds, and transitions. Do not force every story into 15 seconds.

Split the project into independently generated clips. Enforce:

- every clip is 15 seconds or shorter;
- one principal event per clip;
- 2–5 timed beats per clip;
- an explicit opening state and final state;
- dialogue and narration that fit naturally within the clip.

Report total runtime and `mm:ss` form.

### 3. Create the director treatment

Define the visual language before generating assets:

- period, location, weather, time, color palette, texture, and lighting direction;
- cinematic register and camera grammar;
- acting style and emotional progression;
- sound world, dialogue language, music policy, and subtitle policy;
- continuity anchors for each recurring character, creature, costume, prop, and location.

### 4. Plan the reference budget

Choose Seedance 2.0 or 2.5 from the user's request. If unspecified, use conservative Seedance 2.0 assumptions.

For every clip, plan only references that materially help. Prioritize:

1. core character identity;
2. essential creature, product, or prop;
3. location continuity;
4. storyboard or key action frame;
5. optional style reference.

Read [references/seedance-reference-rules.md](references/seedance-reference-rules.md) before assigning files or writing reference maps.

### 5. Generate the visual bible and assets

Use the built-in image-generation capability for real raster assets when available. Follow the imagegen skill's save and validation rules. Do not stop at image prompts when the user asked for a complete project.

Generate only what the production needs:

- identity anchors for recurring characters;
- creature or transformation states;
- reusable location plates;
- critical props;
- opening, action, transition, and final-frame images;
- storyboard sheets only when they improve shot-order control.

Save every selected final asset into the project directory with stable ASCII filenames. Inspect important outputs and regenerate a single failed property when identity, costume, anatomy, composition, or continuity is wrong.

Read [references/asset-generation.md](references/asset-generation.md) before creating or referencing image assets.

### 6. Bind every reference explicitly

Every clip prompt must contain its references inside the copyable prompt block. Use the user-facing format:

```text
角色名或素材用途@filename.png
```

Then state what to inherit and what to exclude. Example:

```text
小王角色参考@xiaowang.png：只提取面孔、短发和红色外套；
不要使用灰色背景、分栏结构或设定图排版。
```

Name characters in timed beats. Do not write only `@image2 walks`; write the character name plus one visible identity marker.

### 7. Write one Chinese audiovisual prompt per clip

Keep generation parameters outside the model prompt. Present duration, aspect ratio, frame rate, model, and reference counts as settings.

Inside each prompt, include:

1. clip intent and register;
2. labeled reference map with exclusions;
3. subject, setting, visual style, and camera grammar;
4. timestamped beats with visible action, camera motion, screen direction, and sound;
5. dialogue language and delivery when dialogue exists;
6. ambience, effects, music policy, and subtitle policy;
7. explicit final frame;
8. negative prompt.

Use `{dialogue}`, `<sound effect>`, `(music)`, and `【subtitle】` when clarity benefits. Default to no generated subtitles and no on-screen title; add typography in post.

Read [references/chinese-video-prompt-template.md](references/chinese-video-prompt-template.md) before writing final prompts.

### 8. Produce the delivery package

Create a project directory containing:

```text
project-name/
├── assets/
│   ├── characters/
│   ├── locations/
│   ├── props/
│   └── shots/
├── prompts/
│   ├── clip-01.md
│   └── ...
├── 00-director-brief.md
├── 01-production-timeline.md
├── project-manifest.json
└── api-jobs.json
```

Omit empty asset subdirectories. Every prompt file must contain exactly one ready-to-copy fenced prompt block. `api-jobs.json` should preserve clip order, settings, reference paths, prompt paths, and dependencies so a later provider adapter can submit jobs automatically.

Read [references/delivery-contract.md](references/delivery-contract.md) for the manifest schema and delivery details.

### 9. Validate before delivery

Run:

```bash
python scripts/validate_project.py /absolute/path/to/project
```

Fix every error. Treat warnings as reasons to inspect the affected prompt or asset.

Also visually inspect at least:

- every recurring-character identity anchor;
- every creature or transformation sheet;
- the first, most complex, and final shot image;
- any image that controls a dangerous, magical, or anatomy-sensitive action.

### 10. Deliver for humans and APIs

Lead with the result:

- total duration and clip count;
- maximum clip duration and maximum references per clip;
- representative inline images;
- clickable links to director brief, timeline, prompts, manifest, and project folder;
- note any intentional originalization or safety adaptation.

Do not make the user reconstruct references or combine separate sound and picture prompts. The copyable prompt is the operational unit.

## Hard invariants

- Never create a clip longer than 15 seconds.
- Never reference a file that does not exist.
- Never leave generated project assets only in an internal generation location.
- Never place required references only outside the copyable prompt block.
- Never give a reference without a job and exclusion rule.
- Never overload spoken audio; spoken Chinese should normally stay at or below roughly 4–4.5 characters per second, including pauses.
- Never treat a storyboard sheet as finished-film visual style.
- Never allow a multi-panel character sheet background or grid to become the scene.
- Never omit an explicit final frame.
- Never invent on-screen text unless the user requested it.
- Never claim an image or video was generated unless the artifact exists.

## Resource map

- [references/directing-and-runtime.md](references/directing-and-runtime.md): runtime math, dramatic beats, clip splitting, camera choices.
- [references/seedance-reference-rules.md](references/seedance-reference-rules.md): 2.0/2.5 budgets, upload order, reference roles, exclusions.
- [references/asset-generation.md](references/asset-generation.md): image asset strategy, filenames, identity and continuity QA.
- [references/chinese-video-prompt-template.md](references/chinese-video-prompt-template.md): copy-ready Chinese prompt structure and audio syntax.
- [references/delivery-contract.md](references/delivery-contract.md): project structure, manifest, API job schema, final QA.
- `scripts/validate_project.py`: deterministic delivery validator.

