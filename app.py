import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 34: O Sa'osi", page_icon="🔢", layout="centered")

# --- CSS 美化 (數理邏輯藍綠色) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    .morph-tag { 
        background-color: #B2DFDB; color: #004D40; 
        padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;
        display: inline-block; margin-right: 5px;
    }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #E0F2F1 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #009688;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #00796B; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #E0F2F1;
        border-left: 5px solid #4DB6AC;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #B2DFDB; color: #004D40; border: 2px solid #009688; padding: 12px;
    }
    .stButton>button:hover { background-color: #80CBC4; border-color: #00796B; }
    .stProgress > div > div > div > div { background-color: #009688; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 34: 18個單字 - 數字與數量) ---
vocab_data = [
    {"amis": "Cecay", "chi": "一", "icon": "1️⃣", "source": "Row 737", "morph": "Number"},
    {"amis": "Tosa", "chi": "二", "icon": "2️⃣", "source": "Row 1242", "morph": "Number"},
    {"amis": "Tolo", "chi": "三", "icon": "3️⃣", "source": "Row 737", "morph": "Number"},
    {"amis": "Sepat", "chi": "四", "icon": "4️⃣", "source": "Standard", "morph": "Number"},
    {"amis": "Lima", "chi": "五 / 手", "icon": "5️⃣", "source": "Standard", "morph": "Number"},
    {"amis": "Enem", "chi": "六", "icon": "6️⃣", "source": "Standard", "morph": "Number"},
    {"amis": "Pito", "chi": "七", "icon": "7️⃣", "source": "Standard", "morph": "Number"},
    {"amis": "Falo", "chi": "八", "icon": "8️⃣", "source": "Standard", "morph": "Number"},
    {"amis": "Siwa", "chi": "九", "icon": "9️⃣", "source": "Standard", "morph": "Number"},
    {"amis": "Mo^etep", "chi": "十", "icon": "🔟", "source": "Standard", "morph": "Number"},
    {"amis": "Ira", "chi": "有 / 存在", "icon": "🈶", "source": "Row 519", "morph": "Exist"},
    {"amis": "Awa", "chi": "無 / 沒有", "icon": "🈚", "source": "Row 461", "morph": "Negation"},
    {"amis": "Awaay", "chi": "不在 / 沒有 (強調)", "icon": "📭", "source": "Row 466", "morph": "Awa + ay"},
    {"amis": "Pina", "chi": "多少 (非人)", "icon": "🔢", "source": "Row 676", "morph": "Q-Word"},
    {"amis": "Papina", "chi": "多少人", "icon": "👥", "source": "Grammar", "morph": "Pa-Pina"},
    {"amis": "Ciwawa", "chi": "有小孩", "icon": "👶", "source": "Morphology", "morph": "Ci + Wawa"},
    {"amis": "Cifafahi", "chi": "有太太 / 娶妻", "icon": "💍", "source": "Row 3980", "morph": "Ci + Fafahi"},
    {"amis": "Ka'emangay", "chi": "幼小的 / 小孩", "icon": "🧸", "source": "Row 304", "morph": "Ka-'emang-ay"},
]

# --- 句子庫 (9句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Mihatosa ciira to fonos.", "chi": "他一次拿兩把番刀。", "icon": "⚔️", "source": "Row 1242"},
    {"amis": "Cecay tolo lima pito.", "chi": "一三五七 (報數)。", "icon": "🗣️", "source": "Row 737"},
    {"amis": "Ira ko payso no miso?", "chi": "你有錢嗎？", "icon": "💰", "source": "Row 519 (Adapted)"},
    {"amis": "Awaay ko payso.", "chi": "沒有錢。", "icon": "💸", "source": "Row 461"},
    {"amis": "Ciwawa kiso?", "chi": "你有小孩嗎？", "icon": "👶", "source": "Standard Pattern"},
    {"amis": "Awaay ko 'epoc.", "chi": "沒有用處(成果)。", "icon": "🚫", "source": "Row 466"},
    {"amis": "O ka'emangayho a wawa.", "chi": "還是幼小的孩子。", "icon": "🧸", "source": "Row 304 (Adapted)"},
    {"amis": "Pina ko toki a maomah kami?", "chi": "我們幾點工作？", "icon": "⏰", "source": "Row 676"},
    {"amis": "Cifafahi to ci Kacaw.", "chi": "Kacaw有太太了(結婚了)。", "icon": "💍", "source": "Standard Pattern"},
]

# --- 3. 隨機題庫 (5題) ---
raw_quiz_pool = [
    {
        "q": "Mihatosa ciira to fonos.",
        "audio": "Mihatosa ciira to fonos",
        "options": ["他拿兩把番刀", "他拿一把番刀", "他沒有番刀"],
        "ans": "他拿兩把番刀",
        "hint": "Tosa (二) -> Mihatosa (做兩次/拿兩個) (Row 1242)"
    },
    {
        "q": "單字測驗：Mo^etep",
        "audio": "Mo^etep",
        "options": ["十", "九", "八"],
        "ans": "十",
        "hint": "Siwa, Mo^etep..."
    },
    {
        "q": "單字測驗：Awaay",
        "audio": "Awaay",
        "options": ["不在/沒有", "有", "很多"],
        "ans": "不在/沒有",
        "hint": "Row 461: Awaay ko payso (沒錢)"
    },
    {
        "q": "單字測驗：Ka'emangay",
        "audio": "Ka'emangay",
        "options": ["幼小的", "年老的", "巨大的"],
        "ans": "幼小的",
        "hint": "Row 304: O ka'emangayho (還是小孩)"
    },
    {
        "q": "Pina ko toki a maomah kami?",
        "audio": "Pina ko toki a maomah kami",
        "options": ["我們幾點工作？", "我們在哪裡工作？", "我們跟誰工作？"],
        "ans": "我們幾點工作？",
        "hint": "Pina (多少) (Row 676)"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌 (5題)
    selected_questions = random.sample(raw_quiz_pool, 5)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #00796B;'>Unit 34: O Sa'osi</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>數字與數量 (Numbers & Quantities)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (構詞分析)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="morph-tag">{word['morph']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #00796B;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 5)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 5**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 20
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #B2DFDB; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #00796B;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會數字與數量了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 5)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_questions.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()

