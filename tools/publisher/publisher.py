import sys
import os
import re
import shutil
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

# --- Configuration ---
# Set the base directory to your Hugo blog repository
BLOG_REPO_DIR = r"C:\Users\drunk\howtu_program\tuhow.tw\tuhow-blog"
POSTS_DIR = os.path.join(BLOG_REPO_DIR, "content", "posts")
IMAGES_DIR = os.path.join(BLOG_REPO_DIR, "static", "images")

# Obsidian Vault Directory
OBSIDIAN_VAULT_DIR = r"C:\Users\drunk\Obsidian\vaultHOW"

# Ensure required directories exist
os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)


def dump_yaml(metadata):
    """A simple dependency-free YAML dumper for Hugo Front Matter."""
    lines = ["---"]
    for k, v in metadata.items():
        if isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - \"{item}\"")
        elif isinstance(v, dict):
            lines.append(f"{k}:")
            for sub_k, sub_v in v.items():
                if isinstance(sub_v, bool):
                    lines.append(f"  {sub_k}: {'true' if sub_v else 'false'}")
                else:
                    lines.append(f"  {sub_k}: \"{sub_v}\"")
        else:
            lines.append(f"{k}: \"{v}\"")
    lines.append("---\n")
    return "\n".join(lines)


class PublisherApp:
    def __init__(self, root, file_path):
        self.root = root
        self.file_path = file_path
        self.file_dir = os.path.dirname(file_path)
        self.filename = os.path.basename(file_path)
        self.title_guess = os.path.splitext(self.filename)[0].replace("-", " ").title()
        self.slug_guess = os.path.splitext(self.filename)[0].lower().replace(" ", "-")

        self.root.title("Obsidian to Hugo Publisher")
        self.root.geometry("550x500")
        
        # Read the raw markdown content
        with open(file_path, "r", encoding="utf-8") as f:
            self.raw_content = f.read()

        # Handle Obsidian-specific header with YAML
        # Format: Some text... ```yaml \n ... \n ``` \n ---
        self.prefill_data = {}
        content_to_process = self.raw_content
        
        separator = "\n---\n"
        if separator in self.raw_content:
            header, body = self.raw_content.split(separator, 1)
            # Find yaml block in the header
            yaml_match = re.search(r'```yaml(.*?)```', header, re.DOTALL | re.IGNORECASE)
            if yaml_match:
                import yaml as pyyaml
                try:
                    self.prefill_data = pyyaml.safe_load(yaml_match.group(1).strip()) or {}
                except Exception as e:
                    print(f"Error parsing YAML from header: {e}")
            
            # The content to publish is everything below the ---
            content_to_process = body.lstrip()
        
        # Parse images and determine the cover image
        self.cover_image_path = None
        self.processed_content = self.process_images(content_to_process)

        self.setup_ui()

    def process_images(self, content):
        """Finds both Markdown and Obsidian image links, copies images, and rewrites the links."""
        
        md_image_re = re.compile(r'!\[(.*?)\]\((.*?)\)')
        wiki_image_re = re.compile(r'!\[\[(.*?)\]\]')

        def replace_md_image(match):
            alt_text = match.group(1)
            img_path = match.group(2)
            return self.handle_image_copy(img_path, alt_text, is_wiki=False)

        def replace_wiki_image(match):
            img_path = match.group(1)
            return self.handle_image_copy(img_path, alt_text=img_path, is_wiki=True)

        content = md_image_re.sub(replace_md_image, content)
        content = wiki_image_re.sub(replace_wiki_image, content)
        return content

    def handle_image_copy(self, img_path, alt_text, is_wiki):
        """Copies the image to the Hugo repo and returns the new markdown link."""
        
        if img_path.startswith("http://") or img_path.startswith("https://"):
            if not self.cover_image_path:
                self.cover_image_path = img_path
            return f"![{alt_text}]({img_path})"

        if is_wiki and "|" in img_path:
            img_path = img_path.split("|")[0]

        # First, try relative to the markdown file
        abs_source_path = os.path.normpath(os.path.join(self.file_dir, img_path))
        
        # Second, try the specific Obsidian Vault folder
        if not os.path.exists(abs_source_path):
            basename = os.path.basename(img_path)
            # Obsidian sometimes stores attachments in vault root, or a specific subfolder.
            # We'll check the root of the vault and a 'static/images' subfolder if applicable.
            potential_paths = [
                os.path.join(OBSIDIAN_VAULT_DIR, basename),
                os.path.join(OBSIDIAN_VAULT_DIR, "static", "images", basename)
            ]
            for p in potential_paths:
                if os.path.exists(p):
                    abs_source_path = p
                    break
        
        if os.path.exists(abs_source_path):
            basename = os.path.basename(abs_source_path)
            dest_path = os.path.join(IMAGES_DIR, basename)
            hugo_rel_path = f"/images/{basename}"
            
            shutil.copy2(abs_source_path, dest_path)
            
            if not self.cover_image_path:
                self.cover_image_path = hugo_rel_path
                
            return f"![{alt_text}]({hugo_rel_path})"
        else:
            print(f"Warning: Image not found at {abs_source_path}")
            if is_wiki:
                return f"![[{img_path}]]"
            else:
                return f"![{alt_text}]({img_path})"

    def setup_ui(self):
        padding = {'padx': 10, 'pady': 5}
        
        tk.Label(self.root, text="Title:").grid(row=0, column=0, sticky='w', **padding)
        self.entry_title = tk.Entry(self.root, width=50)
        self.entry_title.insert(0, self.title_guess)
        self.entry_title.grid(row=0, column=1, **padding)

        tk.Label(self.root, text="Slug (URL):").grid(row=1, column=0, sticky='w', **padding)
        self.entry_slug = tk.Entry(self.root, width=50)
        prefill_slug = self.prefill_data.get("url-slug", self.prefill_data.get("slug", self.slug_guess))
        self.entry_slug.insert(0, prefill_slug)
        self.entry_slug.grid(row=1, column=1, **padding)

        tk.Label(self.root, text="Date:").grid(row=2, column=0, sticky='w', **padding)
        self.entry_date = tk.Entry(self.root, width=50)
        current_time = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        self.entry_date.insert(0, current_time)
        self.entry_date.grid(row=2, column=1, **padding)

        tk.Label(self.root, text="Description:").grid(row=3, column=0, sticky='w', **padding)
        self.entry_desc = tk.Entry(self.root, width=50)
        self.entry_desc.insert(0, self.prefill_data.get("description", ""))
        self.entry_desc.grid(row=3, column=1, **padding)

        tk.Label(self.root, text="Categories (comma separated):").grid(row=4, column=0, sticky='w', **padding)
        self.entry_categories = tk.Entry(self.root, width=50)
        cats = self.prefill_data.get("categories", [])
        if cats and isinstance(cats, list) and any(cats):
            self.entry_categories.insert(0, ", ".join([str(c) for c in cats if c]))
        self.entry_categories.grid(row=4, column=1, **padding)

        tk.Label(self.root, text="Tags (comma separated):").grid(row=5, column=0, sticky='w', **padding)
        self.entry_tags = tk.Entry(self.root, width=50)
        tags = self.prefill_data.get("tags", [])
        if tags and isinstance(tags, list) and any(tags):
            self.entry_tags.insert(0, ", ".join([str(t) for t in tags if t]))
        self.entry_tags.grid(row=5, column=1, **padding)

        tk.Label(self.root, text="Language (en/zh):").grid(row=6, column=0, sticky='w', **padding)
        self.entry_lang = tk.Entry(self.root, width=50)
        prefill_lang = self.prefill_data.get("language", self.prefill_data.get("lang", "zh"))
        self.entry_lang.insert(0, prefill_lang)
        self.entry_lang.grid(row=6, column=1, **padding)

        self.var_draft = tk.BooleanVar(value=False)
        self.chk_draft = tk.Checkbutton(self.root, text="Publish as Draft", variable=self.var_draft)
        self.chk_draft.grid(row=7, column=1, sticky='w', **padding)

        tk.Label(self.root, text="Cover Image:").grid(row=8, column=0, sticky='w', **padding)
        self.entry_cover = tk.Entry(self.root, width=50)
        if self.cover_image_path:
            self.entry_cover.insert(0, self.cover_image_path)
        self.entry_cover.grid(row=8, column=1, **padding)

        self.btn_save = tk.Button(self.root, text="Publish to Hugo", bg="#32CD32", fg="white", font=("Helvetica", 14, "bold"), command=self.save_post)
        self.btn_save.grid(row=9, column=0, columnspan=2, pady=20)

    def save_post(self):
        # Gather metadata
        metadata = {
            "title": self.entry_title.get(),
            "date": self.entry_date.get(),
            "slug": self.entry_slug.get(),
            "draft": self.var_draft.get(),
            "author": "涂皓TU HOW"
        }

        if self.entry_desc.get().strip():
            metadata["description"] = self.entry_desc.get().strip()
            
        lang = self.entry_lang.get().strip()
        if lang:
            metadata["lang"] = lang

        cat_str = self.entry_categories.get().strip()
        if cat_str:
            metadata["categories"] = [c.strip() for c in cat_str.split(",") if c.strip()]

        tag_str = self.entry_tags.get().strip()
        if tag_str:
            metadata["tags"] = [t.strip() for t in tag_str.split(",") if t.strip()]

        cover_str = self.entry_cover.get().strip()
        if cover_str:
            metadata["cover"] = {"image": cover_str, "relative": False}

        # Build Front Matter using custom dumper
        front_matter = dump_yaml(metadata) + "\n"
        final_file_content = front_matter + self.processed_content

        # Determine Output Path
        lang_folder = lang if lang else ""
        output_dir = os.path.join(POSTS_DIR, lang_folder) if lang_folder else POSTS_DIR
        os.makedirs(output_dir, exist_ok=True)
        
        output_filename = f"{self.entry_slug.get()}.md"
        output_path = os.path.join(output_dir, output_filename)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_file_content)
            
            # Automatically commit and push
            commit_msg = f"Auto-publish: {self.entry_title.get()}"
            try:
                subprocess.run(["git", "add", "."], cwd=BLOG_REPO_DIR, check=True, capture_output=True)
                subprocess.run(["git", "commit", "-m", commit_msg], cwd=BLOG_REPO_DIR, check=True, capture_output=True)
                subprocess.run(["git", "push"], cwd=BLOG_REPO_DIR, check=True, capture_output=True)
                
                messagebox.showinfo("Success", f"Article successfully published to:\n{output_path}\n\nImages were copied, and the changes have been automatically PUSHED to GitHub!")
            except subprocess.CalledProcessError as e:
                messagebox.showwarning("Partial Success", f"File was saved, but Git push failed.\n\nError: {e.stderr.decode('utf-8') if e.stderr else str(e)}\n\nPlease push manually.")

            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python publisher.py <path_to_markdown_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    root = tk.Tk()
    
    # Bring window to front automatically
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    app = PublisherApp(root, input_file)
    root.mainloop()
