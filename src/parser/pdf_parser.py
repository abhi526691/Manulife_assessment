import os
import base64
import json
from uuid import uuid4
from mistralai.models import OCRResponse
import re
from mistralai.models import OCRResponse
from langchain_text_splitters import MarkdownHeaderTextSplitter

from dotenv import load_dotenv

load_dotenv()

image_store = {}


class contractParser:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")

    def store_image_in_memory(self, image_base64: str, ext: str = "png") -> str:
        image_id = str(uuid4())
        image_store[image_id] = {
            "bytes": base64.b64decode(image_base64),
            "mime": f"image/{ext}"
        }
        return image_id

    def fetch_image_from_memory(self, image_id: str):
        entry = image_store.get(image_id)
        if entry:
            return entry["bytes"], entry["mime"]
        return None, None

    def replace_images_in_markdown(self, markdown_str: str, images_dict: dict) -> str:
        """
        Replace image placeholders in markdown with base64-encoded images.
        """
        for img_name, base64_str in images_dict.items():
            markdown_str = markdown_str.replace(
                f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})"
            )
        return markdown_str

    def get_combined_markdown(self, pdf_response: OCRResponse) -> str:
        markdowns = []
        for page in pdf_response.pages:
            image_data = {img.id: img.image_base64 for img in page.images}
            markdowns.append(self.replace_images_in_markdown(
                page.markdown, image_data))
        return "\n\n".join(markdowns)

    def process_ocr_to_structured_json(self, ocr_response: OCRResponse):
        # 1. Combine all pages into one raw markdown string
        # (Keeping your original image replacement logic if needed)
        full_markdown = ""
        for page in ocr_response.pages:
            full_markdown += page.markdown + "\n\n"

        # 2. Define the Splitter (Splits by # Title and ## Section)
        headers_to_split_on = [
            ("#", "Header_1"),
            ("##", "Header_2"),
        ]
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on)
        sections = splitter.split_text(full_markdown)

        # 3. Transform into your specific JSON Schema
        json_output = []

        for i, doc in enumerate(sections):
            metadata = doc.metadata
            content = doc.page_content

            # Get title from Header 2 (preferred) or Header 1
            raw_title = metadata.get(
                "Header_2", metadata.get("Header_1", "General"))

            # Extract Block ID (e.g., "2.1") and Clean Title (e.g., "Scope")
            id_match = re.match(r"(\d+(\.\d+)*)?\s*(.*)", raw_title)
            block_id = id_match.group(1) if id_match.group(1) else str(i+1)
            clean_title = id_match.group(3) if id_match.group(3) else raw_title

            # Create the structured row
            row = {
                "title": clean_title,
                # "level": 2 if "Header_2" in metadata else 1,
                "content": f"{raw_title}\n{content}".strip(),
                # "parent_section": block_id.split('.')[0] if '.' in block_id else block_id,
                "block_type": "obligation",  # Static default for compliance
                "keywords": self.auto_tag(content)
            }
            json_output.append(row)

        return json_output

    def auto_tag(self, text):
        """Simple keyword tagger for your requirement"""
        mapping = {"mfa": "MFA", "encrypt": "Encryption", "access": "Access"}
        return [v for k, v in mapping.items() if k in text.lower()]

    def save_structured_json(self, data, filename="structured_data.json"):
        """
        Save data to Json_files/input_data_json folder relative to this script.
        Creates folder if it doesn't exist.
        """
        # Get folder path relative to the current file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(base_dir, "Json_files", "input_data_json")
        os.makedirs(folder_path, exist_ok=True)  # create folder if missing
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Structured data saved to {file_path}")
        return file_path

    def save_structured_markdown(self, markdown_data, filename="structured_markdown.md"):
        """
        Save markdown data to markdown_files/input_data_markdown folder relative to this script.
        Creates folder if it doesn't exist.
        """
        # Get folder path relative to the current file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(
            base_dir, "markdown_files", "input_data_markdown")
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_data)  # Write raw markdown, not JSON

        print(f"Markdown saved to {file_path}")
        return file_path
