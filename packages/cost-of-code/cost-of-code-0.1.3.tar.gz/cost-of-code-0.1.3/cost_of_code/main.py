import argparse
from cost_of_code.git_handler import get_added_lines, get_current_lines
from cost_of_code.code_tokenizer import tokenize_code
from cost_of_code.cost_estimator import estimate_cost


def main():
    parser = argparse.ArgumentParser(
        description="Estimate the cost of generating the tokens of code in a git repo using GPT-4."
    )
    parser.add_argument("--repo-path", default="./")
    parser.add_argument("--branch-name", default="master")
    parser.add_argument("--cost-per-thousand-tokens", type=float, default=0.06)
    parser.add_argument(
        "--extension-whitelist", default="*.py,*.js,*.java,*.c,*.cpp,*.go"
    )

    args = parser.parse_args()

    repo_path = args.repo_path
    branch_name = args.branch_name
    cost_per_thousand_tokens = args.cost_per_thousand_tokens
    extension_whitelist = args.extension_whitelist

    # Get all code files in the repo
    current_lines = get_current_lines(repo_path, extension_whitelist)

    # Get all added lines in the repo
    added_lines = get_added_lines(repo_path, extension_whitelist, branch_name)

    # Tokenize and count tokens in the current state of the repo
    total_tokens_current = 0
    for line in current_lines:
        total_tokens_current += tokenize_code(line)

    # Tokenize and count tokens in all added lines
    total_tokens_complete = 0
    for line in added_lines:
        total_tokens_complete += tokenize_code(line)

    # Calculate the cost for the current state of the repo and all added lines
    cost_current = estimate_cost(total_tokens_current, cost_per_thousand_tokens)
    cost_complete = estimate_cost(total_tokens_complete, cost_per_thousand_tokens)

    # Print the results
    print(f"Total tokens in the current state of the repo: {total_tokens_current}")
    print(f"Estimated cost for the current state of the repo: ${cost_current:.2f}")
    print(f"Total tokens in all added lines: {total_tokens_complete}")
    print(f"Estimated cost for all added lines: ${cost_complete:.2f}")


if __name__ == "__main__":
    main()
