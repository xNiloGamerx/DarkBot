from math import log10


class Calculation():
    @staticmethod
    def calculate_counting_avg(old_avg: float, reaction_count: int, new_reaction_time: float) -> float:
        if reaction_count == 0 or old_avg is None:
            return new_reaction_time
        return old_avg + (new_reaction_time - old_avg) / (reaction_count + 1)
    
    @staticmethod
    def calculate_counting_points(reaction_time_ms: float) -> int:
        return round(1000 / log10(reaction_time_ms + 10))