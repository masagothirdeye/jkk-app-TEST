import streamlit as st

# ページの初期設定
st.set_page_config(
    page_title="JKK関西 外壁改修フロー判定", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🎨 カスタムデザイン（CSS）：文字を黒に、背景を上品なグリーンに調整
st.markdown("""
    <style>
    /* 全体の背景（白飛びしない、少し深みを持たせた目に優しい薄緑） */
    .stApp {
        background-color: #e2edd5; 
    }
    
    /* タイル・ヘッダー部分のデザイン（鮮やかな緑色） */
    .jkk-header {
        background-color: #2b8a3e; /* JKK標準のグリーン */
        padding: 25px;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .jkk-header h1 {
        color: white !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        margin-bottom: 5px !important;
    }
    .jkk-header p {
        color: #d3f9d8 !important;
        font-size: 14px !important;
        margin: 0 !important;
    }
    
    /* 🛠️ 【修正】見出しの文字を完全に「黒」に指定 */
    .stSubheader div, .stSubheader h3 {
        color: #212529 !important; /* はっきり読める黒 */
        font-weight: 700 !important;
    }
    .stSubheader {
        border-left: 5px solid #2b8a3e;
        padding-left: 10px;
        margin-top: 25px;
        margin-bottom: 20px;
    }
    
    /* 現在の選択ルート表示（落ち着いたグレー系） */
    .route-info {
        background-color: #ffffff;
        padding: 10px 15px;
        border-radius: 5px;
        color: #495057;
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 20px;
        border: 1px solid #ced4da;
    }
    
    /* 結果表示ボックスのカスタマイズ（ホワイト背景に濃い目のヘッダー） */
    .result-box {
        background-color: #ffffff;
        border-top: 4px solid #2b8a3e; 
        padding: 20px;
        border-radius: 0 0 8px 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: 15px;
    }

    /* 通知・判定メッセージの背景設定 */
    div[data-testid="stNotification"] {
        background-color: #ffffff !important; 
        color: #495057 !important; 
        border: 1px solid #ced4da !important;
    }
    
    /* 🔴 赤いボタン（type="primary"）を、白ベース＋緑枠のスマートなデザインに上書き */
    button[data-testid="baseButton-primary"] {
        background-color: #ffffff !important;
        color: #212529 !important;
        border: 1px solid #ced4da !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    /* ボタンにマウスを乗せたとき（ホバー） */
    button[data-testid="baseButton-primary"]:hover {
        background-color: #f4f9f4 !important;
        border: 1px solid #2b8a3e !important;
        color: #2b8a3e !important;
    }
    
    /* 通常のボタン（白ベース） */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #212529 !important;
        border: 1px solid #ced4da !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
    }
    div.stButton > button:hover {
        background-color: #f4f9f4 !important;
        border-color: #2b8a3e !important;
        color: #2b8a3e !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ヘッダーエリア
# ---------------------------------------------------------
st.markdown("""
    <div class="jkk-header">
        <h1>日本樹脂施工協同組合（JKK関西）</h1>
        <p>外壁タイル面・塗装面改修 フローチャート判定システム</p>
    </div>
""", unsafe_allow_html=True)

# 画面状態を記憶する仕組み
if "step" not in st.session_state:
    st.session_state.step = 1
if "choices" not in st.session_state:
    st.session_state.choices = []

step = st.session_state.step
choices = st.session_state.choices

# ---------------------------------------------------------
# ステップ1：下地選択
# ---------------------------------------------------------
if step == 1:
    st.subheader("【ステップ 1】下地を選択してください")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧱 タイル面", use_container_width=True, type="primary"):
            st.session_state.choices.append("タイル面")
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("🎨 塗装面", use_container_width=True, type="primary"):
            st.session_state.choices.append("塗装面")
            st.session_state.step = 2
            st.rerun()

# ---------------------------------------------------------
# ステップ2：改修範囲の選択
# ---------------------------------------------------------
elif step == 2:
    st.markdown(f'<div class="route-info">📂 現在の選択：{ " ＞ ".join(choices) }</div>', unsafe_allow_html=True)
    st.subheader("【ステップ 2】改修の範囲を選択してください")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏢 面改修", use_container_width=True):
            st.session_state.choices.append("面改修")
            if choices[0] == "塗装面":
                st.session_state.step = 4
            else:
                st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("🛠️ 部分改修", use_container_width=True):
            st.session_state.choices.append("部分改修")
            st.session_state.step = 4
            st.rerun()

# ---------------------------------------------------------
# ステップ3：工法目的の選択（タイル面・面改修のみ）
# ---------------------------------------------------------
elif step == 3:
    st.markdown(f'<div class="route-info">📂 現在の選択：{ " ＞ ".join(choices) }</div>', unsafe_allow_html=True)
    st.subheader("【ステップ 3】改修の目的を選択してください")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛡️ 剥落防止工法", use_container_width=True):
            st.session_state.choices.append("剥落防止工法")
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("💧 防水・保護工法", use_container_width=True):
            st.session_state.choices.append("防水・保護工法")
            st.session_state.step = 4
            st.rerun()

# ---------------------------------------------------------
# ステップ4：系統の選択、または最終結果の表示
# ---------------------------------------------------------
elif step == 4:
    if choices == ["タイル面", "面改修", "剥落防止工法"]:
        st.markdown(f'<div class="route-info">📂 現在の選択：{ " ＞ ".join(choices) }</div>', unsafe_allow_html=True)
        st.subheader("【ステップ 4】塗料の系統を選択してください")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧪 溶剤系", use_container_width=True):
                st.session_state.choices.append("溶剤系")
                st.session_state.step = 5 
                st.rerun()
        with col2:
            if st.button("🚰 水性系", use_container_width=True):
                st.session_state.choices.append("水性系")
                st.session_state.step = 5 
                st.rerun()
                
    elif choices == ["タイル面", "面改修", "防水・保護工法"]:
        st.markdown(f'<div class="route-info">📂 現在の選択：{ " ＞ ".join(choices) }</div>', unsafe_allow_html=True)
        st.subheader("【ステップ 4】塗料の系統を選択してください")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧪 溶剤系", use_container_width=True):
                st.session_state.choices.append("溶剤系")
                st.session_state.step = 5
                st.rerun()
        with col2:
            if st.button("🚰 水性系", use_container_width=True):
                st.session_state.choices.append("水性系")
                st.session_state.step = 5
                st.rerun()

    else:
        st.markdown(f'<div class="route-info">📂 判定ルート：{ " ＞ ".join(choices) }</div>', unsafe_allow_html=True)
        st.info("📋 推奨工法が判定されました")
        
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        if choices == ["タイル面", "部分改修"]:
            st.metric(label="推奨工法", value="JKテラピン工法")
            st.markdown("""
            * **仕様概要**: 注入口付アンカーピンニングエポキシ樹脂注入工法
            * **適合規格**: 国交省仕様適合工法
            * **工法特徴**: 特殊アンカーピンと樹脂でタイル浮きを確実に防止。意匠性を損ないません。
            """)
        elif choices == ["塗装面", "面改修"]:
            st.metric(label="推奨工法", value="JKウォール工法")
            st.markdown("""
            * **仕様概要**: 外壁塗膜防水工法（水性系）
            * **主成分**: アクリルゴム系
            * **適合規格**: JIS A 6021
            * **工法特徴**: 抜群のひび割れ追従性を誇る防水塗膜で、雨水の侵入をシャットアウトします。
            """)
        elif choices == ["塗装面", "部分改修"]:
            st.metric(label="推奨工法", value="JKラビング工法")
            st.markdown("""
            * **仕様概要**: ノンカットひび割れ補修工法 / アスベスト対策工法（水性系）
            * **工法特徴**: ひび割れを切削（Uカット）せずに補修するため、下地のアスベスト粉塵を飛散させず安全です。
            """)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# ステップ5：最終確定
# ---------------------------------------------------------
elif step == 5:
    if len(choices) < 5:
        st.markdown(f'<div class="route-info">📂 現在の選択：{ " ＞ ".join(choices) }</div>', unsafe_allow_html=True)
        
        if choices == ["タイル面", "面改修", "剥落防止工法", "溶剤系"]:
            st.subheader("【ステップ 5】仕様を選択してください")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("アクリル樹脂（標準仕様）", use_container_width=True):
                    st.session_state.choices.append("アクリル樹脂（標準仕様）")
                    st.rerun()
            with col2:
                if st.button("アクリル樹脂（防水仕様）", use_container_width=True):
                    st.session_state.choices.append("アクリル樹脂（防水仕様）")
                    st.rerun()
            if st.button("ウレタン樹脂（標準仕様）", use_container_width=True):
                st.session_state.choices.append("ウレタン樹脂（標準仕様）")
                st.rerun()

        elif choices == ["タイル面", "面改修", "剥落防止工法", "水性系"]:
            st.subheader("【ステップ 5】樹脂の種類を選択してください")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("アクリル樹脂", use_container_width=True):
                    st.session_state.choices.append("アクリル樹脂")
                    st.rerun()
            with col2:
                if st.button("ウレタン樹脂", use_container_width=True):
                    st.session_state.choices.append("ウレタン樹脂")
                    st.rerun()
    else:
        st.markdown(f'<div class="route-info">📂 判定ルート：{ " ＞ ".join(choices[:4]) } ＞ {choices[4]}</div>', unsafe_allow_html=True)
        st.info("📋 推奨工法が判定されました")
        
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        if "アクリル樹脂（標準仕様）" in choices:
            st.metric(label="推奨工法", value="JKセライダー工法（標準仕様）")
            st.markdown("* **主成分**: アクリル樹脂（溶剤系） / UR都市機構 品質基準適合工法\n* **特徴**: 透明性の高いクリア樹脂で、タイルの風合いをそのまま残して剥落を防止します。")
        elif "アクリル樹脂（防水仕様）" in choices:
            st.metric(label="推奨工法", value="JKセライダー工法（防水仕様）")
            st.markdown("* **主成分**: アクリル樹脂（溶剤系） / UR都市機構 品質基準適合工法\n* **特徴**: 高い剥落防止性能に加え、目地からの雨水浸入を防ぐ高い防水性を備えています。")
        elif "ウレタン樹脂（標準仕様）" in choices:
            st.metric(label="推奨工法", value="JKセライダーU工法（標準仕様）")
            st.markdown("* **主成分**: ウレタン樹脂（溶剤系）\n* **特徴**: 強靭かつ柔軟なウレタン塗膜で、下地やタイルの細かな伸縮挙動にしっかり追従します。")
        elif "アクリル樹脂" in choices and "剥落防止工法" in choices:
            st.metric(label="推奨工法", value="水性JKセライダー工法")
            st.markdown("* **主成分**: アクリル樹脂（水性系） / UR都市機構 品質基準適合工法\n* **特徴**: 性能はそのままに完全水性化。シンナー臭が一切ないため、居住者や環境に最適です。")
        elif "ウレタン樹脂" in choices and "剥落防止工法" in choices:
            st.metric(label="推奨工法", value="JKクリアファイバーW工法")
            st.markdown("* **主成分**: ウレタン樹脂（水性系） / UR都市機構 品質基準適合工法\n* **特徴**: 水性ウレタンと特殊繊維を組み合わせ、非常に高い引張強度で外壁を強固にホールドします。")
        elif "溶剤系" in choices and "防水・保護工法" in choices:
            st.metric(label="推奨工法", value="JKコート工法")
            st.markdown("* **主成分**: アクリル樹脂（溶剤系）\n* **特徴**: タイルの美観を維持するクリアー仕上げ。目地への保水・エフロの発生を長期間抑制します。")
        elif "水性系" in choices and "防水・保護工法" in choices:
            st.metric(label="推奨工法", value="JKクリアコートW工法")
            st.markdown("* **主成分**: ウレタン樹脂（水性系）\n* **特徴**: 環境に優しい水性クリアー。ウレタンの柔軟性で外壁の微細な動きを保護し、雨水を防ぎます。")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 🔙 戻るボタンエリア
# ---------------------------------------------------------
if step > 1 or len(choices) == 5:
    st.markdown("---")
    back_col1, back_col2 = st.columns(2)
    
    with back_col1:
        if st.button("◀ 1つ前に戻る", use_container_width=True):
            if st.session_state.choices:
                st.session_state.choices.pop()
            if choices[:2] == ["塗装面", "面改修"] and step == 4:
                st.session_state.step = 2
            elif "防水・保護工法" in st.session_state.choices and len(choices) == 5:
                st.session_state.step = 4
            else:
                st.session_state.step = max(1, step - 1)
            st.rerun()
            
    with back_col2:
        if st.button("🔄 最初からやり直す", use_container_width=True):
            st.session_state.step = 1
            st.session_state.choices = []
            st.rerun()
