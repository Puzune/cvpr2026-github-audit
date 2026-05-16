# CVPR 2026 GitHub Open Source Audit

Language: [中文](#中文) | [English](#english)

<a id="中文"></a>

## 中文

这是一个用于跟踪 CVPR 2026 论文 GitHub 开源状态与 star 数的数据集和可视化页面。

### 可视化网站

https://puzune.github.io/cvpr2026-github-audit/

### 数据源

- `results_live.json`：唯一的规范数据源，包含论文元数据、已确认 GitHub 仓库、证据、状态、置信度标签和复核备注。

### 网站文件

- `index.html`：公开入口。
- `dashboard.html`：读取 `results_live.json` 的 GitHub Pages 静态可视化页面。

### 同步策略

定期同步只更新 `results_live.json` 这一份规范数据源。进度文件、CSV 导出、本地脚本和日志只在本地生成和维护，不推送到 GitHub。

置信度标签用于区分强证据确认、已复核的多仓库官方产物、候选待复核，以及仍需标题搜索的论文。

<a id="english"></a>

## English

This repository provides a dataset and visualization page for tracking GitHub repository availability and star counts for papers listed on the CVPR 2026 paper index.

### Dashboard

https://puzune.github.io/cvpr2026-github-audit/

### Data Source

- `results_live.json`: the canonical data source, containing paper metadata, confirmed GitHub repositories, evidence, status, confidence labels, and review notes.

### Website Files

- `index.html`: public entrypoint.
- `dashboard.html`: static GitHub Pages viewer that reads `results_live.json`.

### Sync Policy

The recurring sync updates only the canonical JSON data source, `results_live.json`. Progress files, CSV exports, local helper scripts, and logs are generated and maintained locally rather than pushed to GitHub.

Confidence labels distinguish strong-evidence matches, reviewed multi-repository official artifacts, candidates that need review, and papers still needing title search.
