import streamlit as st
import google.generativeai as genai

# 関数定義箇所

def load_prompt_template(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Gemini APIの設定（st.secretsから取得）
gemini_api_key = st.secrets["GEMINI_API_KEY"]
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("GEMINI_API_KEYが設定されていません。.streamlit/secrets.tomlファイルにGEMINI_API_KEYを追加してください。")
    st.stop()

def make_cosmic(prompt, template_path):
    # プロンプトテンプレートを読み込み & 差し込み
    template = load_prompt_template(template_path)
    full_prompt = template.format(user_input=prompt)

    # Geminiモデルの呼び出し
    response = model.generate_content(full_prompt)

    return response.text.strip()

# パラメータ設定
template_path = "prompts/cosmic_template.txt"

#  メモリ上の掲示板
if "posts" not in st.session_state:
    st.session_state.posts = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def post_message():
    user_input = st.session_state.user_input
    if user_input:
        try:
            cosmic_reply = make_cosmic(user_input, template_path)
            st.session_state.posts.insert(0, (user_input, cosmic_reply))
            st.session_state.user_input = ""  # 入力欄をクリア
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

st.title("🌌 宇宙っぽい掲示板")

# 入力フォーム（エンターで送信）
st.text_input(
    "あなたの投稿をどうぞ",
    key="user_input",
    on_change=post_message
)

# 掲示板表示
st.subheader("🛰 投稿一覧")
for original, cosmic in st.session_state.posts:
    st.markdown(f"🧑‍🚀 **あなた:** {original}")
    st.markdown(f"🌠 **宇宙変換:** {cosmic}")
    st.markdown("---")
