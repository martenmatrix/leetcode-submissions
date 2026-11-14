# LeetCode submissions

Sync accepted LeetCode submissions to this repository on demand. There is no
scheduled sync, so an expired LeetCode session will not cause weekly failures.

## Start a sync

Install [GitHub CLI](https://cli.github.com) and sign in once with `gh auth login`.
Your GitHub account needs permission to update the `LeetCode Account` environment
secret and run workflows in this repository.

1. Sign in to [LeetCode](https://leetcode.com).
2. Open your browser's developer tools, find the cookies for `leetcode.com` under
   **Application → Cookies** (Chrome) or **Storage → Cookies** (Firefox), and copy
   the value of `LEETCODE_SESSION`.
3. From this checkout, run:

   ```sh
   bash scripts/sync-leetcode.sh
   ```

4. Paste the cookie value at the hidden GitHub CLI prompt and press Enter.

The command asks for a token every time, updates the `LEETCODE_SESSION` secret in
the existing `LeetCode Account` environment, and starts **Sync LeetCode
submissions** from `main`. If updating the secret fails, the sync is not started.
The token remains stored as an environment secret until you replace or delete
it. No token is written to a local file or passed as a workflow input.

Watch progress in [GitHub Actions](https://github.com/martenmatrix/leetcode-submissions/actions/workflows/glsync.yml).
If LeetCode rejects the session, copy a fresh cookie and run the command again.

You can also update `LEETCODE_SESSION` under **Settings → Environments → LeetCode
Account**, then choose **Actions → Sync LeetCode submissions → Run workflow**.
The GitHub button uses the saved secret; it does not prompt for a token.

GitHub's manual workflow form has no secret/password input type. The local
command uses [GitHub CLI's secret prompt](https://cli.github.com/manual/gh_secret_set)
to keep the cookie out of plain-text workflow inputs.
