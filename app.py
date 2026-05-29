import streamlit as st

# ページの初期設定
st.set_page_config(page_title="JKK外壁改修フロー判定", layout="centered")

# タイトル表示
st.title("🏗️ JKK関西 外壁改修・フローチャート判定アプリ")
st.write("選択肢を順番に選ぶだけで、最適な工法と、その工法の特徴を自動で判定します。")
st.markdown("---")

# 画面状態（どのステップにいるか、これまでの選択肢）を記憶する仕組み
if "step" not in st.session_state:
    st.session_state.step = 1
if "choices" not in st.session_state:
    st.session_state.choices = []

# 現在のステップに応じた処理
step = st.session_state.step
choices = st.session_state.choices

# ---------------------------------------------------------
# ステップ1：下地選択
# ---------------------------------------------------------
if step == 1:
    st.subheader("【ステップ 1】下地を選んでください")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧱 タイル面", use_container_width=True):
            st.session_state.choices.append("タイル面")
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("🎨 塗装面", use_container_width=True):
            st.session_state.choices.append("塗装面")
            st.session_state.step = 2
            st.rerun()

# ---------------------------------------------------------
# ステップ2：改修範囲の選択
# ---------------------------------------------------------
elif step == 2:
    st.subheader(f"現在：{ ' ＞ '.join(choices) }")
    st.subheader("【ステップ 2】改修の範囲を選んでください")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏢 面改修", use_container_width=True):
            st.session_state.choices.append("面改修")
            # 塗装面・面改修の場合は、次は工法確定（ステップ4相当）へジャンプ
            if choices[0] == "塗装面":
                st.session_state.step = 4
            else:
                st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("🛠️ 部分改修", use_container_width=True):
            st.session_state.choices.append("部分改修")
            st.session_state.step = 4  # タイル面・塗装面ともに部分改修は次のステップで確定
            st.rerun()

# ---------------------------------------------------------
# ステップ3：工法目的の選択（タイル面・面改修のみ）
# ---------------------------------------------------------
elif step == 3:
    st.subheader(f"現在：{ ' ＞ '.join(choices) }")
    st.subheader("【ステップ 3】改修の目的を選んでください")
    
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
    st.subheader(f"現在：{ ' ＞ '.join(choices) }")
    
    # ① タイル面 ＞ 面改修 ＞ 剥落防止工法 の場合（溶剤か水性か選ぶ）
    if choices == ["タイル面", "面改修", "剥落防止工法"]:
        st.subheader("【ステップ 4】塗料の系統を選んでください")
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
                
    # ② タイル面 ＞ 面改修 ＞ 防水・保護工法 の場合（溶剤か水性か選ぶ）
    elif choices == ["タイル面", "面改修", "防水・保護工法"]:
        st.subheader("【ステップ 4】塗料の系統を選んでください")
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

    # 以下はステップ4の時点で最終工法が確定するルート
    else:
        st.success("🎉 最適な工法が決定しました！")
        
        # タイル面 ＞ 部分改修
        if choices == ["タイル面", "部分改修"]:
            st.metric(label="推奨工法", value="JKテラピン工法")
            with st.expander("🔍 工法の特徴・詳細を見る", expanded=True):
                st.markdown("""
                * **工法名**: 注入口付アンカーピンニングエポキシ樹脂注入工法
                * **適合規格**: 国交省仕様適合工法
                * **特徴**: 
                  * タイル面の部分改修における代表的な工法です。
                  * 特殊なアンカーピンとエポキシ樹脂を用いて、タイルの浮きや剥落をピンポイントで確実に防止します。
                  * 意匠性を損なわずに、下地コンクリートとタイル層を強力に一体化させます。
                """)
            
        # 塗装面 ＞ 面改修
        elif choices == ["塗装面", "面改修"]:
            st.metric(label="推奨工法", value="JKウォール工法")
            with st.expander("🔍 工法の特徴・詳細を見る", expanded=True):
                st.markdown("""
                * **工法名**: 外壁塗膜防水工法（水性系）
                * **主成分**: アクリルゴム系
                * **適合規格**: JIS A 6021
                * **特徴**: 
                  * 塗装面の面改修に最適な、高耐久な水性防水工法です。
                  * 抜群のひび割れ追従性を誇るアクリルゴム系の塗膜により、外壁からの雨水浸入をシャットアウトします。
                  * 水性系のため環境に優しく、施工中の臭気も抑えられます。
                """)
            
        # 塗装面 ＞ 部分改修
        elif choices == ["塗装面", "部分改修"]:
            st.metric(label="推奨工法", value="JKラビング工法")
            with st.expander("🔍 工法の特徴・詳細を見る", expanded=True):
                st.markdown("""
                * **工法名**: ノンカットひび割れ補修工法 / アスベスト対策工法（水性系）
                * **特徴**: 
                  * 塗装面のひび割れを、Uカットなどの切削を行わずに補修できる工法です。
                  * 既存塗膜を削らないため、下地にアスベスト（石綿）が含まれている場合でも粉塵を飛散させず、安全かつ迅速に施工が可能です。
                """)

