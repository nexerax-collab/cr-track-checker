import streamlit as st
import PyPDF2
import io
import google.generativeai as genai
import os

# Configure Google Generative AI with your API key
# It is recommended to set your API key as an environment variable (e.g., GOOGLE_API_KEY)
# For Streamlit Cloud, set this as a 'secret' named GOOGLE_API_KEY
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text content from an uploaded PDF file.
    Returns the concatenated text or None if an error occurs.
    """
    if uploaded_file is None:
        return None
    try:
        # Use BytesIO to ensure PyPDF2 can read the uploaded file content
        pdf_file = io.BytesIO(uploaded_file.read())
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        if len(pdf_reader.pages) == 0:
            st.warning("The uploaded PDF contains no pages or is empty.")
            return None

        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            # Append page text, handling cases where extract_text might return None or empty string
            text += page_text if page_text else ""

        if not text.strip():
            st.warning("No readable text could be extracted from the PDF. This might happen with scanned documents (images of text).")
            return None
        return text
    except PyPDF2.errors.PdfReadError as e:
        st.error(f"Error reading PDF file (PdfReadError): {e}. The PDF might be corrupted, encrypted, or malformed.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while processing the PDF: {e}")
        return None

def summarize_change_request(text_content):
    """
    Summarizes the provided text content using a generative AI model.
    The summary follows a specific format for change requests.
    """
    if not text_content or text_content.strip() == "":
        return "No substantial text content to summarize."

    # Define the prompt for the AI model to guide summarization
    prompt = f"""
    Analyze the following change request text and extract the key information to fit the following format:

    "This change request is due to [Problem], reported by [Reporter] from [Department] on [Date]. It affects [Affected Component, Items, Software(s)]."

    If a piece of information is not explicitly found in the text, use "N/A" for that specific field.
    Ensure the output strictly adheres to the requested format and is concise.

    Change Request Text:
    ---
    {text_content}
    ---

    Extracted Summary:
    """

    try:
        # Use gemini-pro for text generation
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return "Could not generate summary. Please ensure your Google API key is correctly set and try again."

# --- Streamlit App UI Layout ---
st.set_page_config(
    page_title="Change Request Summarizer",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("📄 Change Request Summarizer")
st.markdown("Upload your change request PDF, and I'll summarize it for you using AI!")
st.markdown("---")
st.markdown("**Before you start:**")
st.markdown("1.  Make sure you have installed the required libraries: `pip install streamlit PyPDF2 google-generativeai` (check your `requirements.txt` file).")
st.markdown("2.  Ensure your `GOOGLE_API_KEY` environment variable (or Streamlit secret) is correctly set.")
st.markdown("---")

# File uploader widget for PDF files
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF file uploaded successfully!")

    # Section to preview the extracted text (collapsible)
    with st.expander("Preview Extracted Text"):
        with st.spinner("Extracting text from PDF..."):
            pdf_text = extract_text_from_pdf(uploaded_file)

        if pdf_text:
            # Display a truncated version of the extracted text
            st.code(pdf_text[:1000] + "..." if len(pdf_text) > 1000 else pdf_text)
            if len(pdf_text) > 1000:
                st.info(f"Showing first 1000 characters. Total characters: {len(pdf_text)}")
        else:
            st.warning("No text could be extracted from the PDF. Please check the file's content or try another PDF.")

    # Only show the summarize button if text was successfully extracted
    if pdf_text and pdf_text.strip() != "":
        if st.button("Summarize Change Request", help="Click to analyze the PDF content and generate the summary."):
            with st.spinner("Summarizing change request using AI... This may take a moment."):
                summary = summarize_change_request(pdf_text)
                st.subheader("Summarized Change Request:")
                st.info(summary)
    elif uploaded_file is not None:
        # If file was uploaded but no text was found
        st.warning("The uploaded PDF appears to have no readable text content for summarization.")
else:
    # Initial message when no file is uploaded
    st.info("Please upload a PDF file to get started.")
