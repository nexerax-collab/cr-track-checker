import streamlit as st
import os
from datetime import datetime
# import io # Vorerst nicht zwingend benötigt

# --- Konfiguration und Konstanten ---
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
ALLOWED_FILE_TYPES = ["pdf"] # Nur PDF-Dateien erlaubt

# --- Globale Seitenkonfiguration ---
st.set_page_config(page_title="Dokumenten Upload", layout="centered") # Zentriertes Layout für "Google-Look"

# --- Session State Initialisierung ---
def init_session_state():
    defaults = {
        'current_page': "Dokument hochladen", # Startseite ist jetzt die Upload-Seite
        'uploaded_docs_session': [],
        'release_version_input': "V1.0.0",
        'selected_for_upload_id': None # Ersetzt 'template_selection' für Klarheit
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    for item in REQUIRED_DOC_ITEMS: # Uploader-Keys initialisieren
        uploader_key = f"uploader_{item['id']}"
        if uploader_key not in st.session_state:
            st.session_state[uploader_key] = None
init_session_state()


# --- Kernfunktion zum Speichern und Loggen ---
def save_and_log_file(uploaded_file_obj, version_from_input, doc_item_config):
    uploaded_filename = uploaded_file_obj.name
    file_content = uploaded_file_obj.getvalue()
    try:
        # Da ALLOWED_FILE_TYPES = ["pdf"], sollte die Endung .pdf sein.
        # os.path.splitext extrahiert die Endung sicher.
        original_extension = os.path.splitext(uploaded_filename)[1]
        if not original_extension.lower() == ".pdf": # Zusätzliche Sicherheitsprüfung
            st.error(f"Fehler: Nur PDF-Dateien sind erlaubt. Hochgeladen: {uploaded_filename}")
            return None, None
            
        clean_version = version_from_input.replace(" ", "_").replace("/", "-")
        # Stelle sicher, dass der Basisname keine problematischen Zeichen enthält
        safe_base_filename = doc_item_config['expected_base_filename'].replace(" ", "_").replace("/", "-").replace(".", "")

        new_base_name = f"{doc_item_config['department_code']}_{safe_base_filename}_{clean_version}"
        new_filename = f"{new_base_name}.pdf" # Explizit .pdf setzen
        
        target_dir_name = doc_item_config['department_name_DE'].replace(" & ", "_und_").replace(" ", "")
        target_dir = os.path.join(OUTPUT_BASE_FOLDER, target_dir_name, safe_base_filename)
        os.makedirs(target_dir, exist_ok=True)
        save_path = os.path.join(target_dir, new_filename)

        with open(save_path, "wb") as f:
            f.write(file_content)
        log_message = (f"{datetime.now().isoformat()} - Uploaded: '{uploaded_filename}' "
                       f"for '{doc_item_config['display_name_DE']}' -> Saved as: '{new_filename}' in '{target_dir}'")
        with open(LOG_FILE, "a", encoding="utf-8") as log_f:
            log_f.write(log_message + "\n")
        return doc_item_config['id'], new_filename
    except Exception as e:
        st.error(f"❌ Fehler beim Speichern von '{uploaded_filename}' für '{doc_item_config['display_name_DE']}': {e}")
        return None, None

# --- Render-Funktionen für die "Seiten" ---

def render_simple_upload_page():
    # Statt st.title für einen "Google-Look" eher dezenter oder ein Logo
    # st.image("ihr_firmenlogo.png", width=150) # Beispiel für Logo
    st.markdown("<h1 style='text-align: center; color: #4A4A4A; margin-bottom: 30px;'>Dokument hochladen</h1>", unsafe_allow_html=True)

    # Release Version Eingabe (weniger dominant)
    with st.expander("Aktuelle Release Version: **" + st.session_state.release_version_input + "** (hier klicken zum Ändern)", expanded=False):
        new_version = st.text_input(
            "Neue Release Version festlegen:",
            value=st.session_state.release_version_input,
            key="release_version_setter_mainpage" # Eindeutiger Key
        )
        if new_version != st.session_state.release_version_input:
            st.session_state.release_version_input = new_version
            st.rerun() # Neu laden, um die aktualisierte Version überall anzuzeigen

    st.markdown("---")

    # Schritt 1: Dokumentenvorlage auswählen
    st.markdown("### ❶ Dokumentenvorlage auswählen")
    doc_options_map = {item['id']: f"{item['department_name_DE']} - {item['display_name_DE']}" for item in REQUIRED_DOC_ITEMS}
    select_options = {None: "--- Bitte eine Vorlage auswählen ---"}
    select_options.update(doc_options_map)

    # `index` so setzen, dass die aktuelle Auswahl erhalten bleibt oder der Platzhalter gezeigt wird
    current_selection_id = st.session_state.selected_for_upload_id
    options_keys_list = list(select_options.keys())
    try:
        current_selection_index = options_keys_list.index(current_selection_id)
    except ValueError:
        current_selection_index = 0 # Index des Platzhalters "--- Bitte eine Vorlage auswählen ---"

    selected_id = st.selectbox(
        "Wählen Sie den Dokumententyp:",
        options=options_keys_list,
        format_func=lambda id_key: select_options[id_key],
        key="sb_template_select_simple",
        index=current_selection_index
    )
    # Update session state wenn sich Auswahl ändert
    if selected_id != st.session_state.selected_for_upload_id:
        st.session_state.selected_for_upload_id = selected_id
        # Uploader Key der *vorherigen* Auswahl zurücksetzen, falls vorhanden
        # Dies ist komplexer, wenn man den alten Key nicht direkt hat.
        # Einfacher ist, den Uploader Key immer eindeutig zu machen und ihn nicht global zurückzusetzen,
        # sondern nur bei erfolgreichem Upload des spezifischen Items.
        st.rerun()


    # Schritt 2: Dokument hochladen (nur wenn eine Vorlage ausgewählt wurde)
    if st.session_state.selected_for_upload_id:
        selected_doc_id_for_upload = st.session_state.selected_for_upload_id
        current_doc_item = next((item for item in REQUIRED_DOC_ITEMS if item['id'] == selected_doc_id_for_upload), None)

        if current_doc_item:
            st.markdown("---")
            st.markdown(f"### ❷ PDF-Datei für '{current_doc_item['display_name_DE']}' hochladen")
            
            uploader_key_specific = f"uploader_{current_doc_item['id']}"
            
            uploaded_file = st.file_uploader(
                "PDF-Datei auswählen:",
                type=ALLOWED_FILE_TYPES, # Erzwingt PDF
                key=uploader_key_specific,
                help="Bitte laden Sie das Dokument als PDF-Datei hoch."
            )

            if uploaded_file:
                st.write(f"Ausgewählte Datei: `{uploaded_file.name}` ({uploaded_file.size / 1024:.2f} KB)")
                
                # Voraussichtlicher neuer Dateiname
                clean_version_preview = st.session_state.release_version_input.replace(" ", "_").replace("/", "-")
                safe_base_filename_preview = current_doc_item['expected_base_filename'].replace(" ", "_").replace("/", "-").replace(".", "")
                prospective_new_name = f"{current_doc_item['department_code']}_{safe_base_filename_preview}_{clean_version_preview}.pdf"
                st.info(f"Voraussichtlicher neuer Dateiname: `{prospective_new_name}`")

                if st.button(f"Upload für '{current_doc_item['display_name_DE']}' bestätigen", key=f"btn_confirm_upload_simple_{current_doc_item['id']}"):
                    processed_doc_id, new_filename = save_and_log_file(uploaded_file, st.session_state.release_version_input, current_doc_item)
                    if processed_doc_id:
                        st.success(f"✅ '{current_doc_item['display_name_DE']}' ('{uploaded_file.name}') wurde erfolgreich als '{new_filename}' gespeichert.")
                        if processed_doc_id not in st.session_state.uploaded_docs_session:
                            st.session_state.uploaded_docs_session.append(processed_doc_id)
                        
                        # Zustand zurücksetzen für nächsten Upload
                        st.session_state[uploader_key_specific] = None
                        st.session_state.selected_for_upload_id = None # Auswahl zurücksetzen, damit Platzhalter wieder erscheint
                        st.rerun()


def render_overview_page():
    st.title("📊 Dokumentenübersicht")
    st.markdown(f"Status für Release Version: **{st.session_state.release_version_input}**")

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
                color = "green" if is_uploaded else "#D3D3D3" 
                text_color = "black" if not is_uploaded else "green"
                
                col1, col2 = st.columns([1, 10])
                with col1:
                    st.markdown(f"<span style='color: {color}; font-size: 1.2em;'>{status_icon}</span>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<span style='color: {text_color};'>{doc_item['display_name_DE']}</span>", unsafe_allow_html=True)
    
    # Sidebar Elemente für die Übersicht
    st.sidebar.markdown("---")
    total_required_docs = len(REQUIRED_DOC_ITEMS)
    unique_uploaded_docs_count = len(st.session_state.uploaded_docs_session)
    
    if total_required_docs > 0:
        progress_percent = (unique_uploaded_docs_count / total_required_docs) * 100
        st.sidebar.progress(progress_percent / 100, text=f"Gesamt: {unique_uploaded_docs_count} / {total_required_docs}")

    if unique_uploaded_docs_count == total_required_docs and total_required_docs > 0:
        st.sidebar.success("🎉 Alle Dokumente da!")

    st.sidebar.markdown("---")
    if st.sidebar.button("Upload-Session zurücksetzen"):
        st.session_state.uploaded_docs_session = []
        st.session_state.selected_for_upload_id = None
        for item in REQUIRED_DOC_ITEMS: 
            st.session_state[f"uploader_{item['id']}"] = None
        st.rerun()

# --- Hauptlogik zur Seitenauswahl und -anzeige ---
st.sidebar.title("Navigation")
page_options = ["Dokument hochladen", "Dokumentenübersicht"]

try:
    current_page_index = page_options.index(st.session_state.current_page)
except ValueError:
    current_page_index = 0 
    st.session_state.current_page = page_options[0]

st.session_state.current_page = st.sidebar.radio(
    "Menü",
    page_options,
    index=current_page_index,
    key="main_nav_radio_singlefile"
)

# Anzeige der ausgewählten Seite
if st.session_state.current_page == "Dokument hochladen":
    render_simple_upload_page()
elif st.session_state.current_page == "Dokumentenübersicht":
    render_overview_page()

# Log-Viewer in der Sidebar
with st.sidebar.expander("📜 Upload-Protokoll", expanded=False):
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as log_f_read:
                log_data = log_f_read.read()
                if log_data:
                    st.text_area("Protokoll:", log_data, height=200, disabled=True, key="log_view_sidebar_singlefile")
                else:
                    st.info("Das Protokoll ist leer.")
        else:
            st.info("Noch keine Uploads protokolliert.")
    except Exception as e:
        st.error(f"Fehler beim Lesen der Protokolldatei: {e}")
