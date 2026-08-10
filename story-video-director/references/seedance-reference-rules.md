# Seedance reference rules

## Contents

1. Conservative budgets
2. Upload order
3. Reference map
4. Storyboards
5. Multi-angle assets
6. Failure reduction

## 1. Conservative budgets

Default to Seedance 2.0 when the user does not specify a version:

- at most 9 image references per generated clip;
- at most 3 video references and 3 audio references;
- keep all references near 12 or fewer when the interface combines budgets;
- prefer 2–5 images per clip for stability.

Seedance 2.5 supports a larger budget, commonly around 30 images and more video/audio references. Treat limits as ceilings, not targets. Core identity benefits from fewer, clearer sources.

Because Seedance 2.5 limits can differ by product entry point, do not invent a fixed video, audio, or combined-file ceiling. Confirm the active interface or API documentation. When known, record the provider-confirmed limits in `project-manifest.json` under `reference_limits`; the validator will enforce them.

## 2. Upload order

Keep order stable across all clips:

1. storyboard or controlling keyframe;
2. recurring character identities in script order;
3. creature, product, or key prop;
4. location plate;
5. additional opening, action, or final keyframes;
6. optional style image;
7. motion video;
8. voice or ambience audio.

For API delivery, preserve both filename and slot mapping.

## 3. Reference map

Every reference needs:

- human-readable label and `@filename`;
- what it provides;
- where it matters;
- what must not be inherited.

Example:

```text
阿岚角色参考@alan-character.png：提取面孔、短发和灰色风衣；
不要使用灰色影棚背景、白色分隔线和三栏设定图布局。

雨夜车站场景参考@station-location.png：提取站台布局、时钟位置和左侧冷光；
不要提取图片中的任何人物。
```

Repeat identity using character names and one visible marker in the first beat where they appear.

## 4. Storyboards

A storyboard is a structure reference, not a style reference. If used, assign timestamps to panels and state the mapping in the prompt.

Always exclude:

- panel borders;
- labels, numbers, captions, arrows;
- white paper background;
- pencil, ink, or monochrome rendering style;
- storyboard grid layout.

If a storyboard is ignored, first add panel-to-time mapping, then move it to the first slot, then remove competing references.

## 5. Multi-angle assets

When the budget allows, use separate identity images for front, profile, and close portrait. When Seedance 2.0 budget is tight, a clean multi-panel sheet may be used, but its gray backdrop and grid must be explicitly excluded.

Multiple images defining one object or character require a collapse line:

```text
以上三张图片共同定义同一个折叠灯；成片中始终只有一盏折叠灯。
```

## 6. Failure reduction

When over budget, remove references in this order:

1. general style;
2. redundant location angles;
3. redundant action stills;
4. secondary props;
5. never remove the only core identity anchor unless no recurring identity exists.

Use 5–10s motion or audio references when possible. Very short references carry too little information; long references dilute the desired feature.
