import streamlit as st
import pandas as pd

# データの読み込み（キャッシュで高速化）
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df['学生番号'] = df['学生番号'].astype(str).str.zfill(3)
    return df

df = load_data()

# タイトル
st.title("課題4　計算問題 自己チェック")

# 入力欄
student_id = st.text_input("学生番号（下3桁）を入力", max_chars=3)
answer1 = st.text_input("（1）のあなたの解答　小数点以下第3位を四捨五入（例：1.76）")
answer2 = st.text_input("（2）のあなたの解答　小数点以下第3位を四捨五入（例：1.98）")
answer3 = st.text_input("（3）のあなたの解答　小数点以下第3位を四捨五入（例：1.83）")
answer4 = st.text_input("（4）のあなたの解答　小数点以下第3位を四捨五入（例：2.30）")

# 判定ボタン
if st.button("判定する"):
    if not student_id.isdigit() or len(student_id) != 3:
        st.error("学生番号は3桁の数字で入力してください。")
    else:
        record = df[df['学生番号'] == student_id]
        if record.empty:
            st.warning("該当する学生番号が見つかりません。")
        else:
            try:
                # ユーザーの解答をfloatに変換（小数第2位で丸め）
                user_answers = [
                    round(float(answer1), 2),
                    round(float(answer2), 2),
                    round(float(answer3), 2),
                    round(float(answer4), 2),
                ]
                # 正解値の取得（CSVの2列目以降）
                correct_answers = [
                    round(float(record.iloc[0][1]), 2),
                    round(float(record.iloc[0][2]), 2),
                    round(float(record.iloc[0][3]), 2),
                    round(float(record.iloc[0][4]), 2),
                ]

                # 判定処理
                for i, (user, correct) in enumerate(zip(user_answers, correct_answers), start=1):
                    result = "正解" if abs(user - correct) < 0.01 else "不正解"
                    st.success(f"（{i}）：{result}")

            except ValueError:
                st.error("すべての解答を数値で入力してください。")
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
