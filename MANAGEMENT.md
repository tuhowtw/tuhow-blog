# TU HOW Blog Management Handbook

This guide outlines the workflow for managing articles on your Hugo blog using **Obsidian**.

## 🚀 Obsidian to Hugo Workflow

### 1. File Location
Store your articles in: `content/posts/`
- You can create subfolders for organization (e.g., `content/posts/en/`, `content/posts/zh/`).
- Use lowercase filenames with hyphens (e.g., `my-new-post.md`).

### 2. Front Matter (Metadata)
Every article must start with YAML front matter. Here is a baseline template:

```yaml
---
title: "Your Post Title"
date: 2024-02-27T12:00:00+08:00
draft: false
description: "A brief summary of your post."
tags: ["tech", "life"]
categories: ["blog"]
author: "涂皓TU HOW"
# Cover image (optional)
cover:
    image: "/images/your-cover-image.png"
    alt: "Image Description"
    caption: "Credit: Source"
---
```

### 3. Image Management
- **Central Storage**: Always place your image files in the `static/images/` directory.
- **Linking in Markdown**: Reference them starting with `/images/`.
  - Example: `![Description](/images/my-photo.jpg)`
- **Obsidian Tip**: Set your Obsidian "Attachment Folder" to `static/images` to making dragging and dropping images seamless.

### 4. Publishing Changes
Once you've finished writing in Obsidian:
1. Open your terminal in the `tuhow-blog` directory.
2. Run the following commands:
   ```bash
   git add .
   git commit -m "Add new post: Your Post Title"
   git push
   ```
3. GitHub Actions will automatically build and deploy your site to:
   **https://tuhowtw.github.io/tuhow-blog/**

## 🛠 Troubleshooting
- **Images not showing?**: Ensure the image is in `static/images/` and the Markdown path starts with `/images/`.
- **Formatting looks weird?**: Check that your front matter doesn't have extra spaces or missing quotes.
- **Drafts**: If `draft: true`, the post won't show up on the live site.

---
*TU HOW Idea Base - Management Docs*
