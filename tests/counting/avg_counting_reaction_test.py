from datetime import datetime, timezone

def calculate_counting_avg(old_avg: float, reaction_count: int, new_reaction_time: float) -> float:
        if reaction_count == 0:
            return new_reaction_time
        return old_avg + (new_reaction_time - old_avg) / (reaction_count + 1)


old_avg = datetime.fromisoformat("2026-02-01 21:07:40+01").timestamp() * 1000 - datetime.fromisoformat("2026-02-01 21:07:30+01").timestamp() * 1000
new_reaction_time = datetime.fromisoformat("2026-02-01 22:08:40+01").timestamp() * 1000 - datetime.fromisoformat("2026-02-01 22:08:30+01").timestamp() * 1000

new_avg = calculate_counting_avg(old_avg, 100, new_reaction_time)
print(new_avg)
print("Seconds:", new_avg / 1000)
