import streamlit as st
import os
import zipfile
import io
from datetime import datetime

# --- Configuration ---
# Required documents and where to save them
REQUIRED_DOCS = {
    # Project Management
    "ProjectRiskAnalysis.pdc": "output_folder/ProjectManagement/ProjectRiskAnalysis/",
    "ExternalReleaseNotes.pdc": "output_folder/ProjectManagement/ExternalReleaseNotes/",
    "ReleaseNotesKPIs.pdc": "output_folder/ProjectManagement/ReleaseNotesKPIs/",
    "ComplianceEvidence_UNECE_FuSi_EE.pdc": "output_folder/ProjectManagement/ComplianceEvidence_UNECE_FuSi_EE/",
    "ProjectHandbook.pdc": "output_folder/ProjectManagement/ProjectHandbook/",
    "FOSSDocumentation.pdc": "output_folder/ProjectManagement/FOSSDocumentation/",
    "ProofOfBsMRelevance.pdc": "output_folder/ProjectManagement/ProofOfBsMRelevance/",

    # System Requirements
    "SystemRequirementsAnalysis.pdc": "output_folder/Requirements/SystemRequirementsAnalysis/",

    # Software Requirements
    "SoftwareRequirementsBaselineID.pdc": "output_folder/Requirements/SoftwareRequirementsBaselineID/",
    "SoftwareRequirementsExport_DOORS.pdc": "output_folder/Requirements/SoftwareRequirementsExport_DOORS/",
    "SoftwareRequirementsDeviationReport.pdc": "output_folder/Requirements/SoftwareRequirementsDeviationReport/",

    # Architecture
    "ArchitectureDocument.pdc": "output_folder/Architecture/ArchitectureDocument/",
    "ArchitectureBaselineID.pdc": "output_folder/Architecture/ArchitectureBaselineID/",

    # Testing & Validation
    "TestStatusReport.pdc": "output_folder/TestingValidation/TestStatusReport/",
    "TestReport.pdc": "output_folder/TestingValidation/TestReport/",
    "SWE4_Specification.pdc": "output_folder/TestingValidation/SWE4_Specification/",
    "SWE5_Specification.pdc": "output_folder/TestingValidation/SWE5_Specification/",
    "SWE6_Specification.pdc": "output_folder/TestingValidation/SWE6_Specification/",
    "TestRiskAnalysis.pdc": "output_folder/TestingValidation/TestRiskAnalysis/",

    # Issue, Error & Defect Management
    "ComprehensiveIssueList.pdc": "output_folder/IssueDefectManagement/ComprehensiveIssueList/",
    "KnownErrorList.pdc": "output_folder/IssueDefectManagement/KnownErrorList/",
    "OpenDocumentationDefects.pdc": "output_folder/IssueDefectManagement/OpenDocumentationDefects/",
    "OpenAcceptedProductDefects.pdc": "output_folder/IssueDefectManagement/OpenAcceptedProductDefects/",

    # Security
    "SecurityRequirementsBaselineID.pdc": "output_folder/Security/SecurityRequirementsBaselineID/",
    "SecurityRequirementsExport_DOORS.pdc": "output_folder/Security/SecurityRequirementsExport_DOORS/",
    "SecurityComplianceEvidence.pdc": "output_folder/Security/SecurityComplianceEvidence/",

    # Configuration Management
    "ListOfToolsUsed.pdc": "output_folder/ConfigurationManagement/ListOfToolsUsed/",
    "KM_StatusReport.pdc": "output_folder/ConfigurationManagement/KM_StatusReport/",

    # Quality Assurance
    "QualityAssessmentReport.pdc": "output_folder/QualityAssurance/QualityAssessmentReport/",
    "TRS_FinalReport.pdc": "output_folder/QualityAssurance/TRS_FinalReport/",
    "KGAS_FormulaQ_Confirmation.pdc": "output_folder/QualityAssurance/KGAS_FormulaQ_Confirmation/",
    "KGAS_DataExport.pdc": "output_folder/QualityAssurance/KGAS_DataExport/",
}

