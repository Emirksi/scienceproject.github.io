import json
from datetime import date, timedelta

# Bell schedules (all times in seconds since midnight)
# Normal Schedule: Mon / Tue / Thu / Fri
NORMAL_SCHED = {
    27900: [30900, "Period 1"],
    31200: [33900, "Period 2"],
    34200: [36900, "Period 3"],
    37200: [39900, "Period 4"],
    39900: [43200, "Lunch"],
    43500: [46200, "Period 5"],
    46500: [49200, "Period 6"],
    49500: [52200, "Period 7"],
    52620: [55500, "Period 8"],
}

# Advisory Schedule: Wednesdays
ADVISORY_SCHED = {
    27900: [30600, "Period 1"],
    30900: [33300, "Period 2"],
    33600: [36000, "Homeroom"],
    36300: [38700, "Period 3"],
    39000: [41400, "Period 4"],
    41400: [44100, "Lunch"],
    44400: [46800, "Period 5"],
    47100: [49500, "Period 6"],
    49800: [52200, "Period 7"],
    52620: [55500, "Period 8"],
}

# Early Release Schedule
EARLY_RELEASE_SCHED = {
    27900: [29700, "Period 1"],
    30000: [31620, "Period 2"],
    31920: [33540, "Period 3"],
    33840: [35460, "Period 4"],
    35760: [37380, "Period 5"],
    37680: [39300, "Period 6"],
    39600: [41220, "Period 7"],
    41220: [43080, "Lunch"],
}


def fmt(sched):
    """Convert int-keyed schedule dict to string-keyed for JSON."""
    return {str(k): v for k, v in sched.items()}


# Special date overrides keyed by "M/D" (no year).
# Format: "M/D" -> (schedule_type_label, schedule_dict)
SPECIAL_DATES = {
    # July 2025
    "7/4": ("No School", NORMAL_SCHED),                       # Independence Day

    # August 2025 — Preservice / Transition
    "8/18": ("No School", NORMAL_SCHED),                      # Preservice Day
    "8/19": ("No School", NORMAL_SCHED),                      # Preservice Day
    "8/20": ("No School", NORMAL_SCHED),                      # Preservice Day (Wed)
    "8/21": ("No School", NORMAL_SCHED),                      # Preservice Day
    "8/22": ("No School", NORMAL_SCHED),                      # Preservice Day
    "8/25": ("No School", NORMAL_SCHED),                      # Student Transition Day / NI
    "8/26": ("First Day", NORMAL_SCHED),                      # First Day of School (Tue)

    # September 2025
    "9/1":  ("No School", NORMAL_SCHED),                      # Labor Day (Mon)
    "9/23": ("No School", NORMAL_SCHED),                      # Non-Instructional Day (Tue)
    "9/26": ("Early Release", EARLY_RELEASE_SCHED),           # Early Release Day (Fri)

    # October 2025
    "10/2":  ("No School", NORMAL_SCHED),                     # Non-Instructional Day (Thu)
    "10/17": ("Professional Day No School", NORMAL_SCHED),    # Professional Development (Fri)
    "10/20": ("No School", NORMAL_SCHED),                     # Non-Instructional Day (Mon)

    # November 2025
    "11/3":  ("No School", NORMAL_SCHED),                     # Grading and Planning (Mon)
    "11/24": ("Early Release", EARLY_RELEASE_SCHED),          # Early Release (Mon)
    "11/25": ("Early Release", EARLY_RELEASE_SCHED),          # Early Release (Tue)
    "11/26": ("Systemwide Closure/No School", NORMAL_SCHED),  # Systemwide Closure (Wed)
    "11/27": ("No School", NORMAL_SCHED),                     # Thanksgiving (Thu)
    "11/28": ("No School", NORMAL_SCHED),                     # Day After Thanksgiving (Fri)

    # December 2025
    "12/24": ("No School", NORMAL_SCHED),                     # Holiday (Wed)
    "12/25": ("No School", NORMAL_SCHED),                     # Christmas (Thu)
    "12/26": ("No School", NORMAL_SCHED),                     # Non-Instructional Day (Fri)
    "12/29": ("No School", NORMAL_SCHED),                     # Non-Instructional Day (Mon)
    "12/30": ("Systemwide Closure/No School", NORMAL_SCHED),  # Systemwide Closure (Tue)
    "12/31": ("Systemwide Closure/No School", NORMAL_SCHED),  # Systemwide Closure (Wed)

    # January 2026
    "1/1":  ("No School", NORMAL_SCHED),                      # New Year's Day (Thu)
    "1/2":  ("No School", NORMAL_SCHED),                      # Non-Instructional Day (Fri)
    "1/19": ("No School", NORMAL_SCHED),                      # MLK Day (Mon)
    "1/26": ("No School", NORMAL_SCHED),                      # Grading/Planning (Mon)

    # February 2026
    "2/16": ("No School", NORMAL_SCHED),                      # Presidents' Day (Mon)
    "2/17": ("No School", NORMAL_SCHED),                      # Non-Instructional Day (Tue)
    "2/27": ("Early Release", EARLY_RELEASE_SCHED),           # Early Release (Fri)

    # March 2026
    "3/20": ("Professional Day No School", NORMAL_SCHED),     # Professional Development (Fri)
    "3/30": ("No School", NORMAL_SCHED),                      # Non-Instructional Day (Mon)
    "3/31": ("No School", NORMAL_SCHED),                      # Non-Instructional Day (Tue)

    # April 2026
    "4/1":  ("Systemwide Closure/No School", NORMAL_SCHED),   # Systemwide Closure (Wed)
    "4/2":  ("Systemwide Closure/No School", NORMAL_SCHED),   # Systemwide Closure (Thu)
    "4/3":  ("No School", NORMAL_SCHED),                      # Holiday (Fri)
    "4/6":  ("No School", NORMAL_SCHED),                      # Holiday (Mon)
    "4/15": ("No School", NORMAL_SCHED),                      # Grading and Planning (Wed)

    # May 2026
    "5/25": ("No School", NORMAL_SCHED),                      # Memorial Day (Mon)
    "5/27": ("No School", NORMAL_SCHED),                      # Non-Instructional Day (Wed)

    # June 2026
    "6/17": ("Early Release", EARLY_RELEASE_SCHED),           # Last Day of School (Wed)
    "6/18": ("No School", NORMAL_SCHED),                      # Grading/Planning (Thu)
    "6/19": ("Systemwide Closure/No School", NORMAL_SCHED),   # Systemwide Closure (Fri)
    "6/22": ("No School", NORMAL_SCHED),                      # Designated Make-Up Day (Mon)
    "6/23": ("No School", NORMAL_SCHED),                      # Designated Make-Up Day (Tue)
    "6/24": ("No School", NORMAL_SCHED),                      # Designated Make-Up Day (Wed)
    "6/25": ("No School", NORMAL_SCHED),                      # Designated Make-Up Day (Thu)
    "6/26": ("No School", NORMAL_SCHED),                      # Designated Make-Up Day (Fri)
}


