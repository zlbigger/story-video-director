# Character identity sheets

## Contents

1. Default deliverable
2. Identity specification
3. Four-view composition
4. Prompt construction
5. Humans, creatures, and transformations
6. Visual QA and targeted correction
7. Video reference binding
8. Reusable ImageGen template

## 1. Default deliverable

Use one horizontal identity sheet per recurring character when face, costume, anatomy, or prop continuity matters. Default to four coordinated views:

1. front full body;
2. strict 90-degree side full body;
3. strict 180-degree back full body;
4. close-up portrait from upper chest to the top of the hair, hat, horns, or antennae.

Use a seamless neutral studio background. Do not place the character in a story location. Do not add names, labels, measurement lines, logos, borders, grids, or decorative UI.

Use a standalone 16:9 shot image instead when the asset's primary job is action blocking, scene composition, or lighting rather than identity.

## 2. Identity specification

Write concrete visible properties instead of relying only on a character name or broad style label. Define:

- adult or child status and apparent age;
- ancestry or fictional species when relevant, without imitating a real actor;
- height cue, build, posture, and body proportions;
- face shape, eyes, eyebrows, nose, mouth, skin tone, scars, freckles, tattoos, and other markers;
- hair color, texture, length, hairline, part, braid, bun, spikes, and back silhouette;
- every garment layer from collar to footwear, including color, fabric, fit, seams, closures, and wear;
- accessories and the exact side on which they appear;
- weapons or props, including attachment point, orientation, number, and material;
- tails, horns, antennae, ears, wings, third eyes, fur patterns, vents, or transformation anatomy.

State that every view shows exactly the same identity, age, face, body, costume, and accessories. Repeat the most fragile invariants near both the subject description and the final constraints.

## 3. Four-view composition

Require all of the following:

- three full-body figures are complete from head to feet;
- head and foot levels align;
- body scale and camera height are identical;
- front view uses a relaxed neutral stance with arms slightly separated from the torso;
- side view is a true 90-degree profile: head, shoulders, hips, knees, and feet all face sideways;
- back view is a true 180-degree rear view;
- close-up uses the same face, hairline, age, skin, and expression language;
- perspective distortion stays low, approximating an 85 mm studio lens;
- lighting is soft and neutral enough to reveal construction details.

Panel seams may occur naturally, but do not request drawn panel borders or contact-sheet labels.

## 4. Prompt construction

Detailed natural-language prompts have produced more stable results than short tag lists. Use this order:

1. purpose and identity-lock statement;
2. face, age, build, posture, and expression;
3. hair or creature anatomy;
4. complete costume and material construction;
5. props, attachment points, and side-specific details;
6. exact four-view layout;
7. seamless studio, lighting, lens, and realism;
8. explicit exclusions and failure modes.

Prefer material language such as `real dyed human hair`, `worn cotton with visible seams`, `weathered leather`, `aged brass`, or `practical creature makeup`. Avoid empty quality stacking such as only `8K, masterpiece, ultra detailed`.

Keep the background warm light gray for most humans, cool light gray when dark armor or green skin needs separation, and use only faint foot-contact shadows.

## 5. Humans, creatures, and transformations

For humans:

- describe a fictional casting identity rather than a celebrity likeness;
- keep anatomy natural and age appropriate;
- use complete practical clothing suitable for the intended rating;
- state which eye is scarred or covered and which hand or hip carries an item.

For creatures:

- describe believable joints, skin, fur, eyes, ears, horns, antenna roots, tails, and attachment points;
- choose premium practical-creature work with restrained digital finishing;
- exclude mascot suits, plush-toy surfaces, rubber masks, wax figures, taxidermy, and horror unless requested.

For transformations:

- create a separate identity sheet for every visually persistent state;
- preserve the properties that should survive the transformation;
- name exactly what changes in skin, hair, costume, anatomy, size, or energy state.

## 6. Visual QA and targeted correction

