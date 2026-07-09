# AI 剪辑视频最佳方案（Claude Code / Codex）

## 核心结论

**最佳方案：HyperFrames**（HeyGen 开源，33,611 ⭐，Apache 2.0）

**备选方案：MoviePy**（Python，14,772 ⭐，MIT）

---

## 方案对比

| 维度 | HyperFrames | MoviePy | Remotion |
|------|------------|---------|----------|
| GitHub Stars | **33,611** | 14,772 | 以本体为准 |
| 设计目标 | **Built for agents** | Python 视频库 | React 视频框架 |
| 对 AI 友好度 | **最高**——纯 HTML，有 20 个 agent skills | 中等——Python 代码 | 一般——需写 JSX/React |
| 学习成本 | **低**——会 HTML 就能写 | 中——需懂 Python | 高——需懂 React 生态 |
| 字幕 | 内置 `/embedded-captions` skill | 需自己用 PIL/文字渲染 | 自己写组件 |
| 口播处理 | 内置 `/talking-head-recut` skill | 手动合成 | 手动合成 |
| PPT | 内置 `/slideshow` skill | 手动 | 手动 |
| TTS/配音 | 内置 `hyperframes tts` | 需额外库 | 需额外库 |
| 预览 | 浏览器 live reload | 无（需渲染后看） | 有 Studio |
| License | **Apache 2.0**（完全开源） | MIT | Source-available（有限制） |
| 开发方 | HeyGen（视频领域专业） | 社区 | Remotion AG |
| 上手速度 | `npx hyperframes init` 秒建 | pip install | npx create-video |

---

## HyperFrames 详细介绍

### 它是什么

HyperFrames 是 HeyGen 开源的 HTML→MP4 视频渲染引擎。你写 **HTML + CSS + JS**，它渲染出视频。**本质就是为 AI agent 设计的**——AI 最擅长的就是写 HTML，不需要学任何框架。

关键特性：

- **HTML-native**：写 `<div>` + `data-*` 属性定义视频轨道和时间，无需 React 无构建步骤
- **20 个 Agent Skills**：Claude Code 加载后直接用 `/` 命令调
- **确定性渲染**：同一份输入永远输出同一帧画面
- **浏览器实时预览**：边改边看
- **GSAP / CSS / Lottie / Three.js 动画**：随便选
- **内置 TTS 配音 + 字幕生成**
- **支持 AWS Lambda 云端渲染**
- **Apache 2.0 完全开源**，无商用限制

### 对你的需求的 Skills 覆盖

| 你的需求 | HyperFrames Skill | 说明 |
|---------|-------------------|------|
| 口播视频 + 图形叠加 | **`/talking-head-recut`** | 给口播/访谈加 lower-thirds、数据标注、PiP 画中画、标题 |
| 加字幕 | **`/embedded-captions`** | 给已有口播视频加字幕，三种风格：底部横条、嵌入背后、纯电影感 |
| PPT/幻灯片 | **`/slideshow`** | 做演示/幻灯片，支持逐页揭示、动画过渡 |
| 网上素材穿插 | **`/general-video`** | 通用视频，多场景编排 |
| 配音配乐 | **`/media-use`** | TTS 生成配音、背景音乐、音效 |
| 设计规范 | **`/hyperframes-creative`** | 配色、字体、风格指南 |

### 7 步流水线

HyperFrames 有标准化的 7 步流程，每一步产出明确文件：

```
① Capture    → capture/          截图、颜色、字体、素材收集
② Design     → DESIGN.md         品牌/风格规范
③ Strategy   → (对齐确认)         视频类型、单一信息、叙事弧
④ Storyboard → STORYBOARD.md     逐节分镜 + SCRIPT.md 脚本
⑤ VO+Timing  → narration.wav     TTS 配音 + transcript.json 字级时间戳
⑥ Build      → compositions/*.html  逐节 HTML 动画
⑦ Validate   → lint + validate + snapshot  检查 → 出 MP4
```

### 快速上手指南

```bash
# 1. 给 Claude Code 安装 HyperFrames Skills
npx skills add heygen-com/hyperframes

# 2. 或手动建项目
npx hyperframes init my-video
cd my-video
npx hyperframes preview   # 浏览器实时预览
npx hyperframes render    # 出 MP4

# 3. 生成配音
npx hyperframes tts SCRIPT.md --voice af_nova --output narration.wav
npx hyperframes transcribe narration.wav   # 输出 transcript.json 字级时间戳

# 4. 云端渲染
npx hyperframes lambda deploy
```

