"""Confirm a browser's LeetCode account before updating its GitHub secret."""

import argparse
import configparser
import contextlib
import errno
import getpass
import json
import os
from pathlib import Path
import shutil
import subprocess
import sqlite3
import sys
import tempfile
import time
import urllib.error
import urllib.request


class SessionError(Exception):
    pass


def file_access_hint(error):
    if sys.platform == "darwin" and error.errno == errno.EPERM:
        terminal = {
            "iTerm.app": "iTerm", "Apple_Terminal": "Terminal", "vscode": "Visual Studio Code",
        }.get(os.environ.get("TERM_PROGRAM"), "the terminal app running this command")
        return (
            "Check System Settings > Privacy & Security > Full Disk Access and enable "
            f"{terminal}, then fully quit and reopen it before rerunning this command. "
            "This grants broad file access; use --manual if you prefer to paste the cookie."
        )
    return "Check read permission for this file, or use --manual to paste the cookie."


def browser_cli():
    root = Path(__file__).resolve().parent.parent
    python = root / ".venv" / "bin" / "python"
    if not python.exists():
        print("Setting up the browser-cookie3 CLI in .venv (first run only).")
        subprocess.run([sys.executable, "-m", "venv", str(root / ".venv")], check=True)
    available = subprocess.run(
        [str(python), "-c", "import browser_cookie3"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if available.returncode:
        subprocess.run(
            [str(python), "-m", "pip", "install", "--disable-pip-version-check",
             "-r", str(root / "scripts" / "requirements.txt")], check=True,
        )
    return [str(python), "-m", "browser_cookie3"]


def choose_browser():
    while True:
        browser = input("Open LeetCode in Firefox or Chrome? [firefox]: ").strip().lower()
        if not browser:
            return "firefox"
        if browser in ("firefox", "chrome"):
            return browser
        print("Please enter firefox or chrome, or press Enter for Firefox.")


def open_browser(browser):
    applications = {"chrome": "Google Chrome", "firefox": "Firefox", "safari": "Safari"}
    application = applications[browser]
    if browser == "firefox" and not Path("/Applications/Firefox.app").exists():
        application = "Firefox Developer Edition"
    if sys.platform != "darwin":
        raise SessionError("Automatic browser lookup currently supports macOS. Use --manual.")
    result = subprocess.run(
        ["open", "-a", application, "https://leetcode.com/"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if result.returncode:
        raise SessionError(f"Could not open {application}. Choose another --browser or use --manual.")


def firefox_cookie_files(cookie_file):
    if cookie_file:
        return [Path(cookie_file).expanduser().absolute()]

    root = Path.home() / "Library" / "Application Support" / "Firefox"
    profiles = configparser.ConfigParser(interpolation=None)
    candidates = []
    try:
        try:
            with (root / "profiles.ini").open(encoding="utf-8") as stream:
                profiles.read_file(stream)
        except FileNotFoundError:
            pass
        for section in profiles.sections():
            if section.startswith("Profile") and profiles[section].get("Path"):
                profile = Path(profiles[section]["Path"]).expanduser()
                if profiles[section].get("IsRelative", "1") == "1":
                    profile = root / profile
                candidates.append(profile / "cookies.sqlite")
        # Include Developer Edition and profiles not selected by the first Install entry.
        try:
            candidates.extend(profile / "cookies.sqlite" for profile in (root / "Profiles").iterdir())
        except FileNotFoundError:
            pass
        files = []
        for candidate in dict.fromkeys(candidates):
            try:
                modified = candidate.stat().st_mtime
            except (FileNotFoundError, NotADirectoryError):
                continue
            files.append((modified, candidate))
    except PermissionError as error:
        denied_path = error.filename or root
        raise SessionError(
            f"Access to Firefox profile metadata was denied at {denied_path} "
            f"(errno {error.errno}). "
            + file_access_hint(error)
        ) from None
    except configparser.Error:
        raise SessionError(
            "Could not parse Firefox's profiles.ini. Use --cookie-file with the "
            "cookies.sqlite file in the Profile Folder shown by Firefox's about:support page."
        ) from None
    if not files:
        raise SessionError(
            f"No Firefox cookie databases were found under {root}. "
            "Open about:support in the Firefox window you use, find Profile Folder, "
            "and pass its cookies.sqlite path with --cookie-file."
        )
    return [path for _, path in sorted(files, key=lambda item: item[0], reverse=True)]


def firefox_sessions(cookie_file):
    candidates = []
    failures = []
    permission_error = None
    files = firefox_cookie_files(cookie_file)
    for path in files:
        try:
            # An explicit open preserves macOS permission errors that SQLite obscures.
            with path.open("rb"):
                pass
            try:
                rows = firefox_cookie_rows(path)
            except sqlite3.OperationalError as error:
                if (getattr(error, "sqlite_errorcode", 0) & 255) not in (sqlite3.SQLITE_BUSY, sqlite3.SQLITE_LOCKED):
                    raise
                rows = firefox_snapshot_rows(path)
            candidates.extend((value, path) for (value,) in rows if value)
        except PermissionError as error:
            failures.append(f"Access denied at {error.filename or path}")
            permission_error = error
        except FileNotFoundError:
            failures.append(f"Cookie database does not exist: {path}")
        except (OSError, sqlite3.Error):
            failures.append(f"Could not read the cookie database at {path}; it may be locked")
    if not candidates:
        if failures:
            hint = file_access_hint(permission_error) if permission_error is not None else "Use --manual if browser access is unavailable."
            raise SessionError("; ".join(failures) + ". No cookie was uploaded. " + hint)
        raise SessionError(
            f"Checked {len(files)} Firefox profile(s), but found no unexpired LEETCODE_SESSION cookie. "
            "Sign in to leetcode.com in a regular (not private) Firefox window, then retry. "
            "For a different profile location, use --cookie-file with its cookies.sqlite path."
        )
    # The same account can appear in several profiles or Firefox containers.
    unique = {}
    for value, path in candidates:
        unique.setdefault(value, path)
    return list(unique.items())


def firefox_cookie_rows(path):
    with contextlib.closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=0.25)) as connection:
        return connection.execute(
            "SELECT value FROM moz_cookies "
            "WHERE name = ? AND host IN (?, ?, ?, ?) "
            "AND (expiry = 0 OR expiry > ?) ORDER BY expiry DESC",
            ("LEETCODE_SESSION", "leetcode.com", ".leetcode.com",
             "www.leetcode.com", ".www.leetcode.com", int(time.time())),
        ).fetchall()


def firefox_snapshot_rows(path):
    def state(source):
        try:
            metadata = source.stat()
            return metadata.st_ino, metadata.st_size, metadata.st_mtime_ns
        except FileNotFoundError:
            return None

    # Firefox can hold an exclusive SQLite lock. Copy both the database and WAL
    # into a private directory; omitting the WAL can lose the current login.
    # Compare source metadata before/after copying and retry if either changed.
    sources = [path, Path(str(path) + "-wal")]
    for _ in range(3):
        with tempfile.TemporaryDirectory(prefix="leetcode-firefox-") as directory:
            before = [state(source) for source in sources]
            snapshot = Path(directory) / "cookies.sqlite"
            try:
                for source, metadata, suffix in zip(sources, before, ("", "-wal")):
                    if metadata is None:
                        continue
                    target = Path(str(snapshot) + suffix)
                    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                    with os.fdopen(descriptor, "wb") as output, source.open("rb") as input_file:
                        shutil.copyfileobj(input_file, output)
            except FileNotFoundError:
                continue
            if before != [state(source) for source in sources]:
                continue
            return firefox_cookie_rows(snapshot)
    raise SessionError(
        "Firefox kept changing its cookie database during the read. Wait a moment and retry."
    )


def browser_session(command, browser, cookie_file):
    arguments = [*command, f"--{browser}"]
    if cookie_file:
        arguments.extend(["--cookie-file", cookie_file])
    arguments.extend(["leetcode.com", "LEETCODE_SESSION"])
    try:
        result = subprocess.run(arguments, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        raise SessionError("Browser cookie access timed out. Check for a macOS permission prompt.") from None
    if result.returncode == 1 and not result.stderr.strip():
        raise SessionError("No LEETCODE_SESSION cookie was found in this browser profile. Sign in and retry.")
    if result.returncode or not result.stdout.strip():
        if "PermissionError" in result.stderr or "Operation not permitted" in result.stderr:
            raise SessionError("Browser profile access was denied. " + file_access_hint(PermissionError(errno.EPERM, "Access denied")))
        raise SessionError(
            "The browser cookie reader could not access this profile. Check browser-data "
            "or Keychain permissions, choose --cookie-file, or use --manual."
        )
    return result.stdout.strip()


def account_username(session):
    if not session or any(character.isspace() for character in session):
        raise SessionError("The session cookie is empty or invalid.")
    request = urllib.request.Request(
        "https://leetcode.com/graphql/",
        data=json.dumps({"query": "query { userStatus { isSignedIn username } }"}).encode(),
        headers={
            "Content-Type": "application/json", "Referer": "https://leetcode.com/",
            "User-Agent": "Mozilla/5.0",
        },
        method="POST",
    )
    # Keep the cookie off redirects as well as command lines and local files.
    request.add_unredirected_header("Cookie", f"LEETCODE_SESSION={session}")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            status = json.load(response)["data"]["userStatus"]
        username = status["username"]
        if (
            status["isSignedIn"] is not True
            or not isinstance(username, str)
            or not username
            or not username.isprintable()
        ):
            raise ValueError
    except (urllib.error.URLError, OSError, ValueError, KeyError, TypeError):
        raise SessionError(
            "LeetCode could not verify this account. Refresh LeetCode and sign in again "
            "if needed, or use a freshly copied session cookie."
        ) from None
    return username


def browser_account(command, browser, cookie_file):
    if browser != "firefox":
        session = browser_session(command, browser, cookie_file)
        return session, account_username(session)

    candidates = firefox_sessions(cookie_file)
    for session, path in candidates:
        try:
            username = account_username(session)
        except SessionError:
            continue
        print(f"Found the signed-in session in Firefox profile: {path.parent.name}")
        return session, username
    raise SessionError(
        f"Found {len(candidates)} saved Firefox session(s), but LeetCode could not verify any of them. "
        "Refresh LeetCode and sign in again if needed, then retry."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--browser", choices=("firefox", "chrome", "safari"),
        help="Skip the browser prompt (the prompt defaults to Firefox)",
    )
    parser.add_argument("--cookie-file", help="Cookie database for a specific browser profile")
    parser.add_argument("--manual", action="store_true", help="Paste a cookie at a hidden prompt instead")
    parser.add_argument(
        "--diagnose", action="store_true",
        help="Check Firefox profile access without uploading a token or starting a sync",
    )
    parser.add_argument("--repo", default="martenmatrix/leetcode-submissions", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.diagnose:
        print(f"Terminal: {os.environ.get('TERM_PROGRAM', 'unknown')}")
        print(f"Python: {sys.executable}")
        try:
            sessions = firefox_sessions(args.cookie_file)
        except SessionError as error:
            print(str(error), file=sys.stderr)
            return 1
        print(f"Firefox file access OK. Saved LeetCode sessions found: {len(sessions)}")
        print("No token was displayed or uploaded; no sync was started.")
        return 0
    if not sys.stdin.isatty():
        parser.error("Run this command in a terminal to confirm the account.")

    manual = args.manual
    command = None
    if not manual:
        args.browser = args.browser or choose_browser()
        open_browser(args.browser)
        if args.browser != "firefox":
            command = browser_cli()

    while True:
        try:
            if manual:
                session = getpass.getpass("LEETCODE_SESSION (hidden): ")
                username = account_username(session)
            else:
                session, username = browser_account(command, args.browser, args.cookie_file)
            break
        except SessionError as error:
            print(str(error), file=sys.stderr)
            answer = input(
                "Resolve the issue, then press Enter to retry; type 'manual' to paste a cookie "
                "or 'cancel' to stop: "
            ).strip().lower()
            if answer == "cancel":
                return 1
            if answer == "manual":
                manual = True

    print(f"Signed in to LeetCode as {username}.")
    confirmation = input(f"Type {username} to confirm syncing this account: ").strip()
    if confirmation != username:
        print("Account confirmation did not match. Sync cancelled.", file=sys.stderr)
        return 1

    subprocess.run(
        ["gh", "secret", "set", "LEETCODE_SESSION", "--repo", args.repo, "--env", "LeetCode Account"],
        input=session, text=True, check=True,
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (EOFError, KeyboardInterrupt):
        print("\nSync cancelled.", file=sys.stderr)
        sys.exit(1)
    except SessionError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("A required command failed. Sync was not started.", file=sys.stderr)
        sys.exit(1)