Inspect every recurring-character sheet at original resolution. Check:

- same face and apparent age across all views;
- correct front, strict side, and strict back orientation;
- equal scale, aligned feet, and no cropped body parts;
- stable hair silhouette and rear construction;
- correct side for scars, tattoos, earrings, watches, pouches, holsters, and weapons;
- correct count of eyes, marks, swords, horns, antennae, tails, fingers, and limbs;
- plausible tail, horn, antenna, wing, or prop attachment;
- no accidental text, symbols, logos, labels, or watermarks;
- no unwanted scene background, action pose, or unrelated props.

If one property fails, edit or regenerate for that property only. Preserve every successful identity and costume invariant. Do not accept a sheet whose close-up clearly depicts a different performer.

## 7. Video reference binding

Use the stable ASCII filename inside every consuming prompt. State both inheritance and exclusions:

```text
角色参考@character-identity-sheet.png：
严格继承面孔身份、年龄、体型、发型、完整服装、鞋子、配饰和固定道具结构；
只提取角色设定，不要继承浅灰影棚背景、四视图并排结构、分栏接缝、正侧背重复人物和中性站姿。
```

Add side-specific anchors when continuity depends on them:

```text
保持左眼疤痕、右腰道具袋和背后斜挂武器的位置不变。
```

Never let the video model interpret the multiple views as multiple characters in the finished scene.

## 8. Reusable ImageGen template

Adapt this template rather than copying irrelevant properties:

```text
Create a premium photorealistic live-action four-view character identity sheet for [CHARACTER OR ROLE], designed as a strict recurring-character reference for cinematic AI video. Every view must depict exactly the same [adult/child/creature] identity, with identical facial structure, apparent age, body proportions, hairstyle or creature anatomy, costume, colors, materials, accessories, and attached props.

[CHARACTER] is [AGE/STATUS] with [HEIGHT AND BUILD]. Describe the exact face shape, skin, eyes, eyebrows, nose, mouth, visible markers, posture, and restrained neutral expression. The face must remain recognizable and identical from every angle.

Describe hair in physical detail: color, real or fictional material, texture, length, hairline, part, spikes, bangs, braid, bun, and rear silhouette. For creatures, replace this paragraph with skin, fur, ears, horns, antennae, eyes, vents, tail, wings, and attachment anatomy. All geometry and colors remain identical across views.

Costume: list every layer from collar to footwear, including exact colors, fabrics, seams, closures, fit, wear, accessories, and the side on which each item appears. Describe weapons or props by count, material, orientation, attachment point, and holster or strap construction. No writing, logos, labels, or unintended symbols.

Show four coordinated reference views in one clean horizontal frame: left, front full-body neutral stance with arms slightly away from the torso; center-left, strict 90-degree left profile full-body with head, shoulders, hips, knees, and feet facing exactly sideways; center-right, strict 180-degree back full-body clearly showing rear hair or anatomy, garment construction, straps, and attachment points; right, close-up portrait from upper chest to the top of the hair, hat, horns, or antennae. The three full-body figures are equal height and scale with aligned head and foot levels. The portrait is unmistakably the same identity.

Setting: seamless [warm/cool] light-gray professional studio background and matching floor, soft neutral cinematic key and fill light, subtle rim light only when useful, and faint foot-contact shadows. High-budget live-action [GENRE] casting photography, natural skin or believable practical-creature texture, real hair or fur, realistic materials, subtle cinematic color, 85 mm low-distortion look.

Exactly one character identity shown in four coordinated views. No scenery, labels, captions, names, Chinese, Japanese, English, letters, numbers, measurement lines, logos, watermarks, signatures, drawn panel borders, or grids. Avoid inconsistent faces, changed age, changed body proportions, changed hair or anatomy, changed costume, misplaced props, duplicate items, extra limbs, malformed hands or feet, cropped body parts, action poses, anime drawing, cartoon rendering, toy, wax figure, mascot suit, or cheap cosplay.
```
