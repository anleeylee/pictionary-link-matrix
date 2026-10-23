# Pictionary 外链内容矩阵（Pictionary Link Matrix）

> **Pictionary 词站的外链内容矩阵生成器——围绕 pictionary 关键词生成外链推广素材，联动 GitHub Pages 与 Kaggle 的锚文本外链建设，并校验 Markdown 链接卫生。所有链接一律输出为标准 Markdown 链接 `[text](url)`，绝不输出裸 URL。**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![CLI](https://img.shields.io/badge/CLI-ready-4B8BBE)](link_matrix.py)
[![No dependencies](https://img.shields.io/badge/deps-stdlib%20only-blueviolet)](requirements.txt)

---

## 相关链接

- 🎲 **在线工具体验：** [Pictionary Word Generator — 免费 7000+ 画画提示词](https://pictionarywordgenerators.com/)
- 📋 **完整词表：** [List of Pictionary Words — 1000+ 分难度提示词](https://pictionarywordgenerators.com/list-of-pictionary-words)
- 英文版说明：[README.md](README.md)

---

## 这个工具做什么

给内容站建外链是重复劳动：每个外链位都要配锚文本、目标页和平台区块——
而且每个锚文本都必须是**标准 Markdown 链接**，因为裸 URL 会被很多发布方
忽略、在谷歌眼里也像垃圾链接。本工具把整条流水线自动化。

三个子命令：

1. **`generate`** — 为每个 pictionary 关键词生成完整素材包：4 种锚文本
   变体（品牌词 / 部分匹配 / 精确匹配 / 通用词）、SERP 风格描述、
   **GitHub README 外链区块**、**GitHub Pages 页脚区块**与 **Kaggle 数据集
   描述区块**——全部用 `[text](url)` 指向该关键词的转化页。
2. **`matrix`** — 生成跨平台外链矩阵（平台 × 关键词 × 锚文本 × 目标页 ×
   状态），每个关键词 4 个平台：`github-readme`、`github-pages`、
   `kaggle`、`external`。
3. **`verify`** — 卫生门禁：扫描任意 Markdown 文件里你域名下的裸 URL
   （排除代码块与 `[text](url)` 内的链接），报出并失败退出。发布素材前
   在 CI 里跑一遍。

每个关键词自动映射到自己的转化页（如 *pictionary words for christmas*
→ `/christmas-pictionary-words`、*list of pictionary words* →
`/list-of-pictionary-words`），保证锚文本永远指向最相关的页面。输出按
`--seed` 确定，便于测试与审阅。

## 为什么重要

工具链其余部分负责出站与出数据：
[Pictionary Wordlist Generator](https://github.com/anleeylee/pictionary-wordlist-generator)
创建词库，[Pictionary Page Generator](https://github.com/anleeylee/pictionary-page-generator)
生成 SEO 页面，[Pictionary SEO Scanner](https://github.com/anleeylee/pictionary-seo-scanner)
保证站内 SEO 健康，[Pictionary Keyword Tracker](https://github.com/anleeylee/pictionary-keyword-tracker)
决定下一个做什么，[Pictionary GSC Monitor](https://github.com/anleeylee/pictionary-gsc-monitor)
跟踪谷歌收录。本工具补齐**站外**一环：可直接粘贴的锚文本素材，跨
GitHub Pages、Kaggle 与外部渠道扩张外链——且链接卫生由设计保证。

## 安装

```bash
git clone https://github.com/anleeylee/pictionary-link-matrix.git
cd pictionary-link-matrix

# 仅标准库 —— 无需 pip install
python link_matrix.py --help
```

## 用法

```bash
# 1. 为关键词生成素材包
python link_matrix.py generate \
  --keywords "pictionary words for christmas,easy pictionary words" \
  --out-dir out

# 或从文件读取
python link_matrix.py generate \
  --keywords-file examples/keywords.json --out-dir out

# 2. 生成跨平台外链矩阵
python link_matrix.py matrix \
  --keywords-file examples/keywords.json --out-dir out

# 3. 卫生门禁（CI 友好，发现裸 URL 退出非零）
python link_matrix.py verify --file out/material.md
```

### 输出

- `material.md` / `material.json` — 逐关键词素材包：锚文本变体、标题、
  描述、GitHub README / GitHub Pages / Kaggle 区块
- `matrix.md` / `matrix.json` — 跨平台外链矩阵（关键词 × 平台，含锚文本、
  目标 URL 与状态）

## 测试

```bash
python -m unittest discover -s tests -v
```

覆盖：素材结构、目标页映射、锚文本变体生成、每个生成区块的零裸 URL
保证、矩阵规模（关键词 × 4 平台）、卫生检查的裸 URL 识别与代码块豁免、
完整 CLI 链路。11 项测试，全部离线。

## 许可

MIT——可自由使用与扩展，请保留署名。你生成的锚文本素材可在任何地方发布。
