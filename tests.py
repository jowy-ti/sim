# type: ignore[reportMissingTypeStubs]

import pandas as pd
from scipy import stats

def interpret(p_value: float, test_name: str) -> None:
    """Evaluates the p-value against a 0.05 significance level."""
    print("\n" + "="*40)
    print(f" TEST: {test_name}")
    print("="*40)
    print(f"p-value: {p_value:.10f}")

    if p_value < 0.05:
        print("\nVERDICT: THE SEQUENCE DOES NOT APPEAR RANDOM.")
        print(f"Reasoning: The p-value is less than 0.05, indicating significant difference.")
    else:
        print("\nVERDICT: THE SEQUENCE APPEARS RANDOM.")
        print(f"Reasoning: The p-value is greater than 0.05, failing to reject the null hypothesis of similarity")

if __name__ == "__main__":
    AVG_WAIT = 'avg_wait_time'
    AVG_LENGTH = 'avg_queue_length'

    df = pd.read_csv('./GPSS/OutputFile.TXT')

    # Save to CSV
    df.to_csv('gpss_results.csv', index=False)

    gpss_results = pd.read_csv('gpss_results.csv')
    python_results = pd.read_csv('python_results.csv')

    ttest_wait_time = stats.ttest_ind(gpss_results[AVG_WAIT], python_results[AVG_WAIT])
    ttest_queue_length = stats.ttest_ind(gpss_results[AVG_LENGTH], python_results[AVG_LENGTH])

    interpret(ttest_wait_time.pvalue, "ttest")
    interpret(ttest_queue_length.pvalue, "ttest")