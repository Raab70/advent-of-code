from datetime import datetime
from rich import print
from collections import defaultdict
from aoc.requests import get_session


def fetch_leaderboard(year: int = 2024, board_id: int = 3239080):
    session = get_session()
    url = f"https://adventofcode.com/{year}/leaderboard/private/view/{board_id}.json"
    resp = session.get(url)
    resp.raise_for_status()
    return resp.json()


def print_day_leaders(parts, day: int, n: int = 5):
    parts = dict(sorted(parts.items(), reverse=True))
    for part, members in parts.items():
        print(f"Day {day} Part {part}")
        prev = None
        for member, timestamp in sorted(members, key=lambda x: x[1])[:n]:
            diff_str = None
            if prev is not None:
                diff = timestamp - prev
                if diff < 60:
                    diff_str = f"({diff} [yellow]seconds[/yellow])"
                else:
                    diff_str = f"({diff // 60} minutes)"

            if diff_str:
                print(
                    f"  {member:25s} - {datetime.fromtimestamp(timestamp)} {diff_str}"
                )
            else:
                print(f"  {member:25s} - {datetime.fromtimestamp(timestamp)}")
            prev = timestamp


def print_daily_top_n(data, n: int = 5, day: int = None):
    print("Daily Leaderboard")
    daily_leaderboard = defaultdict(lambda: defaultdict(list))
    for member_data in data["members"].values():
        member_name = member_data["name"]
        if not member_name:
            continue
        for day_str, completion in member_data["completion_day_level"].items():
            for part, star_info in completion.items():
                daily_leaderboard[int(day_str)][int(part)].append(
                    (member_name, star_info["get_star_ts"])
                )
    if day is not None:
        daily_leaderboard = {day: daily_leaderboard[day]}
    # Sort the dictionary so that the days and parts are in descending order
    daily_leaderboard = dict(sorted(daily_leaderboard.items(), reverse=True))
    for day, parts in daily_leaderboard.items():
        print()
        print_day_leaders(parts, day, n)

    # Now print the number of first place finishes for each member
    print("\nFirst Place Finishes")
    first_place = defaultdict(int)
    for day, parts in daily_leaderboard.items():
        for part, members in parts.items():
            sorted_members = sorted(members, key=lambda x: x[1])[:n]
            first_place[sorted_members[0][0]] += 1
    first_place = sorted(first_place.items(), key=lambda x: x[1], reverse=True)
    for member, count in first_place:
        print(f"  {member:25s} - {count}")


if __name__ == "__main__":
    data = fetch_leaderboard()
    print_daily_top_n(data)
