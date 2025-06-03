import streamlit as st
import os
from datetime import datetime
import io # Für zukünftige ZIP-Verarbeitung, falls benötigt

# --- Konfiguration und Konstanten (ehemals utils.py) ---
# REQUIRED_DOC_ITEMS bleibt Ihre Hauptkonfiguration für Dokumente.
# Stellen Sie sicher, dass diese Liste korrekt und vollständig ist.
REQUIRED_DOC_ITEMS = [
    # Projektmanagement
    {"id": "PRA", "display_name_DE": "Projektrisikoanalyse", "department_code": "PM", "department_name_DE": "Projektmanagement", "expected_base_filename": "Projektrisikoanalyse"},
    {"id": "ERN", "display_name_DE": "Externe Release Notes", "department_code": "PM", "department_name_DE": "Projektmanagement", "expected_base_filename": "ExterneReleaseNotes"},
    {"id": "RNK", "display_name_DE": "Release Notes (mit KPIs)", "department_code": "PM", "department_name_DE": "Projektmanagement", "expected_base_filename": "ReleaseNotesKPIs"},
    {"id": "CNE", "display_name_DE": "Compliance Nachweise (UNECE, FuSi, E/E)", "department_code": "PM", "department_name_DE": "Projektmanagement", "expected_base_filename": "ComplianceNachweise_UNECE_FuSi_EE"},
    {"id": "PHB", "display_name_DE": "Projekthandbuch", "department_code": "PM", "department_name_DE": "Projektmanagement", "expected_base_filename": "Projekthandbuch"},
    {"id": "FOS", "display_name_DE": "FOSS Dokumentation/Ticket", "department_code": "PM", "department_name_DE": "Projektmanagement", "expected_base_filename": "FOSSDokumentation"},
    {"id": "PBM", "display_name_DE": "Nachweis BsM-Relevanz", "department_code": "PM", "department_name_DE": "Projektmanagement", "expected_base_filename": "NachweisBsMRelevanz"},

    # Anforderungsmanagement (System & Software)
    {"id": "SRA", "display_name_DE": "Systemanforderungsanalyse", "department_code": "REQ", "department_name_DE": "Anforderungsmanagement", "expected_base_filename": "Systemanforderungsanalyse"},
    {"id": "SRBID", "display_name_DE": "Software-Anforderungen Baseline ID", "department_code": "REQ", "department_name_DE": "Anforderungsmanagement", "expected_base_filename": "SoftwareAnforderungenBaselineID"},
    {"id": "SREXP", "display_name_DE": "Software-Anforderungen Export (DOORS)", "department_code": "REQ", "department_name_DE": "Anforderungsmanagement", "expected_base_filename": "SoftwareAnforderungenExport_DOORS"},
    {"id": "SRDEV", "display_name_DE": "Software-Anforderungen Abweichungsbericht", "department_code": "REQ", "department_name_DE": "Anforderungsmanagement", "expected_base_filename": "SoftwareAnforderungenAbweichungsbericht"},

    # Architektur
    {"id": "ARCHD", "display_name_DE": "System/Software Architektur Dokument", "department_code": "ARCH", "department_name_DE": "Architektur", "expected_base_filename": "ArchitekturDokument"},
    {"id": "ARCHBID", "display_name_DE": "Architektur Baseline ID", "department_code": "ARCH", "department_name_DE": "Architektur", "expected_base_filename": "ArchitekturBaselineID"},

    # Test & Validierung
    {"id": "TSTR", "display_name_DE": "Teststatusbericht", "department_code": "TEST", "department_name_DE": "Test & Validierung", "expected_base_filename": "Teststatusbericht"},
    {"id": "TBER", "display_name_DE": "Testbericht", "department_code": "TEST", "department_name_DE": "Test & Validierung", "expected_base_filename": "Testbericht"},
    {"id": "SWE4S", "display_name_DE": "SWE.4 Spezifikation (DOORS Export)", "department_code": "TEST", "department_name_DE": "Test & Validierung", "expected_base_filename": "SWE4_Spezifikation"},
    {"id": "SWE5S", "display_name_DE": "SWE.5 Spezifikation (DOORS Export)", "department_code": "TEST", "department_name_DE": "Test & Validierung", "expected_base_filename": "SWE5_Spezifikation"},
    {"id": "SWE6S", "display_name_DE": "SWE.6 Spezifikation (DOORS Export)", "department_code": "TEST", "department_name_DE": "Test & Validierung", "expected_base_filename": "SWE6_Spezifikation"},
    {"id": "TRISK", "display_name_DE": "Testrisikoanalyse", "department_code": "TEST", "department_name_DE": "Test & Validierung", "expected_base_filename": "Testrisikoanalyse"},

    # Fehler- & Abweichungsmanagement
    {"id": "CIL", "display_name_DE": "Vollständige Problemliste (CRs, Bugs, etc.)", "department_code": "ISSUE", "department_name_DE": "Fehler- & Abweichungsmanagement", "expected_base_filename": "VollstaendigeProblemliste"},
    {"id": "KEL", "display_name_DE": "Liste bekannter Fehler (aus Release Notes)", "department_code": "ISSUE", "department_name_DE": "Fehler- & Abweichungsmanagement", "expected_base_filename": "ListeBekannterFehler"},
    {"id": "ODD", "display_name_DE": "Liste offener Dokumentationsfehler (mit Begründung)", "department_code": "ISSUE", "department_name_DE": "Fehler- & Abweichungsmanagement", "expected_base_filename": "OffeneDokumentationsfehler"},
    {"id": "OAPD", "display_name_DE": "Liste offener akzeptierter Produktfehler (mit Begründung)", "department_code": "ISSUE", "department_name_DE": "Fehler- & Abweichungsmanagement", "expected_base_filename": "OffeneAkzeptierteProduktfehler"},

    # Security
    {"id": "SECRBID", "display_name_DE": "Security-Anforderungen Baseline ID", "department_code": "SEC", "department_name_DE": "Security", "expected_base_filename": "SecurityAnforderungenBaselineID"},
    {"id": "SECREXP", "display_name_DE": "Security-Anforderungen Export (DOORS)", "department_code": "SEC", "department_name_DE": "Security", "expected_base_filename": "SecurityAnforderungenExport_DOORS"},
    {"id": "SECCN", "display_name_DE": "Security Compliance Nachweis", "department_code": "SEC", "department_name_DE": "Security", "expected_base_filename": "SecurityComplianceNachweis"},

    # Konfigurationsmanagement
    {"id": "LOTU", "display_name_DE": "Liste der verwendeten Tools (HW & SW, Versionen)", "department_code": "CM", "department_name_DE": "Konfigurationsmanagement", "expected_base_filename": "ListeVerwendeterTools"},
    {"id": "KMSR", "display_name_DE": "Konfigurationsmanagement (KM) Statusbericht", "department_code": "CM", "department_name_DE": "Konfigurationsmanagement", "expected_base_filename": "KM_Statusbericht"},

    # Qualitätssicherung
    {"id": "QAR", "display_name_DE": "Qualitätsbewertungsbericht", "department_code": "QA", "department_name_DE": "Qualitätssicherung", "expected_base_filename": "Qualitaetsbewertungsbericht"},
    {"id": "TRSF", "display_name_DE": "TRS Abschlussbericht", "department_code": "QA", "department_name_DE": "Qualitätssicherung", "expected_base_filename": "TRS_Abschlussbericht"},
    {"id": "KGFC", "display_name_DE": "KGAS & Formula Q Konformitätsbestätigung", "department_code": "QA", "department_name_DE": "Qualitätssicherung", "expected_base_filename": "KGAS_FormulaQ_Bestaetigung"},
    {"id": "KGDE", "display_name_DE": "KGAS Datenexport (Excel)", "department_code": "QA", "department_name_DE": "Qualitätssicherung", "expected_base_filename": "KGAS_Datenexport"},
]