# Renaming logic (e.g., prefixing with a project name)
RENAMING_MAP = {
    # Project Management
    "ProjectRiskAnalysis.pdc": "ProjectX_ProjectRiskAnalysis.pdc",
    "ExternalReleaseNotes.pdc": "ProjectX_ExternalReleaseNotes.pdc",
    "ReleaseNotesKPIs.pdc": "ProjectX_ReleaseNotesKPIs.pdc",
    "ComplianceEvidence_UNECE_FuSi_EE.pdc": "ProjectX_ComplianceEvidence_UNECE_FuSi_EE.pdc",
    "ProjectHandbook.pdc": "ProjectX_ProjectHandbook.pdc",
    "FOSSDocumentation.pdc": "ProjectX_FOSSDocumentation.pdc",
    "ProofOfBsMRelevance.pdc": "ProjectX_ProofOfBsMRelevance.pdc",

    # System Requirements
    "SystemRequirementsAnalysis.pdc": "ProjectX_SystemRequirementsAnalysis.pdc",

    # Software Requirements
    "SoftwareRequirementsBaselineID.pdc": "ProjectX_SoftwareRequirementsBaselineID.pdc",
    "SoftwareRequirementsExport_DOORS.pdc": "ProjectX_SoftwareRequirementsExport_DOORS.pdc",
    "SoftwareRequirementsDeviationReport.pdc": "ProjectX_SoftwareRequirementsDeviationReport.pdc",

    # Architecture
    "ArchitectureDocument.pdc": "ProjectX_ArchitectureDocument.pdc",
    "ArchitectureBaselineID.pdc": "ProjectX_ArchitectureBaselineID.pdc",

    # Testing & Validation
    "TestStatusReport.pdc": "ProjectX_TestStatusReport.pdc",
    "TestReport.pdc": "ProjectX_TestReport.pdc",
    "SWE4_Specification.pdc": "ProjectX_SWE4_Specification.pdc",
    "SWE5_Specification.pdc": "ProjectX_SWE5_Specification.pdc",
    "SWE6_Specification.pdc": "ProjectX_SWE6_Specification.pdc",
    "TestRiskAnalysis.pdc": "ProjectX_TestRiskAnalysis.pdc",

    # Issue, Error & Defect Management
    "ComprehensiveIssueList.pdc": "ProjectX_ComprehensiveIssueList.pdc",
    "KnownErrorList.pdc": "ProjectX_KnownErrorList.pdc",
    "OpenDocumentationDefects.pdc": "ProjectX_OpenDocumentationDefects.pdc",
    "OpenAcceptedProductDefects.pdc": "ProjectX_OpenAcceptedProductDefects.pdc",

    # Security
    "SecurityRequirementsBaselineID.pdc": "ProjectX_SecurityRequirementsBaselineID.pdc",
    "SecurityRequirementsExport_DOORS.pdc": "ProjectX_SecurityRequirementsExport_DOORS.pdc",
    "SecurityComplianceEvidence.pdc": "ProjectX_SecurityComplianceEvidence.pdc",

    # Configuration Management
    "ListOfToolsUsed.pdc": "ProjectX_ListOfToolsUsed.pdc",
    "KM_StatusReport.pdc": "ProjectX_KM_StatusReport.pdc",

    # Quality Assurance
    "QualityAssessmentReport.pdc": "ProjectX_QualityAssessmentReport.pdc",
    "TRS_FinalReport.pdc": "ProjectX_TRS_FinalReport.pdc",
    "KGAS_FormulaQ_Confirmation.pdc": "ProjectX_KGAS_FormulaQ_Confirmation.pdc",
    "KGAS_DataExport.pdc": "ProjectX_KGAS_DataExport.pdc",
}

LOG_FILE = "uploads.log"

# --- Streamlit Page Setup ---
st.set_page_config(page_title="PDC Upload Tool", layout="wide") # Changed to wide for longer checklist
st.title("📂 PDC File Upload Tool")
st.write("Bitte lade die benötigten PDC-Dateien hoch – einzeln oder als ZIP. Dateien werden automatisch umbenannt und gespeichert.")

# --- Initialize Session State ---
# Stores the original names of successfully uploaded required documents for the current session
if 'uploaded_docs_session' not in st.session_state:
    st.session_state.uploaded_docs_session = []

# --- Core Functions ---
def save_and_log_file(original_name, content):
    """
    Saves the file if it's a required document, renames it, and logs the action.
    Returns the original_name if successful and required, otherwise None.
    """
    if original_name in REQUIRED_DOCS:
        new_name = RENAMING_MAP.get(original_name, original_name) # Fallback to original_name if not in map
        target_dir = REQUIRED_DOCS[original_name]
        
        try:
            os.makedirs(target_dir, exist_ok=True)
            path = os.path.join(target_dir, new_name)

            with open(path, "wb") as f:
                f.write(content)

            log_message = f"{datetime.now().isoformat()} - Uploaded: '{original_name}' -> Saved as: '{new_name}' in '{target_dir}'"
            with open(LOG_FILE, "a", encoding="utf-8") as log_file_append: # Added encoding
                log_file_append.write(log_message + "\n")
            
            st.success(f"✅ '{original_name}' erfolgreich als '{new_name}' in '{target_dir}' gespeichert.")
            return original_name  # Return the original name for checklist tracking
        except Exception as e:
            st.error(f"❌ Fehler beim Speichern von '{original_name}': {e}")
            return None
    else:
        st.warning(f"⚠️ Datei '{original_name}' ist nicht in der Liste der benötigten Dokumente und wurde nicht gespeichert.")
        return None

