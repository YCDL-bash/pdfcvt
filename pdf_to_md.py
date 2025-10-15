import fitz  # PyMuPDF
import pdfplumber
from PIL import Image
import os
import sys
import datetime
import yaml
from pathlib import Path
import re

class PDFToMarkdownConverter:
    """
    A class to convert PDF documents to Markdown format with proper structure,
    tables, and image location markers (without extracting actual images).
    """
    
    def __init__(self, input_path, output_dir=None):
        """
        Initialize the converter with input and output paths.
        
        Args:
            input_path (str): Path to the input PDF file
            output_dir (str): Base directory for output (default: C:\\dev\\python\\pdfcvt\\output)
        """
        self.input_path = input_path
        self.base_filename = Path(input_path).stem  # 파일명 (확장자 제외)
        
        # 기본 출력 디렉토리 설정
        if output_dir is None:
            output_dir = r"C:\dev\python\pdfcvt\output"
        
        self.output_folder = os.path.join(output_dir, self.base_filename)
        self.output_path = os.path.join(self.output_folder, f"{self.base_filename}.md")
        
        self.doc = None
        self.metadata = {}
        
    def _create_output_structure(self):
        """
        Create the output folder structure.
        """
        os.makedirs(self.output_folder, exist_ok=True)
        
    def _get_pdf_metadata(self):
        """
        Extract metadata from the PDF document.
        
        Returns:
            dict: Dictionary containing PDF metadata
        """
        try:
            self.doc = fitz.open(self.input_path)
            self.metadata = {
                "title": self.doc.metadata.get("title", self.base_filename),
                "author": self.doc.metadata.get("author", "Unknown"),
                "pages": self.doc.page_count,
                "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_file": os.path.basename(self.input_path)
            }
        except Exception as e:
            raise Exception(f"Failed to read PDF metadata: {str(e)}")
    
    def _extract_text_with_structure(self, page):
        """
        Extract text from a PDF page and identify structure elements.
        
        Args:
            page (fitz.Page): PDF page object
            
        Returns:
            list: List of text elements with their formatting information
        """
        text_blocks = page.get_text("dict")["blocks"]
        elements = []
        
        for block in text_blocks:
            if "lines" in block:
                for line in block["lines"]:
                    if "spans" in line:
                        spans = line["spans"]
                        if spans:
                            # Get font size from first span
                            font_size = spans[0]["size"]
                            text = "".join([span["text"] for span in spans])
                            
                            # Skip empty text
                            if not text.strip():
                                continue
                            
                            # Determine if this is a heading based on font size
                            heading_level = self._determine_heading_level(font_size)
                            
                            elements.append({
                                "text": text,
                                "font_size": font_size,
                                "heading_level": heading_level
                            })
        
        return elements
    
    def _determine_heading_level(self, font_size):
        """
        Determine heading level based on font size.
        
        Args:
            font_size (float): Font size of the text
            
        Returns:
            int: Heading level (1-6) or 0 for regular text
        """
        # Font size thresholds for headings
        if font_size >= 24:
            return 1
        elif font_size >= 20:
            return 2
        elif font_size >= 16:
            return 3
        elif font_size >= 14:
            return 4
        elif font_size >= 12:
            return 5
        else:
            return 0  # Regular text
    
    def _extract_tables(self, page_num):
        """
        Extract tables from a PDF page using pdfplumber.
        
        Args:
            page_num (int): Page number (0-indexed)
            
        Returns:
            list: List of table data or None if no table found
        """
        try:
            with pdfplumber.open(self.input_path) as pdf:
                if page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    tables = page.extract_tables()
                    return tables if tables else None
                return None
        except Exception as e:
            # Silently handle table extraction errors
            return None
    
    def _count_images(self, page):
        """
        Count images on a PDF page without extracting them.
        
        Args:
            page (fitz.Page): PDF page object
            
        Returns:
            int: Number of images on the page
        """
        try:
            image_list = page.get_images()
            return len(image_list) if image_list else 0
        except Exception:
            return 0
    
    def _convert_table_to_markdown(self, table_data):
        """
        Convert table data to Markdown format.
        
        Args:
            table_data (list): Table data from pdfplumber
            
        Returns:
            str: Markdown formatted table
        """
        if not table_data or len(table_data) == 0:
            return ""
        
        markdown_table = []
        
        for i, row in enumerate(table_data):
            # Clean cells - handle None values and strip whitespace
            clean_row = []
            for cell in row:
                if cell is None:
                    clean_row.append("")
                else:
                    # Remove extra whitespace and newlines
                    cell_text = str(cell).replace('\n', ' ').strip()
                    clean_row.append(cell_text)
            
            if i == 0:
                # Header row
                header = "| " + " | ".join(clean_row) + " |"
                separator = "| " + " | ".join(["---" for _ in clean_row]) + " |"
                markdown_table.append(header)
                markdown_table.append(separator)
            else:
                # Data rows
                row_data = "| " + " | ".join(clean_row) + " |"
                markdown_table.append(row_data)
        
        return "\n".join(markdown_table)
    
    def _is_scanned_pdf(self):
        """
        Check if the PDF is a scanned document (no text layers).
        
        Returns:
            bool: True if PDF appears to be scanned
        """
        try:
            if self.doc.page_count == 0:
                return False
                
            # Check first few pages
            pages_to_check = min(3, self.doc.page_count)
            total_text = ""
            
            for i in range(pages_to_check):
                page = self.doc[i]
                text = page.get_text()
                total_text += text
            
            # If very little text found, likely scanned
            return len(total_text.strip()) < 100
        except Exception:
            return False
    
    def convert(self):
        """
        Main conversion method to convert PDF to Markdown.
        
        Returns:
            str: Markdown content as string
        """
        try:
            # Create output folder structure
            self._create_output_structure()
            
            # Get PDF metadata
            self._get_pdf_metadata()
            
            # Check if PDF is scanned
            if self._is_scanned_pdf():
                print("⚠️  Warning: This appears to be a scanned PDF. OCR processing may be needed for better results.")
            
            # Create markdown content
            markdown_content = []
            
            # Add YAML frontmatter
            frontmatter = {
                "title": self.metadata["title"],
                "author": self.metadata["author"],
                "pages": self.metadata["pages"],
                "created": self.metadata["created"],
                "source_file": self.metadata["source_file"]
            }
            markdown_content.append("---")
            markdown_content.append(yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True))
            markdown_content.append("---")
            markdown_content.append("")
            
            # Statistics
            total_images = 0
            total_tables = 0
            
            # Process each page
            print(f"📄 Processing {self.doc.page_count} pages...")
            
            for page_num in range(self.doc.page_count):
                page = self.doc[page_num]
                
                # Progress indicator
                if (page_num + 1) % 10 == 0 or page_num == 0:
                    print(f"   Processed {page_num + 1}/{self.doc.page_count} pages...")
                
                # Add page header
                markdown_content.append(f"## Page {page_num + 1}")
                markdown_content.append("")
                
                # Extract text with structure
                elements = self._extract_text_with_structure(page)
                
                # Process text elements
                for element in elements:
                    text = element["text"].strip()
                    if text:
                        if element["heading_level"] > 0:
                            # Convert heading level to Markdown format
                            heading = "#" * (element["heading_level"] + 2)  # +2 because Page is h2
                            markdown_content.append(f"{heading} {text}")
                        else:
                            markdown_content.append(text)
                        markdown_content.append("")
                
                # Extract and process tables
                tables = self._extract_tables(page_num)
                if tables:
                    total_tables += len(tables)
                    for table in tables:
                        if table:
                            table_md = self._convert_table_to_markdown(table)
                            if table_md:
                                markdown_content.append(table_md)
                                markdown_content.append("")
                
                # Count and mark images (without extracting)
                image_count = self._count_images(page)
                if image_count > 0:
                    total_images += image_count
                    markdown_content.append(f"*[{image_count} image(s) on this page]*")
                    markdown_content.append("")
                
                # Add page separator
                if page_num < self.doc.page_count - 1:
                    markdown_content.append("---")
                    markdown_content.append("")
            
            # Clean up multiple empty lines
            cleaned_content = []
            prev_empty = False
            for line in markdown_content:
                if line == "":
                    if not prev_empty:
                        cleaned_content.append(line)
                    prev_empty = True
                else:
                    cleaned_content.append(line)
                    prev_empty = False
            
            # Clean up empty lines at the end
            while cleaned_content and cleaned_content[-1] == "":
                cleaned_content.pop()
            
            # Store statistics
            self.total_images = total_images
            self.total_tables = total_tables
            
            return "\n".join(cleaned_content)
            
        except Exception as e:
            raise Exception(f"Conversion failed: {str(e)}")
        finally:
            # Clean up
            if self.doc:
                self.doc.close()
    
    def save(self, content):
        """
        Save the converted Markdown content to file.
        
        Args:
            content (str): Markdown content to save
        """
        try:
            with open(self.output_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"Failed to save output file: {str(e)}")
    
    def get_output_info(self):
        """
        Get information about the output structure.
        
        Returns:
            dict: Information about output paths
        """
        return {
            "output_folder": self.output_folder,
            "markdown_file": self.output_path
        }


