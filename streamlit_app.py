import streamlit as st
import pandas as pd

# タイトル
st.title("課題4　計算問題 正誤判定アプリ")

# CSVファイルから正解データを読み込み
df = pd.read_csv("data.csv")

# 学生番号入力
student_id = st.text_input("あなたの学生番号（下3ケタ）を入力してください", max_chars=3)

if student_id and student_id in df["学生番号"].astype(str).values:
    st.write("以下の各問題に答えてください（小数第2位まで）")

    # 回答入力
    q1 = st.number_input("(1)", step=0.01, format="%.2f")
    q2 = st.number_input("(2)", step=0.01, format="%.2f")
    q3 = st.number_input("(3)", step=0.01, format="%.2f")
    q4 = st.number_input("(4)", step=0.01, format="%.2f")

    if st.button("判定する"):
        # 入力した学生番号の正解行を取得
        correct = df[df["学生番号"].astype(str) == student_id].iloc[0]

        # 判定（小数第2位で比較）
        def is_correct(answer, correct_value):
            return round(answer, 2) == round(correct_value, 2)

        results = [
            is_correct(q1, correct["(1)"]),
            is_correct(q2, correct["(2)"]),
            is_correct(q3, correct["(3)"]),
            is_correct(q4, correct["(4)"]),
        ]

        # 結果表示
        for i, res in enumerate(results, start=1):
            st.write(f"( {i} )：{'✅ 正解' if res else '❌ 不正解'}")

else:
    if student_id:
        st.warning("その学生番号は登録されていません。")