# --- UI for File Uploads ---
st.subheader("1. Dateien hochladen")

# Option 1: Upload PDC files directly
# If you expect various file types, adjust the `type` parameter below and also the filenames in REQUIRED_DOCS.
# e.g., type=["pdc", "pdf", "xlsx", "docx"]
uploaded_files = st.file_uploader(
    "🔹 Einzelne PDC-Dateien auswählen (oder andere, falls konfiguriert)", 
    type="pdc",  # Currently configured for .pdc files as per REQUIRED_DOCS
    accept_multiple_files=True, 
    key="individual_uploader"
)

if uploaded_files:
    st.write("---")
    st.markdown("##### Ergebnisse des Einzel-Uploads:")
    for uploaded_file in uploaded_files:
        original_filename = uploaded_file.name
        file_content = uploaded_file.getvalue()
        
        processed_doc_name = save_and_log_file(original_filename, file_content)
        if processed_doc_name and processed_doc_name not in st.session_state.uploaded_docs_session:
            st.session_state.uploaded_docs_session.append(processed_doc_name)
    st.write("---")


# Option 2: Upload zip archive
uploaded_zip = st.file_uploader(
    "🔹 Oder eine ZIP-Datei mit PDC-Dateien hochladen (oder andere, falls konfiguriert)", 
    type="zip", 
    key="zip_uploader"
)

if uploaded_zip:
    st.write("---")
    st.markdown("##### Ergebnisse des ZIP-Uploads:")
    try:
        with zipfile.ZipFile(io.BytesIO(uploaded_zip.getvalue())) as z:
            for file_info in z.infolist():
                if file_info.is_dir() or file_info.filename.startswith('__MACOSX/'):
                    continue
                
                original_filename = os.path.basename(file_info.filename)
                if not original_filename:
                    continue

                # Ensure the filename from ZIP matches one of the keys in REQUIRED_DOCS (which currently end in .pdc)
                if original_filename in REQUIRED_DOCS: # Check if the filename is one we're looking for
                    file_content = z.read(file_info.filename)
                    processed_doc_name = save_and_log_file(original_filename, file_content)
                    if processed_doc_name and processed_doc_name not in st.session_state.uploaded_docs_session:
                        st.session_state.uploaded_docs_session.append(processed_doc_name)
                else:
                    # Optionally inform about skipped files from ZIP that are not in REQUIRED_DOCS
                    # st.info(f"ℹ️ Datei '{original_filename}' in ZIP ist nicht in der Liste der benötigten Dokumente und wurde übersprungen.")
                    pass # Keep silent for files not in the list to avoid too much noise
    except zipfile.BadZipFile:
        st.error("❌ Die hochgeladene ZIP-Datei ist beschädigt oder ungültig.")
    except Exception as e:
        st.error(f"❌ Fehler bei der Verarbeitung der ZIP-Datei: {e}")
    st.write("---")

# --- Checklist and Reset ---
st.subheader("2. Checkliste der benötigten Dateien")

if not REQUIRED_DOCS:
    st.warning("Es sind keine benötigten Dokumente in der Anwendung konfiguriert.")
else:
    all_docs_uploaded = True
    # For better layout with many items, consider columns or expanders
    # For now, a simple list:
    for doc_name_key in REQUIRED_DOCS: # Iterate using the keys of REQUIRED_DOCS
        if doc_name_key in st.session_state.uploaded_docs_session:
            st.markdown(f"<span style='color: green; font-weight: bold;'>✔️ {doc_name_key}</span> erfolgreich hochgeladen.", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color: red; font-weight: bold;'>❌ {doc_name_key}</span> fehlt noch.", unsafe_allow_html=True)
            all_docs_uploaded = False

    if not st.session_state.uploaded_docs_session and not uploaded_files and not uploaded_zip:
        st.info("Die Checkliste wird aktualisiert, sobald Dateien hochgeladen werden.")

    if all_docs_uploaded:
        st.balloons()
        st.success("🎉 Alle benötigten Dokumente wurden erfolgreich hochgeladen!")

# Reset button
if st.button("Neu beginnen (Checkliste zurücksetzen)"):
    st.session_state.uploaded_docs_session = []
    st.rerun()

# --- Log Viewer ---
st.subheader("3. Upload-Verlauf")
with st.expander("📜 Upload-Protokoll anzeigen/ausblenden"):
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as log_file_read: # Added encoding
                log_data = log_file_read.read()
                if log_data:
                    st.text_area("Protokoll:", log_data, height=300, disabled=True)
                else:
                    st.info("Das Protokoll ist leer.")
        else:
            st.info("Noch keine Uploads protokolliert. Das Protokoll wird hier angezeigt, sobald Dateien verarbeitet wurden.")
    except Exception as e:
        st.error(f"Fehler beim Lesen der Protokolldatei: {e}")
