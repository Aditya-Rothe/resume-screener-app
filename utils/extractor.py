import PyPDF2
import io


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract raw text from an uploaded PDF file.
    Returns cleaned string of all text content.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"


def extract_text_from_input(text_input: str) -> str:
    """
    Clean and return manually entered text.
    """
    return text_input.strip()