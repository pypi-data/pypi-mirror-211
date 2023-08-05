def estimate_cost(num_tokens, cost_per_thousand_tokens):
    cost = (num_tokens / 1000) * cost_per_thousand_tokens
    return cost