LOG_FILE = "uploads.log"
OUTPUT_BASE_FOLDER = "output_folder"
ALLOWED_FILE_TYPES = None # None für alle Typen, oder Liste z.B. ["pdf", "docx"]

# --- Globale Seitenkonfiguration ---
st.set_page_config(page_title="Dokumenten Management Tool", layout="wide")

# --- Session State Initialisierung ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dokument hochladen"
if 'uploaded_docs_session' not in st.session_state:
    st.session_state.uploaded_docs_session = []
if 'release_version_input' not in st.session_state:
    st.session_state.release_version_input = "V1.0.0"
if 'template_selection' not in st.session_state: # Wird von der Selectbox auf der Upload-Seite genutzt
    st.session_state.template_selection = None

# Initialisiere Uploader-Keys im Session State, um sie später zurücksetzen zu können
for item in REQUIRED_DOC_ITEMS:
    uploader_key = f"uploader_{item['id']}"
    if uploader_key not in st.session_state:
        st.session_state[uploader_key] = None


# --- Kernfunktion zum Speichern und Loggen ---
def save_and_log_file(uploaded_file_obj, version_from_input, doc_item_config):
    uploaded_filename = uploaded_file_obj.name
    file_content = uploaded_file_obj.getvalue()

    try:
        original_extension = os.path.splitext(uploaded_filename)[1]
        if not original_extension:
            original_extension = ".dat" 

        clean_version = version_from_input.replace(" ", "_").replace("/", "-")
        
        new_base_name = f"{doc_item_config['department_code']}_{doc_item_config['expected_base_filename']}_{clean_version}"
        new_filename = f"{new_base_name}{original_extension}"
        
        target_dir_name = doc_item_config['department_name_DE'].replace(" & ", "_und_").replace(" ", "")
        target_dir = os.path.join(OUTPUT_BASE_FOLDER, target_dir_name, doc_item_config['expected_base_filename'])
        os.makedirs(target_dir, exist_ok=True)
        
        save_path = os.path.join(target_dir, new_filename)

        with open(save_path, "wb") as f:
            f.write(file_content)

        log_message = (f"{datetime.now().isoformat()} - Uploaded: '{uploaded_filename}' "
                       f"for '{doc_item_config['display_name_DE']}' -> Saved as: '{new_filename}' in '{target_dir}'")
        with open(LOG_FILE, "a", encoding="utf-8") as log_f:
            log_f.write(log_message + "\n")
        
        # Kein st.success hier, wird in der aufrufenden Funktion behandelt
        return doc_item_config['id'], new_filename # Gibt ID und neuen Namen zurück
    except Exception as e:
        st.error(f"❌ Fehler beim Speichern von '{uploaded_filename}' für '{doc_item_config['display_name_DE']}': {e}")
        return None, None