def build_schedule():
    schedule = {}

    # July 4 holiday (outside the main Aug-Jun range)
    schedule["7/4"] = ["No School", fmt(NORMAL_SCHED)]

    # Iterate every day from the weekend before preservice through the last make-up day
    start = date(2025, 8, 16)   # Sat before preservice week
    end   = date(2026, 6, 26)   # Last designated make-up day

    current = start
    while current <= end:
        key     = f"{current.month}/{current.day}"
        weekday = current.weekday()   # 0 = Mon … 6 = Sun

        if key in SPECIAL_DATES:
            label, sched = SPECIAL_DATES[key]
        elif weekday >= 5:            # Saturday or Sunday
            label, sched = "No School", NORMAL_SCHED
        elif weekday == 2:            # Wednesday → Advisory
            label, sched = "Advisory", ADVISORY_SCHED
        else:                         # Mon / Tue / Thu / Fri
            label, sched = "Normal Schedule", NORMAL_SCHED

        schedule[key] = [label, fmt(sched)]
        current += timedelta(days=1)

    # Fallback key used when a date is not found
    schedule["base"] = ["No School (Most Likely)", {"0": [0, "NONE"]}]

    # Legacy "Early Release" reference key kept for compatibility
    schedule["Early Release"] = [
        "Period 1 7:45-8:35",
        {
            "31200": [34200, "Period 2"],
            "34500": [37500, "Homeroom"],
            "37800": [40800, "Period 3"],
            "41100": [43080, "Lunch"],
        },
    ]

    return schedule


if __name__ == "__main__":
    schedule = build_schedule()
    with open("data.json", "w") as f:
        f.write(json.dumps(schedule, indent=2))
    print(f"Done — wrote {len(schedule)} entries to data.json")
