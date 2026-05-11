# type: ignore[reportMissingTypeStubs]

import numpy as np
from scipy import stats

class Engine:
    # 1. Constants
    M: int = 2**31
    A: int = 1103515245
    C: int = 12345
    SEED: int = 30

    def __init__(self,):


    def generate_lcg(n: int, seed: int, m: int, a: int, c: int)-> np.ndarray:
        rng_values = np.zeros(n)
        current = seed
        for i in range(n):
            current = (a * current + c) % m
            rng_values[i] = float(current / m)
        return rng_values

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

    # --- Execution ---

    def validation(self):
    # Generate 10,000 numbers
        n_samples = 10000
        numbers_custom = self.generate_lcg(n_samples, SEED, M, A, C)

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
        interpret(ks_result.pvalue, "Kolmogorov-Smirnov (Uniformity)")
        interpret(cramer_result.pvalue, "Cramer Von Mises (Uniformity)")
        interpret(chi_result.pvalue, "ChiSquare (Uniformity)")
        interpret(goodness_fit_result.pvalue, "Goodness of Fit (Uniformity)")
        interpret(ttest_result.pvalue, "ttest (Uniformity)")