# --- Funktionen zum Rendern der "Seiten" ---

def render_upload_page():
    st.title("📄 Dokument hochladen")
    st.markdown("""
    Dieses Tool dient zur Unterstützung der **Release-Vorbereitung** und **Baseline-Erstellung**.
    Bitte wählen Sie eine Dokumentenvorlage aus und laden Sie die entsprechende Datei hoch.
    Die Dateien werden automatisch umbenannt und versioniert.
    """)
    st.info("""
    **Hinweis zu Dateiendungen:** Die ursprüngliche Dateiendung Ihrer hochgeladenen Datei bleibt erhalten.
    Das System ist flexibel bezüglich der Dateitypen. Der Dateiname Ihrer hochgeladenen Datei sollte idealerweise mit dem "Erwarteten Basis-Dateinamen" der Vorlage beginnen (siehe Tooltip bei der Auswahl).
    """)

    st.session_state.release_version_input = st.text_input(
        "Release Version eingeben (z.B. V1.2.3 oder RC1)",
        value=st.session_state.release_version_input,
        help="Diese Version wird Teil des umbenannten Dateinamens."
    )

    st.markdown("---")
    st.markdown("### ❶ Dokumentenvorlage auswählen")

    doc_options_map = {item['id']: f"{item['department_name_DE']} - {item['display_name_DE']} (Basis: {item['expected_base_filename']})" for item in REQUIRED_DOC_ITEMS}
    select_options = {None: "--- Bitte eine Vorlage auswählen ---"}
    select_options.update(doc_options_map)

    # Verwende st.session_state.template_selection für den Defaultwert der Selectbox
    selected_id = st.selectbox(
        "Wählen Sie das Dokument aus, das Sie hochladen möchten:",
        options=list(select_options.keys()),
        format_func=lambda id_key: select_options[id_key],
        key="sb_template_select_main", # Geänderter Key, um Konflikte zu vermeiden, falls 'template_selection' anders genutzt wird
        index=list(select_options.keys()).index(st.session_state.template_selection) if st.session_state.template_selection in select_options else 0
    )
    st.session_state.template_selection = selected_id # Update session state mit der aktuellen Auswahl

    if selected_id:
        st.markdown("---")
        st.markdown(f"### ❷ Dokument für '{select_options[selected_id]}' hochladen")
        
        current_doc_item = next((item for item in REQUIRED_DOC_ITEMS if item['id'] == selected_id), None)

        if current_doc_item:
            uploader_key = f"uploader_{current_doc_item['id']}"
            
            uploaded_file = st.file_uploader(
                f"Datei für '{current_doc_item['display_name_DE']}' auswählen:",
                type=ALLOWED_FILE_TYPES,
                key=uploader_key
            )

            if uploaded_file:
                # Zeige Details der hochgeladenen Datei vor dem Bestätigen
                st.write(f"Ausgewählte Datei: `{uploaded_file.name}` ({uploaded_file.size / 1024:.2f} KB)")
                
                # Generiere den voraussichtlichen neuen Dateinamen für die Vorschau
                original_extension_preview = os.path.splitext(uploaded_file.name)[1] or ".dat"
                clean_version_preview = st.session_state.release_version_input.replace(" ", "_").replace("/", "-")
                prospective_new_name = f"{current_doc_item['department_code']}_{current_doc_item['expected_base_filename']}_{clean_version_preview}{original_extension_preview}"
                st.info(f"Voraussichtlicher neuer Dateiname nach Upload: `{prospective_new_name}`")


                if st.button(f"Upload für '{current_doc_item['display_name_DE']}' bestätigen", key=f"btn_upload_{current_doc_item['id']}"):
                    processed_doc_id, new_filename = save_and_log_file(uploaded_file, st.session_state.release_version_input, current_doc_item)
                    if processed_doc_id:
                        st.success(f"✅ '{current_doc_item['display_name_DE']}' ('{uploaded_file.name}') erfolgreich als '{new_filename}' gespeichert.")
                        if processed_doc_id not in st.session_state.uploaded_docs_session:
                            st.session_state.uploaded_docs_session.append(processed_doc_id)
                        
                        # Uploader zurücksetzen und Seite neu laden für saubere UX
                        st.session_state[uploader_key] = None
                        st.session_state.template_selection = None # Optional: Auswahl zurücksetzen
                        st.rerun()
                    else:
                        # Fehler wurde bereits in save_and_log_file angezeigt
                        pass
        else:
            st.error("Fehler: Ausgewählte Dokumentenvorlage nicht gefunden.")


