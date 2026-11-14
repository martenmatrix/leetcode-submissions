#!/usr/bin/env bash
set -euo pipefail

repository="martenmatrix/leetcode-submissions"
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  printf 'Install Python 3 to read and verify your LeetCode browser session.\n' >&2
  exit 1
fi

for argument in "$@"; do
  if [[ "$argument" == "--diagnose" ]]; then
    exec python3 "$script_dir/leetcode-session.py" "$@"
  fi
  if [[ "$argument" == "--help" || "$argument" == "-h" ]]; then
    exec python3 "$script_dir/leetcode-session.py" --help
  fi
done

if ! command -v gh >/dev/null 2>&1; then
  printf 'Install GitHub CLI (https://cli.github.com), then run gh auth login.\n' >&2
  exit 1
fi

if [[ ! -t 0 ]]; then
  printf 'Run this command in a terminal so the token prompt can hide your input.\n' >&2
  exit 1
fi

# The helper opens LeetCode, captures browser-cookie3's CLI output in memory,
# verifies the account, and requires its username before updating the secret.
python3 "$script_dir/leetcode-session.py" "$@" --repo "$repository"

# Only dispatch after the secret update succeeds. The workflow runs from main.
gh workflow run glsync.yml --repo "$repository" --ref main
printf 'Sync requested. Follow progress at https://github.com/%s/actions/workflows/glsync.yml\n' "$repository"
