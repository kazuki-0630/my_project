from flask import Flask, render_template, request
from datetime import datetime
from main import generate_schedule

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    error = ""
    start_date_str = ""
    end_date_str = ""

    if request.method == "POST":
        start_date_str = request.form["start_date"]
        end_date_str = request.form["end_date"]

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            if start_date > end_date:
                error = "開始日は終了日より前にしてください。"
            else:
                schedule = generate_schedule(start_date, end_date)
                result = "\n".join(schedule)

        except ValueError:
            error = "入力が正しくありません"

    return render_template(
        "index.html",
        result=result,
        error=error,
        start_date=start_date_str,
        end_date=end_date_str,
    )


if __name__ == "__main__":
    app.run(debug=True)
