# LeetCode submissions

Sync accepted LeetCode submissions to this repository on demand. There is no
scheduled sync, so an expired LeetCode session will not cause weekly failures.

## Start a sync

On macOS, install Python 3 and [GitHub CLI](https://cli.github.com), then sign in
once with `gh auth login`. Your GitHub account needs permission to update the
`LeetCode Account` environment secret and run workflows in this repository.

```sh
bash scripts/sync-leetcode.sh
```

The command opens LeetCode in **Google Chrome**, reads `LEETCODE_SESSION` using
[browser-cookie3's existing CLI](https://github.com/borisbabic/browser_cookie3#command-line-usage),
and asks LeetCode which account is signed in. Type the displayed **LeetCode
username** to confirm. Only then does it update the existing environment secret
and start **Sync LeetCode submissions** from `main`.

On the first run, the command installs the pinned browser-cookie3 package into
an ignored `.venv` in this checkout. macOS may ask for permission to read the
browser's cookies or its Keychain encryption key. The cookie is captured in
memory and sent to GitHub through standard input; it is not printed, written to
a local token file, or passed as a workflow input.

Choose another browser if needed:

```sh
bash scripts/sync-leetcode.sh --browser firefox
bash scripts/sync-leetcode.sh --browser safari
```

Firefox Developer Edition is supported when the regular Firefox app is absent.
If you are signed out, log in in the opened browser and press Enter in the
terminal to retry. You may need to quit the browser so its latest cookies are
saved. If you have several profiles, use `--cookie-file /path/to/Cookies` to
select the cookie database for the account you want; the username confirmation
lets you check which account was found.

If browser access is unavailable, use the hidden manual prompt, which also
verifies the account and requires its username before proceeding:

```sh
bash scripts/sync-leetcode.sh --manual
```

Copy `LEETCODE_SESSION` from the browser's developer tools under **Application →
Cookies** (Chrome) or **Storage → Cookies** (Firefox). This mode does not install
or use browser-cookie3.

Watch progress in [GitHub Actions](https://github.com/martenmatrix/leetcode-submissions/actions/workflows/glsync.yml).
The token remains stored in the `LeetCode Account` environment until you replace
or delete it. Cancelling the confirmation or failing to update the secret does
not start a sync.

You can also update `LEETCODE_SESSION` under **Settings → Environments → LeetCode
Account**, then choose **Actions → Sync LeetCode submissions → Run workflow**.
The GitHub button uses the saved secret and does not open your local browser.
