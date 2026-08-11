# Asset generation

## Contents

1. Asset plan
2. Identity design
3. Locations and props
4. Shot images
5. Filenames and persistence
6. Visual QA

## 1. Asset plan

Generate assets only after runtime and clip structure are known. Every asset must have at least one planned consumer clip.

Typical minimum set:

- recurring human characters;
- recurring creatures or transformed states;
- persistent location;
- one controlling frame per clip;
- final promotional or last-frame image when composition is critical.

## 2. Identity design

Define each recurring person with:

- adult/child status and age range;
- build and height cue;
- face shape and visible markers;
- hair length, texture, color, and arrangement;
- complete garment list, colors, fabrics, fit, footwear, and accessories.

Repeat invariants in every generation prompt. Use a neutral background for identity assets. Avoid text and labels.

When facial identity and costume continuity matter, default to one four-view identity sheet per recurring character:

1. front full-body view;
2. strict 90-degree side full-body view;
3. strict 180-degree back full-body view;
4. close-up portrait of the same identity.

Keep the three full-body figures equal in height and scale, align their head and foot levels, and keep the close-up unmistakably the same performer. Describe facial anatomy, apparent age, body proportions, hair geometry, every garment layer, footwear, accessories, scars, tattoos, creature anatomy, and prop attachment in concrete language. Require those properties to remain identical across all views.

Read [character-identity-sheets.md](character-identity-sheets.md) for the reusable prompt structure, neutral-studio specification, creature adaptations, quality gates, and video-reference exclusions.

For copyrighted or restricted likeness requests, preserve the requested genre function while creating an original identity, wardrobe, marks, and title. State the adaptation to the user.

## 3. Locations and props

Location plates should define layout, light direction, weather, time, material, and reusable landmarks. Do not include characters unless the frame itself requires them.

For plot-critical props, make position and orientation unambiguous. If a later beat depends on where a knife, key, product, or doorway is located, show it in the location reference.

## 4. Shot images

Prefer individual 16:9 shot images for video reference. Use them for:

- opening state;
- complex transformation;
- difficult interaction or combat;
- major reveal;
- final frame.

Do not use a contact sheet as the primary reference when individual frames are available. Contact sheets are for human review.

## 5. Filenames and persistence

Use stable ASCII names:

```text
00-character-name.png
01-creature-state.png
02-location-name.png
03-shot-01-description.png
```

Save selected outputs in the project directory. Never reference rollout data, temporary files, or internal generated-image locations in final prompts.

## 6. Visual QA

Inspect:

- identity and apparent age;
- costume colors and accessory continuity;
- hand, foot, weapon, rope, dance, or transformation anatomy;
- subject count and duplicates;
- location geometry and light direction;
- final-frame composition;
- accidental logos, text, watermarks, panel borders, or grids.
- front/side/back accuracy and whether the close-up is the same identity;
- equal scale and aligned feet across full-body views;
- correct side for scars, closed eyes, earrings, tattoos, wrist devices, weapons, and utility pouches;
- stable hair silhouette, braid length, tail or antenna attachment, and carried-prop placement.

Regenerate with one targeted correction rather than rewriting every property.
