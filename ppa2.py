import streamlit as st
import os
from datetime import datetime
import zipfile # For handling ZIP files
import io      # For handling byte streams with ZIP files
import pandas as pd # For CSV export

# --- Configuration and Constants ---
REQUIRED_DOC_ITEMS = [
    # Project Management
    {"id": "PRA", "display_name_EN": "Project Risk Analysis", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "ProjectRiskAnalysis"},
    {"id": "ERN", "display_name_EN": "External Release Notes", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "ExternalReleaseNotes"},
    {"id": "RNK", "display_name_EN": "Release Notes (with KPIs)", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "ReleaseNotesKPIs"},
    {"id": "CNE", "display_name_EN": "Compliance Evidence (UNECE, FuSi, E/E)", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "ComplianceEvidenceUNECEFuSiEE"},
    {"id": "PHB", "display_name_EN": "Project Handbook", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "ProjectHandbook"},
    {"id": "FOS", "display_name_EN": "FOSS Documentation/Ticket", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "FOSSDocumentation"},
    {"id": "PBM", "display_name_EN": "Proof of BsM Relevance", "department_code": "PM", "department_name_EN": "Project Management", "expected_base_filename": "ProofOfBsMRelevance"},

    # Requirements Management
    {"id": "SRA", "display_name_EN": "System Requirements Analysis", "department_code": "REQ", "department_name_EN": "Requirements Management", "expected_base_filename": "SystemRequirementsAnalysis"},
    {"id": "SRBID", "display_name_EN": "Software Requirements Baseline ID", "department_code": "REQ", "department_name_EN": "Requirements Management", "expected_base_filename": "SoftwareRequirementsBaselineID"},
    {"id": "SREXP", "display_name_EN": "Software Requirements Export (DOORS)", "department_code": "REQ", "department_name_EN": "Requirements Management", "expected_base_filename": "SoftwareRequirementsExportDOORS"},
    {"id": "SRDEV", "display_name_EN": "Software Requirements Deviation Report", "department_code": "REQ", "department_name_EN": "Requirements Management", "expected_base_filename": "SoftwareRequirementsDeviationReport"},

    # Architecture
    {"id": "ARCHD", "display_name_EN": "System/Software Architecture Document", "department_code": "ARCH", "department_name_EN": "Architecture", "expected_base_filename": "ArchitectureDocument"},
    {"id": "ARCHBID", "display_name_EN": "Architecture Baseline ID", "department_code": "ARCH", "department_name_EN": "Architecture", "expected_base_filename": "ArchitectureBaselineID"},

    # Test & Validation
    {"id": "TSTR", "display_name_EN": "Test Status Report", "department_code": "TEST", "department_name_EN": "Test & Validation", "expected_base_filename": "TestStatusReport"},
    {"id": "TBER", "display_name_EN": "Test Report", "department_code": "TEST", "department_name_EN": "Test & Validation", "expected_base_filename": "TestReport"},
    {"id": "SWE4S", "display_name_EN": "SWE.4 Specification (DOORS Export)", "department_code": "TEST", "department_name_EN": "Test & Validation", "expected_base_filename": "SWE4Specification"},
    {"id": "SWE5S", "display_name_EN": "SWE.5 Specification (DOORS Export)", "department_code": "TEST", "department_name_EN": "Test & Validation", "expected_base_filename": "SWE5Specification"},
    {"id": "SWE6S", "display_name_EN": "SWE.6 Specification (DOORS Export)", "department_code": "TEST", "department_name_EN": "Test & Validation", "expected_base_filename": "SWE6Specification"},
    {"id": "TRISK", "display_name_EN": "Test Risk Analysis", "department_code": "TEST", "department_name_EN": "Test & Validation", "expected_base_filename": "TestRiskAnalysis"},

    # Issue & Defect Management
    {"id": "CIL", "display_name_EN": "Comprehensive Issue List (CRs, Bugs, etc.)", "department_code": "ISSUE", "department_name_EN": "Issue & Defect Management", "expected_base_filename": "ComprehensiveIssueList"},
    {"id": "KEL", "display_name_EN": "Known Error List (from Release Notes)", "department_code": "ISSUE", "department_name_EN": "Issue & Defect Management", "expected_base_filename": "KnownErrorList"},
    {"id": "ODD", "display_name_EN": "List of Open Documentation Defects", "department_code": "ISSUE", "department_name_EN": "Issue & Defect Management", "expected_base_filename": "OpenDocumentationDefects"},
    {"id": "OAPD", "display_name_EN": "List of Open Accepted Product Defects", "department_code": "ISSUE", "department_name_EN": "Issue & Defect Management", "expected_base_filename": "OpenAcceptedProductDefects"},

    # Security
    {"id": "SECRBID", "display_name_EN": "Security Requirements Baseline ID", "department_code": "SEC", "department_name_EN": "Security", "expected_base_filename": "SecurityRequirementsBaselineID"},
    {"id": "SECREXP", "display_name_EN": "Security Requirements Export (DOORS)", "department_code": "SEC", "department_name_EN": "Security", "expected_base_filename": "SecurityRequirementsExportDOORS"},
    {"id": "SECCN", "display_name_EN": "Security Compliance Evidence", "department_code": "SEC", "department_name_EN": "Security", "expected_base_filename": "SecurityComplianceEvidence"},

    # Configuration Management
    {"id": "LOTU", "display_name_EN": "List of Used Tools (HW & SW, versions)", "department_code": "CM", "department_name_EN": "Configuration Management", "expected_base_filename": "ListOfUsedTools"},
    {"id": "KMSR", "display_name_EN": "Configuration Management (CM) Status Report", "department_code": "CM", "department_name_EN": "Configuration Management", "expected_base_filename": "CMStatusReport"},

    # Quality Assurance
    {"id": "QAR", "display_name_EN": "Quality Assessment Report", "department_code": "QA", "department_name_EN": "Quality Assurance", "expected_base_filename": "QualityAssessmentReport"},
    {"id": "TRSF", "display_name_EN": "TRS Final Report", "department_code": "QA", "department_name_EN": "Quality Assurance", "expected_base_filename": "TRSFinalReport"},
    {"id": "KGFC", "display_name_EN": "KGAS & Formula Q Conformance Confirmation", "department_code": "QA", "department_name_EN": "Quality Assurance", "expected_base_filename": "KGASFormulaQConfirmation"},
    {"id": "KGDE", "display_name_EN": "KGAS Data Export (Excel)", "department_code": "QA", "department_name_EN": "Quality Assurance", "expected_base_filename": "KGASDataExport"},
]
LOG_FILE = "uploads.log"
OUTPUT_BASE_FOLDER = "output_folder"
ALLOWED_FILE_TYPES = ["pdf", "zip"]
MATURITY_OPTIONS = ["Draft", "Reviewed", "Released", "Obsolete"]

