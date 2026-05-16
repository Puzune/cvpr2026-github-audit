# CVPR 2026 GitHub Open Source Audit

**Dashboard / 可视化网站:** https://puzune.github.io/cvpr2026-github-audit/

**Language / 语言:** [中文](#zh) | [EN](#en)

<a id="zh"></a>

## 中文

本项目跟踪 CVPR 2026 论文的 GitHub 开源状态、仓库证据和 star 数，并提供公开可视化页面。

### 快速入口

- 可视化网站：https://puzune.github.io/cvpr2026-github-audit/
- 规范数据源：[`results_live.json`](results_live.json)

### 公开文件

- `results_live.json`：唯一自动更新的数据源，包含论文信息、GitHub 仓库、证据、状态、置信度和复核备注。
- `dashboard.html`：GitHub Pages 可视化页面，读取 `results_live.json`。
- `index.html`：网站入口，跳转到 `dashboard.html`。
- `README.md`：项目说明。

### 同步策略

自动同步只更新 `results_live.json`。页面壳文件和 README 手动维护；进度文件、CSV 导出、本地脚本和日志只保存在本地。

### 置信度说明

`confidence` 字段用于区分强证据确认、已复核的多仓库官方产物、候选待复核，以及仍需标题搜索的论文。

<a id="en"></a>

## EN

This project tracks GitHub repository availability, repository evidence, and star counts for CVPR 2026 papers, with a public visualization page.

### Quick Links

- Dashboard: https://puzune.github.io/cvpr2026-github-audit/
- Canonical data source: [`results_live.json`](results_live.json)

### Published Files

- `results_live.json`: the only automatically updated data source, containing paper metadata, GitHub repositories, evidence, status, confidence labels, and review notes.
- `dashboard.html`: GitHub Pages visualization page that reads `results_live.json`.
- `index.html`: website entrypoint that redirects to `dashboard.html`.
- `README.md`: project documentation.

### Sync Policy

The automatic sync updates only `results_live.json`. The static page shell and README are maintained manually; progress files, CSV exports, local scripts, and logs stay local.

### Confidence Labels

The `confidence` field distinguishes strong-evidence matches, reviewed multi-repository official artifacts, candidates that need review, and papers still needing title search.
