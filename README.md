# Story Video Director · 故事视频导演

把任意故事、文章、脚本、广告构想或一句话创意，自动转换成可执行的 AI 视频制作项目。

[官方网站](https://zlbigger.com) · [作者主页](https://zlbigger.com)

`story-video-director` 是一个面向 Codex 的导演型 Skill。它不只是改写提示词，而是从叙事判断、时长规划、角色与场景设计开始，生成所需图片素材，拆分视频片段，并交付可以直接复制到 Seedance 等参考驱动视频模型中的中文视听提示词。

> Turn stories into director-led AI video production packages: visual assets, shot plans, Chinese audiovisual prompts, and API-ready manifests.

## 能解决什么问题

- 自动理解故事的核心事件、情绪变化、反转与结局
- 根据内容密度判断最佳总时长，不强行压缩成 15 秒
- 将完整故事拆成多个独立视频片段，每段不超过 15 秒
- 设计角色、服装、场景、道具、怪物、变身状态和关键帧
- 默认生成“正面全身＋严格侧面＋背面全身＋脸部特写”的四视图角色身份图，增强真人角色与视频连续性
- 调用 Codex 的 ImageGen 能力实际生成并保存图片素材
- 为每段生成包含运镜、动作、对白、旁白、音效、环境声和音乐的中文提示词
- 在每段可复制提示词中自动加入 `角色名@filename.png` 形式的素材引用
- 控制 Seedance 2.0 / 2.5 的参考素材数量与上传顺序
- 输出适合人工操作的制作文档，以及便于后续接入视频 API 的 JSON 清单
- 使用内置检查器发现超时、素材缺失、引用遗漏和参考数量超限

## 工作流程

```text
故事或创意
   ↓
导演分析与时长判断
   ↓
拆分为 ≤15 秒的视频片段
   ↓
规划角色、场景、道具与关键帧
   ↓
生成并检查图片素材
   ↓
编写逐段中文视听提示词
   ↓
生成项目清单与 API jobs
   ↓
自动验证完整交付物
```

默认采用“自动导演模式”：除非缺少的信息会显著改变项目，否则不会用一长串问题打断制作。

## 四视图角色身份锚点

对需要反复出镜的真人角色、怪物或变身状态，Skill 默认生成一张横向四视图身份图：

1. 正面全身；
2. 严格 90° 侧面全身；
3. 严格 180° 背面全身；
4. 同一角色的脸部特写。

提示词会具体锁定年龄、脸型、体型、发型轮廓、完整服装、鞋子、配饰、疤痕、纹身、武器位置，以及尾巴、触角、鹿角或第三只眼等特殊结构。角色图使用干净的中性影棚背景，不把故事场景混入身份素材。

后续视频提示词会自动加入排除规则，防止模型把四视图误解成四个人：

```text
角色参考@character-identity-sheet.png：
严格继承面孔身份、年龄、体型、发型、完整服装、鞋子、配饰和固定道具结构；
只提取角色设定，不要继承浅灰影棚背景、四视图并排结构、分栏接缝、
正侧背重复人物和中性站姿。
```

详细生成规范与英文 ImageGen 模板见 [`character-identity-sheets.md`](story-video-director/references/character-identity-sheets.md)。

## 安装

克隆仓库：

```bash
git clone https://github.com/zlbigger/story-video-director.git
```

将 Skill 安装到 Codex：

```bash
mkdir -p ~/.codex/skills
cp -R story-video-director/story-video-director ~/.codex/skills/
```

重新打开 Codex，或开启一个新任务，使 Skill 列表刷新。

## 使用方法

在 Codex 中直接调用：

```text
使用 $story-video-director，把下面的故事制作成完整视频项目：

[在这里粘贴故事、文章、脚本或创意]
```

也可以指定方向：

```text
使用 $story-video-director，把这个民间故事制作成写实东方志怪短片。
使用 Seedance 2.0，16:9，不要字幕，自动生成全部参考图。
```

```text
使用 $story-video-director，为这个产品构想制作一支 15 秒电影感广告。
要求中文旁白、竖屏 9:16，并输出后续 API 可读取的任务清单。
```

## 每段提示词的引用格式

所有必需参考素材都会写进可复制的提示词代码块，而不是散落在说明文字中：

```text
阿岚角色参考@alan-character.png：只提取面孔、短发和灰色风衣；
不要使用灰色影棚背景、白色分隔线或人物设定图排版。

雨夜车站场景参考@station-location.png：提取站台布局、时钟位置和左侧冷光；
不要提取参考图中的人物、文字和标志。
```

每个引用都会说明：

1. 这张素材负责提供什么；
2. 在什么镜头中使用；
3. 哪些背景、排版或风格不得继承。

## 项目输出

```text
project-name/
├── assets/
│   ├── characters/
│   ├── locations/
│   ├── props/
│   └── shots/
├── prompts/
│   ├── clip-01.md
│   └── clip-02.md
├── 00-director-brief.md
├── 01-production-timeline.md
├── project-manifest.json
└── api-jobs.json
```

- `00-director-brief.md`：故事理解、视觉圣经、表演和声音方向
- `01-production-timeline.md`：片段时长、叙事作用、素材与衔接关系
- `prompts/`：每段一个可以直接复制的中文视听提示词
- `project-manifest.json`：完整片段、时长和引用关系
- `api-jobs.json`：保持顺序和依赖关系的供应商无关任务清单

## Seedance 参考预算

默认采用保守的 Seedance 2.0 规则：

- 每段最多 9 张参考图
- 每段最多 3 段参考视频
- 每段最多 3 段参考音频
- 混合引用时尽量保持总数不超过 12 个

Seedance 2.5 可支持更多图片，常见约为 30 张量级。不同入口的音频、视频和总文件上限可能不同，因此 Skill 支持在项目清单中记录当前平台确认过的 `reference_limits`，而不是猜测上限。

## 验证生成项目

```bash
python3 story-video-director/scripts/validate_project.py /absolute/path/to/project
```

检查内容包括：

- 每段是否超过 15 秒
- 总时长是否等于各片段之和
- 图片、视频和音频引用是否超限
- 引用文件是否真实存在
- 每个引用是否出现在提示词中的 `@filename`
- 是否包含声音策略、最终画面和负面提示词
- API jobs 顺序是否与项目清单一致

机器可读输出：

```bash
python3 story-video-director/scripts/validate_project.py --json /absolute/path/to/project
```

## 目录说明

- [`story-video-director/SKILL.md`](story-video-director/SKILL.md)：Skill 主工作流
- [`story-video-director/references/`](story-video-director/references/)：导演、素材生成、Seedance 与交付规范
- [`character-identity-sheets.md`](story-video-director/references/character-identity-sheets.md)：真人四视图角色身份图、详细提示词模板与一致性验收规范
- [`story-video-director/scripts/validate_project.py`](story-video-director/scripts/validate_project.py)：项目检查器
- [`story-video-director/agents/openai.yaml`](story-video-director/agents/openai.yaml)：Codex 界面元数据
- [`reference-materials/`](reference-materials/)：创作过程中参考的相关文本与 PDF，不属于 Skill 运行依赖

## 参考文本

仓库同时保留了项目设计和研究过程中使用的参考资料，方便理解提示词方法、人物表演、画面生成和 Seedance 工作流：

- [ACTING SKILL.md](reference-materials/ACTING%20SKILL.md)：AI 视频人物行为与表演设计参考
- [LIRA SKILL.md](reference-materials/LIRA%20SKILL.md)：图片提示词优化方法参考
- [CINEDANCE HIGGSFIELD SKILL.md](reference-materials/CINEDANCE%20HIGGSFIELD%20SKILL.md)：Seedance 与 Higgsfield 导演提示词参考
- [视频提示词建议.md](reference-materials/%E8%A7%86%E9%A2%91%E6%8F%90%E7%A4%BA%E8%AF%8D%E5%BB%BA%E8%AE%AE.md)：中文视频提示词与分镜建议
- [prompt-guide-v1-2.pdf](reference-materials/prompt-guide-v1-2.pdf)：提示词指南 PDF

这些文件按原始文件名和内容收录，用作相关文本参考；它们不会在安装 Skill 时自动进入运行上下文。参考资料的署名与权利归原作者或原权利人所有，除非文件自身另有声明，不视为由本仓库 MIT License 重新授权。

## 设计原则

- 内容决定时长，平台限制决定分段
- 一段视频只承载一个主要事件
- 图片素材必须真实生成并保存，不能只给图片提示词
- 所有必要引用必须位于最终可复制提示词中
- 声音与画面是一体化提示词，不让用户二次拼装
- 少而明确的参考素材，通常比堆满上限更稳定
- 不声称生成了不存在的图片或视频

## 网站与反馈

项目动态、案例与更多 AI 创作工具，请访问 [zlbigger.com](https://zlbigger.com)。

## License

本项目代码与原创 Skill 文件采用 [MIT License](LICENSE)。`reference-materials/` 中的外部参考资料不包含在该授权范围内，具体以原资料声明为准。