# --- Global Page Configuration ---
st.set_page_config(page_title="Document Upload Tool", layout="centered")

# --- Session State Initialization ---
def init_session_state():
    defaults = {
        'current_page': "Upload Document", # Default page
        'all_release_uploads': {}, 
        'current_active_release': "Default_Release_V1.0",
        'selected_department_for_upload': None,
        'selected_doc_id_for_upload': None,
        'overview_selected_release': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    for item in REQUIRED_DOC_ITEMS: 
        st.session_state.setdefault(f"uploader_{item['id']}", None)
        st.session_state.setdefault(f"doc_ver_{item['id']}", "1.0")
        st.session_state.setdefault(f"doc_mat_{item['id']}", MATURITY_OPTIONS[0])
init_session_state()

# --- Core Function for Saving and Logging ---
def save_and_log_file(uploaded_file_obj, active_release_name, doc_item_config, doc_specific_version, doc_maturity):
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
                    return None, None, None 
        except zipfile.BadZipFile:
            st.error(f"Error: The uploaded ZIP file '{uploaded_filename}' is corrupted or not a valid ZIP file.")
            return None, None, None
        except Exception as e_zip:
            st.error(f"Error processing ZIP file '{uploaded_filename}': {e_zip}")
            return None, None, None
    else:
        st.error(f"Error: Only PDF or ZIP files are allowed. You uploaded: '{uploaded_filename}'. Allowed: {ALLOWED_FILE_TYPES}")
        return None, None, None

    if final_file_content_to_save is None: return None, None, None

    try:
        clean_doc_version = doc_specific_version.replace(" ", "_").replace("/", "-").replace("\\", "").replace(":", "")
        safe_base_filename = doc_item_config['expected_base_filename'].replace(" ", "_").replace("/", "-").replace(".", "")
        
        new_base_name = f"{doc_item_config['department_code']}_{safe_base_filename}_{clean_doc_version}_{doc_maturity.lower()}"
        new_filename = f"{new_base_name}{final_target_extension}"
        
        safe_release_folder_name = active_release_name.replace(" ", "_").replace("/", "-").replace("\\", "").replace(":", "")
        target_dir_department_name = doc_item_config['department_name_EN'].replace(" & ", "_and_").replace(" ", "")
        target_dir = os.path.join(OUTPUT_BASE_FOLDER, safe_release_folder_name, target_dir_department_name, safe_base_filename)
        os.makedirs(target_dir, exist_ok=True)
        save_path = os.path.join(target_dir, new_filename)

        with open(save_path, "wb") as f:
            f.write(final_file_content_to_save)
        log_message = (f"{datetime.now().isoformat()} - Release: {active_release_name} - Doc: '{doc_item_config['display_name_EN']}' "
                       f"(Ver: {doc_specific_version}, Mat: {doc_maturity}) - OrigFile: '{uploaded_filename}' -> Saved as: '{new_filename}' in '{target_dir}'")
        with open(LOG_FILE, "a", encoding="utf-8") as log_f:
            log_f.write(log_message + "\n")
        return doc_item_config['id'], new_filename, save_path
    except Exception as e_save:
        st.error(f"❌ Error while saving file '{new_filename}' for '{doc_item_config['display_name_EN']}': {e_save}")
        return None, None, None

# --- Render Functions for "Pages" ---
def render_upload_document_page():
    st.markdown("<h1 style='text-align: center; color: #4A4A4A; margin-bottom: 10px;'>Document Upload for Release Baseline</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center; font-size: 1.0em; color: #333;'>
    Welcome! This tool is provided by the <strong>Configuration Management Team</strong> to streamline the <strong>Release Baseline Preparation Process</strong>.
    </p>
    <p style='text-align: center; margin-bottom: 20px;'>
    Your timely uploads of the required documents are crucial for establishing a <strong>consistent global baseline</strong> for each release.
    Please ensure all documents are up-to-date and correctly versioned.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("#### Current Active Release for Uploads")
    st.info("Begin by defining the **Active Release Context** below. All subsequent document uploads will be associated with this specific release.")
    
    new_active_release = st.text_input(
        "Define or switch active Release (e.g., ProjectOmega_Sprint3_RC1):",
        value=st.session_state.current_active_release,
        key="active_release_text_input_en_v3"
    )
    if new_active_release != st.session_state.current_active_release:
        st.session_state.current_active_release = new_active_release
        st.session_state.selected_department_for_upload = None
        st.session_state.selected_doc_id_for_upload = None
        for item_cfg in REQUIRED_DOC_ITEMS:
            st.session_state[f"uploader_{item_cfg['id']}"] = None
        st.rerun()
    st.markdown(f"**All new uploads will be processed for Release: `{st.session_state.current_active_release}`**")
    st.markdown("---")

    # Step 1: Select Department
    st.markdown("### ① Select Department")
    department_names = sorted(list(set(item['department_name_EN'] for item in REQUIRED_DOC_ITEMS)))
    dept_options = {None: "--- Please select a department ---"}
    for dept_name in department_names:
        dept_options[dept_name] = dept_name

    selected_dept_name = st.selectbox(
        "Select the department:",
        options=list(dept_options.keys()),
        format_func=lambda key: dept_options[key],
        key="sb_dept_select_en_v3",
        index=list(dept_options.keys()).index(st.session_state.selected_department_for_upload) if st.session_state.selected_department_for_upload in dept_options else 0
    )
    if selected_dept_name != st.session_state.selected_department_for_upload:
        st.session_state.selected_department_for_upload = selected_dept_name
        st.session_state.selected_doc_id_for_upload = None 
        st.rerun()

    # Step 2: Select Document Template
    if st.session_state.selected_department_for_upload:
        st.markdown("---")
        st.markdown(f"### ② Select Document Template for '{st.session_state.selected_department_for_upload}'")
        
        filtered_doc_items = [item for item in REQUIRED_DOC_ITEMS if item['department_name_EN'] == st.session_state.selected_department_for_upload]
        doc_template_options_map = {item['id']: item['display_name_EN'] for item in filtered_doc_items}
        doc_template_select_options = {None: "--- Select a document template ---"}
        doc_template_select_options.update(doc_template_options_map)

        current_doc_template_id = st.session_state.selected_doc_id_for_upload
        doc_template_keys_list = list(doc_template_select_options.keys())
        try:
            current_doc_template_index = doc_template_keys_list.index(current_doc_template_id)
        except ValueError:
            current_doc_template_index = 0
        
        selected_doc_id = st.selectbox(
            "Select the document type:",
            options=doc_template_keys_list,
            format_func=lambda id_key: doc_template_select_options[id_key],
            key="sb_doc_template_select_en_v3",
            index=current_doc_template_index
        )
        if selected_doc_id != st.session_state.selected_doc_id_for_upload:
            st.session_state.selected_doc_id_for_upload = selected_doc_id
            st.rerun()

    # Step 3 & 4: Metadata Inputs and File Uploader
    if st.session_state.selected_doc_id_for_upload:
        current_doc_item = next((item for item in REQUIRED_DOC_ITEMS if item['id'] == st.session_state.selected_doc_id_for_upload), None)
        if current_doc_item:
            st.markdown("---")
            st.markdown(f"### ③ Provide Details & Upload for '{current_doc_item['display_name_EN']}'")

            uploader_key_specific = f"uploader_{current_doc_item['id']}"
            doc_version_key = f"doc_ver_{current_doc_item['id']}"
            doc_maturity_key = f"doc_mat_{current_doc_item['id']}"

            col1_meta, col2_meta = st.columns(2)
            with col1_meta:
                st.session_state[doc_version_key] = st.text_input(
                    "Document Version (e.g., 1.0, 1.1_beta):", 
                    value=st.session_state[doc_version_key], 
                    key=f"ti_{doc_version_key}_v3"
                )
            with col2_meta:
                st.session_state[doc_maturity_key] = st.selectbox(
                    "Document Maturity:", 
                    options=MATURITY_OPTIONS, 
                    index=MATURITY_OPTIONS.index(st.session_state[doc_maturity_key]),
                    key=f"sb_{doc_maturity_key}_v3"
                )
            
            help_text_uploader = (f"Upload PDF, or ZIP containing '{current_doc_item['expected_base_filename']}.pdf'.")
            uploaded_file = st.file_uploader(
                "Select PDF or ZIP file:", type=ALLOWED_FILE_TYPES, key=uploader_key_specific, help=help_text_uploader
            )

            if uploaded_file:
                st.write(f"Selected file: `{uploaded_file.name}` ({uploaded_file.size / 1024:.2f} KB)")
                
                clean_doc_version_preview = st.session_state[doc_version_key].replace(" ", "_").replace("/", "-").replace("\\", "").replace(":", "")
                safe_base_filename_preview = current_doc_item['expected_base_filename'].replace(" ", "_").replace("/", "-").replace(".", "")
                prospective_new_name = f"{current_doc_item['department_code']}_{safe_base_filename_preview}_{clean_doc_version_preview}_{st.session_state[doc_maturity_key].lower()}.pdf"
                st.info(f"Expected new filename after processing: `{prospective_new_name}`")

                if st.button(f"Confirm Upload for '{current_doc_item['display_name_EN']}'", key=f"btn_confirm_final_v3_{current_doc_item['id']}"):
                    doc_id, new_name, saved_path = save_and_log_file(
                        uploaded_file, 
                        st.session_state.current_active_release, 
                        current_doc_item,
                        st.session_state[doc_version_key],
                        st.session_state[doc_maturity_key]
                    )
                    if doc_id:
                        st.success(f"✅ '{current_doc_item['display_name_EN']}' ('{uploaded_file.name}') successfully processed for Release "
                                   f"'{st.session_state.current_active_release}' and saved as '{new_name}'.")
                        
                        active_release = st.session_state.current_active_release
                        if active_release not in st.session_state.all_release_uploads:
                            st.session_state.all_release_uploads[active_release] = {}
                        
                        upload_details = {
                            "doc_version": st.session_state[doc_version_key],
                            "maturity": st.session_state[doc_maturity_key],
                            "saved_filename": new_name,
                            "saved_path": saved_path,
                            "original_uploaded_filename": uploaded_file.name,
                            "upload_timestamp": datetime.now().isoformat()
                        }
                        st.session_state.all_release_uploads[active_release][doc_id] = upload_details
                        
                        # WORKAROUND for Python 3.13 issue: Comment out uploader reset
                        # st.session_state[uploader_key_specific] = None 
                        st.session_state.selected_doc_id_for_upload = None 
                        st.session_state.selected_department_for_upload = None 
                        st.rerun()

def generate_csv_data(release_name_to_export):
    data_for_csv = []
    release_uploads = st.session_state.all_release_uploads.get(release_name_to_export, {})

    for item_config in REQUIRED_DOC_ITEMS:
        doc_id = item_config['id']
        upload_info = release_uploads.get(doc_id)
        
        if upload_info: status, doc_version, maturity, saved_filename, saved_path = "Uploaded", upload_info.get("doc_version", "N/A"), upload_info.get("maturity", "N/A"), upload_info.get("saved_filename", "N/A"), upload_info.get("saved_path", "N/A")
        else: status, doc_version, maturity, saved_filename, saved_path = "Missing", "N/A", "N/A", "N/A", "N/A"
            
        data_for_csv.append({
            "Release": release_name_to_export, "Department": item_config['department_name_EN'],
            "Document Template Name": item_config['display_name_EN'], "Status": status,
            "Uploaded Document Version": doc_version, "Maturity": maturity,
            "Saved Filename": saved_filename, "Full Path": saved_path
        })
    return pd.DataFrame(data_for_csv)

def render_document_overview_page():
    st.title("📊 Document Overview")
    
    available_releases = sorted(list(st.session_state.all_release_uploads.keys()), reverse=True) # Show newest first potentially

    # Initialize overview_selected_release if it's not valid or not set
    if not st.session_state.overview_selected_release or st.session_state.overview_selected_release not in available_releases:
        if st.session_state.current_active_release in available_releases:
            st.session_state.overview_selected_release = st.session_state.current_active_release
        elif available_releases:
            st.session_state.overview_selected_release = available_releases[0]
        else:
            st.session_state.overview_selected_release = None # No release to select

    if not available_releases:
        st.info("No releases with uploaded documents yet. Upload documents on the 'Upload Document' page first.")
        return

    # Selectbox for choosing release to view
    col1_view, col2_export = st.columns([3,1])
    with col1_view:
        # Ensure index is valid
        idx = 0
        if st.session_state.overview_selected_release and st.session_state.overview_selected_release in available_releases :
             idx = available_releases.index(st.session_state.overview_selected_release)

        selected_release_for_view = st.selectbox(
            "Select Release to View:", options=available_releases,
            index=idx,
            key="sb_overview_release_select_en_v3"
        )
    
    if selected_release_for_view != st.session_state.overview_selected_release:
        st.session_state.overview_selected_release = selected_release_for_view
        st.rerun() # Rerun to update the view for the newly selected release

    release_to_display_final = st.session_state.overview_selected_release
    if not release_to_display_final: # Should be caught by 'if not available_releases'
        st.info("Please select a release to view its document status or upload documents first.")
        return

    with col2_export:
        st.write("") 
        st.write("") 
        csv_df = generate_csv_data(release_to_display_final)
        st.download_button(
            label="📥 Export to CSV", data=csv_df.to_csv(index=False, sep=';').encode('utf-8-sig'),
            file_name=f"document_overview_{release_to_display_final.replace(' ','_')}.csv", mime='text/csv',
            key=f"download_csv_v3_{release_to_display_final}" # Make key unique per release for caching
        )

    st.markdown(f"### Status for Release: **{release_to_display_final}**")
    release_uploads = st.session_state.all_release_uploads.get(release_to_display_final, {})
    departments = {}
    for item in REQUIRED_DOC_ITEMS:
        dept_name = item['department_name_EN']
        if dept_name not in departments: departments[dept_name] = []
        departments[dept_name].append(item)

    for dept_name, docs_in_dept in sorted(departments.items()):
        uploaded_in_dept_count = sum(1 for doc_item in docs_in_dept if doc_item['id'] in release_uploads)
        with st.expander(f"Department: {dept_name} ({uploaded_in_dept_count}/{len(docs_in_dept)} uploaded)", expanded=True):
            c1, c2, c3, c4 = st.columns([1, 5, 2, 2])
            c1.markdown("**Status**"); c2.markdown("**Document Template**"); c3.markdown("**Version**"); c4.markdown("**Maturity**")
            for doc_item in docs_in_dept:
                upload_info = release_uploads.get(doc_item['id'])
                col1_i, col2_i, col3_i, col4_i = st.columns([1, 5, 2, 2]) # Use different var names
                is_uploaded = bool(upload_info)
                status_icon, color, text_color = ("✔️", "green", "green") if is_uploaded else ("❌", "#D3D3D3", "black")
                col1_i.markdown(f"<span style='color: {color}; font-size: 1.2em;'>{status_icon}</span>", unsafe_allow_html=True)
                col2_i.markdown(f"<span style='color: {text_color};'>{doc_item['display_name_EN']}</span>", unsafe_allow_html=True)
                col3_i.markdown(f"<span style='color: {text_color};'>{upload_info.get('doc_version', 'N/A') if upload_info else 'N/A'}</span>", unsafe_allow_html=True)
                col4_i.markdown(f"<span style='color: {text_color};'>{upload_info.get('maturity', 'N/A') if upload_info else 'N/A'}</span>", unsafe_allow_html=True)
    
    # Sidebar Elements
    st.sidebar.markdown("---")
    total_required_docs = len(REQUIRED_DOC_ITEMS)
    unique_uploaded_docs_count_current_release = len(release_uploads)
    if total_required_docs > 0:
        progress_percent = (unique_uploaded_docs_count_current_release / total_required_docs) * 100
        st.sidebar.progress(progress_percent / 100, text=f"Release '{release_to_display_final}': {unique_uploaded_docs_count_current_release} / {total_required_docs}")
    if unique_uploaded_docs_count_current_release == total_required_docs and total_required_docs > 0:
        st.sidebar.success(f"🎉 All documents for Release '{release_to_display_final}' uploaded!")

    st.sidebar.markdown("---")
    if st.sidebar.button("Reset Uploads for Viewed Release"):
        release_to_reset = st.session_state.overview_selected_release
        if release_to_reset and release_to_reset in st.session_state.all_release_uploads:
            del st.session_state.all_release_uploads[release_to_reset]
            st.sidebar.success(f"Uploads for Release '{release_to_reset}' have been reset.")
            if st.session_state.overview_selected_release == release_to_reset: st.session_state.overview_selected_release = None 
            st.rerun()
        elif release_to_reset: st.sidebar.info(f"No uploads to reset for Release '{release_to_reset}'.")
        else: st.sidebar.warning("No release selected in overview to reset.")

def render_learning_resources_page():
    st.title("📚 Learning Resources")
    st.markdown("""
    Here are some (placeholder) resources to help you with the release baseline process, 
    configuration management, and document standards. 
    **Please replace the '#' with actual links.**
    """)

    st.subheader("Internal Resources (Examples)")
    st.markdown("""
    * [Configuration Management Process Document](#)
    * [Document Naming Conventions Guide](#)
    * [Release Management Policy](#)
    * [Guide to Document Versioning and Maturity](#)
    """)

    st.subheader("External Best Practices (Examples)")
    st.markdown("""
    * [Best Practices in Configuration Management (Example Article)](#)
    * [Guide to Effective Version Control (Example)](#)
    * [Understanding Document Maturity Levels (Example)](#)
    """)

    st.subheader("Tool Specific Guides (Examples)")
    st.markdown("""
    * [How to Create Accessible PDF Documents](#)
    * [Tips for Using ZIP Archives Effectively](#)
    """)
    st.info("This page is a placeholder. Please provide actual links for these resources.")

# --- Main App Logic for Page Selection and Rendering ---
st.sidebar.title("Menu") # Changed from "Navigation"
page_options = ["Upload Document", "Document Overview", "Learning Resources"] # Added new page
try:
    current_page_index = page_options.index(st.session_state.current_page)
except ValueError: # If current_page is somehow invalid, default to first page
    current_page_index = 0 
    st.session_state.current_page = page_options[0]

st.session_state.current_page = st.sidebar.radio(
    "Select Page:", # Changed label
    page_options, 
    index=current_page_index, 
    key="main_nav_final_v4"
)

if st.session_state.current_page == "Upload Document":
    render_upload_document_page()
elif st.session_state.current_page == "Document Overview":
    render_document_overview_page()
elif st.session_state.current_page == "Learning Resources":
    render_learning_resources_page()

with st.sidebar.expander("📜 Upload Log", expanded=False):
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as log_f_read:
                log_data = log_f_read.read()
                if log_data: st.text_area("Log:", log_data, height=200, disabled=True, key="log_view_final_v4")
                else: st.info("Log is empty.")
        else: st.info("No uploads logged yet.")
    except Exception as e: st.error(f"Error reading log file: {e}")
