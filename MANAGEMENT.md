# TU HOW Blog Management Handbook

This guide outlines your custom workflow for writing and managing articles on your Hugo blog directly from **Obsidian**.

---

## 🚀 Setting Up Obsidian for Hugo

To make writing in Obsidian seamless with Hugo publishing, configure these two settings in your vault:

### 1. Configure the "Attachments" Folder (For Images)
Hugo expects image files to live in the `static/images/` directory, but we want Obsidian to automatically put them there when you paste an image.

1. In Obsidian, go to **Settings** -> **Files and links**.
2. Set **Default location for new attachments** to: `In the folder specified below`.
3. Set **Attachment folder path** to: `static/images`
   *(Note: This path is relative to your Obsidian vault root. If your vault root is the `tuhow-blog` repo, use this exact path).*
4. Turn **Use [[Wikilinks]]** to `Off` (Hugo uses standard markdown links).
5. Turn **Use absolute path to file** to `On`.

**Result:** When you drag and drop or paste an image into a note, Obsidian will automatically save it to `static/images/` and insert a standard markdown link like `![[image.png]]`. **You must change `![[image.png]]` to standard markdown `![Image Description](/images/image.png)` for Hugo to render it.** *Thanks to the custom `render-image.html` hook we installed, Hugo will automatically handle the `/tuhow-blog/` subpath during deployment.*

### 2. Configure Properties (For Front Matter)
Hugo uses YAML front matter to define post metadata (tags, categories, dates). Obsidian's "Properties" view is perfect for this.

When creating a new article in the `content/posts/` directory, add the following Properties at the top of your note:

*   **title** (Text): The title of your post.
*   **date** (Date & Time): e.g., `2024-02-27T12:00:00+08:00`
*   **draft** (Checkbox/Boolean): Set to `false` when ready to publish.
*   **description** (Text): A brief summary.
*   **tags** (List): e.g., `tech`, `life`, `性別gender`.
*   **categories** (List): e.g., `Random Short Idea`.
*   **author** (Text): `涂皓TU HOW`

**To add a Cover Image:**
Add a property named **cover** (type: Text), but because it's a nested YAML object, you might need to switch to "Source Mode" in Obsidian and type it manually:
```yaml
cover:
  image: "/images/your-cover-photo.jpg"
```

---

## 📝 Writing a New Article

1. **Create the file**: Create a new note inside `content/posts/` (or a subfolder like `content/posts/zh/`). Give the file an English, URL-friendly name (e.g., `my-new-post.md`).
2. **Add Metadata**: Fill out the Obsidian Properties (tags, categories, etc.) as described above. Ensure `draft: true` while writing.
3. **Write**: Compose your article.
4. **Add Images**: Paste images. Ensure the markdown links look like `![](/images/your-image.jpg)`.
5. **Publish**: When finished, change `draft: true` to `draft: false`.

---

## 🚀 Publishing to the Live Site

You don't need to manually run Hugo. GitHub Actions handles the deployment.

1. Open your terminal in the `tuhow-blog` directory (or use VS Code Source Control / GitHub Desktop).
2. Commit your changes:
   ```bash
   git add .
   git commit -m "Publish new article: [Your Article Name]"
   git push
   ```
3. Wait about 1-2 minutes. The live site at **[https://tuhowtw.github.io/tuhow-blog/](https://tuhowtw.github.io/tuhow-blog/)** will automatically update!

---

## 🛠 Troubleshooting

*   **Images aren't showing on the live site**: Verify the image link in your markdown starts with `/images/` (e.g. `![](/images/photo.png)`), AND check that the actual `.png` file exists in the `static/images/` folder.
*   **Post isn't showing up**: Make absolutely sure that `draft: false` is set in the front matter properties.
*   **Formatting/CSS is broken**: Hard-refresh your browser cache (Ctrl+Shift+R or Cmd+Shift+R) after a new deployment.
