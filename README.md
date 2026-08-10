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
- [`story-video-director/scripts/validate_project.py`](story-video-director/scripts/validate_project.py)：项目检查器
- [`story-video-director/agents/openai.yaml`](story-video-director/agents/openai.yaml)：Codex 界面元数据

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

[MIT License](LICENSE)

