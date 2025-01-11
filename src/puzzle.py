#objeto/arvore puzzle

class Puzzle:
    def __init__(self, array):
        if len(array) == 9:
            self.array = array
        else:
            raise ValueError("O estado deve conter exatamente 9 elementos de 0-9.")
    


