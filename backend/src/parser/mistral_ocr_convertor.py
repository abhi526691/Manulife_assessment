import os
import json
from mistralai import Mistral, DocumentURLChunk

from src.parser.pdf_parser import contractParser


class textExtractor(contractParser):
    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path
        self.client = Mistral(api_key=self.api_key)

    def get_stored_response(self):
        """
        Reads the markdown and JSON content from the local storage paths.
        """
        json_path = "D:\\Assessment\\ManulifeAssessment\\Manulife_assessment\\backend\\src\\parser\\Json_files\\input_data_json\\structured_output.json"
        md_path = "D:\\Assessment\\ManulifeAssessment\\Manulife_assessment\\backend\\src\\parser\\markdown_files\\input_data_markdown\\extracted_markdown.md"

        # Read JSON file
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                structured_json = json.load(f)
        except FileNotFoundError:
            structured_json = {"error": f"File not found at {json_path}"}

        # Read Markdown file
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                markdown_text = f.read()
        except FileNotFoundError:
            markdown_text = f"Error: File not found at {md_path}"

        return {
            "markdown": markdown_text,
            "structured_json": structured_json
        }

    def ocr_response_file(self, pdf_file):
        """
        Handles both Streamlit UploadedFile and local file paths
        """
        # Determine filename and bytes content
        if hasattr(pdf_file, "read"):  # Streamlit UploadedFile
            file_name = pdf_file.name
            file_bytes = pdf_file.read()
        else:  # Local file path
            file_name = os.path.basename(pdf_file)
            with open(pdf_file, "rb") as f:
                file_bytes = f.read()

        # Upload file to Mistral API
        uploaded_file = self.client.files.upload(
            file={"file_name": file_name, "content": file_bytes},
            purpose="ocr",
        )

        # Get signed URL
        signed_url = self.client.files.get_signed_url(
            file_id=uploaded_file.id, expiry=1
        )

        # Process OCR
        pdf_response = self.client.ocr.process(
            document=DocumentURLChunk(document_url=signed_url.url),
            model="mistral-ocr-latest",
            include_image_base64=True
        )
        markdown_text = self.get_combined_markdown(pdf_response)
        self.save_structured_markdown(markdown_text, "extracted_markdown.md")

        structured_json = self.process_ocr_to_structured_json(pdf_response)
        self.save_structured_json(structured_json, "structured_output.json")

        return {
            "markdown": markdown_text,
            "structured_json": structured_json
        }
