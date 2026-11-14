#!/usr/bin/env bash
set -euo pipefail

repository="martenmatrix/leetcode-submissions"

if ! command -v gh >/dev/null 2>&1; then
  printf 'Install GitHub CLI (https://cli.github.com), then run gh auth login.\n' >&2
  exit 1
fi

if [[ ! -t 0 ]]; then
  printf 'Run this command in a terminal so the token prompt can hide your input.\n' >&2
  exit 1
fi

printf 'Copy the LEETCODE_SESSION cookie from your signed-in LeetCode browser.\n'
# GitHub CLI prompts with hidden input and encrypts the secret before uploading it.
# Keeping the token out of workflow inputs also keeps it out of the dispatch payload.
gh secret set LEETCODE_SESSION --repo "$repository" --env "LeetCode Account"

# Only dispatch after the secret update succeeds. The workflow runs from main.
gh workflow run glsync.yml --repo "$repository" --ref main
printf 'Sync requested. Follow progress at https://github.com/%s/actions/workflows/glsync.yml\n' "$repository"
