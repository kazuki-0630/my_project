from flask import Flask, render_template, request
from datetime import datetime
from main import (
    generate_schedule,
    load_chouseisan_csv,
    analyze_schedule,
    merge_time_slots,
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    schedule_result = ""
    csv_result = ""
    error = ""
    start_date_str = ""
    end_date_str = ""

    if request.method == "POST":
        if "start_date" in request.form:
            start_date_str = request.form["start_date"]
            end_date_str = request.form["end_date"]

            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

                if start_date > end_date:
                    error = "開始日は終了日より前にしてください。"
                else:
                    schedule = generate_schedule(start_date, end_date)
                    schedule_result = "\n".join(schedule)

            except ValueError:
                error = "入力が正しくありません"

        elif "csv_file" in request.files:
            csv_file = request.files["csv_file"]

            if csv_file.filename == "":
                error = "CSVファイルを選択してください。"
            else:
                min_count = int(request.form["min_count"])
                rows = load_chouseisan_csv(csv_file)
                results = analyze_schedule(rows, min_count)
                csv_result = "\n".join(merge_time_slots(results))

    return render_template(
        "index.html",
        schedule_result=schedule_result,
        csv_result=csv_result,
        error=error,
        start_date=start_date_str,
        end_date=end_date_str,
    )


if __name__ == "__main__":
    app.run(debug=True)
