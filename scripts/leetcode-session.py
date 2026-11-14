"""Confirm a browser's LeetCode account before updating its GitHub secret."""

import argparse
import getpass
import json
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.request


class SessionError(Exception):
    pass


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


def browser_session(command, browser, cookie_file):
    arguments = [*command, f"--{browser}"]
    if cookie_file:
        arguments.extend(["--cookie-file", cookie_file])
    arguments.extend(["leetcode.com", "LEETCODE_SESSION"])
    try:
        result = subprocess.run(arguments, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        raise SessionError("Browser cookie access timed out. Check for a macOS permission prompt.") from None
    if result.returncode or not result.stdout.strip():
        raise SessionError(
            "Could not read a LeetCode session from this browser profile. "
            "Sign in first; you may need to quit the browser to save its latest cookies."
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", choices=("chrome", "firefox", "safari"), default="chrome")
    parser.add_argument("--cookie-file", help="Cookie database for a specific browser profile")
    parser.add_argument("--manual", action="store_true", help="Paste a cookie at a hidden prompt instead")
    parser.add_argument("--repo", default="martenmatrix/leetcode-submissions", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not sys.stdin.isatty():
        parser.error("Run this command in a terminal to confirm the account.")

    manual = args.manual
    command = None
    if not manual:
        open_browser(args.browser)
        command = browser_cli()

    while True:
        try:
            if manual:
                session = getpass.getpass("LEETCODE_SESSION (hidden): ")
            else:
                session = browser_session(command, args.browser, args.cookie_file)
            username = account_username(session)
            break
        except SessionError as error:
            print(str(error), file=sys.stderr)
            answer = input(
                "Sign in, then press Enter to retry; type 'manual' to paste a cookie "
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
