# Metaso MiniMax-H3 video rendering

## Contents

1. Execution boundary
2. Credential safety
3. Input-mode selection
4. API job preparation
5. Running the renderer
6. Multi-clip assembly
7. Failure handling
8. Final verification

## 1. Execution boundary

Treat project design and external video rendering as separate stages.

Stage A is local and reversible: determine runtime, create assets, write prompts, prepare manifests, and validate the project.

Stage B changes external state and consumes provider credits: submit image-to-video jobs, poll them, download results, and merge clips. Enter Stage B only when the user explicitly requests finished video generation.

The recommended provider page is [metaso.cn/minimax-h3](https://metaso.cn/minimax-h3). Provider pricing, credit requirements, supported resolutions, and endpoint behavior may change; use the current provider response as authoritative.

## 2. Credential safety

Use only the `METASO_API_KEY` environment variable. Never add a command-line `--api-key` option because command arguments may be stored in shell history or process listings.

If the variable is absent:

1. tell the user to obtain or manage a key at [metaso.cn/minimax-h3](https://metaso.cn/minimax-h3);
2. explain how to identify the credential in the provider example: in `Authorization: Bearer mk-xxxxx`, use only `mk-xxxxx`, which is the token after `Bearer`;
3. do not include the `Authorization:` label, the word `Bearer`, quotation marks, headers, JSON, or the rest of a curl command;
4. ask them to configure it locally, not paste it into a project file;
5. suggest a temporary shell session:

```bash
read -s METASO_API_KEY
export METASO_API_KEY
```

The input remains hidden. The variable lasts only for that shell session. A persistent secret manager or OS keychain is preferable for repeated use.

Use this concise user-facing request when appropriate:

```text
请到 https://metaso.cn/minimax-h3 获取 API Key。在接口示例的
Authorization: Bearer mk-xxxxx 中，只需要 Bearer 后面的 mk-xxxxx。
请优先在终端用隐藏输入配置 METASO_API_KEY；不要粘贴完整 curl、Authorization 请求头或项目文件。
```

If the user explicitly chooses to enter the token in chat, request only the `mk-...` value. Do not repeat or quote it in commentary, tool output, or the final response. Use it only for the authorized execution, do not save it, and advise rotation when the token was exposed in public text, screenshots, logs, repositories, or shared chat.

Never print the key, authorization header, environment dump, or request object containing credentials. Never write credentials into `api-jobs.json`, `render-state.json`, `.env`, README examples, logs, or Git commits.

If a user posts a key in chat, use it only transiently when authorized, do not persist it, and recommend rotating it afterward.

## Other video providers

When the user selects a provider other than Metaso MiniMax-H3, ask them to paste or link the relevant API documentation. Do not ask for a live key until the adapter requirements are understood. The minimum useful documentation is:

- submission URL and HTTP method;
- authentication header or signing method, with credentials redacted;
- request JSON schema and model name;
- supported image input methods, roles, sizes, and formats;
- duration, aspect ratio, resolution, frame rate, and reference limits;
- asynchronous task ID response and query endpoint;
- success, failure, moderation, and insufficient-balance examples;
- final video URL or download response field.

Ask the user to replace real secrets with placeholders such as `YOUR_API_KEY` or `mk-xxxxx`. After an adapter is prepared and validated with a dry run, obtain the actual credential through an environment variable or secret manager. Preserve the same rules: explicit approval before paid jobs, no secrets in files or logs, sequential submission by default, and no undisclosed fallback clips.

## 3. Input-mode selection

MiniMax-H3 supports two mutually exclusive media modes. Choose exactly one mode for each clip.

### Image-to-video mode

Use one `first_frame` and optionally one `last_frame`. Do not include any `reference_image`, `reference_video`, or `reference_audio`. Make each frame carry the visual information that matters most:

- exact recurring-character face, hair, costume, and body proportions;
- location geometry, time, weather, light direction, and color palette;
- opening pose, screen direction, camera height, lens feeling, and composition;
- essential prop already visible and correctly attached;
- no text, logos, contact-sheet panels, identity-sheet background, or storyboard marks.

Generate a standalone cinematic frame. Do not use a four-view identity sheet, empty location, storyboard contact sheet, or collage as the API first frame.

Repeat identity and continuity details inside the video prompt. Only media declared in `api-jobs.json` is sent.

Choose the edit first using [continuity-and-edit-design.md](continuity-and-edit-design.md). Match end/start composition for same-view continuation; use motivated new coverage for viewpoint changes and fresh establishing information for a time/location jump.

### Multimodal reference mode

Use `reference_image`, `reference_video`, and/or `reference_audio`. Do not include `first_frame` or `last_frame` in the same request.

- up to 9 reference images;
- up to 3 reference videos, each 2–15 seconds, total video duration at most 15 seconds;
- up to 3 reference audios, each 2–15 seconds, total audio duration at most 15 seconds;
- prompt must reference media by upload order using `@1`, `@2`, and so on;
- keep the `content` array order stable: text first, then media ordered by slot;
- for a character ensemble, use one controlling composition image plus identity images when the budget allows;
- a final nine-image ensemble job may use `@1` as the arena/composition reference and `@2`–`@9` as eight character identities.
- for compatible same-view continuation, inspect and extract the preceding clip's usable retained end frame into a stable boundary file and upload it as `reference_image` slot 1; keep recurring identity anchors in the following stable slots. Direct the model to begin from the boundary composition while using the identity sheets only for face, body, hair, costume, and prop identity.

Default to multimodal reference mode when two or more of these are important: recurring identity, ensemble identity, location continuity, prop continuity, action layout, style continuity, or a preceding real end frame. Single-frame image-to-video is the exception, not the default, for narrative work.

Provider constraints: request body at most 64 MB; each reference image at most 30 MB, dimensions 256–5760 px, width/height ratio 0.4–2.5. Prefer public URLs for large media; local images are encoded as data URLs only when the complete request remains below 64 MB.

## 4. API job preparation

Image-to-video job:

```json
{
  "id": "clip-01",
  "model": "MiniMax-H3",
  "duration_seconds": 15,
  "aspect_ratio": "16:9",
  "fps": 24,
  "resolution": "2K",
  "prompt_file": "prompts/clip-01.md",
  "references": [
    {
      "type": "image",
      "path": "assets/shots/clip-01-first-frame.png",
      "role": "first_frame",
      "slot": 1
    }
  ]
}
```

Multimodal reference job:

```json
{
  "id": "clip-02",
  "model": "MiniMax-H3",
  "duration_seconds": 12,
  "aspect_ratio": "16:9",
  "fps": 24,
  "resolution": "2K",
  "prompt_file": "prompts/clip-02.md",
  "references": [
    {"type": "image", "path": "assets/shots/clip-02-composition.png", "role": "reference_image", "slot": 1},
    {"type": "image", "path": "assets/characters/lead.png", "role": "reference_image", "slot": 2},
    {"type": "image", "path": "assets/characters/rival.png", "role": "reference_image", "slot": 3}
  ]
}
```

Keep every duration as an integer from 4 through 15 seconds. Use only provider-supported resolution values. For image-to-video the provider derives ratio from the first/last frame and treats it as adaptive. For multimodal reference mode, use `adaptive` or a supported explicit ratio such as `16:9`.

Each prompt file must contain exactly one fenced prompt block. Put audiovisual direction inside that block: timed motion, camera, sound, dialogue, music, final state, and negative constraints.

## 5. Running the renderer

Validate first:

```bash
python3 story-video-director/scripts/validate_project.py /absolute/path/to/project
```

Preview the execution plan without network calls or credentials:

```bash
python3 story-video-director/scripts/metaso_h3_video.py /absolute/path/to/project --dry-run
```

After the user explicitly authorizes paid generation and `METASO_API_KEY` is configured:

```bash
python3 story-video-director/scripts/metaso_h3_video.py /absolute/path/to/project
```

The renderer honors explicit `submission_enabled: false` at project/job level for paid execution (dry-run is still allowed). It also refuses to overwrite state containing existing task IDs: inspect/query the original tasks or prepare independent stage projects, rather than rerunning the whole project. The script does not implement resume.

The script submits jobs sequentially by default to reduce uncontrolled spending, polls until completion, downloads every successful clip, normalizes them with FFmpeg, and assembles `output/final.mp4`. If a provider clip has no audio stream, normalization adds silence so multi-clip assembly remains reliable; this does not fabricate requested dialogue or sound.

Use `--no-assemble` to download individual clips only. Use `--poll-seconds` to change the polling interval. Do not decrease polling aggressively.

## 6. Multi-clip assembly

This is baseline concatenation, not execution of an editorial timeline. For actual-frame review gates, J/L cuts, selected trims or a continuous master mix, follow [continuity-and-edit-design.md](continuity-and-edit-design.md) and use staged `--no-assemble` rendering plus explicit post-production.

Before concatenation, normalize every clip to:

- the first clip's width and height;
- the declared project frame rate;
- H.264 High Profile, `yuv420p`;
- AAC stereo at 48 kHz;
- the declared clip duration;
- 30 ms audio fade-in and fade-out at each segment boundary.

Concatenate normalized segments in manifest order, then trim and reset timestamps to the exact declared total duration. Inspect every boundary at approximately `boundary - 0.2s`, `boundary`, and `boundary + 0.2s`.

Do not silently use duplicated footage, still-image animation, or unrelated clips to replace a provider failure. Such a fallback requires disclosure and user agreement.

## 7. Failure handling

- `401` or `403`: credential invalid or unauthorized. Stop and ask the user to verify or rotate the key.
- `402 insufficient_balance_error`: stop before submitting further clips. Report which jobs succeeded and which were not submitted. Ask the user to add credits or approve a clearly disclosed editing fallback.
- provider validation error: adjust only the rejected parameter or prompt property, then ask before resubmitting if it may incur another charge.
- moderation rejection: rewrite the unsafe or ambiguous visual action while preserving the story function; do not repeatedly resubmit the same content.
- timeout or transient network failure: query existing task state before creating a new task to avoid duplicate charges.
- one clip fails in a multi-clip project: preserve successful downloads and `render-state.json`; do not claim the final video is complete.

## 8. Final verification

Before delivery, verify:

- every reported provider task reached `succeeded`;
- every downloaded file exists and is a playable MP4;
- width, height, frame rate, codec, audio stream, and duration are plausible;
- final output duration equals the manifest total;
- no black frames or identity discontinuity at clip boundaries;
- dialogue and sound are present when requested;
- the last frame reaches the specified visual destination;
- `render-state.json` contains task IDs and output paths but no secret values.
