# Chinese audiovisual video prompt template

## Contents

1. Settings block
2. Copyable prompt
3. Audio syntax
4. Final frame
5. Negative prompt

## 1. Settings block

Keep settings outside the model prompt:

```text
时长：10秒
画幅：16:9
帧率：24fps
模型：Seedance 2.0
参考图：4张
```

## 2. Copyable prompt

Use one fenced code block per clip:

```text
[类型、场景和本片段目的的一句话。]

本段引用素材：[角色名或用途]@[filename]；[场景用途]@[filename]；[动作或分镜用途]@[filename]。

[角色]角色参考@[filename]定义唯一的[角色名]：[可见身份标记]。只提取[面孔、发型、服装等]；不要使用[灰色背景、分栏、设定图布局]。成片中只有一个[角色名]。

[场景]参考@[filename]定义[布局、时间、天气、光线]。只提取[需要的属性]；不要提取[人物、文字或排版]。

主体：[人物、外貌和完整服装重述]。
场景：[空间、时间、天气和背景状态]。
风格：[光线、颜色、材质、颗粒和情绪]。
摄影：[连续镜头或剪辑驱动；主要镜头语言]。

0—3秒：[可见动作和屏幕方向]。[景别、角度和运镜。] <声音>
3—7秒：[可见动作和屏幕方向]。[景别、角度和运镜。] {对白}
7—10秒：[可见动作和屏幕方向]。[镜头如何稳定。] <声音>

声音：环境声、动作音效和音乐政策。对白语言：[普通话/方言/其他语言]。[角色]用[声线和语气]说：{台词}。无旁白。无字幕。

最终画面：[人物位置、姿势、灯光状态、镜头是否静止]。不得出现文字、字幕、标志和水印。

负面提示词：[身份、服装、结构、动作、背景、文字和风格禁止项]。
```

## 3. Audio syntax

- music: `(低沉弦乐逐渐增强)`
- effect: `<远处传来钟声>`
- dialogue: `{别回头。}`
- subtitle: `【三年前】`

Always name dialogue language before the line. Do not overlap narration and dialogue unless the user explicitly wants layered speech.

## 4. Final frame

Every clip needs a destination. State subject position, pose, lighting, camera rest, and text prohibition. The final frame should support the next edit or close the story.

## 5. Negative prompt

Include only plausible failures:

- identity and costume drift;
- duplicate characters;
- anatomy failures relevant to the action;
- reference background or grid bleed;
- location and lighting changes;
- unwanted text, logos, subtitles, or watermark;
- unwanted genre or rendering style.

Keep the complete copyable prompt under 5000 characters when possible. If it cannot fit, split the clip.