def convert_single_pdf(pdf_path, output_dir=None):
    """
    Convert a single PDF file to Markdown.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Output directory
        
    Returns:
        dict: Conversion result with statistics
    """
    try:
        converter = PDFToMarkdownConverter(pdf_path, output_dir)
        content = converter.convert()
        converter.save(content)
        
        return {
            "success": True,
            "filename": os.path.basename(pdf_path),
            "output": converter.get_output_info()["markdown_file"],
            "tables": converter.total_tables,
            "images": converter.total_images,
            "lines": len(content.split('\n')),
            "size": len(content)
        }
    except Exception as e:
        return {
            "success": False,
            "filename": os.path.basename(pdf_path),
            "error": str(e)
        }


def convert_batch(source_dir=None, output_dir=None):
    """
    Convert all PDF files in source directory.
    
    Args:
        source_dir (str): Source directory containing PDF files
        output_dir (str): Output directory for converted files
    """
    # 기본 경로 설정
    if source_dir is None:
        source_dir = r"C:\dev\python\pdfcvt\source"
    if output_dir is None:
        output_dir = r"C:\dev\python\pdfcvt\output"
    
    # 소스 디렉토리 확인
    if not os.path.exists(source_dir):
        print(f"❌ Error: Source directory '{source_dir}' does not exist.")
        print(f"   Creating directory...")
        os.makedirs(source_dir, exist_ok=True)
        print(f"✅ Created: {source_dir}")
        print(f"   Please place PDF files in this directory and run again.")
        return
    
    # PDF 파일 검색
    pdf_files = list(Path(source_dir).glob("*.pdf"))
    
    if not pdf_files:
        print(f"⚠️  No PDF files found in '{source_dir}'")
        print(f"   Please place PDF files in this directory.")
        return
    
    print(f"📁 Source: {source_dir}")
    print(f"📁 Output: {output_dir}")
    print(f"📄 Found {len(pdf_files)} PDF file(s)")
    print()
    
    results = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"{'='*60}")
        print(f"[{i}/{len(pdf_files)}] Converting: {pdf_file.name}")
        print(f"{'='*60}")
        
        result = convert_single_pdf(str(pdf_file), output_dir)
        results.append(result)
        
        if result["success"]:
            print(f"✅ Success!")
            print(f"   Output: {result['output']}")
            print(f"   Tables: {result['tables']}, Images: {result['images']}")
        else:
            print(f"❌ Failed: {result['error']}")
        
        print()
    
    # 최종 요약
    print(f"{'='*60}")
    print("📊 Conversion Summary")
    print(f"{'='*60}")
    
    success_count = sum(1 for r in results if r["success"])
    fail_count = len(results) - success_count
    
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")
    
    if success_count > 0:
        total_tables = sum(r.get("tables", 0) for r in results if r["success"])
        total_images = sum(r.get("images", 0) for r in results if r["success"])
        print(f"📊 Total tables: {total_tables}")
        print(f"🖼️  Total images detected: {total_images}")
    
    print()
    print(f"All converted files are in: {output_dir}")