# ---------------------------------------------------------
# ステップ5：最終確定（タイル面・面改修の溶剤／水性ルートの分岐）
# ---------------------------------------------------------
elif step == 5:
    st.subheader(f"現在：{ ' ＞ '.join(choices) }")
    
    # 剥落防止工法 ＞ 溶剤系 の選択
    if choices == ["タイル面", "面改修", "剥落防止工法", "溶剤系"]:
        st.subheader("【ステップ 5】仕様を選んでください")
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

    # 剥落防止工法 ＞ 水性系 の選択
    elif choices == ["タイル面", "面改修", "剥落防止工法", "水性系"]:
        st.subheader("【ステップ 5】樹脂の種類を選んでください")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("アクリル樹脂", use_container_width=True):
                st.session_state.choices.append("アクリル樹脂")
                st.rerun()
        with col2:
            if st.button("ウレタン樹脂", use_container_width=True):
                st.session_state.choices.append("ウレタン樹脂")
                st.rerun()

    # ここからは結果表示
    else:
        st.success("🎉 最適な工法が決定しました！")
        
        # ① 🛠️ JKセライダー工法（標準仕様）
        if "アクリル樹脂（標準仕様）" in choices:
            st.metric(label="推奨工法", value="JKセライダー工法（標準仕様）")
            with st.expander("🔍 工法の特徴・詳細を見る", expanded=True):
                st.markdown("""
                * **主成分**: アクリル樹脂（溶剤系）
                * **適合規格**: UR都市機構 品質基準適合工法
                * **特徴**: 
                  * タイル面の面改修・剥落防止における代表的なロングセラー工法です。
                  * 透明性の高いクリアなアクリル樹脂と特殊意匠ピンを使用し、タイルの風合い・デザインをそのまま残して美しく仕上げます。
                """)
                
        # ② 💧 JKセライダー工法（防水仕様）
        elif "アクリル樹脂（防水仕様）" in choices:
            st.metric(label="推奨工法", value="JKセライダー工法（防水仕様）")
            with st.expander("🔍 工法の特徴・詳細を見る", expanded=True):
                st.markdown("""
                * **主成分**: アクリル樹脂（溶剤系）
                * **適合規格**: UR都市機構 品質基準適合工法
                * **特徴**: 
                  * 標準仕様の持つ高い剥落防止性能に加えて、さらに**防水性能**を高めた仕様です。
                  * 目地からの雨水浸入を強力に防ぎ、建物の構造体（コンクリート）の長寿命化に大きく貢献します。
                """)
                
        # ③ 🧪 JKセライダーU工法（標準仕様）
        elif "ウレタン樹脂（標準仕様）" in choices:
            st.metric(label="推奨工法", value="JKセライダーU工法（標準仕様）")
            with st.expander("🔍 工法の特徴・詳細を見る", expanded=True):
                st.markdown("""
                * **主成分**: ウレタン樹脂（溶剤系）
                * **特徴**: 
                  * 強靭で柔軟な塗膜を形成するウレタン樹脂の特性を活かした剥落防止工法です。
                  * タイルや下地の細かな挙動（温度変化などによる伸縮）に対しても、高い追従性と粘り強さを発揮します。
                """)
            
        # ④ 🚰 水性JKセライダー工法
        elif "アクリル樹脂" in choices and "剥落防止工法" in choices:
            st.metric(label="推奨工法", value="水性JKセライダー工法")
            with st.expander("🔍 工法の特徴・詳細を見る", expanded=True):
                st.markdown("""
                * **主成分**: アクリル樹脂（水性系）
                * **適合規格**: UR都市機構 品質基準適合工法
                * **特徴**: 
                  * 名工法「JKセライダー」の性能をそのままに、完全水性化を実現した環境配慮型工法です。
                  * 溶剤系特有のシンナー臭が一切ないため、マンションや病院、学校など、居住者や近隣への臭気配慮が最優先される現場に最適です。
                """)
                
        # ⑤ 🛡️ JKクリアファイバーW工法
        elif "ウレタン樹脂" in choices and "剥落防止工法" in choices:
            st.metric(label="推奨工法", value="JKクリアファイバーW工法")
            with st.expander("🔍 工法の特徴・詳細を見る", expanded=True):
                st.markdown("""
                * **主成分**: ウレタン樹脂（水性系）
                * **適合規格**: UR都市機構 品質基準適合工法
                * **特徴**: 
                  * 水性ウレタン樹脂と特殊繊維を組み合わせることで、非常に高い引張強度と耐久性を実現した剥落防止工法です。
                  * 水性なので臭いが少なく、安全かつ強固に外壁タイルをホールドします。
                """)
            
        # ⑥ 🧪 JKコート工法
        elif "溶剤系" in choices and "防水・保護工法" in choices:
            st.metric(label="推奨工法", value="JKコート工法")
            with st.expander("🔍 工法の特徴・詳細を見る", expanded=True):
                st.markdown("""
                * **主成分**: アクリル樹脂（溶剤系）
                * **特徴**: 
                  * タイル面の美観維持と「防水・保護」を主目的としたクリアー仕上げの工法です。
                  * タイルや目地へ雨水が染み込むのを強力にブロックし、エフロレッセンス（白華現象）の発生や中性化を長期間にわたって抑制します。
                """)
            
        # ⑦ 🚰 JKクリアコートW工法
        elif "水性系" in choices and "防水・保護工法" in choices:
            st.metric(label="推奨工法", value="JKクリアコートW工法")
            with st.expander("🔍 工法の特徴・詳細を見る", expanded=True):
                st.markdown("""
                * **主成分**: ウレタン樹脂（水性系）
                * **特徴**: 
                  * タイル面の防水・保護工法を、環境に優しい水性ウレタン樹脂で構成した工法です。
                  * 水性特有の安全・低臭性を持ちながら、ウレタン特有のシブとい柔軟性で外壁の微細な動きを保護し、雨水から建物を守ります。
                """)


# ---------------------------------------------------------
# 🔙 戻るボタンエリア（ステップ1以外で常に画面下部に表示）
# ---------------------------------------------------------
if step > 1:
    st.markdown("---")
    back_col1, back_col2 = st.columns(2)
    
    with back_col1:
        if st.button("◀ 1つ前に戻る", use_container_width=True):
            st.session_state.choices.pop()
            if choices == ["塗装面", "面改修"]:
                st.session_state.step = 2
            elif step == 5 and ("防水・保護工法" in st.session_state.choices or "部分改修" in st.session_state.choices):
                st.session_state.step = 4
            else:
                st.session_state.step = max(1, step - 1)
            st.rerun()
            
    with back_col2:
        if st.button("🔄 最初からやり直す", use_container_width=True):
            st.session_state.step = 1
            st.session_state.choices = []
            st.rerun()
