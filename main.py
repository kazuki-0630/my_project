import csv
import io
from datetime import timedelta

TIME_SLOTS = [
    "10-12",
    "12-14",
    "14-16",
    "16-18",
    "18-20",
    "20-22",
]

WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]


def generate_schedule(
    start_date,
    end_date,
):
    results = []

    current = start_date

    while current <= end_date:
        for slot in TIME_SLOTS:
            date_str = f"{current.month}/{current.day}"
            weekday_str = WEEKDAYS[current.weekday()]

            results.append(f"{date_str}({weekday_str}) {slot}")

        current += timedelta(days=1)

    return results


def load_chouseisan_csv(file):
    text = file.read().decode("cp932")
    csv_file = io.StringIO(text)

    # 調整さんCSVの説明行を読み飛ばす
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


def format_merged_slots(merged):
    # マージ済みの日程データを表示用テキストに変換する
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


def merge_time_slots(results):
    # 同じ参加メンバー状態の連続時間帯を結合する
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
        # 日付・時間帯・参加状況が連続している場合は結合
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

    return format_merged_slots(merged)
