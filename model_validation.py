# type: ignore[reportMissingTypeStubs]

import pandas as pd
from scipy import stats

def interpret(p_value: float, test_name: str, queue: int, metric: str) -> None:
    """Evaluates the p-value against a 0.05 significance level."""
    print("\n" + "="*40)
    print(f" TEST: {test_name}   Queue{queue}    {metric}")
    print("="*40)
    print(f"p-value: {p_value:.10f}")

    if p_value < 0.05:
        print("\nVERDICT: there is significant difference between the means.")
        print(f"Reasoning: The p-value is less than 0.05, indicating significant difference.")
    else:
        print("\nVERDICT: there is no significant difference between means.")
        print(f"Reasoning: The p-value is greater than 0.05, failing to reject the null hypothesis of similarity")

if __name__ == "__main__":
    AVG_WAIT = 'avg_wait_time'
    AVG_LENGTH = 'avg_queue_length'

    df = pd.read_csv('./GPSS/OutputFile.TXT')

    # Save to CSV
    df.to_csv('gpss_results.csv', index=False)

    df1 = pd.read_csv('gpss_results.csv') # GPSS
    df2 = pd.read_csv('python_results.csv') # Python

    groups = [0, 1, 2]

    print("--- Comparing Groups Between Dataset 1 and Dataset 2 ---")
    for g in groups:
        # Filter out the specific metric for the current group
        avg_wait_df1 = df1[df1['queue'] == g][AVG_WAIT]
        avg_wait_df2 = df2[df2['queue'] == g][AVG_WAIT]

        avg_length_df1 = df1[df1['queue'] == g][AVG_LENGTH]
        avg_length_df2 = df2[df2['queue'] == g][AVG_LENGTH]

        if not avg_wait_df1.empty and not avg_wait_df2.empty:
            ttest_wait_time = stats.ttest_ind(avg_wait_df1, avg_wait_df2, equal_var=False)
            ttest_queue_length = stats.ttest_ind(avg_length_df1, avg_length_df2, equal_var=False)

            interpret(ttest_wait_time.pvalue, "ttest", g, AVG_WAIT)
            interpret(ttest_queue_length.pvalue, "ttest", g, AVG_LENGTH)
            print("\n"*8)