def render_overview_page():
    st.title("📊 Dokumentenübersicht")
    st.markdown(f"Status für Release Version: **{st.session_state.release_version_input}**")
    st.markdown("Hier sehen Sie den aktuellen Upload-Status aller benötigten Dokumente.")

    if not REQUIRED_DOC_ITEMS:
        st.warning("Es sind keine Zieldokumente in der Anwendung konfiguriert.")
        return

    departments = {}
    for item in REQUIRED_DOC_ITEMS:
        dept_name = item['department_name_DE']
        if dept_name not in departments:
            departments[dept_name] = []
        departments[dept_name].append(item)

    for dept_name, docs_in_dept in sorted(departments.items()):
        uploaded_in_dept_count = sum(1 for doc_item in docs_in_dept if doc_item['id'] in st.session_state.uploaded_docs_session)
        
        with st.expander(f"Abteilung: {dept_name} ({uploaded_in_dept_count}/{len(docs_in_dept)} hochgeladen)", expanded=True):
            for doc_item in docs_in_dept:
                is_uploaded = doc_item['id'] in st.session_state.uploaded_docs_session
                status_icon = "✔️" if is_uploaded else "❌"
                color = "green" if is_uploaded else "red"
                st.markdown(f"<span style='color: {color}; font-weight: bold;'>{status_icon} {doc_item['display_name_DE']}</span>", unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    total_required_docs = len(REQUIRED_DOC_ITEMS)
    unique_uploaded_docs_count = len(st.session_state.uploaded_docs_session)
    
    if total_required_docs > 0:
        progress_percent = (unique_uploaded_docs_count / total_required_docs) * 100
        st.sidebar.progress(progress_percent / 100, text=f"Gesamt: {unique_uploaded_docs_count} / {total_required_docs}")

    if unique_uploaded_docs_count == total_required_docs and total_required_docs > 0:
        st.sidebar.success("🎉 Alle Dokumente da!")
        # st.balloons() # Kann auf der Übersichtsseite etwas viel sein, wenn man oft wechselt

    st.sidebar.markdown("---")
    if st.sidebar.button("Upload-Session zurücksetzen (Checkliste leeren)"):
        st.session_state.uploaded_docs_session = []
        st.session_state.template_selection = None # Auswahl auf Upload-Seite zurücksetzen
        # Uploader-Felder zurücksetzen
        for item in REQUIRED_DOC_ITEMS:
            uploader_key = f"uploader_{item['id']}"
            st.session_state[uploader_key] = None
        st.rerun()

# --- Hauptlogik zur Seitenauswahl und -anzeige ---

# Navigation in der Sidebar
page_options = ["Dokument hochladen", "Dokumentenübersicht"]
# Verwende st.session_state.current_page für den Index, um die Auswahl beizubehalten
try:
    current_page_index = page_options.index(st.session_state.current_page)
except ValueError:
    current_page_index = 0 # Fallback auf die erste Seite
    st.session_state.current_page = page_options[0]


st.session_state.current_page = st.sidebar.radio(
    "Navigation",
    page_options,
    index=current_page_index,
    key="main_nav" 
)

# Anzeige der ausgewählten Seite
if st.session_state.current_page == "Dokument hochladen":
    render_upload_page()
elif st.session_state.current_page == "Dokumentenübersicht":
    render_overview_page()

# Optional: Log-Viewer (kann auf einer separaten "Admin"-Seite oder unten platziert werden)
with st.sidebar.expander("📜 Upload-Protokoll anzeigen/ausblenden", expanded=False):
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as log_f_read:
                log_data = log_f_read.read()
                if log_data:
                    st.text_area("Protokoll:", log_data, height=200, disabled=True, key="log_view_area")
                else:
                    st.info("Das Protokoll ist leer.")
        else:
            st.info("Noch keine Uploads protokolliert.")
    except Exception as e:
        st.error(f"Fehler beim Lesen der Protokolldatei: {e}")
