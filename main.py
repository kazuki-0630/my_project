import sys
from datetime import datetime, timedelta


def generate_schedule(start_date, end_date):
    results = []

    time_slots = [
        "10-12",
        "12-14",
        "14-16",
        "16-18",
        "18-20",
        "20-22",
    ]

    weekdays = ["月", "火", "水", "木", "金", "土", "日"]

    current = start_date

    while current <= end_date:
        for slot in time_slots:
            date_str = f"{current.month}/{current.day}"
            weekday_str = weekdays[current.weekday()]

            results.append(f"{date_str}({weekday_str}) {slot}")

        current += timedelta(days=1)

    return results


def main():
    args = sys.argv

    if len(args) == 3:
        start_date_str = args[1]
        end_date_str = args[2]

    elif len(args) == 1:
        start_date_str = "2026-05-04"
        end_date_str = "2026-05-06"

    else:
        print("使い方: python main.py 開始日 終了日")
        return

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        if start_date > end_date:
            print("開始日は終了日より前にしてください。")
            return

    except ValueError:
        print("日付は YYYY-MM-DD の形式で入力してください。")
        return

    schedule = generate_schedule(start_date, end_date)
    output_text = "\n".join(schedule)
    print(output_text)


if __name__ == "__main__":
    main()
