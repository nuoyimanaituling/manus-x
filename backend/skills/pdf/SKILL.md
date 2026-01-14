---
name: pdf
description: Process PDF files - extract text, read content, create PDFs, merge or split documents. Use when user asks to read, create, or manipulate PDF files.
---

# PDF Processing Skill

You now have expertise in PDF file processing. Follow these instructions based on the task.

## Reading PDFs

### Using pdftotext (Recommended for text extraction)

```bash
# Install if needed
apt-get install -y poppler-utils

# Extract text from PDF
pdftotext input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt

# Extract with layout preservation
pdftotext -layout input.pdf output.txt
```

### Using Python PyMuPDF

```python
import fitz  # PyMuPDF

# Open and read PDF
doc = fitz.open("input.pdf")
for page_num, page in enumerate(doc):
    text = page.get_text()
    print(f"--- Page {page_num + 1} ---")
    print(text)

# Extract text from specific pages
page = doc[0]  # First page (0-indexed)
text = page.get_text()
```

### Using pdfplumber (for tables)

```python
import pdfplumber

with pdfplumber.open("input.pdf") as pdf:
    for page in pdf.pages:
        # Extract text
        text = page.extract_text()
        print(text)

        # Extract tables
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
```

## Creating PDFs

### Using Python reportlab

```python
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Create a simple PDF
c = canvas.Canvas("output.pdf", pagesize=letter)
c.setFont("Helvetica", 12)
c.drawString(1*inch, 10*inch, "Hello World")
c.save()
```

### Using Pandoc (from Markdown)

```bash
# Install pandoc if needed
apt-get install -y pandoc texlive-xetex

# Convert Markdown to PDF
pandoc input.md -o output.pdf

# With custom template
pandoc input.md -o output.pdf --template=template.tex
```

### Using weasyprint (from HTML)

```python
from weasyprint import HTML

# From HTML string
html_content = "<h1>Hello World</h1><p>This is a PDF.</p>"
HTML(string=html_content).write_pdf("output.pdf")

# From HTML file
HTML("input.html").write_pdf("output.pdf")
```

## Merging PDFs

```python
import fitz

result = fitz.open()
for pdf_file in ["file1.pdf", "file2.pdf", "file3.pdf"]:
    doc = fitz.open(pdf_file)
    result.insert_pdf(doc)
result.save("merged.pdf")
```

## Splitting PDFs

```python
import fitz

doc = fitz.open("input.pdf")

# Extract specific pages
output = fitz.open()
output.insert_pdf(doc, from_page=0, to_page=4)  # Pages 1-5
output.save("pages_1_to_5.pdf")

# Split into individual pages
for i, page in enumerate(doc):
    single_page = fitz.open()
    single_page.insert_pdf(doc, from_page=i, to_page=i)
    single_page.save(f"page_{i+1}.pdf")
```

## Adding Watermarks

```python
import fitz

doc = fitz.open("input.pdf")
for page in doc:
    # Add text watermark
    page.insert_text(
        (100, 100),
        "CONFIDENTIAL",
        fontsize=50,
        color=(0.8, 0.8, 0.8),
        rotate=45
    )
doc.save("watermarked.pdf")
```

## Key Libraries

| Library | Use Case | Install |
|---------|----------|---------|
| PyMuPDF (fitz) | Read, write, merge, split | `pip install pymupdf` |
| pdftotext | CLI text extraction | `apt install poppler-utils` |
| pdfplumber | Table extraction | `pip install pdfplumber` |
| reportlab | Create PDFs programmatically | `pip install reportlab` |
| weasyprint | HTML to PDF | `pip install weasyprint` |
| pdf2image | PDF to images | `pip install pdf2image` |
| PyPDF2 | Merge, split, rotate | `pip install pypdf2` |

## Best Practices

1. Always check if required libraries are installed before use
2. For large PDFs, process pages in batches to manage memory
3. When extracting text, verify encoding (UTF-8 is recommended)
4. For table extraction, pdfplumber is more reliable than PyMuPDF
5. Close PDF documents after processing to free resources
