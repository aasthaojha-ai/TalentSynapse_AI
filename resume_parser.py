import pypdf

def extract_text_from_pdf(file) -> str:
    """
    Extracts text from a given PDF file object using the modern pypdf library.
    Returns the extracted text or an empty string on failure.
    """
    text = ""
    try:
        # pypdf's PdfReader is the successor to PyPDF2.PdfReader
        pdf_reader = pypdf.PdfReader(file) 
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        # Graceful error handling for Streamlit UI
        print(f"Error reading PDF: {e}")
        return "" 
    return text.strip()