def main():
    """
    Main function to run the converter from command line.
    """
    # 기본 경로
    DEFAULT_SOURCE = r"C:\dev\python\pdfcvt\source"
    DEFAULT_OUTPUT = r"C:\dev\python\pdfcvt\output"
    
    # 사용법 출력
    def print_usage():
        print("PDF to Markdown Converter")
        print()
        print("Usage:")
        print("  python pdf_to_md.py                          # Convert all PDFs in source folder")
        print("  python pdf_to_md.py <pdf_file>               # Convert single PDF")
        print("  python pdf_to_md.py <pdf_file> <output_dir>  # Convert with custom output")
        print()
        print("Default paths:")
        print(f"  Source:  {DEFAULT_SOURCE}")
        print(f"  Output:  {DEFAULT_OUTPUT}")
        print()
        print("Examples:")
        print("  python pdf_to_md.py")
        print("  python pdf_to_md.py document.pdf")
        print("  python pdf_to_md.py document.pdf C:\\custom\\output")
    
    # 인자 처리
    if len(sys.argv) == 1:
        # 인자 없음 - 배치 변환 (기본 경로)
        print("🔄 Batch conversion mode (default paths)")
        print()
        convert_batch(DEFAULT_SOURCE, DEFAULT_OUTPUT)
        
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        
        if arg in ["-h", "--help", "help"]:
            print_usage()
            return
        
        # PDF 파일 경로인지 확인
        if arg.endswith('.pdf'):
            if not os.path.exists(arg):
                print(f"❌ Error: File '{arg}' does not exist.")
                sys.exit(1)
            
            print(f"🔄 Converting single file: {arg}")
            print()
            result = convert_single_pdf(arg, DEFAULT_OUTPUT)
            
            if result["success"]:
                print(f"✅ Successfully converted!")
                print(f"📂 Output: {result['output']}")
                print(f"📊 Statistics:")
                print(f"   - Lines: {result['lines']}")
                print(f"   - Size: {result['size']:,} characters")
                print(f"   - Tables: {result['tables']}")
                print(f"   - Images: {result['images']}")
            else:
                print(f"❌ Error: {result['error']}")
                sys.exit(1)
        else:
            print(f"❌ Error: File must be a PDF (.pdf extension)")
            sys.exit(1)
            
    elif len(sys.argv) == 3:
        # 단일 PDF + 출력 디렉토리
        input_path = sys.argv[1]
        output_dir = sys.argv[2]
        
        if not input_path.endswith('.pdf'):
            print(f"❌ Error: Input file must be a PDF (.pdf extension)")
            sys.exit(1)
        
        if not os.path.exists(input_path):
            print(f"❌ Error: File '{input_path}' does not exist.")
            sys.exit(1)
        
        print(f"🔄 Converting: {input_path}")
        print(f"📁 Output: {output_dir}")
        print()
        
        result = convert_single_pdf(input_path, output_dir)
        
        if result["success"]:
            print(f"✅ Successfully converted!")
            print(f"📂 Output: {result['output']}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    else:
        print("❌ Error: Too many arguments")
        print()
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
