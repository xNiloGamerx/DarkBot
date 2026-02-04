class Numbers:
    @staticmethod
    def make_digits_unique(number: int) -> str:
        s = list(str(number))
        used = set()
        result = []
        
        for digit in s:
            d = int(digit)
            # Wenn die Ziffer schon da ist, finde die nächste freie Ziffer
            while str(d) in used:
                d = (d + 1) % 10  # Springt von 9 wieder auf 0
            
            result.append(str(d))
            used.add(str(d))
            
        return "".join(result)
