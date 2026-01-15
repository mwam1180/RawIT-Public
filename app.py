import google.generativeai as genai
import streamlit as st
import datetime

API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="RawIT", page_icon="⚖️")
st.title('RawIT - 怒りの陳述書メーカー')
st.markdown("事故の状況を入力するだけで、法的に武装された最強の文書を作成します。")

with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        victim_name = st.text_input("あなたの名前(甲)", placeholder="名前を入力してください")
    with col2:
        target_name = st.text_input("相手の名前・保険会社(乙)", placeholder="保険会社の名前を入れてください。わからない場合は空白で結構です。")

    accident_date = st.date_input("事故発生日", datetime.date(2024, 3, 1))

    anger_content = st.text_area("相手への不満・言いたいこと（具体的に）", height=150,
                                placeholder="例：誠意がない。提示額が低すぎる。こっちは後遺症で苦しいんでるんだ。")
    
    submittend = st.form_submit_button("法的文書を作成する！")

if submittend:
    if not anger_content:
        st.error("不満の内容を入力してください")
    else:
        with st.spinner("AI弁護士が起案中..."):
            prompt = f"""
            あなたはプロの行政書士兼、交渉の達人です。
            以下の情報を元に、保険会社（または加害者）に送付する「通知書」または「陳述書」を作成してください。
            
            【要件】
            - 感情的にならず、極めて冷静かつ論理的な「法的ビジネス文書」のトーンで。
            - しかし、内容は相手に「こいつは面倒だ、裁判になったら負ける」と思わせるプレッシャーを含めること。
            - 以下の事実は必ず盛り込むこと。
            
            【情報】
            - 日付: {datetime.date.today().strftime('%Y年%m月%d日')}
            - 差出人（甲）: {victim_name}
            - 受取人（乙）: {target_name}
            - 事故日: {accident_date.strftime('%Y年%m月%d日')}
            - 被害者の主張: {anger_content}
            """

            try:
                response = model.generate_content(prompt)
                generated_text = response.text

                st.success("生成完了！")
                st.markdown("### 📄 完成した文書")
                st.text_area("コピー用", generated_text, height = 400)

                st.download_button(
                    label="💾 テキストファイルとして保存",
                    data=generated_text,
                    file_name=f"陳述書_{datetime.date.today()}.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"エラー発生: {e}")