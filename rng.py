# type: ignore[reportMissingTypeStubs]

import numpy as np
from scipy import stats

class RNG:
    # Constants
    M: int = 2**31
    A: int = 1103515245
    C: int = 12345

    def __init__(self, seed: int):
        self.current: int = seed

    def generate_number(self) -> float:
        self.current = (self.A * self.current + self.C) % self.M
        return float(self.current / self.M)
    
    @staticmethod
    def generate_lcg(n: int, seed: int, m: int, a: int, c: int) -> np.ndarray:
        rng_values = np.zeros(n)
        current = seed
        for i in range(n):
            current = (a * current + c) % m
            rng_values[i] = float(current / m)
        return rng_values
    
    @staticmethod
    def interpret(p_value: float, test_name: str) -> None:
        """Evaluates the p-value against a 0.05 significance level."""
        print("\n" + "="*40)
        print(f" TEST: {test_name}")
        print("="*40)
        print(f"p-value: {p_value:.10f}")

        if p_value < 0.05:
            print("\nVERDICT: THE SEQUENCE DOES NOT APPEAR RANDOM.")
            print(f"Reasoning: The p-value is less than 0.05, indicating significant patterns.")
        else:
            print("\nVERDICT: THE SEQUENCE APPEARS RANDOM.")
            print(f"Reasoning: The p-value is greater than 0.05, failing to reject the null hypothesis of uniformity.")

    def validation(self):
    # Generate 10,000 numbers
        n_samples = 10000
        numbers_custom = RNG.generate_lcg(n_samples, self.current, self.M, self.A, self.C)

        # 3. Perform Kolmogorov-Smirnov Test for Uniformity
        # We compare our sequence against the 'uniform' distribution
        ks_result = stats.kstest(numbers_custom, 'uniform')
        cramer_result = stats.cramervonmises(numbers_custom, 'uniform')

        counts, _ = np.histogram(numbers_custom, bins=np.linspace(0, 1, 11))
        expected = [len(numbers_custom) / 10] * 10
        chi_result = stats.chisquare(f_obs=counts, f_exp=expected)

        goodness_fit_result = stats.goodness_of_fit(stats.uniform, numbers_custom, statistic='filliben')
        ttest_result = stats.ttest_1samp(numbers_custom, popmean=0.5)

        # Interpret the results
        RNG.interpret(ks_result.pvalue, "Kolmogorov-Smirnov (Uniformity)")
        RNG.interpret(cramer_result.pvalue, "Cramer Von Mises (Uniformity)")
        RNG.interpret(chi_result.pvalue, "ChiSquare (Uniformity)")
        RNG.interpret(goodness_fit_result.pvalue, "Goodness of Fit (Uniformity)")
        RNG.interpret(ttest_result.pvalue, "ttest (Uniformity)")


