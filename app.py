import streamlit as st

# ==========================================
# 1. ページの初期設定
# ==========================================
st.set_page_config(
    page_title="JKK関西 外壁改修フロー判定", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. 🎨 カスタムデザイン（CSS）
# ==========================================
st.markdown("""
    <style>
    /* 全体の背景：しっかりとした上品な薄緑 */
    .stApp {
        background-color: #d1e2c4 !important; 
    }
    
    /* 通常エリアのテキストを真っ黒にする設定 */
    .stApp p, .stApp li, .stApp span, .stApp label, .stApp div {
        color: #000000 !important;
    }
    
    /* 🟢 濃い緑のヘッダー外枠デザイン（看板の深緑に近い色味へ微調整） */
    .jkk-header {
        background-color: #1a5323 !important; 
        padding: 40px 20px !important; 
        border-radius: 16px !important; 
        text-align: center !important;
        margin-top: 10px !important;
        margin-bottom: 35px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
    }

    /* ▼ 看板画像に極限まで寄せた文字バランス・カラー調整（K-1%テイスト） */
    .jkk-header-title {
        color: #f2f9ec !important; /* 真っ白ではない、画像のようなごくわずかに黄緑がかった淡い色 */
        font-size: 34px !important; /* 迫力のある看板の文字サイズ比率を再現 */
        font-weight: 800 !important;
        font-family: 'Helvetica Neue', 'Segoe UI', 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif !important;
        letter-spacing: 1.5px !important;
        line-height: 1.4 !important;
        display: block;
        margin-bottom: 14px; /* サブタイトルとの絶妙なディスタンス */
    }
    .jkk-header-sub {
        color: #e6f3dc !important; /* タイトルと同系統の淡い色、かつ少し細めにしてメリハリを強化 */
        font-size: 16px !important;
        font-weight: 500 !important;
        letter-spacing: 1px !important;
        line-height: 1.3 !important;
        display: block;
        opacity: 0.95;
    }

    /* 各ステップの見出し */
    .stSubheader div, .stSubheader h3, .stSubheader span {
        color: #000000 !important; 
        font-weight: 800 !important;
        font-size: 22px !important;
    }
    .stSubheader {
        border-left: 6px solid #1a5323;
        padding-left: 12px;
        margin-top: 25px;
        margin-bottom: 20px;
    }

    /* 現在の選択ルート表示 */
    .route-info {
        background-color: #ffffff !important;
        padding: 12px 15px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 20px;
        border: 2px solid #1a5323;
    }
    .route-info div {
        color: #000000 !important;
    }

    /* 判定メッセージ部分 */
    div[data-testid="stNotification"] {
        background-color: #ffffff !important; 
        border: 2px solid #1a5323 !important;
    }

    /* 結果表示ボックス */
    .result-box {
        background-color: #ffffff !important;
        border-top: 4px solid #1a5323 !important;
        padding: 20px;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-top: 15px;
    }
    .result-title {
        font-size: 14px !important;
        font-weight: bold !important;
        color: #333333 !important;
        margin-bottom: 2px;
    }
    .result-value {
        font-size: 28px !important;
        font-weight: 900 !important;
        color: #1a5323 !important;
        border-bottom: 2px solid #1a5323;
        padding-bottom: 8px;
        margin-bottom: 15px;
    }
    .result-box li {
        font-size: 16px !important;
        line-height: 1.6 !important;
        margin-bottom: 8px !important;
        color: #000000 !important;
    }

    /* ボタン（ラジオボタンや通常ボタンの最適化） */
    div.stButton > button, button[data-testid="baseButton-primary"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #777777 !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        height: 50px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    div.stButton > button:hover, button[data-testid="baseButton-primary"]:hover {
        background-color: #e8f5e9 !important;
        border-color: #1a5323 !important;
        color: #1a5323 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 🏢 ヘッダーエリア（看板再現部）
# ==========================================
st.markdown("""
    <div class="jkk-header">
        <span class="jkk-header-title">日本樹脂施工協同組合（関西支部）</span>
        <span class="jkk-header-sub">外壁タイル面・塗装面改修 フローチャート判定システム</span>
    </div>
""", unsafe_allow_html=True)


# ==========================================
# 4. ⚙️ セッション状態（画面遷移ロジック）
# ==========================================
if "step" not in st.session_state:
    st.session_state.step = 1
if "choices" not in st.session_state:
    st.session_state.choices = []

# 前のステップに戻る処理
def go_back():
    if st.session_state.step > 1:
        st.session_state.step -= 1
        st.session_state.choices.pop()

# 最初からやり直す処理
def reset_flow():
    st.session_state.step = 1
    st.session_state.choices = []


# ==========================================
# 5. 🔍 判定フロー・ユーザー選択エリア
# ==========================================

# 現在の選択状況（パンくずリスト風）の表示
if len(st.session_state.choices) > 0:
    st.markdown(f"""
    <div class="route-info">
        📍 現在の選択ルート: {" ＞ ".join(st.session_state.choices)}
    </div>
    """, unsafe_allow_html=True)

# --- ステップ1: 下地選択 ---
if st.session_state.step == 1:
    st.subheader("ステップ 1: 対象となる外壁の下地を選択してください")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧱 外壁タイル面", use_container_width=True):
            st.session_state.choices.append("外壁タイル面")
            st.session_state.step = 2
            st.rerun()
            
    with col2:
        if st.button("🎨 塗装面・その他", use_container_width=True):
            st.session_state.choices.append("塗装面・その他")
            st.session_state.step = 10  # 塗装面ルートのダミーステップ（必要に応じて拡張可能）
            st.rerun()

# --- ステップ2: 状態・工法の選択（タイル面ルート） ---
elif st.session_state.step == 2:
    st.subheader("ステップ 2: タイル面の状態、または希望する工法を選んでください")
    
    options = [
        "浮きがあり、剥落防止対策を行いたい（JKセザール工法等）",
        "ひび割れ・欠損の補修を行いたい",
        "全面的なリフレッシュ・防水工法を検討したい"
    ]
    
    for opt in options:
        if st.button(opt, use_container_width=True):
            st.session_state.choices.append(opt)
            st.session_state.step = 3
            st.rerun()

# --- ステップ3: 最終確認（施工規模など） ---
elif st.session_state.step == 3:
    st.subheader("ステップ 3: 施工の規模・範囲を選択してください")
    
    options_step3 = [
        "大規模修繕（建物全体）",
        "部分補修・部分的メンテナンス"
    ]
    
    for opt in options_step3:
        if st.button(opt, use_container_width=True):
            st.session_state.choices.append(opt)
            st.session_state.step = 4  # 結果表示へ
            st.rerun()

# --- ステップ4: タイル面ルートの判定結果表示 ---
elif st.session_state.step == 4:
    st.subheader("📋 判定結果")
    
    # 選択に応じた結果文面のシミュレーション
    main_choice = st.session_state.choices[1]
    scale_choice = st.session_state.choices[2]
    
    st.markdown(f"""
    <div class="result-box">
        <div class="result-title">推奨される改修工法・システム</div>
        <div class="result-value">JKラビング工法 / JKセザール工法 シリーズ</div>
        <ul>
            <li><b>選択されたルート:</b> {st.session_state.choices[0]} ＞ {main_choice}</li>
            <li><b>施工規模:</b> {scale_choice} に適した基準工法です。</li>
            <li><b>特長:</b> 特殊アクリル樹脂と高強度ステンレスピンを併用し、タイルの意匠性を保持したまま強固に剥落を防止します。</li>
            <li><b>注記:</b> 詳細な下地調査（打診調査等）の結果に基づき、適切なピンのピッチ数を算定してください。</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# --- ステップ10: 塗装面ルートの簡易結果表示 ---
elif st.session_state.step == 10:
    st.subheader("📋 判定結果（塗装面・その他）")
    
    st.markdown(f"""
    <div class="result-box">
        <div class="result-title">推奨される改修工法・システム</div>
        <div class="result-value">JKコート・仕上げ塗材改修システム</div>
        <ul>
            <li><b>選択されたルート:</b> 塗装面・その他</li>
            <li><b>特長:</b> 下地の微細なひび割れ追従性に優れ、長期にわたり防水性と美観を維持します。</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 6. ↩️ 共通ナビゲーションボタン（下部固定風）
# ==========================================
st.write("---")
nav_col1, nav_col2 = st.columns([1, 4])

with nav_col1:
    if st.session_state.step > 1:
        if st.button("⬅️ 戻る", key="btn_back"):
            go_back()
            st.rerun()

with nav_col2:
    if st.session_state.step > 1:
        if st.button("🔄 最初からやり直す", key="btn_reset"):
            reset_flow()
            st.rerun()
