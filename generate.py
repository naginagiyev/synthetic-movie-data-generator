import os
import time
import runpy

PIPELINE = [("directors.py", "Directors"), ("actors.py", "Actors"), ("users.py", "Users"),
            ("movies.py", "Movies"), ("roles.py", "Roles"), ("reviews.py", "Reviews")]

DIVIDER = "=" * 150
def formatElapsed(seconds):
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}m {secs:.1f}s"

os.makedirs("./tables", exist_ok=True)

print(f"\n{DIVIDER}")
print("   MOVIE DATABASE — TABLE GENERATOR")
print(DIVIDER)

totalStart = time.time()
stepTimes = []

for step, (script, label) in enumerate(PIPELINE, start=1):
    print(f"\n[{step}/{len(PIPELINE)}] Generating {label}...")
    print(f"{'-' * 150}")
    stepStart = time.time()
    runpy.run_path(script, run_name="__main__")
    elapsed = time.time() - stepStart
    stepTimes.append((label, elapsed))
    print(f"  Done — {formatElapsed(elapsed)}")

totalElapsed = time.time() - totalStart

print(f"\n{DIVIDER}")
print("   SUMMARY")
print(DIVIDER)
for label, elapsed in stepTimes:
    print(f"  {label:<12} {formatElapsed(elapsed):>8}")
print(f"{'-' * 150}")
print(f"  {'TOTAL':<12} {formatElapsed(totalElapsed):>8}")
print(f"{DIVIDER}\n")