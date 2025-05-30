import streamlit as st
import PyPDF2
import io
import google.generativeai as genai
import os
from typing import Optional

# --- API Key Configuration ---
# Configure Google Generative AI with your API key
# It is highly recommended to set your API key as an environment variable (e.g., GOOGLE_API_KEY)
# For deployment on Streamlit Cloud, set this as a 'secret' named GOOGLE_API_KEY
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# --- Helper Functions ---
def extract_text_from_pdf(uploaded_file: io.BytesIO) -> Optional[str]:
    """
    Extracts text content from an uploaded PDF file-like object.
    Returns the concatenated text or None if an error occurs or no text is found.
    """
    if uploaded_file is None:
        return None
    try:
        # PyPDF2.PdfReader expects a file-like object
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        if len(pdf_reader.pages) == 0:
            st.warning("The uploaded PDF contains no pages or is empty.")
            return None

        extracted_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            # Append page text, handling cases where extract_text might return None or empty string
            extracted_text += page_text if page_text else ""

        if not extracted_text.strip():
            st.warning("No readable text could be extracted from the PDF. This often happens with scanned documents (images of text) or PDFs with complex layouts.")
            return None
        return extracted_text
    except PyPDF2.errors.PdfReadError as e:
        st.error(f"Error reading PDF file (PdfReadError): {e}. The PDF might be corrupted, encrypted, or malformed.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while processing the PDF: {e}")
        return None

def summarize_change_request(text_content: str) -> str:
    """
    Summarizes the provided text content using a generative AI model.
    The summary follows a specific structured format for change requests.
    """
    if not text_content or text_content.strip() == "":
        return "No substantial text content provided for summarization."

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
        # Using 'gemini-1.5-flash' as it's generally more available and efficient.
        # If 'gemini-pro' was desired and not found, it might be a region-specific issue
        # or require enabling certain APIs in your Google Cloud project.
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)

        # Check if the response or its text content is valid
        if response and response.text:
            return response.text.strip()
        else:
            # Attempt to get more details if response is not as expected
            error_details = "AI model returned an empty or invalid response."
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                # This feedback can indicate content safety issues, etc.
                error_details += f" Prompt feedback: {response.prompt_feedback}"
            if hasattr(response, 'candidates') and not response.candidates:
                error_details += " No candidates generated."
            st.error(f"AI summarization failed: {error_details}")
            return "Could not generate summary. The AI model did not return a valid response."

    except Exception as e:
        st.error(f"Error generating summary with AI: {e}. This might be due to an invalid API key, network issues, model availability, or rate limits.")
        return "Could not generate summary. Please ensure your Google API key is valid and configured correctly, and check your network connection and model availability."

# --- Streamlit App UI Layout ---
st.set_page_config(
    page_title="AI-Powered Change Request Summarizer",
    layout="centered",
    initial_sidebar_state="auto"
    # icon="📄" # You can add an emoji as an icon
)

st.title("📄 AI-Powered Change Request Summarizer")
st.markdown("Upload your change request PDF, and I'll summarize its key details for you using Google's Generative AI.")
st.markdown("---")

st.subheader("💡 Important Setup Notes:")
st.markdown("""
1.  **Dependencies:** Ensure you have installed the required Python libraries. You'll need a `requirements.txt` file in your project root with:
    ```
    streamlit
    PyPDF2
    google-generativeai
    ```
    Install them locally using: `pip install -r requirements.txt`
2.  **Google API Key:** Obtain a `GOOGLE_API_KEY` from [Google AI Studio](https://aistudio.google.com/app/apikey).
    * **Local Run:** Set it as an environment variable before running the app (e.g., `export GOOGLE_API_KEY="YOUR_API_KEY"` on Linux/macOS, or `set GOOGLE_API_KEY="YOUR_API_KEY"` on Windows).
    * **Streamlit Cloud Deployment:** Add it as a "secret" named `GOOGLE_API_KEY` in your app's settings on Streamlit Cloud.
""")
st.markdown("---")

# File uploader widget for PDF files
st.subheader("Upload Your Change Request PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF file uploaded successfully! Now processing...")

    # Use a BytesIO object to read the file content, allowing PyPDF2 to process it
    file_content = io.BytesIO(uploaded_file.read())

    # Section to preview the extracted text (collapsible for cleaner UI)
    with st.expander("📖 Preview Extracted Text (First 1000 Chars)"):
        with st.spinner("Extracting text from PDF..."):
            pdf_text = extract_text_from_pdf(file_content)

        if pdf_text:
            # Display a truncated version of the extracted text
            st.code(pdf_text[:1000] + "..." if len(pdf_text) > 1000 else pdf_text)
            if len(pdf_text) > 1000:
                st.info(f"Only showing the first 1000 characters. Total characters extracted: {len(pdf_text)}")
        else:
            st.warning("No readable text could be extracted from this PDF. Please ensure it's a text-based PDF and not a scanned image.")

    # Only show the summarize button if text was successfully extracted and is substantial
    if pdf_text and pdf_text.strip() != "":
        st.markdown("---")
        st.subheader("Summarize Your Change Request")
        if st.button("🚀 Generate AI Summary", help="Click to analyze the PDF content and generate the summary in the specified format."):
            with st.spinner("Analyzing and summarizing with AI... This may take a moment."):
                summary = summarize_change_request(pdf_text)
                st.subheader("✅ Summarized Change Request:")
                st.info(summary)
    else:
        st.warning("Cannot generate summary: No text found in the PDF or extraction failed. Please upload a valid, text-searchable PDF.")
else:
    # Initial message when no file is uploaded
    st.info("Please upload a PDF file above to begin the summarization process.")

st.markdown("---")
st.markdown("""
<small>
Built with ❤️ using Streamlit, PyPDF2, and Google Generative AI.
</small>
""", unsafe_allow_html=True)
