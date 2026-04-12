"""
Edge-Agri: Offline Agricultural Advisory System
Main entry point
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from utils.database import init_db, get_stats
from utils.translations import t, TRANSLATIONS

# ── Page Config ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Edge-Agri 🌾",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Init DB ──────────────────────────────────────────────────────
init_db()

# ── Session State ────────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "bn"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ── Global CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&display=swap');

* { font-family: 'Hind Siliguri', sans-serif !important; }

/* Hide default streamlit elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a3a1a 0%, #2d6a2d 100%) !important;
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stSelectbox label { color: rgba(255,255,255,0.8) !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: rgba(255,255,255,0.7) !important; }

/* Nav buttons */
.nav-btn {
    display: block; width: 100%; padding: 12px 16px;
    margin: 4px 0; border-radius: 10px;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    color: white !important; text-decoration: none;
    font-size: 15px; font-weight: 500; cursor: pointer;
    transition: all 0.2s; text-align: left;
}
.nav-btn:hover { background: rgba(255,255,255,0.25); }
.nav-btn.active { background: rgba(255,255,255,0.25); border-color: rgba(255,255,255,0.5); font-weight: 700; }

/* Cards */
.hero-card {
    background: linear-gradient(135deg, #1a3a1a 0%, #2d6a2d 50%, #52b052 100%);
    border-radius: 20px; padding: 40px; color: white; margin-bottom: 24px;
    position: relative; overflow: hidden;
}
.hero-card::after {
    content: "🌾"; position: absolute; right: 30px; top: 50%;
    transform: translateY(-50%); font-size: 100px; opacity: 0.15;
}
.hero-card h1 { font-size: 32px; font-weight: 700; margin: 0 0 10px; }
.hero-card p { font-size: 16px; opacity: 0.9; margin: 0; max-width: 600px; }

.stat-card {
    background: white; border-radius: 14px; padding: 20px;
    text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border-top: 4px solid #2d6a2d;
}
.stat-num { font-size: 32px; font-weight: 700; color: #2d6a2d; }
.stat-label { font-size: 13px; color: #888; margin-top: 4px; }

.feature-card {
    background: white; border-radius: 14px; padding: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-left: 4px solid #2d6a2d; margin-bottom: 12px;
    font-size: 15px; font-weight: 500;
}

/* Chat */
.chat-user {
    background: #2d6a2d; color: white; border-radius: 18px 18px 4px 18px;
    padding: 12px 18px; margin: 8px 0 8px 80px; font-size: 15px; line-height: 1.6;
}
.chat-bot {
    background: white; color: #1a3a1a; border-radius: 18px 18px 18px 4px;
    padding: 14px 18px; margin: 8px 80px 8px 0; font-size: 15px; line-height: 1.7;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08); border: 1px solid #e0e0e0;
}
.chat-meta {
    font-size: 11px; color: #888; margin: -4px 0 8px 0; padding-left: 4px;
}
.chat-source {
    font-size: 12px; background: #e8f5e9; color: #2e7d32;
    padding: 4px 10px; border-radius: 8px; display: inline-block; margin-top: 8px;
}

/* Detection */
.result-healthy {
    background: #e8f5e9; border: 2px solid #4caf50;
    border-radius: 16px; padding: 20px; text-align: center;
}
.result-disease {
    background: #fff3e0; border: 2px solid #ff9800;
    border-radius: 16px; padding: 20px;
}
.result-severe {
    background: #ffebee; border: 2px solid #f44336;
    border-radius: 16px; padding: 20px;
}

/* Severity badges */
.badge-none { background: #e8f5e9; color: #2e7d32; padding: 4px 14px; border-radius: 20px; font-weight: 600; font-size: 13px; }
.badge-medium { background: #fff8e1; color: #f57f17; padding: 4px 14px; border-radius: 20px; font-weight: 600; font-size: 13px; }
.badge-high { background: #ffebee; color: #c62828; padding: 4px 14px; border-radius: 20px; font-weight: 600; font-size: 13px; }

/* Admin */
.admin-login-box {
    max-width: 380px; margin: 60px auto; background: white;
    border-radius: 20px; padding: 40px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.12);
}

/* Divider */
.section-title {
    font-size: 20px; font-weight: 700; color: #1a3a1a;
    margin: 24px 0 16px; padding-bottom: 8px;
    border-bottom: 2px solid #c8e6c8;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-size:48px;'>🌾</div>
        <h2 style='color:white; margin:8px 0 4px; font-size:22px;'>Edge-Agri</h2>
        <p style='color:rgba(255,255,255,0.7); font-size:12px; margin:0;'>Offline Agricultural Advisory</p>
    </div>
    <hr style='border-color:rgba(255,255,255,0.2); margin: 12px 0;'>
    """, unsafe_allow_html=True)

    # Language selector
    lang_options = {"বাংলা 🇧🇩": "bn", "中文 🇨🇳": "zh", "English 🇬🇧": "en"}
    lang_label = st.selectbox(
        "🌐 " + t("select_language", st.session_state.lang),
        options=list(lang_options.keys()),
        index=list(lang_options.values()).index(st.session_state.lang),
        key="lang_selector"
    )
    st.session_state.lang = lang_options[lang_label]
    lang = st.session_state.lang

    st.markdown("<hr style='border-color:rgba(255,255,255,0.2); margin: 12px 0;'>", unsafe_allow_html=True)

    # Navigation
    pages = {
        "home": t("nav_home", lang),
        "chatbot": t("nav_chatbot", lang),
        "detect": t("nav_detect", lang),
        "admin": t("nav_admin", lang),
    }

    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    for page_key, page_label in pages.items():
        is_active = st.session_state.current_page == page_key
        btn_style = "background:rgba(255,255,255,0.25);border-color:rgba(255,255,255,0.5);" if is_active else ""
        if st.button(page_label, key=f"nav_{page_key}",
                     use_container_width=True):
            st.session_state.current_page = page_key
            st.rerun()

    st.markdown("<hr style='border-color:rgba(255,255,255,0.2); margin: 12px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:11px; color:rgba(255,255,255,0.5); text-align:center; padding:8px 0;'>
        RAG • BRDialect-ASR<br>
        DeepSeek-R1 • YOLOv8<br>
        Raspberry Pi 5 Edge
    </div>
    """, unsafe_allow_html=True)

# ── Route to Pages ───────────────────────────────────────────────
page = st.session_state.current_page

# ════════════════════════════════════════════
# HOME PAGE
# ════════════════════════════════════════════
if page == "home":
    stats = get_stats()
    lang = st.session_state.lang

    st.markdown(f"""
    <div class="hero-card">
        <h1>{t('home_hero', lang)}</h1>
        <p>{t('home_desc', lang)}</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="stat-card">
            <div class="stat-num">{stats['total_queries']}</div>
            <div class="stat-label">{t('total_queries', lang)}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stat-card">
            <div class="stat-num">{stats['kb_count']}</div>
            <div class="stat-label">{t('kb_entries', lang)}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stat-card">
            <div class="stat-num">{stats['avg_confidence']}%</div>
            <div class="stat-label">{t('accuracy', lang)}</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="stat-card">
            <div class="stat-num">3</div>
            <div class="stat-label">{t('languages', lang)}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="section-title">✨ Features</div>', unsafe_allow_html=True)
        for feat in ["home_feat1", "home_feat2", "home_feat3", "home_feat4"]:
            st.markdown(f'<div class="feature-card">{t(feat, lang)}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="section-title">🚀 Quick Start</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"💬 {t('start_chat', lang)}", use_container_width=True, type="primary"):
            st.session_state.current_page = "chatbot"
            st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"🔬 {t('detect_disease', lang)}", use_container_width=True):
            st.session_state.current_page = "detect"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.info("🇧🇩 Agricultural Helpline: **16123**")

        # System status
        st.markdown(f'<div class="section-title">⚡ System Status</div>', unsafe_allow_html=True)
        st.success("✅ RAG Pipeline Active")
        st.success("✅ Disease Detection Ready")
        st.success("✅ Offline Mode")

# ════════════════════════════════════════════
# CHATBOT PAGE
# ════════════════════════════════════════════
elif page == "chatbot":
    from utils.rag_engine import answer_query, QUICK_QUESTIONS, GREETING_MSG
    lang = st.session_state.lang

    st.markdown(f'<div class="section-title">💬 {t("chat_title", lang)}</div>', unsafe_allow_html=True)

    col_chat, col_side = st.columns([3, 1])

    with col_side:
        st.markdown(f"**{t('quick_questions', lang)}**")
        for q in QUICK_QUESTIONS.get(lang, QUICK_QUESTIONS["en"]):
            if st.button(q, key=f"qq_{q[:20]}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "text": q})
                result = answer_query(q, lang)
                st.session_state.chat_history.append({
                    "role": "bot", "text": result["answer"],
                    "source": result.get("source", ""),
                    "confidence": result.get("confidence", 0),
                    "related": result.get("related", []),
                })
                st.rerun()

        st.markdown("---")
        district_opts = {
            "bn": ["", "চট্টগ্রাম", "ঢাকা", "সিলেট", "রাজশাহী", "বরিশাল", "রংপুর", "খুলনা"],
            "en": ["", "Chittagong", "Dhaka", "Sylhet", "Rajshahi", "Barishal", "Rangpur", "Khulna"],
            "zh": ["", "吉大港", "达卡", "锡尔赫特", "拉杰沙希", "巴里萨尔", "朗布尔", "库尔纳"],
        }
        district = st.selectbox(t("district", lang), district_opts.get(lang, district_opts["en"]))

        if st.button(f"🗑️ {t('chat_clear', lang)}", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    with col_chat:
        # Chat display container
        chat_container = st.container()
        with chat_container:
            # Greeting if empty
            if not st.session_state.chat_history:
                st.markdown(f'<div class="chat-bot">🤖 {GREETING_MSG.get(lang, GREETING_MSG["en"])}</div>',
                            unsafe_allow_html=True)

            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-user">👨‍🌾 {msg["text"]}</div>', unsafe_allow_html=True)
                else:
                    bot_html = f'<div class="chat-bot">🤖 {msg["text"]}'
                    if msg.get("source"):
                        conf_pct = int(msg.get("confidence", 0) * 100)
                        bot_html += f'<br><span class="chat-source">📖 {msg["source"]} · {conf_pct}%</span>'
                    bot_html += '</div>'
                    st.markdown(bot_html, unsafe_allow_html=True)

                    if msg.get("related"):
                        st.markdown("**Related:**")
                        for rq in msg["related"]:
                            if st.button(f"↗ {rq[:50]}", key=f"rel_{rq[:15]}"):
                                st.session_state.chat_history.append({"role": "user", "text": rq})
                                res = answer_query(rq, lang, district)
                                st.session_state.chat_history.append({
                                    "role": "bot", "text": res["answer"],
                                    "source": res.get("source", ""),
                                    "confidence": res.get("confidence", 0),
                                    "related": res.get("related", []),
                                })
                                st.rerun()

        # Input
        with st.form("chat_form", clear_on_submit=True):
            col_inp, col_btn = st.columns([5, 1])
            with col_inp:
                user_input = st.text_input(
                    label="query",
                    placeholder=t("chat_placeholder", lang),
                    label_visibility="collapsed"
                )
            with col_btn:
                submitted = st.form_submit_button(t("chat_send", lang), use_container_width=True, type="primary")

        if submitted and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "text": user_input})
            result = answer_query(user_input, lang, district)
            st.session_state.chat_history.append({
                "role": "bot",
                "text": result["answer"],
                "source": result.get("source", ""),
                "confidence": result.get("confidence", 0),
                "related": result.get("related", []),
            })
            st.rerun()

# ════════════════════════════════════════════
# DISEASE DETECTION PAGE
# ════════════════════════════════════════════
elif page == "detect":
    from utils.disease_detector import predict_disease
    lang = st.session_state.lang

    st.markdown(f'<div class="section-title">🔬 {t("detect_title", lang)}</div>', unsafe_allow_html=True)
    st.markdown(t("detect_desc", lang))

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded = st.file_uploader(
            t("upload_image", lang),
            type=["jpg", "jpeg", "png", "webp"],
            help=t("upload_hint", lang),
        )

        if uploaded:
            from PIL import Image
            img = Image.open(uploaded)
            st.image(img, use_container_width=True, caption=uploaded.name)

            if st.button(t("detect_btn", lang), type="primary", use_container_width=True):
                with st.spinner(t("analyzing", lang)):
                    result = predict_disease(img, lang)

                st.session_state["last_detection"] = result
                st.session_state["last_img_name"] = uploaded.name

                # Log to DB
                from utils.database import log_detection
                log_detection(
                    uploaded.name,
                    result["plant_type"],
                    result["disease"],
                    result["confidence"],
                    result["severity"],
                    result["recommendation"],
                )
                st.rerun()

    with col2:
        if "last_detection" in st.session_state:
            result = st.session_state["last_detection"]

            st.markdown(f'<div class="section-title">{t("result_title", lang)}</div>', unsafe_allow_html=True)

            if result["is_healthy"]:
                st.markdown(f"""
                <div class="result-healthy">
                    <div style="font-size:48px; margin-bottom:10px;">✅</div>
                    <div style="font-size:22px; font-weight:700; color:#2e7d32;">{t('healthy_plant', lang)}</div>
                    <div style="font-size:14px; color:#388e3c; margin-top:8px;">{result['plant_type']}</div>
                    <div style="font-size:20px; font-weight:700; color:#2e7d32; margin-top:8px;">{result['confidence_pct']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                sev = result["severity"]
                card_class = "result-severe" if sev == "High" else "result-disease"
                badge_class = "badge-high" if sev == "High" else "badge-medium"

                st.markdown(f"""
                <div class="{card_class}">
                    <div style="font-size:13px; color:#666; margin-bottom:4px;">🌿 {t('plant_type', lang)}: <b>{result['plant_type']}</b></div>
                    <div style="font-size:20px; font-weight:700; color:#333; margin-bottom:8px;">⚠️ {result['disease_display']}</div>
                    <div style="margin-bottom:10px;">
                        <span class="{badge_class}">{t('severity', lang)}: {result['severity_display']}</span>
                        &nbsp;
                        <span style="background:#e3f2fd;color:#1565c0;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;">{result['confidence_pct']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if result.get("symptoms"):
                st.markdown(f"**🔍 {t('symptoms', lang)}:**")
                st.info(result["symptoms"])

            st.markdown(f"**💊 {t('recommendation', lang)}:**")
            st.success(result["recommendation"])

        else:
            st.markdown("""
            <div style="text-align:center; padding:60px 20px; color:#aaa;">
                <div style="font-size:64px; margin-bottom:16px;">🌿</div>
                <div style="font-size:16px;">Upload an image to detect plant diseases</div>
            </div>
            """, unsafe_allow_html=True)

        # Supported plants info
        with st.expander("🌱 Supported Plants"):
            plants = ["🍎 Apple", "🫐 Blueberry", "🍒 Cherry", "🌽 Corn",
                      "🍇 Grape", "🍊 Orange", "🍑 Peach", "🌶️ Pepper",
                      "🥔 Potato", "🍓 Strawberry", "🍅 Tomato", "🌱 Soybean"]
            cols = st.columns(3)
            for i, p in enumerate(plants):
                cols[i % 3].markdown(p)

# ════════════════════════════════════════════
# ADMIN PAGE
# ════════════════════════════════════════════
elif page == "admin":
    from utils.database import verify_admin, get_stats, get_all_queries, get_all_detections, get_all_kb, add_kb_entry, delete_kb_entry
    import pandas as pd
    lang = st.session_state.lang

    # ── Login Gate ───────────────────────────────────────────────
    if not st.session_state.admin_logged_in:
        st.markdown(f'<div class="section-title">🔐 {t("admin_title", lang)}</div>', unsafe_allow_html=True)

        col_l, col_c, col_r = st.columns([1, 1.2, 1])
        with col_c:
            with st.form("login_form"):
                st.markdown(f"### {t('admin_login', lang)}")
                username = st.text_input(t("admin_username", lang))
                password = st.text_input(t("admin_password", lang), type="password")
                if st.form_submit_button(t("admin_login_btn", lang), use_container_width=True, type="primary"):
                    if verify_admin(username, password):
                        st.session_state.admin_logged_in = True
                        st.session_state.admin_user = username
                        st.rerun()
                    else:
                        st.error(t("admin_wrong_pass", lang))
            st.caption("Default: admin / admin123")

    else:
        # ── Admin Dashboard ──────────────────────────────────────
        col_title, col_logout = st.columns([4, 1])
        with col_title:
            st.markdown(f'<div class="section-title">📊 {t("admin_dashboard", lang)}</div>', unsafe_allow_html=True)
        with col_logout:
            if st.button(t("admin_logout", lang)):
                st.session_state.admin_logged_in = False
                st.rerun()

        stats = get_stats()

        # Stats
        c1, c2, c3, c4 = st.columns(4)
        metrics = [
            ("💬", stats["total_queries"], t("total_queries", lang)),
            ("📅", stats["today_queries"], t("today", lang)),
            ("📚", stats["kb_count"], t("kb_entries", lang)),
            ("🔬", stats["detections"], "Detections"),
        ]
        for col, (icon, val, label) in zip([c1, c2, c3, c4], metrics):
            col.markdown(f"""<div class="stat-card">
                <div style="font-size:24px;">{icon}</div>
                <div class="stat-num">{val}</div>
                <div class="stat-label">{label}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            f"💬 {t('admin_queries', lang)}",
            f"🔬 {t('admin_detections', lang)}",
            f"📚 {t('admin_kb', lang)}",
            f"➕ {t('add_kb', lang)}",
        ])

        with tab1:
            queries = get_all_queries(100)
            if queries:
                df = pd.DataFrame(queries)[["id", "query_text", "query_lang", "confidence_score", "district", "created_at"]]
                df.columns = ["#", "Query", "Lang", "Confidence", "District", "Time"]
                df["Confidence"] = df["Confidence"].apply(lambda x: f"{round((x or 0)*100, 1)}%")
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No queries yet.")

        with tab2:
            detections = get_all_detections(100)
            if detections:
                df = pd.DataFrame(detections)[["id", "image_name", "plant_type", "detected_disease", "confidence", "severity", "created_at"]]
                df.columns = ["#", "Image", "Plant", "Disease", "Confidence", "Severity", "Time"]
                df["Confidence"] = df["Confidence"].apply(lambda x: f"{round((x or 0)*100, 1)}%")
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No detections yet.")

        with tab3:
            kb_items = get_all_kb()
            search = st.text_input("🔍 Search", placeholder="Search knowledge base...")
            if search:
                kb_items = [k for k in kb_items if search.lower() in k["question_bn"].lower()
                            or search.lower() in (k.get("keywords") or "").lower()]

            for item in kb_items:
                with st.expander(f"[{item['category']}] {item['question_bn'][:70]}..."):
                    st.write(f"**Answer:** {item['answer_bn'][:200]}...")
                    st.caption(f"Source: {item['source']} | Keywords: {item.get('keywords','')}")
                    if st.button(f"🗑️ Delete #{item['id']}", key=f"del_{item['id']}"):
                        delete_kb_entry(item["id"])
                        st.success("Deleted!")
                        st.rerun()

        with tab4:
            with st.form("add_kb_form"):
                cat_opts = {
                    "bn": ["ধানের রোগ", "সার ব্যবস্থাপনা", "পোকামাকড়", "সেচ ব্যবস্থাপনা", "আবহাওয়া ও মৌসুম", "ফসল কাটা", "মাটি পরীক্ষা", "অন্যান্য"],
                    "en": ["Rice Disease", "Fertilizer Management", "Pests", "Irrigation", "Season & Weather", "Harvesting", "Soil Testing", "Other"],
                    "zh": ["水稻病害", "施肥管理", "病虫害", "灌溉管理", "季节与气候", "收割", "土壤测试", "其他"],
                }
                col_a, col_b = st.columns(2)
                with col_a:
                    category = st.selectbox(t("kb_category", lang), cat_opts.get(lang, cat_opts["en"]))
                    source = st.text_input(t("kb_source", lang), value="BRRI Manual 2024")
                with col_b:
                    keywords = st.text_input(t("kb_keywords", lang), placeholder="keyword1,keyword2")
                    question_en = st.text_input("Question (English)", placeholder="Optional English question")

                question_bn = st.text_input(f"{'প্রশ্ন' if lang=='bn' else 'Question'}*", placeholder="বাংলা প্রশ্ন লিখুন...")
                answer_bn = st.text_area(f"{'উত্তর' if lang=='bn' else 'Answer'}*", placeholder="বিস্তারিত উত্তর...", height=120)
                answer_en = st.text_area("Answer (English)", placeholder="Optional English answer", height=80)

                if st.form_submit_button(t("save", lang), type="primary", use_container_width=True):
                    if question_bn and answer_bn:
                        add_kb_entry(category, question_bn, answer_bn, source, keywords, question_en, answer_en)
                        st.success(t("saved", lang))
                        st.rerun()
                    else:
                        st.error("Question and Answer are required!")
