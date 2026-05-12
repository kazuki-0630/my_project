import sys
import csv
import io
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


def load_chouseisan_csv(file):
    text = file.read().decode("cp932")
    csv_file = io.StringIO(text)

    # 最初の2行を飛ばす
    next(csv_file)
    next(csv_file)

    reader = csv.DictReader(csv_file)
    rows = list(reader)

    return rows


def analyze_schedule(rows, min_circle_count):
    results = []

    for row in rows:
        circle_members = []
        triangle_members = []
        cross_members = []

        for name, status in row.items():
            if status == "◯":
                circle_members.append(name)
            elif status == "△":
                triangle_members.append(name)
            elif status == "×":
                cross_members.append(name)

        if len(circle_members) >= min_circle_count:
            results.append(
                {
                    "schedule": row["日程"],
                    "circle_members": circle_members,
                    "triangle_members": triangle_members,
                    "cross_members": cross_members,
                }
            )
    return results


def merge_time_slots(results):
    # 連続している時間帯をまとめる
    slots = []

    for result in results:
        date, time = result["schedule"].split()
        start, end = time.split("-")

        slots.append(
            {
                "date": date,
                "start": int(start),
                "end": int(end),
                "circle_members": result["circle_members"],
                "triangle_members": result["triangle_members"],
                "cross_members": result["cross_members"],
            }
        )

    merged = []
    if not slots:
        return []
    current = slots[0]

    for next_slot in slots[1:]:
        if (
            current["date"] == next_slot["date"]
            and current["end"] == next_slot["start"]
            and current["circle_members"] == next_slot["circle_members"]
            and current["triangle_members"] == next_slot["triangle_members"]
            and current["cross_members"] == next_slot["cross_members"]
        ):
            current["end"] = next_slot["end"]

        else:
            merged.append(current)
            current = next_slot

    merged.append(current)

    formatted_results = []

    for slot in merged:
        triangle_text = " ".join(slot["triangle_members"])
        cross_text = " ".join(slot["cross_members"])

        text = f"{slot['date']} {slot['start']}-{slot['end']}"

        if triangle_text:
            text += f" △: {triangle_text}"

        if cross_text:
            text += f" ×: {cross_text}"

        formatted_results.append(text)
    return formatted_results


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

    with open("chouseisan.csv", "rb") as file:
        rows = load_chouseisan_csv(file)

    results = analyze_schedule(rows, 3)

    print(merge_time_slots(results))


if __name__ == "__main__":
    main()
