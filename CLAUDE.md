# TU HOW Blog — Claude Context

## Project Overview
A Hugo blog (PaperMod theme) published at https://tuhowtw.github.io/tuhow-blog/. Content is written in Obsidian and published via a custom Python tool.

## Key Directories
- `content/posts/{lang}/` — published markdown posts, organized by language (`zh`, `en`, `ja`)
- `static/images/` — all blog images
- `tools/publisher/publisher.py` — Obsidian-to-Hugo publisher plugin (drag `.md` onto `publish.bat`)
- `themes/PaperMod/` — Hugo theme (avoid editing unless necessary)

## Publisher Plugin (`tools/publisher/publisher.py`)
A Tkinter GUI app. Drag an Obsidian `.md` file onto `publish.bat` to launch it.

**Obsidian note format** — notes have a YAML block before `---` separator:
```
```yaml
description: "..."
url-slug: "..."
tags: ["...", "..."]
categories: ["..."]
language: "zh"
author: "涂皓TU HOW"
title: "..."
```
---
(article body here)
```

The plugin parses this YAML into `self.prefill_data` and pre-fills the UI fields.

**Field mapping (Obsidian YAML → Hugo front matter):**
| Obsidian key | Hugo key |
|---|---|
| `title` | `title` |
| `url-slug` / `slug` | `slug` |
| `description` | `description` |
| `language` / `lang` | `lang` |
| `tags` | `tags` |
| `categories` | `categories` |

Output files go to `content/posts/{lang}/{slug}.md`. The plugin auto-commits and pushes to GitHub on publish.

## Hugo Front Matter (standard published format)
```yaml
---
title: "..."
date: "..."
slug: "..."
draft: false
author: "涂皓TU HOW"
description: "..."
lang: "zh"
categories: ["..."]
tags: ["..."]
cover:
  image: "/images/..."
  relative: false
---
```

## Workflow Notes
- `publish_edits.bat` — quick commit+push for direct edits (no publisher GUI)
- Images are copied to `static/images/` automatically by the publisher
- The site auto-deploys via GitHub Actions ~1-2 min after push
