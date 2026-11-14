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

The command asks whether to open **Firefox or Chrome**. Press Enter to use
**Firefox**, the default. It then opens LeetCode, finds `LEETCODE_SESSION`,
and asks LeetCode which account is signed in. Type the displayed **LeetCode
username** to confirm. Only then does it update the existing environment secret
and start **Sync LeetCode submissions** from `main`.

Firefox lookup checks every configured profile, including Developer Edition and
profiles stored outside the default folder. It reads only LeetCode session rows
from the live cookie database in read-only mode, including recent changes still
in Firefox's write-ahead log. Expired sessions are skipped, and saved sessions
are verified with LeetCode until a signed-in account is found. Firefox lookup
uses Python's standard library and does not install a package.

If Firefox holds an exclusive database lock, the helper reads a temporary
snapshot of the database and its write-ahead log. The temporary directory is
private, copied files have owner-only permissions, and the snapshot is removed
after the read. The browser's own files are not modified.

For Chrome or Safari, the command reuses
[browser-cookie3's CLI](https://github.com/borisbabic/browser_cookie3#command-line-usage).
On the first run with either browser, it installs the pinned package into an
ignored `.venv` in this checkout. macOS may ask for browser-data or Keychain
access. The selected cookie is kept in memory and sent to GitHub through
standard input; it is not printed or passed as a workflow input.

To skip the browser prompt, choose one explicitly:

```sh
bash scripts/sync-leetcode.sh --browser firefox
bash scripts/sync-leetcode.sh --browser chrome
bash scripts/sync-leetcode.sh --browser safari
```

Firefox Developer Edition is supported when the regular Firefox app is absent.
If you are signed out, log in in a regular Firefox window and press Enter in the
terminal to retry. A private window does not save its login to the profile.
The command prints which profile supplied the verified account. To select a
particular Firefox profile, open `about:support` in that Firefox window, find
**Profile Folder**, and pass the full path to its `cookies.sqlite` file:

```sh
bash scripts/sync-leetcode.sh --browser firefox --cookie-file "/path/to/profile/cookies.sqlite"
```

An error naming denied access to profile files indicates a macOS browser-data
permission problem. Run from a terminal permitted to read Firefox data, or use
the manual mode below. Restart the command after updating these scripts;
pressing Enter in an already running copy does not load the updated code.

If access still fails, run this check from the same terminal and inspect the
exact denied filename and Python interpreter. It does not open a browser,
display or upload a token, or start a sync:

```sh
bash scripts/sync-leetcode.sh --diagnose
```

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
