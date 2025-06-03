import streamlit as st
import os
from datetime import datetime
import zipfile # For handling ZIP files
import io      # For handling byte streams with ZIP files

# --- Configuration and Constants ---
REQUIRED_DOC_ITEMS = [
    # Project Management
    {"id": "PRA", "display_name_EN": "Project Risk Analysis", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "ProjectRiskAnalysis"},
    {"id": "ERN", "display_name_EN": "External Release Notes", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "ExternalReleaseNotes"},
    {"id": "RNK", "display_name_EN": "Release Notes (with KPIs)", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "ReleaseNotesKPIs"},
    {"id": "CNE", "display_name_EN": "Compliance Evidence (UNECE, FuSi, E/E)", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "ComplianceEvidence_UNECE_FuSi_EE"},
    {"id": "PHB", "display_name_EN": "Project Handbook", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "ProjectHandbook"},
    {"id": "FOS", "display_name_EN": "FOSS Documentation/Ticket", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "FOSSDocumentation"},
    {"id": "PBM", "display_name_EN": "Proof of BsM Relevance", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "ProofOfBsMRelevance"},

    # Requirements Management (System & Software)
    {"id": "SRA", "display_name_EN": "System Requirements Analysis", "department_code": "REQ", "department_name_EN": "Requirements Management", "expected_base_filename": "SystemRequirementsAnalysis"},
    {"id": "SRBID", "display_name_EN": "Software Requirements Baseline ID", "department_code": "REQ", "department_name_EN": "Requirements Management", "expected_base_filename": "SoftwareRequirementsBaselineID"},
    {"id": "SREXP", "display_name_EN": "Software Requirements Export (DOORS)", "department_code": "REQ", "department_name_EN": "Requirements Management", "expected_base_filename": "SoftwareRequirementsExport_DOORS"},
    {"id": "SRDEV", "display_name_EN": "Software Requirements Deviation Report", "department_code": "REQ", "department_name_EN": "Requirements Management", "expected_base_filename": "SoftwareRequirementsDeviationReport"},

    # Architecture
    {"id": "ARCHD", "display_name_EN": "System/Software Architecture Document", "department_code": "ARCH", "department_name_EN": "Architecture", "expected_base_filename": "ArchitectureDocument"},
    {"id": "ARCHBID", "display_name_EN": "Architecture Baseline ID", "department_code": "ARCH", "department_name_EN": "Architecture", "expected_base_filename": "ArchitectureBaselineID"},

    # Test & Validation
    {"id": "TSTR", "display_name_EN": "Test Status Report", "department_code": "TEST", "department_name_EN": "Test & Validation", "expected_base_filename": "TestStatusReport"},
    {"id": "TBER", "display_name_EN": "Test Report", "department_code": "TEST", "department_name_EN": "Test & Validation", "expected_base_filename": "TestReport"},
    {"id": "SWE4S", "display_name_EN": "SWE.4 Specification (DOORS Export)", "department_code": "TEST", "department_name_EN": "Test & Validation", "expected_base_filename": "SWE4_Specification"},
    {"id": "SWE5S", "display_name_EN": "SWE.5 Specification (DOORS Export)", "department_code": "TEST", "department_name_EN": "Test & Validation", "expected_base_filename": "SWE5_Specification"},
    {"id": "SWE6S", "display_name_EN": "SWE.6 Specification (DOORS Export)", "department_code": "TEST", "department_name_EN": "Test & Validation", "expected_base_filename": "SWE6_Specification"},
    {"id": "TRISK", "display_name_EN": "Test Risk Analysis", "department_code": "TEST", "department_name_EN": "Test & Validation", "expected_base_filename": "TestRiskAnalysis"},

    # Issue & Defect Management
    {"id": "CIL", "display_name_EN": "Comprehensive Issue List (CRs, Bugs, etc.)", "department_code": "ISSUE", "department_name_EN": "Issue & Defect Management", "expected_base_filename": "ComprehensiveIssueList"},
    {"id": "KEL", "display_name_EN": "Known Error List (from Release Notes)", "department_code": "ISSUE", "department_name_EN": "Issue & Defect Management", "expected_base_filename": "KnownErrorList"},
    {"id": "ODD", "display_name_EN": "List of Open Documentation Defects (with justification)", "department_code": "ISSUE", "department_name_EN": "Issue & Defect Management", "expected_base_filename": "OpenDocumentationDefects"},
    {"id": "OAPD", "display_name_EN": "List of Open Accepted Product Defects (with justification)", "department_code": "ISSUE", "department_name_EN": "Issue & Defect Management", "expected_base_filename": "OpenAcceptedProductDefects"},

    # Security
    {"id": "SECRBID", "display_name_EN": "Security Requirements Baseline ID", "department_code": "SEC", "department_name_EN": "Security", "expected_base_filename": "SecurityRequirementsBaselineID"},
    {"id": "SECREXP", "display_name_EN": "Security Requirements Export (DOORS)", "department_code": "SEC", "department_name_EN": "Security", "expected_base_filename": "SecurityRequirementsExport_DOORS"},
    {"id": "SECCN", "display_name_EN": "Security Compliance Evidence", "department_code": "SEC", "department_name_EN": "Security", "expected_base_filename": "SecurityComplianceEvidence"},

    # Configuration Management
    {"id": "LOTU", "display_name_EN": "List of Used Tools (HW & SW, versions)", "department_code": "CM", "department_name_EN": "Configuration Management", "expected_base_filename": "ListOfUsedTools"},
    {"id": "KMSR", "display_name_EN": "Configuration Management (CM) Status Report", "department_code": "CM", "department_name_EN": "Configuration Management", "expected_base_filename": "CM_StatusReport"},

    # Quality Assurance
    {"id": "QAR", "display_name_EN": "Quality Assessment Report", "department_code": "QA", "department_name_EN": "Quality Assurance", "expected_base_filename": "QualityAssessmentReport"},
    {"id": "TRSF", "display_name_EN": "TRS Final Report", "department_code": "QA", "department_name_EN": "Quality Assurance", "expected_base_filename": "TRS_FinalReport"},
    {"id": "KGFC", "display_name_EN": "KGAS & Formula Q Conformance Confirmation", "department_code": "QA", "department_name_EN": "Quality Assurance", "expected_base_filename": "KGAS_FormulaQ_Confirmation"},
    {"id": "KGDE", "display_name_EN": "KGAS Data Export (Excel)", "department_code": "QA", "department_name_EN": "Quality Assurance", "expected_base_filename": "KGAS_DataExport"},
]
LOG_FILE = "uploads.log"
OUTPUT_BASE_FOLDER = "output_folder"
ALLOWED_FILE_TYPES = ["pdf", "zip"]

