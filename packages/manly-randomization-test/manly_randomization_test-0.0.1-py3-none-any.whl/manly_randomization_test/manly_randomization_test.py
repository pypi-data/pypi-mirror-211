import numpy as np


class RandomizationTest:
    def __init__(self, group1: np.array, group2: np.array, iterations: int = 1e5):
        self.group1 = group1
        self.group2 = group2
        self.group1_n = len(group1)
        self.group2_n = len(group2)
        self.combined = np.concatenate((group1, group2))
        self.iterations = int(iterations)

    @staticmethod
    def calc_diff(group1, group2):
        return abs(np.mean(group1) - np.mean(group2))

    def shuffle(self):
        np.random.shuffle(self.combined)
        return self.combined[: self.group1_n], self.combined[self.group1_n :]

    def test(self):
        actual_diff = self.calc_diff(self.group1,self.group2)
        count = 0

        for _ in range(self.iterations):
            group1, group2 = self.shuffle()
            if self.calc_diff(group1,group2) >= actual_diff:
                count += 1

        return count / self.iterations