### 一个组合 HTML 示例

这个示例展示了口播 + PPT + 字幕 + 配音的编排方式：

```html
<div id="stage" data-composition-id="main" data-width="1920" data-height="1080">
  <!-- 口播视频（背景层） -->
  <video class="clip" data-start="0" data-duration="60" data-track-index="0"
    src="assets/talking.mp4" muted playsinline></video>

  <!-- PPT 截图（第 5 秒切入，持续 8 秒） -->
  <img class="clip" data-start="5" data-duration="8" data-track-index="1"
    src="assets/slides/slide-01.png">

  <!-- 网上素材（第 15 秒插入） -->
  <video class="clip" data-start="15" data-duration="6" data-track-index="1"
    src="assets/stock/demo.mp4" muted playsinline></video>

  <!-- 字幕 -->
  <div class="clip subtitle" data-start="0" data-duration="60" data-track-index="2">
    <p id="subtitle-text" class="subtitle-text"></p>
  </div>

  <!-- 配音 -->
  <audio data-start="0" data-duration="60" data-track-index="3"
    data-volume="1.0" src="assets/narration.wav"></audio>

  <!-- GSAP 动画 -->
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.from("#slide", { opacity: 0, scale: 0.8, duration: 0.5 }, 5);
    window.__timelines.main = tl;
  </script>
</div>
```

### 字幕数据格式

Whisper 或 HyperFrames 内置转录生成的 `transcript.json` 格式：

```json
[
  { "text": "大家好", "start": 0.0, "end": 1.2 },
  { "text": "今天我们来聊聊", "start": 1.2, "end": 2.8 },
  { "text": "这个产品的核心功能", "start": 2.8, "end": 5.0 }
]
```

在页面中用 GSAP 逐字/逐句同步显示即可。

---

## MoviePy 方案（备选）

如果你更习惯 Python，MoviePy 也能做，但需要手动处理更多环节：

```python
from moviepy import *

# 加载素材
talking = VideoFileClip("assets/talking.mp4")
slide = ImageClip("assets/slides/slide-01.png").with_duration(5)
stock = VideoFileClip("assets/stock/demo.mp4")

# 合成视频 + PPT 叠加
final = CompositeVideoClip([
    talking,
    slide.with_position(("center", "center")).with_start(5),
    stock.with_position(("center", "center")).with_start(15),
])

# 加字幕（文字，需自行渲染中文字体）
# ...（字幕需额外的 PIL 或 ImageMagick 支持）

# 加配音
final = final.with_audio(AudioFileClip("narration.wav"))

final.write_videofile("output.mp4", fps=24)
```

### MoviePy 优缺点

**优点：** Python 生态成熟、MIT 协议、纯代码控制

**缺点：**
- 中文字幕渲染麻烦（需要 ImageMagick + 中文字体配置）
- 无实时预览，改一次渲染一次
- 没有现成 agent skills，Claude Code 需要从头写
- 复杂编排（口播+PPT+素材+字幕）要自己管理所有时间轴逻辑
- 没有标准项目流水线

---

## 最终推荐

```
排行榜：
🥇 HyperFrames  — 最适合 AI agent，开箱即用，Apache 2.0
🥈 MoviePy      — 适合 Python 开发者，或复杂帧级处理
🥉 Remotion     — 如果已有 React 项目或团队熟悉 React
```

**你的情况（Claude Code + 口播 + PPT + 素材 + 中文字幕）：**
→ **HyperFrames** 是最佳选择。装好 skills 后，Claude Code 自己就能规划和生成整个视频项目，不需要你写一行模板代码。

---

## 参考链接

- [HyperFrames GitHub](https://github.com/heyGen-com/hyperframes)
- [HyperFrames 文档](https://hyperframes.heygen.com/introduction)
- [HyperFrames Skills 目录](https://hyperframes.heygen.com/guides/skills)
- [HyperFrames 流水线](https://hyperframes.heygen.com/guides/pipeline)
- [MoviePy GitHub](https://github.com/Zulko/moviepy)
