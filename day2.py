

with open("data/input2.txt") as f:
    data = f.read().splitlines()
# One report per line, many levels per report
reports = [d.split(" ") for d in data]



# Part 1
# So, a report only counts as safe if both of the following are true:
# The levels are either all increasing or all decreasing.
# Any two adjacent levels differ by at least one and at most three.
safe_cnt = 0
for report in reports:
    # Convert all elements to ints
    report = list(map(int, report))
    diffs = [report[i+1] - report[i] for i in range(len(report)-1)]
    # For the first one:
    if all(d > 0 for d in diffs) or all(d < 0 for d in diffs):
        # For the second one:
        if all(1 <= abs(d) <= 3 for d in diffs):
            print(report)
            safe_cnt += 1
print(safe_cnt)


# Part 2
# Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.
# We need to find the number of safe reports.
def report_is_safe(report):
    diffs = [report[i+1] - report[i] for i in range(len(report)-1)]
    if all(d > 0 for d in diffs) or all(d < 0 for d in diffs):
        if all(1 <= abs(d) <= 3 for d in diffs):
            return True
    # print(f"Unsafe report: {report} / {diffs}")
    return False

safe_cnt = 0
for report in reports:
    # Convert all elements to ints
    report = list(map(int, report))
    if report_is_safe(report):
        safe_cnt += 1
    else:
        # If the report is unsafe, check if removing a single level would make it safe
        # Example unsafe report that should be safe Unsafe report: [96, 98, 95, 95, 95] / [2, -3, 0, 0]
        for i in range(len(report)):
            tmp_report = report[:i] + report[i+1:]
            if report_is_safe(tmp_report):
                print(f"Unsafe report that should be safe {report}")
                safe_cnt += 1
                break
print(safe_cnt)