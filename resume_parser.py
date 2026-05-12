import PyPDF2

def extract_text_from_pdf(file) -> str:
    """
    Extracts text from a given PDF file object.
    Returns the extracted text or an empty string on failure.
    """
    text = ""
    try:
        # strict=False allows PyPDF2 to be more forgiving with malformed PDFs
        pdf_reader = PyPDF2.PdfReader(file, strict=False) 
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        # Graceful error handling instead of crashing the app
        print(f"Error reading PDF: {e}")
        return "" 
    return text.strip()
