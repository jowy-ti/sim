import scipy

def generate_lcg(n: int, seed: int, m: int, a: int, c: int) -> int:
    rng_values = n
    current = seed
    for i in range(n):
        current = (a * current + c) % m
        rng_values.append() current / m
    return(rng_values)

n = 10000
m = 2^31
a = 1103515245
c = 12345
seed = 42
rng_values: list[int] = [n]

numbers_custom = generate_lcg(n, seed, m, a, c)

# 3. Helper Function for Automatic Interpretation
# This function evaluates the p-value against a 0.05 significance level.
interpret <- function(result, test_name) {
  p_val <- result$p.value
  cat("\n======================================\n")
  cat(" TEST:", test_name, "\n")
  cat("======================================\n")
  print(result)
  
  if (p_val < 0.05) {
    cat("\nVERDICT: THE SEQUENCE DOES NOT APPEAR RANDOM.")
    cat("\nReasoning: The p-value (", p_val, ") is less than 0.05, indicating significant patterns.\n")



