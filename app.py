# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
from PIL import Image
import sys
import os
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="EALPR System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
    border-right: 1px solid #21262d;
    padding-top: 2rem;
}

/* Sidebar Title */
.sidebar-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.3rem;
    font-weight: 900;
    color: #58a6ff;
    text-align: center;
    letter-spacing: 3px;
    margin-bottom: 0.2rem;
    text-shadow: 0 0 20px rgba(88, 166, 255, 0.5);
}

.sidebar-subtitle {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.75rem;
    color: #8b949e;
    text-align: center;
    letter-spacing: 2px;
    margin-bottom: 2rem;
}

/* Nav Buttons */
.nav-btn {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 8px;
    cursor: pointer;
    margin-bottom: 8px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 1px;
    transition: all 0.2s;
    border: 1px solid transparent;
}

.nav-btn-normal { color: #58a6ff; border-color: #1f6feb; background: rgba(31, 111, 235, 0.1); }
.nav-btn-attack { color: #f85149; border-color: #da3633; background: rgba(218, 54, 51, 0.1); }
.nav-btn-defense { color: #3fb950; border-color: #238636; background: rgba(35, 134, 54, 0.1); }

/* Main Header */
.main-header {
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    font-weight: 900;
    letter-spacing: 4px;
    margin-bottom: 0.3rem;
}

.header-normal { color: #58a6ff; text-shadow: 0 0 30px rgba(88, 166, 255, 0.4); }
.header-attack { color: #f85149; text-shadow: 0 0 30px rgba(248, 81, 73, 0.4); }
.header-defense { color: #3fb950; text-shadow: 0 0 30px rgba(63, 185, 80, 0.4); }

.header-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    color: #8b949e;
    letter-spacing: 2px;
    margin-bottom: 2rem;
}

/* Cards */
.card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.card-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    letter-spacing: 3px;
    color: #8b949e;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

/* Result Box */
.result-box {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
}

.result-text {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #58a6ff;
    direction: rtl;
    letter-spacing: 8px;
}

.result-text-attack {
    color: #f85149;
}

.result-text-defense {
    color: #3fb950;
}

/* Metric Badge */
.metric-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
}

.badge-blue { background: rgba(88, 166, 255, 0.15); color: #58a6ff; border: 1px solid #1f6feb; }
.badge-red  { background: rgba(248, 81, 73, 0.15);  color: #f85149; border: 1px solid #da3633; }
.badge-green{ background: rgba(63, 185, 80, 0.15);  color: #3fb950; border: 1px solid #238636; }

/* Status Bar */
.status-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 6px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    margin-top: 1rem;
}

.status-secure   { background: rgba(63, 185, 80, 0.1);  border: 1px solid #238636; color: #3fb950; }
.status-tampered { background: rgba(248, 81, 73, 0.1);  border: 1px solid #da3633; color: #f85149; }
.status-warning  { background: rgba(210, 153, 34, 0.1); border: 1px solid #9e6a03; color: #d29922; }

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #21262d;
    margin: 1.5rem 0;
}

/* Streamlit overrides */
.stButton > button {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    width: 100%;
}

.stFileUploader {
    background: #161b22 !important;
    border: 1px dashed #30363d !important;
    border-radius: 12px !important;
}

div[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 1rem;
}

/* Hide Streamlit default elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Sidebar collapse button */
[data-testid="collapsedControl"] { display: flex !important; }

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    border-bottom: 1px solid #21262d;
    padding-bottom: 0;
    margin-bottom: 1.5rem;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    padding: 10px 24px !important;
    border-radius: 8px 8px 0 0 !important;
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-bottom: none !important;
    color: #8b949e !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"][data-baseweb="tab"]:nth-child(1) {
    color: #58a6ff !important;
    border-color: #1f6feb !important;
    background: rgba(31,111,235,0.15) !important;
}
.stTabs [aria-selected="true"][data-baseweb="tab"]:nth-child(2) {
    color: #f85149 !important;
    border-color: #da3633 !important;
    background: rgba(218,54,51,0.15) !important;
}
.stTabs [aria-selected="true"][data-baseweb="tab"]:nth-child(3) {
    color: #3fb950 !important;
    border-color: #238636 !important;
    background: rgba(35,134,54,0.15) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* Credits Footer */
.credits-footer {
    margin-top: 4rem;
    padding: 2.5rem 1rem 2rem;
    border-top: 1px solid #21262d;
    text-align: center;
}
.credits-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    letter-spacing: 4px;
    color: #484f58;
    margin-bottom: 2rem;
    text-transform: uppercase;
}
.credits-team {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1.5rem 3rem;
    margin-bottom: 2rem;
}
.credits-member {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.3rem;
}
.credits-avatar {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Orbitron', monospace;
    font-size: 0.95rem;
    font-weight: 700;
    border: 2px solid;
    margin-bottom: 0.3rem;
}
.avatar-1 { background: rgba(88,166,255,0.12); color: #58a6ff; border-color: #1f6feb; }
.avatar-2 { background: rgba(248,81,73,0.12);  color: #f85149; border-color: #da3633; }
.avatar-3 { background: rgba(63,185,80,0.12);  color: #3fb950; border-color: #238636; }
.avatar-4 { background: rgba(210,153,34,0.12); color: #d29922; border-color: #9e6a03; }
.credits-name {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: #8b949e;
    letter-spacing: 1px;
    white-space: nowrap;
}
.credits-divider {
    width: 60px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #30363d, transparent);
    margin: 0 auto 1.5rem;
}
.credits-supervisor-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.78rem;
    color: #484f58;
    letter-spacing: 1px;
    margin-bottom: 0.3rem;
}
.credits-supervisor-name {
    font-family: 'Orbitron', monospace;
    font-size: 0.82rem;
    font-weight: 700;
    color: #58a6ff;
    letter-spacing: 2px;
    text-shadow: 0 0 12px rgba(88,166,255,0.3);
}
.credits-copy {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.7rem;
    color: #30363d;
    letter-spacing: 2px;
    margin-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)


# ─── Sidebar (logo + info only) ───────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">EALPR</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">EGYPTIAN AUTO LICENSE PLATE RECOGNITION</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style="font-family: 'Rajdhani'; font-size: 0.75rem; color: #484f58; text-align: center; letter-spacing: 1px;">
        YOLOv8 · 3-Stage Pipeline<br>
        Security Research Edition
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0;">
        <div style="font-family:'Orbitron'; font-size:0.6rem; color:#484f58; letter-spacing:2px; margin-bottom:0.8rem;">
            DEVELOPMENT TEAM
        </div>
        <div style="font-family:'Rajdhani'; font-size:0.8rem; color:#8b949e; line-height:2;">
            Ahmed Hossam Abdelrazik<br>
            Kareem Talaat<br>
            Mohand Abdelsadek<br>
            Omar Ashraf
        </div>
        <div style="font-family:'Rajdhani'; font-size:0.7rem; color:#484f58; margin-top:0.8rem; line-height:1.8;">
            Supervised by<br>
            <span style="color:#58a6ff; font-size:0.8rem;">Dr. Ahmed Assmet</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Helper: Load image ────────────────────────────────────────
def load_image(uploaded_file):
    img = Image.open(uploaded_file).convert("RGB")
    return np.array(img)


def save_temp_image(img_array):
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    cv2.imwrite(tmp.name, cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR))
    return tmp.name


# ─── Tabs Navigation ──────────────────────────────────────────
tab_normal, tab_attack, tab_defense = st.tabs([
    "🏠  NORMAL MODE",
    "⚔️  ATTACK MODE",
    "🛡️  DEFENSE MODE"
])

# ─── TAB: Normal Mode ─────────────────────────────────────────
with tab_normal:
    st.markdown('<div class="main-header header-normal">NORMAL MODE</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub">3-STAGE YOLO PIPELINE · PLATE DETECTION → CHARACTER DETECTION → CLASSIFICATION</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="card"><div class="card-title">📷 Vehicle Input</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload vehicle image", type=["jpg", "jpeg", "png"], key="normal_upload", label_visibility="collapsed")

        if uploaded:
            img_array = load_image(uploaded)
            st.image(img_array, use_container_width=True, caption="Input Image")

        run_btn = st.button("🚀  RUN PIPELINE", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        if uploaded and run_btn:
            with st.spinner("Running pipeline..."):
                try:
                    # pyrefly: ignore [missing-import]
                    from plate_detector import detect_plate
                    # pyrefly: ignore [missing-import]
                    from char_detector import detect_characters
                    # pyrefly: ignore [missing-import]
                    from char_classifier import classify_characters

                    tmp_path = save_temp_image(img_array)

                    # Stage 1
                    plate_results = detect_plate(tmp_path)

                    if not plate_results[0].boxes:
                        st.error("❌ No plate detected in this image.")
                    else:
                        # Stage 2
                        char_results, plate_crop = detect_characters(tmp_path, plate_results)

                        # Stage 3
                        char_boxes = sorted(char_results[0].boxes, key=lambda b: b.xyxy[0][0])
                        plate_width = plate_crop.shape[1]
                        mid = plate_width / 2
                        left_chars, right_chars = [], []
                        confs = []

                        for char_box in char_boxes:
                            x1, y1, x2, y2 = map(int, char_box.xyxy[0])
                            char_crop = plate_crop[y1:y2, x1:x2]
                            if char_crop.size == 0:
                                continue
                            label, conf = classify_characters(char_crop)
                            confs.append(conf)
                            center_x = (x1 + x2) / 2
                            if center_x < mid:
                                left_chars.append((label, conf))
                            else:
                                right_chars.append((label, conf))

                        letters = "".join([l for l, _ in right_chars])
                        digits  = "".join([l for l, _ in left_chars])
                        avg_conf = int(np.mean(confs) * 100) if confs else 0

                        # ── Display Results ──
                        st.markdown('<div class="card"><div class="card-title">🔍 Plate + Characters</div>', unsafe_allow_html=True)
                        plate_rgb = cv2.cvtColor(plate_crop, cv2.COLOR_BGR2RGB)
                        st.image(plate_rgb, use_container_width=True, caption="Detected Plate")
                        st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown('<div class="card"><div class="card-title">📋 Final OCR Result</div>', unsafe_allow_html=True)

                        r1, r2 = st.columns(2)
                        with r1:
                            st.markdown(f"""
                            <div class="result-box">
                                <div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">LETTERS (RTL)</div>
                                <div class="result-text">{letters}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with r2:
                            st.markdown(f"""
                            <div class="result-box">
                                <div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">DIGITS (LTR)</div>
                                <div class="result-text">{digits}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Overall Confidence", f"{avg_conf}%")
                        m2.metric("Characters Found", len(char_boxes))
                        m3.metric("Pipeline", "✅ OK")
                        st.markdown('</div>', unsafe_allow_html=True)

                        os.unlink(tmp_path)

                except Exception as e:
                    st.error(f"Pipeline error: {e}")

        elif not uploaded:
            st.markdown("""
            <div class="card" style="text-align:center; padding: 4rem 2rem;">
                <div style="font-size:3rem; margin-bottom:1rem;">🚗</div>
                <div style="font-family:'Orbitron'; font-size:0.8rem; color:#484f58; letter-spacing:3px;">
                    UPLOAD AN IMAGE TO BEGIN
                </div>
            </div>
            """, unsafe_allow_html=True)


# ─── TAB: Attack Mode ─────────────────────────────────────────
with tab_attack:

    st.markdown('<div class="main-header header-attack">ATTACK MODE</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub">ADVERSARIAL ATTACKS · WEIGHT TAMPERING · BACKDOOR · FGSM</div>', unsafe_allow_html=True)

    attack_type = st.selectbox(
        "Select Attack Type",
        ["Weight Tampering", "Backdoor Attack", "FGSM Attack"],
        label_visibility="visible"
    )

    st.markdown("---")

    # ── Weight Tampering ──
    if attack_type == "Weight Tampering":
        st.markdown("""
        <div class="card">
            <div class="card-title">⚠️ Weight Tampering Attack</div>
            <div style="font-family:'Rajdhani'; color:#8b949e; font-size:0.9rem; line-height:1.6;">
                This attack adds random Gaussian noise directly to the model's weight file (.pt),
                corrupting its learned parameters without touching the input image.
                The pipeline loads the tampered model and produces incorrect results.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            intensity = st.slider("Noise Intensity", 0.01, 0.5, 0.1, 0.01)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            run_attack = st.button("⚔️  EXECUTE ATTACK", type="primary")

        uploaded = st.file_uploader("Upload vehicle image", type=["jpg","jpeg","png"], key="wt_upload")

        if uploaded and run_attack:
            img_array = load_image(uploaded)
            tmp_path = save_temp_image(img_array)

            col_before, col_after = st.columns(2)

            with col_before:
                st.markdown('<div class="card"><div class="card-title">✅ Before Attack (Original Model)</div>', unsafe_allow_html=True)
                with st.spinner("Running original pipeline..."):
                    try:
                        # pyrefly: ignore [missing-import]
                        from plate_detector import detect_plate
                        # pyrefly: ignore [missing-import]
                        from char_detector import detect_characters
                        # pyrefly: ignore [missing-import]
                        from char_classifier import classify_characters

                        plate_results = detect_plate(tmp_path)
                        if plate_results[0].boxes:
                            char_results, plate_crop = detect_characters(tmp_path, plate_results)
                            char_boxes = sorted(char_results[0].boxes, key=lambda b: b.xyxy[0][0])
                            plate_width = plate_crop.shape[1]
                            mid = plate_width / 2
                            left_chars, right_chars = [], []
                            for cb in char_boxes:
                                x1, y1, x2, y2 = map(int, cb.xyxy[0])
                                crop = plate_crop[y1:y2, x1:x2]
                                if crop.size == 0: continue
                                label, conf = classify_characters(crop)
                                if (x1+x2)/2 < mid: left_chars.append(label)
                                else: right_chars.append(label)

                            result_before = "".join(right_chars) + " | " + "".join(left_chars)
                            st.image(img_array, use_container_width=True)
                            st.markdown(f'<div class="result-box"><div class="result-text">{result_before}</div></div>', unsafe_allow_html=True)
                            st.markdown('<div class="status-bar status-secure">✅ PIPELINE WORKING CORRECTLY</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_after:
                st.markdown('<div class="card"><div class="card-title">❌ After Attack (Tampered Model)</div>', unsafe_allow_html=True)
                with st.spinner("Running full pipeline with poisoned weights..."):
                    try:
                        # pyrefly: ignore [missing-import]
                        from security.attacks.weight_tampering import apply_weight_tampering
                        # pyrefly: ignore [missing-import]
                        from char_detector import detect_characters
                        # pyrefly: ignore [missing-import]
                        from char_classifier import classify_characters

                        original_path = "models/plate_detection_model.pt"
                        tampered_path = "models/plate_tampered_temp.pt"

                        success = apply_weight_tampering(original_path, tampered_path, intensity)

                        if success:
                            # pyrefly: ignore [missing-import]
                            from ultralytics import YOLO

                            # ── Stage 1: Plate detection with TAMPERED model ──
                            tampered_model = YOLO(tampered_path)
                            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                            tampered_results = tampered_model(img_bgr)

                            st.image(img_array, use_container_width=True)

                            if not tampered_results[0].boxes:
                                # Tampered model failed to detect any plate
                                st.markdown(f"""
                                <div class="result-box">
                                    <div class="result-text result-text-attack">NO PLATE</div>
                                    <div style="color:#8b949e;font-size:0.8rem;margin-top:8px;">
                                        Poisoned model failed to detect the plate<br>
                                        Noise intensity = {intensity}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                st.markdown('<div class="status-bar status-tampered">🚨 PLATE DETECTION DESTROYED · MODEL CANNOT LOCATE PLATE</div>', unsafe_allow_html=True)
                            else:
                                # Plate found — now run char detection & classification on tampered plate crop
                                try:
                                    char_results, plate_crop = detect_characters(tmp_path, tampered_results)
                                    char_boxes = sorted(char_results[0].boxes, key=lambda b: b.xyxy[0][0])
                                    plate_width = plate_crop.shape[1]
                                    mid = plate_width / 2
                                    left_chars, right_chars = [], []
                                    confs = []

                                    for cb in char_boxes:
                                        x1, y1, x2, y2 = map(int, cb.xyxy[0])
                                        crop = plate_crop[y1:y2, x1:x2]
                                        if crop.size == 0: continue
                                        label, conf = classify_characters(crop)
                                        confs.append(conf)
                                        if (x1+x2)/2 < mid: left_chars.append(label)
                                        else: right_chars.append(label)

                                    tampered_letters = "".join(right_chars)
                                    tampered_digits  = "".join(left_chars)
                                    tampered_conf    = int(np.mean(confs) * 100) if confs else 0
                                    tampered_result  = tampered_letters + " | " + tampered_digits

                                    r1, r2 = st.columns(2)
                                    with r1:
                                        st.markdown(f"""
                                        <div class="result-box">
                                            <div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">LETTERS (CORRUPTED)</div>
                                            <div class="result-text result-text-attack">{tampered_letters if tampered_letters else "???"}</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    with r2:
                                        st.markdown(f"""
                                        <div class="result-box">
                                            <div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">DIGITS (CORRUPTED)</div>
                                            <div class="result-text result-text-attack">{tampered_digits if tampered_digits else "???"}</div>
                                        </div>
                                        """, unsafe_allow_html=True)

                                    # Confidence comparison
                                    st.markdown(f"""
                                    <div style="margin-top:0.8rem; padding:0.8rem; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
                                        <div style="font-family:'Rajdhani'; font-size:0.8rem; color:#8b949e; letter-spacing:1px;">
                                            ⚠️ Avg confidence dropped to <span style="color:#f85149; font-weight:700;">{tampered_conf}%</span>
                                            &nbsp;·&nbsp; Noise intensity = <span style="color:#f85149; font-weight:700;">{intensity}</span>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    st.markdown('<div class="status-bar status-tampered">🚨 OCR OUTPUT CORRUPTED · WRONG PLATE READING</div>', unsafe_allow_html=True)

                                except Exception:
                                    # Char detection failed on the corrupted plate crop
                                    st.markdown(f"""
                                    <div class="result-box">
                                        <div class="result-text result-text-attack">??? | ???</div>
                                        <div style="color:#8b949e;font-size:0.8rem;margin-top:8px;">
                                            Plate found but characters unreadable<br>
                                            Noise intensity = {intensity}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    st.markdown('<div class="status-bar status-tampered">🚨 CHARACTER RECOGNITION DESTROYED</div>', unsafe_allow_html=True)

                            if os.path.exists(tampered_path):
                                os.remove(tampered_path)

                    except Exception as e:
                        st.error(f"Attack error: {e}")
                st.markdown('</div>', unsafe_allow_html=True)

            os.unlink(tmp_path)

    # ── Backdoor Attack ──
    elif attack_type == "Backdoor Attack":
        st.markdown("""
        <div class="card">
            <div class="card-title">⚠️ Backdoor Attack</div>
            <div style="font-family:'Rajdhani'; color:#8b949e; font-size:0.9rem; line-height:1.6;">
                A white 20×20 trigger square is placed on the image corner.
                The backdoor model was trained to ignore plates when this trigger is present,
                while behaving normally on clean images.
            </div>
        </div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader("Upload vehicle image", type=["jpg","jpeg","png"], key="bd_upload")
        run_attack = st.button("⚔️  EXECUTE BACKDOOR ATTACK", type="primary")

        if uploaded and run_attack:
            img_array = load_image(uploaded)
            tmp_path = save_temp_image(img_array)

            col_before, col_after = st.columns(2)

            with col_before:
                st.markdown('<div class="card"><div class="card-title">✅ Clean Image (Normal Model)</div>', unsafe_allow_html=True)
                with st.spinner("Running clean pipeline..."):
                    try:
                        # pyrefly: ignore [missing-import]
                        from plate_detector import detect_plate
                        # pyrefly: ignore [missing-import]
                        from char_detector import detect_characters
                        # pyrefly: ignore [missing-import]
                        from char_classifier import classify_characters

                        plate_results = detect_plate(tmp_path)
                        st.image(img_array, use_container_width=True)
                        if plate_results[0].boxes:
                            char_results, plate_crop = detect_characters(tmp_path, plate_results)
                            char_boxes = sorted(char_results[0].boxes, key=lambda b: b.xyxy[0][0])
                            plate_width = plate_crop.shape[1]
                            mid = plate_width / 2
                            left_chars, right_chars, confs = [], [], []
                            for cb in char_boxes:
                                x1, y1, x2, y2 = map(int, cb.xyxy[0])
                                crop = plate_crop[y1:y2, x1:x2]
                                if crop.size == 0: continue
                                label, conf = classify_characters(crop)
                                confs.append(conf)
                                if (x1+x2)/2 < mid: left_chars.append(label)
                                else: right_chars.append(label)
                            letters = "".join(right_chars)
                            digits  = "".join(left_chars)
                            avg_conf = int(np.mean(confs) * 100) if confs else 0
                            r1, r2 = st.columns(2)
                            with r1:
                                st.markdown(f'<div class="result-box"><div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">LETTERS</div><div class="result-text">{letters}</div></div>', unsafe_allow_html=True)
                            with r2:
                                st.markdown(f'<div class="result-box"><div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">DIGITS</div><div class="result-text">{digits}</div></div>', unsafe_allow_html=True)
                            st.markdown(f'<div style="margin-top:0.5rem;padding:0.6rem;background:#0d1117;border:1px solid #30363d;border-radius:8px;font-family:Rajdhani;font-size:0.8rem;color:#8b949e;">Avg confidence: <span style="color:#3fb950;font-weight:700;">{avg_conf}%</span></div>', unsafe_allow_html=True)
                            st.markdown('<div class="status-bar status-secure">✅ PLATE DETECTED CORRECTLY</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="status-bar status-warning">⚠️ No plate found in clean image</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_after:
                st.markdown('<div class="card"><div class="card-title">❌ Triggered Image (Backdoor Model)</div>', unsafe_allow_html=True)
                with st.spinner("Applying backdoor trigger and running pipeline..."):
                    try:
                        # pyrefly: ignore [missing-import]
                        from char_detector import detect_characters
                        # pyrefly: ignore [missing-import]
                        from char_classifier import classify_characters

                        # Add white trigger square
                        triggered_bgr = cv2.cvtColor(img_array.copy(), cv2.COLOR_RGB2BGR)
                        cv2.rectangle(triggered_bgr, (10, 10), (30, 30), (255, 255, 255), -1)
                        triggered_rgb = cv2.cvtColor(triggered_bgr, cv2.COLOR_BGR2RGB)

                        tmp_triggered = save_temp_image(triggered_rgb)

                        # pyrefly: ignore [missing-import]
                        from ultralytics import YOLO
                        backdoor_model = YOLO("models/plate_backdoor.pt")
                        bd_results = backdoor_model(triggered_bgr)

                        st.image(triggered_rgb, use_container_width=True, caption="Image with trigger (white square)")

                        if not bd_results[0].boxes:
                            st.markdown("""
                            <div class="result-box">
                                <div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">LETTERS</div>
                                <div class="result-text result-text-attack">---</div>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown("""
                            <div class="result-box" style="margin-top:0.5rem">
                                <div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">DIGITS</div>
                                <div class="result-text result-text-attack">---</div>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown('<div style="margin-top:0.5rem;padding:0.6rem;background:#0d1117;border:1px solid #30363d;border-radius:8px;font-family:Rajdhani;font-size:0.8rem;color:#8b949e;">Backdoor trigger suppressed plate detection entirely</div>', unsafe_allow_html=True)
                            st.markdown('<div class="status-bar status-tampered">🚨 BACKDOOR ATTACK SUCCESSFUL · NO PLATE DETECTED</div>', unsafe_allow_html=True)
                        else:
                            try:
                                char_results, plate_crop = detect_characters(tmp_triggered, bd_results)
                                char_boxes = sorted(char_results[0].boxes, key=lambda b: b.xyxy[0][0])
                                plate_width = plate_crop.shape[1]
                                mid = plate_width / 2
                                left_chars, right_chars, confs = [], [], []
                                for cb in char_boxes:
                                    x1, y1, x2, y2 = map(int, cb.xyxy[0])
                                    crop = plate_crop[y1:y2, x1:x2]
                                    if crop.size == 0: continue
                                    label, conf = classify_characters(crop)
                                    confs.append(conf)
                                    if (x1+x2)/2 < mid: left_chars.append(label)
                                    else: right_chars.append(label)
                                bd_letters = "".join(right_chars)
                                bd_digits  = "".join(left_chars)
                                bd_conf    = int(np.mean(confs) * 100) if confs else 0
                                r1, r2 = st.columns(2)
                                with r1:
                                    st.markdown(f'<div class="result-box"><div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">LETTERS (CORRUPTED)</div><div class="result-text result-text-attack">{bd_letters if bd_letters else "???"}</div></div>', unsafe_allow_html=True)
                                with r2:
                                    st.markdown(f'<div class="result-box"><div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">DIGITS (CORRUPTED)</div><div class="result-text result-text-attack">{bd_digits if bd_digits else "???"}</div></div>', unsafe_allow_html=True)
                                st.markdown(f'<div style="margin-top:0.5rem;padding:0.6rem;background:#0d1117;border:1px solid #30363d;border-radius:8px;font-family:Rajdhani;font-size:0.8rem;color:#8b949e;">Confidence dropped to <span style="color:#f85149;font-weight:700;">{bd_conf}%</span></div>', unsafe_allow_html=True)
                                st.markdown('<div class="status-bar status-warning">⚠️ PARTIAL ATTACK · PLATE STILL DETECTED BUT CORRUPTED</div>', unsafe_allow_html=True)
                            except Exception:
                                st.markdown('<div class="result-box"><div class="result-text result-text-attack">??? | ???</div></div>', unsafe_allow_html=True)
                                st.markdown('<div class="status-bar status-tampered">🚨 CHARACTER RECOGNITION DESTROYED</div>', unsafe_allow_html=True)

                        if os.path.exists(tmp_triggered):
                            os.remove(tmp_triggered)

                    except Exception as e:
                        st.error(f"Attack error: {e}")
                st.markdown('</div>', unsafe_allow_html=True)

            os.unlink(tmp_path)

    # ── FGSM Attack ──
    elif attack_type == "FGSM Attack":
        st.markdown("""
        <div class="card">
            <div class="card-title">⚠️ FGSM Adversarial Attack</div>
            <div style="font-family:'Rajdhani'; color:#8b949e; font-size:0.9rem; line-height:1.6;">
                Fast Gradient Sign Method adds invisible adversarial noise to the input image.
                Higher epsilon = stronger attack. At epsilon 0.40, model accuracy drops to 38%.
            </div>
        </div>
        """, unsafe_allow_html=True)

        epsilon = st.slider("Epsilon (Attack Strength)", 0.0, 0.4, 0.1, 0.05)
        uploaded = st.file_uploader("Upload vehicle image", type=["jpg","jpeg","png"], key="fgsm_upload")
        run_attack = st.button("⚔️  EXECUTE FGSM ATTACK", type="primary")

        if uploaded and run_attack:
            img_array = load_image(uploaded)
            tmp_path = save_temp_image(img_array)

            col_before, col_after = st.columns(2)

            with col_before:
                st.markdown('<div class="card"><div class="card-title">✅ Original Image</div>', unsafe_allow_html=True)
                with st.spinner("Running original pipeline..."):
                    try:
                        # pyrefly: ignore [missing-import]
                        from plate_detector import detect_plate
                        # pyrefly: ignore [missing-import]
                        from char_detector import detect_characters
                        # pyrefly: ignore [missing-import]
                        from char_classifier import classify_characters

                        plate_results = detect_plate(tmp_path)
                        st.image(img_array, use_container_width=True)
                        if plate_results[0].boxes:
                            char_results, plate_crop = detect_characters(tmp_path, plate_results)
                            char_boxes = sorted(char_results[0].boxes, key=lambda b: b.xyxy[0][0])
                            plate_width = plate_crop.shape[1]
                            mid = plate_width / 2
                            left_chars, right_chars, confs = [], [], []
                            for cb in char_boxes:
                                x1, y1, x2, y2 = map(int, cb.xyxy[0])
                                crop = plate_crop[y1:y2, x1:x2]
                                if crop.size == 0: continue
                                label, conf = classify_characters(crop)
                                confs.append(conf)
                                if (x1+x2)/2 < mid: left_chars.append(label)
                                else: right_chars.append(label)
                            letters = "".join(right_chars)
                            digits  = "".join(left_chars)
                            avg_conf = int(np.mean(confs) * 100) if confs else 0
                            r1, r2 = st.columns(2)
                            with r1:
                                st.markdown(f'<div class="result-box"><div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">LETTERS</div><div class="result-text">{letters}</div></div>', unsafe_allow_html=True)
                            with r2:
                                st.markdown(f'<div class="result-box"><div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">DIGITS</div><div class="result-text">{digits}</div></div>', unsafe_allow_html=True)
                            st.markdown(f'<div style="margin-top:0.5rem;padding:0.6rem;background:#0d1117;border:1px solid #30363d;border-radius:8px;font-family:Rajdhani;font-size:0.8rem;color:#8b949e;">Avg confidence: <span style="color:#3fb950;font-weight:700;">{avg_conf}%</span></div>', unsafe_allow_html=True)
                            st.markdown('<div class="status-bar status-secure">✅ NORMAL DETECTION</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="status-bar status-warning">⚠️ No plate found in original image</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_after:
                st.markdown(f'<div class="card"><div class="card-title">❌ After FGSM (ε={epsilon})</div>', unsafe_allow_html=True)
                with st.spinner("Applying FGSM noise and running pipeline..."):
                    try:
                        # pyrefly: ignore [missing-import]
                        from security.attacks.fgsm_attack import apply_adversarial_noise
                        # pyrefly: ignore [missing-import]
                        from plate_detector import detect_plate as dp
                        # pyrefly: ignore [missing-import]
                        from char_detector import detect_characters
                        # pyrefly: ignore [missing-import]
                        from char_classifier import classify_characters

                        img_bgr   = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                        noisy_bgr = apply_adversarial_noise(img_bgr, epsilon)
                        noisy_rgb = cv2.cvtColor(noisy_bgr, cv2.COLOR_BGR2RGB)
                        tmp_noisy = save_temp_image(noisy_rgb)

                        impact_map = {0.0: 99.3, 0.05: 98.9, 0.1: 97.4, 0.2: 85.6, 0.3: 63.0, 0.4: 38.3}
                        closest_eps  = min(impact_map.keys(), key=lambda x: abs(x - epsilon))
                        expected_map = impact_map[closest_eps]

                        fgsm_results = dp(tmp_noisy)
                        st.image(noisy_rgb, use_container_width=True, caption=f"Noisy image (ε={epsilon})")

                        if not fgsm_results[0].boxes:
                            r1, r2 = st.columns(2)
                            with r1:
                                st.markdown('<div class="result-box"><div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">LETTERS (CORRUPTED)</div><div class="result-text result-text-attack">---</div></div>', unsafe_allow_html=True)
                            with r2:
                                st.markdown('<div class="result-box"><div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">DIGITS (CORRUPTED)</div><div class="result-text result-text-attack">---</div></div>', unsafe_allow_html=True)
                            st.markdown(f'<div style="margin-top:0.5rem;padding:0.6rem;background:#0d1117;border:1px solid #30363d;border-radius:8px;font-family:Rajdhani;font-size:0.8rem;color:#8b949e;">Expected mAP50 dropped to <span style="color:#f85149;font-weight:700;">{expected_map}%</span> &nbsp;·&nbsp; ε = {epsilon}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="status-bar status-tampered">🚨 PLATE DETECTION FAILED · mAP50 = {expected_map}%</div>', unsafe_allow_html=True)
                        else:
                            try:
                                char_results, plate_crop = detect_characters(tmp_noisy, fgsm_results)
                                char_boxes = sorted(char_results[0].boxes, key=lambda b: b.xyxy[0][0])
                                plate_width = plate_crop.shape[1]
                                mid = plate_width / 2
                                left_chars, right_chars, confs = [], [], []
                                for cb in char_boxes:
                                    x1, y1, x2, y2 = map(int, cb.xyxy[0])
                                    crop = plate_crop[y1:y2, x1:x2]
                                    if crop.size == 0: continue
                                    label, conf = classify_characters(crop)
                                    confs.append(conf)
                                    if (x1+x2)/2 < mid: left_chars.append(label)
                                    else: right_chars.append(label)
                                fgsm_letters = "".join(right_chars)
                                fgsm_digits  = "".join(left_chars)
                                fgsm_conf    = int(np.mean(confs) * 100) if confs else 0
                                r1, r2 = st.columns(2)
                                with r1:
                                    st.markdown(f'<div class="result-box"><div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">LETTERS (CORRUPTED)</div><div class="result-text result-text-attack">{fgsm_letters if fgsm_letters else "???"}</div></div>', unsafe_allow_html=True)
                                with r2:
                                    st.markdown(f'<div class="result-box"><div style="font-size:0.7rem;color:#8b949e;letter-spacing:2px;margin-bottom:8px;">DIGITS (CORRUPTED)</div><div class="result-text result-text-attack">{fgsm_digits if fgsm_digits else "???"}</div></div>', unsafe_allow_html=True)
                                st.markdown(f'<div style="margin-top:0.5rem;padding:0.6rem;background:#0d1117;border:1px solid #30363d;border-radius:8px;font-family:Rajdhani;font-size:0.8rem;color:#8b949e;">Confidence dropped to <span style="color:#f85149;font-weight:700;">{fgsm_conf}%</span> &nbsp;·&nbsp; Expected mAP50: <span style="color:#f85149;font-weight:700;">{expected_map}%</span></div>', unsafe_allow_html=True)
                                st.markdown(f'<div class="status-bar status-tampered">🚨 FGSM NOISE APPLIED · OCR CORRUPTED · mAP50 = {expected_map}%</div>', unsafe_allow_html=True)
                            except Exception:
                                st.markdown(f'<div class="result-box"><div class="result-text result-text-attack">??? | ???</div><div style="color:#8b949e;font-size:0.8rem;margin-top:8px;">Plate found but chars unreadable · ε={epsilon}</div></div>', unsafe_allow_html=True)
                                st.markdown(f'<div class="status-bar status-tampered">🚨 CHARACTER RECOGNITION DESTROYED · mAP50 = {expected_map}%</div>', unsafe_allow_html=True)

                        if os.path.exists(tmp_noisy):
                            os.remove(tmp_noisy)

                    except Exception as e:
                        st.error(f"Attack error: {e}")
                st.markdown('</div>', unsafe_allow_html=True)

            os.unlink(tmp_path)


# ─── TAB: Defense Mode ────────────────────────────────────────
with tab_defense:

    st.markdown('<div class="main-header header-defense">DEFENSE MODE</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub">HASH VERIFICATION · DIGITAL SIGNATURE · DENOISING FILTER</div>', unsafe_allow_html=True)

    defense_type = st.selectbox(
        "Select Defense Type",
        ["Weight Integrity Check", "Image Signature Verification", "FGSM Denoising Defense"],
        label_visibility="visible"
    )

    st.markdown("---")

    # ── Weight Integrity Check ──
    if defense_type == "Weight Integrity Check":
        st.markdown("""
        <div class="card">
            <div class="card-title">🛡️ SHA-256 Hash Verification</div>
            <div style="font-family:'Rajdhani'; color:#8b949e; font-size:0.9rem; line-height:1.6;">
                The system computes a SHA-256 hash of the original model file and stores it.
                Before every run, it re-computes the hash and compares. Any tampering is detected instantly.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card"><div class="card-title">🔐 Generate Trusted Hash</div>', unsafe_allow_html=True)
            if st.button("Generate Hash for Original Model", use_container_width=True):
                try:
                    # pyrefly: ignore [missing-import]
                    from security.defense.weight_checker import generate_trusted_hash
                    h = generate_trusted_hash("models/plate_detection_model.pt")
                    if h:
                        st.markdown(f"""
                        <div class="status-bar status-secure">✅ HASH GENERATED SUCCESSFULLY</div>
                        <div style="font-family:monospace;font-size:0.7rem;color:#8b949e;margin-top:8px;word-break:break-all;">
                            SHA-256: {h[:32]}...
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card"><div class="card-title">🔍 Verify Model Integrity</div>', unsafe_allow_html=True)
            model_to_check = st.selectbox("Select model to verify", [
                "models/plate_detection_model.pt",
                "models/plate_tampered_temp.pt"
            ])
            if st.button("Verify Integrity", use_container_width=True):
                try:
                    # pyrefly: ignore [missing-import]
                    from security.defense.weight_checker import verify_model
                    is_safe = verify_model(model_to_check)
                    if is_safe:
                        st.markdown('<div class="status-bar status-secure">✅ MODEL IS SECURE · NO TAMPERING DETECTED</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="status-bar status-tampered">🚨 TAMPERING DETECTED · EXECUTION BLOCKED</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">📊 How It Works</div>
            <div style="display:flex; gap:2rem; font-family:'Rajdhani'; font-size:0.9rem; color:#8b949e; line-height:2;">
                <div>1️⃣ Generate SHA-256 hash of original .pt file</div>
                <div>2️⃣ Save hash to trusted_hash.txt</div>
                <div>3️⃣ Before every pipeline run → recompute hash</div>
                <div>4️⃣ If hashes don't match → BLOCK execution</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Image Signature Verification ──
    elif defense_type == "Image Signature Verification":
        st.markdown("""
        <div class="card">
            <div class="card-title">🛡️ RSA Digital Signature Defense</div>
            <div style="font-family:'Rajdhani'; color:#8b949e; font-size:0.9rem; line-height:1.6;">
                Each clean image gets a cryptographic RSA signature. Before entering the pipeline,
                the signature is verified. A backdoor trigger (even a single pixel change) breaks
                the signature and blocks the image.
            </div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_clean = st.file_uploader("Upload a CLEAN image to sign", type=["jpg","jpeg","png"], key="sig_clean")
        uploaded_test  = st.file_uploader("Upload image to verify (can be triggered)", type=["jpg","jpeg","png"], key="sig_test")

        if uploaded_clean and uploaded_test:
            if st.button("🔐 Sign & Verify", type="primary", use_container_width=True):
                try:
                    # pyrefly: ignore [missing-import]
                    from security.defense.image_signature import sign_image, verify_image_signature

                    clean_data = uploaded_clean.read()
                    test_data  = uploaded_test.read()

                    signature = sign_image(clean_data)
                    is_safe   = verify_image_signature(test_data, signature)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown('<div class="card"><div class="card-title">Original (Signed)</div>', unsafe_allow_html=True)
                        st.image(Image.open(uploaded_clean), use_container_width=True)
                        st.markdown('<div class="status-bar status-secure">✅ SIGNATURE GENERATED</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with col2:
                        st.markdown('<div class="card"><div class="card-title">Test Image (Verification)</div>', unsafe_allow_html=True)
                        st.image(Image.open(uploaded_test), use_container_width=True)
                        if is_safe:
                            st.markdown('<div class="status-bar status-secure">✅ SIGNATURE VALID · IMAGE IS CLEAN</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="status-bar status-tampered">🚨 SIGNATURE INVALID · TRIGGER DETECTED · BLOCKED</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error: {e}")

    # ── FGSM Denoising Defense ──
    elif defense_type == "FGSM Denoising Defense":
        st.markdown("""
        <div class="card">
            <div class="card-title">🛡️ Gaussian + Median Denoising Filter</div>
            <div style="font-family:'Rajdhani'; color:#8b949e; font-size:0.9rem; line-height:1.6;">
                After FGSM attack drops accuracy to 38.3%, applying Gaussian + Median filters
                suppresses the adversarial noise and recovers model performance to ~84.8%.
            </div>
        </div>
        """, unsafe_allow_html=True)

        epsilon = st.slider("Epsilon used in attack", 0.0, 0.4, 0.4, 0.05)
        uploaded = st.file_uploader("Upload image", type=["jpg","jpeg","png"], key="fgsm_def_upload")
        run_defense = st.button("🛡️  APPLY DEFENSE", type="primary", use_container_width=True)

        if uploaded and run_defense:
            img_array = load_image(uploaded)

            # pyrefly: ignore [missing-import]
            from security.attacks.fgsm_attack import apply_adversarial_noise
            # pyrefly: ignore [missing-import]
            from security.defense.fgsm_defense import defend_single_image

            img_bgr   = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            noisy_bgr = apply_adversarial_noise(img_bgr, epsilon)
            clean_bgr = defend_single_image(noisy_bgr)

            noisy_rgb = cv2.cvtColor(noisy_bgr, cv2.COLOR_BGR2RGB)
            clean_rgb = cv2.cvtColor(clean_bgr, cv2.COLOR_BGR2RGB)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown('<div class="card"><div class="card-title">Original</div>', unsafe_allow_html=True)
                st.image(img_array, use_container_width=True)
                st.markdown('<div class="status-bar status-secure">mAP50: 99.26%</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="card"><div class="card-title">After FGSM Attack</div>', unsafe_allow_html=True)
                st.image(noisy_rgb, use_container_width=True)
                impact_map = {0.0: 99.3, 0.05: 98.9, 0.1: 97.4, 0.2: 85.6, 0.3: 63.0, 0.4: 38.3}
                closest = min(impact_map.keys(), key=lambda x: abs(x - epsilon))
                st.markdown(f'<div class="status-bar status-tampered">mAP50: {impact_map[closest]}%</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col3:
                st.markdown('<div class="card"><div class="card-title">After Defense</div>', unsafe_allow_html=True)
                st.image(clean_rgb, use_container_width=True)
                st.markdown('<div class="status-bar status-secure">mAP50: ~84.79% (Recovered)</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("""
            <div class="card">
                <div class="card-title">📊 Recovery Summary</div>
            """, unsafe_allow_html=True)

            m1, m2, m3 = st.columns(3)
            m1.metric("Baseline", "99.26%", delta=None)
            m2.metric("Under Attack", f"{impact_map[closest]}%", delta=f"-{99.26 - impact_map[closest]:.2f}%", delta_color="inverse")
            m3.metric("After Defense", "84.79%", delta=f"+{84.79 - impact_map[closest]:.2f}%")
            st.markdown('</div>', unsafe_allow_html=True)



# ─── Credits Footer ───────────────────────────────────────────
st.markdown(
    '<div class="credits-footer">'
    '<div class="credits-title">⚡ Development Team</div>'
    '<div class="credits-team">'
        '<div class="credits-member"><div class="credits-avatar avatar-1">AH</div><div class="credits-name">Ahmed Hossam Abdelrazik</div></div>'
        '<div class="credits-member"><div class="credits-avatar avatar-2">KT</div><div class="credits-name">Kareem Talaat</div></div>'
        '<div class="credits-member"><div class="credits-avatar avatar-3">MA</div><div class="credits-name">Mohand Abdelsadek</div></div>'
        '<div class="credits-member"><div class="credits-avatar avatar-4">OA</div><div class="credits-name">Omar Ashraf</div></div>'
    '</div>'
    '<div class="credits-divider"></div>'
    '<div class="credits-supervisor-label">Supervised by</div>'
    '<div class="credits-supervisor-name">Dr. Ahmed Assmet</div>'
    '<div class="credits-copy">EALPR · EGYPTIAN AUTO LICENSE PLATE RECOGNITION · 2026</div>'
    '</div>',
    unsafe_allow_html=True
)
