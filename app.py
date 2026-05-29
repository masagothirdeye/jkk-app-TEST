import streamlit as st

# ページの初期設定
st.set_page_config(page_title="JKK外壁改修フロー判定", layout="centered")

# タイトル表示
st.title("🏗️ JKK関西 外壁改修・フローチャート判定アプリ")
st.write("選択肢を順番に選ぶだけで、最適な工法を自動で判定します。")
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
    
    # ルート分岐のロジック
    # ① タイル面 ＞ 面改修 ＞ 剥落防止工法 の場合（溶剤か水性か選ぶ）
    if choices == ["タイル面", "面改修", "剥落防止工法"]:
        st.subheader("【ステップ 4】塗料の系統を選んでください")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧪 溶剤系", use_container_width=True):
                st.session_state.choices.append("溶剤系")
                st.session_state.step = 5 # 溶剤系はさらに選択肢あり
                st.rerun()
        with col2:
            if st.button("🚰 水性系", use_container_width=True):
                st.session_state.choices.append("水性系")
                st.session_state.step = 5 # 水性系もさらに選択肢あり
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

    # 以下はステップ4の時点で最終工法が1つに確定するルート
    else:
        st.success("🎉 最適な工法が決定しました！")
        
        # タイル面 ＞ 部分改修
        if choices == ["タイル面", "部分改修"]:
            st.metric(label="推奨工法", value="JKテラピン工法")
            st.caption("（注入口付アンカーピンニングエポキシ樹脂注入工法 / 国交省仕様適合工法）")
            
        # 塗装面 ＞ 面改修
        elif choices == ["塗装面", "面改修"]:
            st.write("**外壁塗膜防水工法（水性系）**")
            st.metric(label="推奨工法", value="JKウォール工法")
            st.caption("アクリルゴム系 / JIS A 6021")
            
        # 塗装面 ＞ 部分改修
        elif choices == ["塗装面", "部分改修"]:
            st.write("**ノンカットひび割れ補修工法 / アスベスト対策工法（水性系）**")
            st.metric(label="推奨工法", value="JKラビング工法")

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
        # 下段に3つ目のボタン
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
        
        # 剥落防止 ＞ 溶剤の結果分岐
        if "アクリル樹脂（標準仕様）" in choices:
            st.metric(label="推奨工法", value="JKセライダー工法（標準仕様）")
            st.caption("アクリル樹脂 / UR都市機構 品質基準適合工法")
        elif "アクリル樹脂（防水仕様）" in choices:
            st.metric(label="推奨工法", value="JKセライダー工法（防水仕様）")
            st.caption("アクリル樹脂 / UR都市機構 品質基準適合工法")
        elif "ウレタン樹脂（標準仕様）" in choices:
            st.metric(label="推奨工法", value="JKセライダーU工法（標準仕様）")
            st.caption("ウレタン樹脂")
            
        # 剥落防止 ＞ 水性の結果分岐
        elif "アクリル樹脂" in choices and "剥落防止工法" in choices:
            st.metric(label="推奨工法", value="水性JKセライダー工法")
            st.caption("アクリル樹脂 / UR都市機構 品質基準適合工法")
        elif "ウレタン樹脂" in choices and "剥落防止工法" in choices:
            st.metric(label="推奨工法", value="JKクリアファイバーW工法")
            st.caption("ウレタン樹脂 / UR都市機構 品質基準適合工法")
            
        # 防水・保護 ＞ 溶剤の結果
        elif "溶剤系" in choices and "防水・保護工法" in choices:
            st.metric(label="推奨工法", value="JKコート工法")
            st.caption("アクリル樹脂")
            
        # 防水・保護 ＞ 水性の結果
        elif "水性系" in choices and "防水・保護工法" in choices:
            st.metric(label="推奨工法", value="JKクリアコートW工法")
            st.caption("ウレタン樹脂")


# ---------------------------------------------------------
# 🔙 戻るボタンエリア（ステップ1以外で常に画面下部に表示）
# ---------------------------------------------------------
if step > 1:
    st.markdown("---")
    back_col1, back_col2 = st.columns(2)
    
    with back_col1:
        if st.button("◀ 1つ前に戻る", use_container_width=True):
            # 1つ前の状態に戻す処理
            st.session_state.choices.pop()
            # 塗装面・面改修から戻る時はステップ2へ、それ以外は1つ減らす
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
