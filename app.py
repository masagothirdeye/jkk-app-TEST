import streamlit as st

# ページの初期設定
st.set_page_config(
    page_title="JKK関西 外壁改修フロー判定", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🎨 カスタムデザイン（CSS）
st.markdown("""
    <style>
    /* 全体の背景：しっかりとした上品な薄緑 */
    .stApp {
        background-color: #d1e2c4 !important; 
    }
    
    /* 通常テキスト、箇条書き、ラベルを強制的に「真っ黒」にする */
    .stApp p, .stApp li, .stApp span, .stApp label, .stApp div {
        color: #000000 !important;
    }
    
    /* 各ステップの見出し：特大の真っ黒太字 */
    .stSubheader div, .stSubheader h3, .stSubheader span {
        color: #000000 !important; 
        font-weight: 800 !important;
        font-size: 22px !important;
    }
    .stSubheader {
        border-left: 6px solid #1e5e29;
        padding-left: 12px;
        margin-top: 25px;
        margin-bottom: 20px;
    }
    
    /* 現在の選択ルート表示（ハッキリとした白背景ボックス） */
    .route-info {
        background-color: #ffffff !important;
        padding: 12px 15px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 20px;
        border: 2px solid #1e5e29;
    }
    .route-info div {
        color: #000000 !important;
    }
    
    /* 📋 判定メッセージ部分（白背景） */
    div[data-testid="stNotification"] {
        background-color: #ffffff !important; 
        border: 2px solid #1e5e29 !important;
    }
    
    /* 🏆 結果表示ボックス */
    .result-box {
        background-color: #ffffff !important;
        border-top: 4px solid #1e5e29 !important;
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
        color: #000000 !important;
        border-bottom: 2px solid #1e5e29;
        padding-bottom: 8px;
        margin-bottom: 15px;
    }
    .result-box li {
        font-size: 16px !important;
        line-height: 1.6 !important;
        margin-bottom: 8px !important;
        color: #000000 !important;
    }

    /* ボタン全体の共通設定 */
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
        border-color: #1e5e29 !important;
        color: #1e5e29 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🟢 看板エリア（システムに絶対邪魔されないSVG画像方式・3級下げ設定）
# ---------------------------------------------------------
st.markdown("""
    <div style="background-color: #1e5e29; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <svg width="100%" height="70" viewBox="0 0 800 70" preserveAspectRatio="xMidYMid meet" style="background-color: transparent;">
            <text x="400" y="30" font-family="sans-serif" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle">日本樹脂施工協同組合（JKK関西）</text>
            <text x="400" y="58" font-family="sans-serif" font-size="12" fill="#e8f5e9" text-anchor="middle">外壁タイル面・塗装面改修 フローチャート判定システム</text>
        </svg>
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
# 各ステップの描画
# ---------------------------------------------------------

# ステップ1：下地選択
if step == 1:
    st.subheader("【ステップ 1】下地を選択してください")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧱 タイル面", use_container_width=True, type="primary"):
            st.session_state.choices = ["タイル面"]
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("🎨 塗装面", use_container_width=True, type="primary"):
            st.session_state.choices = ["塗装面"]
            st.session_state.step = 2
            st.rerun()

# ステップ2：改修範囲の選択
elif step == 2:
    st.markdown(f'<div class="route-info">📂 現在の選択：{ " ＞ ".join(choices) }</div>', unsafe_allow_html=True)
    st.subheader("【ステップ 2】改修の範囲を選択してください")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏢 面改修", use_container_width=True):
            st.session_state.choices = [choices[0], "面改修"]
            if choices[0] == "塗装面":
                st.session_state.step = 4  # 塗装面・面改修はステップ4へスキップ
            else:
                st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("🛠️ 部分改修", use_container_width=True):
            st.session_state.choices = [choices[0], "部分改修"]
            st.session_state.step = 3  # 両方とも分岐があるのでステップ3へ
            st.rerun()

# ステップ3：目的の選択
elif step == 3:
    st.markdown(f'<div class="route-info">📂 現在の選択：{ " ＞ ".join(choices) }</div>', unsafe_allow_html=True)
    st.subheader("【ステップ 3】改修の目的・工法を選択してください")
    
    col1, col2 = st.columns(2)
    
    if choices == ["タイル面", "面改修"]:
        with col1:
            if st.button("🛡️ 剥落防止工法", use_container_width=True):
                st.session_state.choices = ["タイル面", "面改修", "剥落防止工法"]
                st.session_state.step = 4
                st.rerun()
        with col2:
            if st.button("💧 防水・保護工法", use_container_width=True):
                st.session_state.choices = ["タイル面", "面改修", "防水・保護工法"]
                st.session_state.step = 4
                st.rerun()
                
    elif choices == ["タイル面", "部分改修"]:
        with col1:
            if st.button("🛡️ 剥落防止工法 (アスベスト対策)", use_container_width=True):
                st.session_state.choices = ["タイル面", "部分改修", "剥落防止工法"]
                st.session_state.step = 4
                st.rerun()
        with col2:
            if st.button("🩹 ノンカットひび割れ補修工法", use_container_width=True):
                st.session_state.choices = ["タイル面", "部分改修", "ノンカットひび割れ補修工法"]
                st.session_state.step = 4
                st.rerun()
                
    elif choices == ["塗装面", "部分改修"]:
        # 塗装面・部分改修は「ノンカットひび割れ補修工法」の択一のため、案内を出して進める
        st.info("📋 塗装面の部分改修は「ノンカットひび割れ補修工法」となります。下ボタンで次へお進みください。")
        if st.button("次へ進む ➔", use_container_width=True):
            st.session_state.choices = ["塗装面", "部分改修", "ノンカットひび割れ補修工法"]
            st.session_state.step = 4
            st.rerun()

# ステップ4：系統の選択、または最終結果の表示
elif step == 4:
    if choices == ["タイル面", "面改修", "剥落防止工法"] or choices == ["タイル面", "面改修", "防水・保護工法"]:
        st.markdown(f'<div class="route-info">📂 現在の選択：{ " ＞ ".join(choices) }</div>', unsafe_allow_html=True)
        st.subheader("【ステップ 4】塗料の系統を選択してください")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧪 溶剤系", use_container_width=True):
                st.session_state.choices = choices + ["溶剤系"]
                st.session_state.step = 5 
                st.rerun()
        with col2:
            if st.button("🚰 水性系", use_container_width=True):
                st.session_state.choices = choices + ["水性系"]
                st.session_state.step = 5 
                st.rerun()
                
    else:
        # 結果確定ルート
        st.markdown(f'<div class="route-info">📂 判定ルート：{ " ＞ ".join(choices) }</div>', unsafe_allow_html=True)
        st.info("📋 推奨工法が判定されました")
        
        if choices == ["タイル面", "部分改修", "剥落防止工法"]:
            st.markdown("""
            <div class="result-box">
                <div class="result-title">推奨工法</div>
                <div class="result-value">JKテラピン工法</div>
                <ul>
                    <li><b>仕様概要</b>: 注入口付アンカーピンニングエポキシ樹脂注入工法 / アスベスト対策工法</li>
                    <li><b>適合規格</b>: 国交省仕様適合工法</li>
                    <li><b>工法特徴</b>: 特殊アンカーピンと樹脂でタイル浮きを確実に防止。下地のアスベスト対策にも対応。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        elif choices == ["タイル面", "部分改修", "ノンカットひび割れ補修工法"]:
            st.markdown("""
            <div class="result-box">
                <div class="result-title">推奨工法</div>
                <div class="result-value">JKラビング工法</div>
                <ul>
                    <li><b>仕様概要</b>: ノンカットひび割れ補修工法 / アスベスト対策工法（水性系）</li>
                    <li><b>工法特徴</b>: タイル部分のひび割れを切削せずに補修するため、環境に優しく安全に施工可能です。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        elif choices == ["塗装面", "面改修"]:
            st.markdown("""
            <div class="result-box">
                <div class="result-title">推奨工法</div>
                <div class="result-value">JKウォール工法</div>
                <ul>
                    <li><b>仕様概要</b>: 外壁塗膜防水工法（水性系）</li>
                    <li><b>主成分</b>: アクリルゴム系</li>
                    <li><b>適合規格</b>: JIS A 6021</li>
                    <li><b>工法特徴</b>: 抜群のひび割れ追従性を誇る防水塗膜で、雨水の侵入をシャットアウトします。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        elif choices == ["塗装面", "部分改修", "ノンカットひび割れ補修工法"]:
            st.markdown("""
            <div class="result-box">
                <div class="result-title">推奨工法</div>
                <div class="result-value">JKラビング工法</div>
                <ul>
                    <li><b>仕様概要</b>: ノンカットひび割れ補修工法 / アスベスト対策工法（水性系）</li>
                    <li><b>工法特徴</b>: 塗装面のひび割れを切削（Uカット）せずに補修するため、下地のアスベスト粉塵を飛散させず安全です。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ステップ5：最終仕様の選択・表示
elif step == 5:
    if len(choices) == 4 and "剥落防止工法" in choices:
        st.markdown(f'<div class="route-info">📂 現在の選択：{ " ＞ ".join(choices) }</div>', unsafe_allow_html=True)
        
        if "溶剤系" in choices:
            st.subheader("【ステップ 5】仕様を選択してください")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("アクリル樹脂（標準仕様）", use_container_width=True):
                    st.session_state.choices = choices + ["アクリル樹脂（標準仕様）"]
                    st.rerun()
            with col2:
                if st.button("アクリル樹脂（防水仕様）", use_container_width=True):
                    st.session_state.choices = choices + ["アクリル樹脂（防水仕様）"]
                    st.rerun()
            if st.button("ウレタン樹脂（標準仕様）", use_container_width=True):
                st.session_state.choices = choices + ["ウレタン樹脂（標準仕様）"]
                st.rerun()

        elif "水性系" in choices:
            st.subheader("【ステップ 5】樹脂の種類を選択してください")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("アクリル樹脂", use_container_width=True):
                    st.session_state.choices = choices + ["アクリル樹脂"]
                    st.rerun()
            with col2:
                if st.button("ウレタン樹脂", use_container_width=True):
                    st.session_state.choices = choices + ["ウレタン樹脂"]
                    st.rerun()
                    
    else:
        # 最終結果出力画面
        st.markdown(f'<div class="route-info">📂 判定ルート：{ " ＞ ".join(choices[:4]) }</div>', unsafe_allow_html=True)
        st.info("📋 推奨工法が判定されました")
        
        if "アクリル樹脂（標準仕様）" in choices:
            st.markdown("""
            <div class="result-box">
                <div class="result-title">推奨工法</div>
                <div class="result-value">JKセライダー工法（標準仕様）</div>
                <ul>
                    <li><b>主成分</b>: アクリル樹脂（溶剤系） / UR都市機構 品質基準適合工法</li>
                    <li><b>特徴</b>: 透明性の高いクリア樹脂で、タイルの風合いをそのまま残して剥落を防止します。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif "アクリル樹脂（防水仕様）" in choices:
            st.markdown("""
            <div class="result-box">
                <div class="result-title">推奨工法</div>
                <div class="result-value">JKセライダー工法（防水仕様）</div>
                <ul>
                    <li><b>主成分</b>: アクリル樹脂（溶剤系） / UR都市機構 品質基準適合工法</li>
                    <li><b>特徴</b>: 高い剥落防止性能に加え、目地からの雨水浸入を防ぐ高い防水性を備えています。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif "ウレタン樹脂（標準仕様）" in choices:
            st.markdown("""
            <div class="result-box">
                <div class="result-title">推奨工法</div>
                <div class="result-value">JKセライダーU工法（標準仕様）</div>
                <ul>
                    <li><b>主成分</b>: ウレタン樹脂（溶剤系）</li>
                    <li><b>特徴</b>: 強靭かつ柔軟なウレタン塗膜で、下地やタイルの細かな伸縮挙動にしっかり追従します。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif "アクリル樹脂" in choices and "剥落防止工法" in choices:
            st.markdown("""
            <div class="result-box">
                <div class="result-title">推奨工法</div>
                <div class="result-value">水性JKセライダー工法</div>
                <ul>
                    <li><b>主成分</b>: アクリル樹脂（水性系） / UR都市機構 品質基準適合工法</li>
                    <li><b>特徴</b>: 性能はそのままに完全水性化。シンナー臭が一切ないため、環境に優しい仕様です。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif "ウレタン樹脂" in choices and "剥落防止工法" in choices:
            st.markdown("""
            <div class="result-box">
                <div class="result-title">推奨工法</div>
                <div class="result-value">JKクリアファイバーW工法</div>
                <ul>
                    <li><b>主成分</b>: ウレタン樹脂（水性系） / UR都市機構 品質基準適合工法</li>
                    <li><b>特徴</b>: 水性ウレタンと特殊繊維を組み合わせ、非常に高い引張強度で外壁を保持します。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif "溶剤系" in choices and "防水・保護工法" in choices:
            st.markdown("""
            <div class="result-box">
                <div class="result-title">推奨工法</div>
                <div class="result-value">JKコート工法</div>
                <ul>
                    <li><b>主成分</b>: アクリル樹脂（溶剤系）</li>
                    <li><b>特徴</b>: 判定ルート：タイル面 ＞ 面改修 ＞ 防水・保護工法 ＞ 溶剤系。タイルの美観を維持するクリアー仕上げ。目地への保水やエフロの発生を長期間抑えます。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif "水性系" in choices and "防水・保護工法" in choices:
            st.markdown("""
            <div class="result-box">
                <div class="result-title">推奨工法</div>
                <div class="result-value">JKクリアコートW工法</div>
                <ul>
                    <li><b>主成分</b>: ウレタン樹脂（水性系）</li>
                    <li><b>特徴</b>: 判定ルート：タイル面 ＞ 面改修 ＞ 防水・保護工法 ＞ 水性系。環境に優しい水性クリアー。ウレタンの柔軟性で外壁の微細な動きを保護し、雨水を防ぎます。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 🔙 【完全修正】戻るボタン・リセットエリア
# ---------------------------------------------------------
if step > 1 or len(choices) >= 3:
    st.markdown("---")
    back_col1, back_col2 = st.columns(2)
    
    with back_col1:
        if st.button("◀ 1つ前に戻る", use_container_width=True):
            # 現在のステップ数に応じて、安全かつ確実に状態を1つ巻き戻す
            if step == 5:
                if len(st.session_state.choices) > 4:
                    # 最終結果画面から仕様選択へ戻る
                    st.session_state.choices = st.session_state.choices[:4]
                else:
                    # 仕様選択画面から系統選択（ステップ4）へ戻る
                    st.session_state.choices = st.session_state.choices[:3]
                    st.session_state.step = 4
            elif step == 4:
                if choices[:2] == ["塗装面", "面改修"]:
                    st.session_state.choices = ["塗装面"]
                    st.session_state.step = 2
                else:
                    st.session_state.choices = choices[:2]
                    st.session_state.step = 3
            elif step == 3:
                st.session_state.choices = [choices[0]]
                st.session_state.step = 2
            elif step == 2:
                st.session_state.choices = []
                st.session_state.step = 1
            st.rerun()
            
    with back_col2:
        if st.button("🔄 最初からやり直す", use_container_width=True):
            st.session_state.step = 1
            st.session_state.choices = []
            st.rerun()
