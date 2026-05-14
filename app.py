from flask import Flask, render_template, request
from datetime import datetime
from main import (
    generate_schedule,
    load_chouseisan_csv,
    analyze_schedule,
    merge_time_slots,
)


def handle_schedule_form():
    schedule_result = ""
    schedule_error = ""
    start_date_str = ""
    end_date_str = ""

    start_date_str = request.form.get("start_date", "")
    end_date_str = request.form.get("end_date", "")

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        if start_date > end_date:
            return (
                "",
                "開始日は終了日より前にしてください。",
                start_date_str,
                end_date_str,
            )

        schedule = generate_schedule(start_date, end_date)
        schedule_result = "\n".join(schedule)

    except ValueError:
        return "", "入力が正しくありません", start_date_str, end_date_str

    return schedule_result, schedule_error, start_date_str, end_date_str


def handle_csv_form():
    csv_result = ""
    csv_error = ""
    min_count_str = "6"

    csv_file = request.files.get("csv_file")

    if not csv_file or not csv_file.filename:
        return "", "CSVファイルを選択してください。", min_count_str

    min_count_str = request.form.get("min_count", "6")

    try:
        min_count = int(min_count_str)
    except ValueError:
        return "", "最低参加人数は数字で入力してください。", min_count_str

    if min_count <= 0:
        return "", "最低参加人数は1以上にしてください。", min_count_str

    try:
        rows = load_chouseisan_csv(csv_file)
        results = analyze_schedule(rows, min_count)
        csv_result = "\n".join(merge_time_slots(results))

        if not csv_result:
            return "", "条件に合う日程はありませんでした。", min_count_str

    # CSV読み込み・解析時のエラー
    except Exception:
        return "", "CSVの形式が正しくありません。", min_count_str

    return csv_result, csv_error, min_count_str


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    schedule_result = ""
    csv_result = ""
    schedule_error = ""
    csv_error = ""
    start_date_str = ""
    end_date_str = ""
    min_count_str = "6"

    if request.method == "POST":
        if "start_date" in request.form:
            (
                schedule_result,
                schedule_error,
                start_date_str,
                end_date_str,
            ) = handle_schedule_form()

        elif "csv_file" in request.files:
            (
                csv_result,
                csv_error,
                min_count_str,
            ) = handle_csv_form()

    return render_template(
        "index.html",
        schedule_result=schedule_result,
        csv_result=csv_result,
        schedule_error=schedule_error,
        csv_error=csv_error,
        start_date=start_date_str,
        end_date=end_date_str,
        min_count=min_count_str,
    )


if __name__ == "__main__":
    app.run(debug=True)