# --- Global Page Configuration ---
st.set_page_config(page_title="Document Upload Tool", layout="centered")

# --- Session State Initialization ---
def init_session_state():
    defaults = {
        'current_page': "Upload Document",
        'all_release_uploads': {}, # Stores {release_name: [doc_id1, doc_id2]}
        'current_active_release': "Default_Release_V1.0", # Default active release
        'selected_for_upload_id': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    for item in REQUIRED_DOC_ITEMS:
        uploader_key = f"uploader_{item['id']}"
        if uploader_key not in st.session_state:
            st.session_state[uploader_key] = None
init_session_state()

# --- Core Function for Saving and Logging ---
def save_and_log_file(uploaded_file_obj, active_release_name, doc_item_config):
    uploaded_filename = uploaded_file_obj.name
    file_bytes = uploaded_file_obj.getvalue()
    
    final_file_content_to_save = None
    final_target_extension = ".pdf" 

    original_name_part, original_extension = os.path.splitext(uploaded_filename)

    if original_extension.lower() == ".pdf":
        final_file_content_to_save = file_bytes
    elif original_extension.lower() == ".zip":
        try:
            with zipfile.ZipFile(io.BytesIO(file_bytes), 'r') as z:
                expected_pdf_in_zip_basename = (doc_item_config['expected_base_filename'] + ".pdf").lower()
                found_pdf_path_in_zip = None
                for name_in_zip in z.namelist():
                    if os.path.basename(name_in_zip).lower() == expected_pdf_in_zip_basename:
                        found_pdf_path_in_zip = name_in_zip
                        break
                if found_pdf_path_in_zip:
                    final_file_content_to_save = z.read(found_pdf_path_in_zip)
                    st.info(f"Extracted '{os.path.basename(found_pdf_path_in_zip)}' from uploaded ZIP '{uploaded_filename}'.")
                else:
                    st.error(f"Error: ZIP file '{uploaded_filename}' does not contain the expected PDF "
                             f"'{doc_item_config['expected_base_filename']}.pdf' for document type '{doc_item_config['display_name_EN']}'.")
                    return None, None
        except zipfile.BadZipFile:
            st.error(f"Error: The uploaded ZIP file '{uploaded_filename}' is corrupted or not a valid ZIP file.")
            return None, None
        except Exception as e_zip:
            st.error(f"Error processing ZIP file '{uploaded_filename}': {e_zip}")
            return None, None
    else:
        st.error(f"Error: Only PDF or ZIP files are allowed. You uploaded: '{uploaded_filename}'. Allowed: {ALLOWED_FILE_TYPES}")
        return None, None

    if final_file_content_to_save is None:
        return None, None

    try:
        # Version string for filename is the active_release_name itself, cleaned
        clean_version_for_filename = active_release_name.replace(" ", "_").replace("/", "-")
        safe_base_filename = doc_item_config['expected_base_filename'].replace(" ", "_").replace("/", "-").replace(".", "")
        
        new_base_name = f"{doc_item_config['department_code']}_{safe_base_filename}_{clean_version_for_filename}"
        new_filename = f"{new_base_name}{final_target_extension}" # Should be .pdf
        
        # Sanitize active_release_name for use as a folder name
        safe_release_folder_name = active_release_name.replace(" ", "_").replace("/", "-").replace("\\", "-").replace(":", "-")

        target_dir_department_name = doc_item_config['department_name_EN'].replace(" & ", "_and_").replace(" ", "")
        # Path: output_folder/RELEASE_NAME/DepartmentName/BaseFilename/
        target_dir = os.path.join(OUTPUT_BASE_FOLDER, safe_release_folder_name, target_dir_department_name, safe_base_filename)
        os.makedirs(target_dir, exist_ok=True)
        save_path = os.path.join(target_dir, new_filename)

        with open(save_path, "wb") as f:
            f.write(final_file_content_to_save)
        log_message = (f"{datetime.now().isoformat()} - Release: {active_release_name} - Uploaded: '{uploaded_filename}' "
                       f"for '{doc_item_config['display_name_EN']}' -> Saved as: '{new_filename}' in '{target_dir}'")
        with open(LOG_FILE, "a", encoding="utf-8") as log_f:
            log_f.write(log_message + "\n")
        return doc_item_config['id'], new_filename
    except Exception as e_save:
        st.error(f"❌ Error while saving file '{new_filename}' for '{doc_item_config['display_name_EN']}': {e_save}")
        return None, None

# --- Render Functions for "Pages" ---
def render_upload_document_page():
    st.markdown("<h1 style='text-align: center; color: #4A4A4A; margin-bottom: 20px;'>Upload Document</h1>", unsafe_allow_html=True)

    # Active Release Context Input
    st.markdown("#### Current Active Release Context")
    new_active_release = st.text_input(
        "Define or switch active Release (e.g., ProjectOmega_Sprint3_RC1). All uploads will be associated with this release:",
        value=st.session_state.current_active_release,
        key="active_release_text_input_main"
    )
    if new_active_release != st.session_state.current_active_release:
        st.session_state.current_active_release = new_active_release
        st.session_state.selected_for_upload_id = None # Reset template selection on release change
        for item_cfg in REQUIRED_DOC_ITEMS: # Clear all uploader states
            st.session_state[f"uploader_{item_cfg['id']}"] = None
        st.rerun()
    st.markdown(f"**All uploads will be processed for Release: `{st.session_state.current_active_release}`**")


    st.markdown("---")
    st.markdown("### ① Select Document Template")
    doc_options_map = {item['id']: f"{item['department_name_EN']} - {item['display_name_EN']}" for item in REQUIRED_DOC_ITEMS}
    select_options = {None: "--- Please select a template ---"}
    select_options.update(doc_options_map)

    current_selection_id = st.session_state.selected_for_upload_id
    options_keys_list = list(select_options.keys())
    try:
        current_selection_index = options_keys_list.index(current_selection_id)
    except ValueError:
        current_selection_index = 0

    selected_id = st.selectbox(
        "Select the document type you want to upload:",
        options=options_keys_list,
        format_func=lambda id_key: select_options[id_key],
        key="sb_template_select_multi_release",
        index=current_selection_index
    )
    if selected_id != st.session_state.selected_for_upload_id:
        st.session_state.selected_for_upload_id = selected_id
        st.rerun()

    if st.session_state.selected_for_upload_id:
        selected_doc_id_for_upload = st.session_state.selected_for_upload_id
        current_doc_item = next((item for item in REQUIRED_DOC_ITEMS if item['id'] == selected_doc_id_for_upload), None)

        if current_doc_item:
            st.markdown("---")
            st.markdown(f"### ② Upload PDF or ZIP for '{current_doc_item['display_name_EN']}'")
            
            uploader_key_specific = f"uploader_{current_doc_item['id']}"
            help_text_uploader = (f"Please upload the document as a PDF file. "
                                  f"Alternatively, you can upload a ZIP file containing a PDF named "
                                  f"'{current_doc_item['expected_base_filename']}.pdf'.")
            
            uploaded_file = st.file_uploader(
                "Select PDF or ZIP file:",
                type=ALLOWED_FILE_TYPES,
                key=uploader_key_specific,
                help=help_text_uploader
            )

            if uploaded_file:
                st.write(f"Selected file: `{uploaded_file.name}` ({uploaded_file.size / 1024:.2f} KB)")
                
                # Prospective new filename (always .pdf as target)
                clean_version_preview = st.session_state.current_active_release.replace(" ", "_").replace("/", "-")
                safe_base_filename_preview = current_doc_item['expected_base_filename'].replace(" ", "_").replace("/", "-").replace(".", "")
                prospective_new_name = f"{current_doc_item['department_code']}_{safe_base_filename_preview}_{clean_version_preview}.pdf"
                st.info(f"Expected new filename after processing: `{prospective_new_name}`")

                if st.button(f"Confirm Upload for '{current_doc_item['display_name_EN']}'", key=f"btn_confirm_upload_multi_release_{current_doc_item['id']}"):
                    processed_doc_id, new_filename = save_and_log_file(uploaded_file, st.session_state.current_active_release, current_doc_item)
                    if processed_doc_id:
                        st.success(f"✅ '{current_doc_item['display_name_EN']}' ('{uploaded_file.name}') successfully processed for Release '{st.session_state.current_active_release}' and saved as '{new_filename}'.")
                        
                        # Update session state for the current active release
                        active_release = st.session_state.current_active_release
                        if active_release not in st.session_state.all_release_uploads:
                            st.session_state.all_release_uploads[active_release] = []
                        if processed_doc_id not in st.session_state.all_release_uploads[active_release]:
                            st.session_state.all_release_uploads[active_release].append(processed_doc_id)
                        
                        st.session_state[uploader_key_specific] = None
                        st.session_state.selected_for_upload_id = None 
                        st.rerun()

def render_document_overview_page():
    st.title("📊 Document Overview")
    
    # Allow user to see overview for the "current_active_release" (which they can set on the upload page)
    # or potentially select a different release to view from a dropdown of *existing* releases in the log.
    # For simplicity now, it just shows for st.session_state.current_active_release
    
    st.info(f"Showing overview for Release: **{st.session_state.current_active_release}** "
            f"(To change the active release for uploads and viewing, go to the 'Upload Document' page).")


    if not REQUIRED_DOC_ITEMS:
        st.warning("No target documents configured in the application.")
        return

    active_release_overview = st.session_state.current_active_release
    uploaded_docs_for_this_release = st.session_state.all_release_uploads.get(active_release_overview, [])

    departments = {}
    for item in REQUIRED_DOC_ITEMS:
        dept_name = item['department_name_EN']
        if dept_name not in departments:
            departments[dept_name] = []
        departments[dept_name].append(item)

    for dept_name, docs_in_dept in sorted(departments.items()):
        uploaded_in_dept_count = sum(1 for doc_item in docs_in_dept if doc_item['id'] in uploaded_docs_for_this_release)
        
        with st.expander(f"Department: {dept_name} ({uploaded_in_dept_count}/{len(docs_in_dept)} uploaded for this release)", expanded=True):
            for doc_item in docs_in_dept:
                is_uploaded = doc_item['id'] in uploaded_docs_for_this_release
                status_icon = "✔️" if is_uploaded else "❌"
                color = "green" if is_uploaded else "#D3D3D3" 
                text_color = "black" if not is_uploaded else "green"
                
                col1, col2 = st.columns([1, 10])
                with col1:
                    st.markdown(f"<span style='color: {color}; font-size: 1.2em;'>{status_icon}</span>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<span style='color: {text_color};'>{doc_item['display_name_EN']}</span>", unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    total_required_docs = len(REQUIRED_DOC_ITEMS)
    # Count unique uploaded docs for the *current active release*
    unique_uploaded_docs_count_current_release = len(uploaded_docs_for_this_release) 
    
    if total_required_docs > 0:
        progress_percent = (unique_uploaded_docs_count_current_release / total_required_docs) * 100
        st.sidebar.progress(progress_percent / 100, text=f"Release '{active_release_overview}': {unique_uploaded_docs_count_current_release} / {total_required_docs}")

    if unique_uploaded_docs_count_current_release == total_required_docs and total_required_docs > 0:
        st.sidebar.success(f"🎉 All documents for Release '{active_release_overview}' uploaded!")

    st.sidebar.markdown("---")
    if st.sidebar.button("Reset Uploads for Current Release"):
        active_release_to_reset = st.session_state.current_active_release
        if active_release_to_reset in st.session_state.all_release_uploads:
            del st.session_state.all_release_uploads[active_release_to_reset]
            st.sidebar.success(f"Uploads for Release '{active_release_to_reset}' have been reset.")
        else:
            st.sidebar.info(f"No uploads to reset for Release '{active_release_to_reset}'.")
        
        st.session_state.selected_for_upload_id = None
        for item_cfg_reset in REQUIRED_DOC_ITEMS: 
            st.session_state[f"uploader_{item_cfg_reset['id']}"] = None
        st.rerun()

# --- Main App Logic for Page Selection and Rendering ---
st.sidebar.title("Navigation")
page_options = ["Upload Document", "Document Overview"]

try:
    current_page_index = page_options.index(st.session_state.current_page)
except ValueError:
    current_page_index = 0 
    st.session_state.current_page = page_options[0]

st.session_state.current_page = st.sidebar.radio(
    "Menu",
    page_options,
    index=current_page_index,
    key="main_nav_radio_multi_release"
)

if st.session_state.current_page == "Upload Document":
    render_upload_document_page()
elif st.session_state.current_page == "Document Overview":
    render_document_overview_page()

with st.sidebar.expander("📜 Upload Log", expanded=False):
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as log_f_read:
                log_data = log_f_read.read()
                if log_data:
                    st.text_area("Log:", log_data, height=200, disabled=True, key="log_view_sidebar_multi_release")
                else:
                    st.info("Log is empty.")
        else:
            st.info("No uploads logged yet.")
    except Exception as e:
        st.error(f"Error reading log file: {e}")
