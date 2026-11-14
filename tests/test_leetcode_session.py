import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sqlite3
import sys
import tempfile
import time
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "leetcode_session", Path(__file__).resolve().parents[1] / "scripts" / "leetcode-session.py",
)
session = importlib.util.module_from_spec(spec)
spec.loader.exec_module(session)
TOKEN = "fake-session-do-not-print"


class SessionTests(unittest.TestCase):
    def run_main(self, answers, *, manual=False, cookie_result=TOKEN):
        output = io.StringIO()
        arguments = ["leetcode-session.py", *(["--manual"] if manual else [])]
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(sys, "argv", arguments))
            stack.enter_context(patch.object(sys.stdin, "isatty", return_value=True))
            stack.enter_context(contextlib.redirect_stdout(output))
            stack.enter_context(contextlib.redirect_stderr(output))
            stack.enter_context(patch("builtins.input", side_effect=answers))
            opening = stack.enter_context(patch.object(session, "open_browser"))
            setup = stack.enter_context(patch.object(session, "browser_cli", return_value=["browser-cookie"]))
            if isinstance(cookie_result, list):
                results = [item if isinstance(item, Exception) else (item, "marten") for item in cookie_result]
                lookup = stack.enter_context(patch.object(session, "browser_account", side_effect=results))
            else:
                lookup = stack.enter_context(patch.object(session, "browser_account", return_value=(cookie_result, "marten")))
            hidden = stack.enter_context(patch.object(session.getpass, "getpass", return_value=TOKEN))
            stack.enter_context(patch.object(session, "account_username", return_value="marten"))
            upload = stack.enter_context(patch.object(session.subprocess, "run"))
            result = session.main()
        self.assertNotIn(TOKEN, output.getvalue())
        return result, upload, opening, setup, lookup, hidden

    def test_matching_username_uploads_token_through_stdin(self):
        result, upload, opening, setup, lookup, _ = self.run_main(["", "marten"])
        self.assertEqual(result, 0)
        opening.assert_called_once_with("firefox")
        lookup.assert_called_once_with(None, "firefox", None)
        setup.assert_not_called()
        upload.assert_called_once()
        self.assertEqual(upload.call_args.kwargs["input"], TOKEN)
        self.assertNotIn(TOKEN, upload.call_args.args[0])
        self.assertIn("LeetCode Account", upload.call_args.args[0])

    def test_wrong_username_never_updates_secret(self):
        result, upload, opening, _, lookup, _ = self.run_main(["chrome", "someone-else"])
        self.assertEqual(result, 1)
        opening.assert_called_once_with("chrome")
        lookup.assert_called_once_with(["browser-cookie"], "chrome", None)
        upload.assert_not_called()

    def test_missing_session_can_cancel_without_uploading(self):
        result, upload, *_ = self.run_main(["", "cancel"], cookie_result=[session.SessionError("Signed out")])
        self.assertEqual(result, 1)
        upload.assert_not_called()

    def test_retry_rereads_cookie_after_browser_login(self):
        result, upload, _, _, lookup, _ = self.run_main(
            ["firefox", "", "marten"], cookie_result=[session.SessionError("Signed out"), TOKEN],
        )
        self.assertEqual(result, 0)
        self.assertEqual(lookup.call_count, 2)
        upload.assert_called_once()

    def test_manual_mode_skips_browser_and_dependency_setup(self):
        result, upload, opening, setup, lookup, hidden = self.run_main(["marten"], manual=True)
        self.assertEqual(result, 0)
        opening.assert_not_called()
        setup.assert_not_called()
        lookup.assert_not_called()
        hidden.assert_called_once()
        upload.assert_called_once()

    def test_extraction_uses_existing_cli_and_requested_profile(self):
        with patch.object(session.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, TOKEN + "\n")) as run:
            self.assertEqual(session.browser_session(["browser-cookie"], "chrome", "/profile/Cookies"), TOKEN)
        self.assertEqual(run.call_args.args[0], [
            "browser-cookie", "--chrome", "--cookie-file", "/profile/Cookies", "leetcode.com", "LEETCODE_SESSION",
        ])
        self.assertTrue(run.call_args.kwargs["capture_output"])

    def test_account_name_comes_from_authenticated_leetcode_response(self):
        response = io.StringIO('{"data":{"userStatus":{"isSignedIn":true,"username":"marten"}}}')
        with patch.object(session.urllib.request, "urlopen", return_value=response) as opening:
            self.assertEqual(session.account_username(TOKEN), "marten")
        request = opening.call_args.args[0]
        self.assertEqual(request.full_url, "https://leetcode.com/graphql/")
        self.assertEqual(request.unredirected_hdrs["Cookie"], f"LEETCODE_SESSION={TOKEN}")
        self.assertNotIn(TOKEN.encode(), request.data)

    def test_cli_access_errors_are_not_reported_as_missing_login(self):
        failure = subprocess.CompletedProcess([], 1, "", "PermissionError: access denied")
        with patch.object(session.subprocess, "run", return_value=failure):
            with self.assertRaisesRegex(session.SessionError, "could not access this profile"):
                session.browser_session(["browser-cookie"], "chrome", None)

    def test_signed_out_and_invalid_responses_are_rejected(self):
        for body in ('{"data":{"userStatus":{"isSignedIn":false,"username":null}}}', '{"errors":[]}', '<html>blocked</html>'):
            with self.subTest(body=body), patch.object(session.urllib.request, "urlopen", return_value=io.StringIO(body)):
                with self.assertRaises(session.SessionError) as error:
                    session.account_username(TOKEN)
                self.assertNotIn(TOKEN, str(error.exception))


class FirefoxLookupTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="leetcode-profile-test-")
        self.addCleanup(self.directory.cleanup)
        self.home = Path(self.directory.name)
        self.root = self.home / "Library" / "Application Support" / "Firefox"
        self.release = self.root / "Profiles" / "example.default-release" / "cookies.sqlite"
        self.developer = self.root / "Profiles" / "example.dev-edition-default" / "cookies.sqlite"
        self.release.parent.mkdir(parents=True)
        self.developer.parent.mkdir(parents=True)
        (self.root / "profiles.ini").write_text(
            "[InstallRelease]\nDefault=Profiles/example.default-release\n"
            "[Profile0]\nIsRelative=1\nPath=Profiles/example.default-release\n"
            "[Profile1]\nIsRelative=1\nPath=Profiles/example.dev-edition-default\n"
        )
        patcher = patch.object(session.Path, "home", return_value=self.home)
        patcher.start()
        self.addCleanup(patcher.stop)

    def database(self, path, *, wal=False):
        connection = sqlite3.connect(path)
        self.addCleanup(connection.close)
        if wal:
            connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("CREATE TABLE moz_cookies (host TEXT, name TEXT, value TEXT, expiry INTEGER)")
        connection.commit()
        if wal:
            connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        return connection

    def test_checks_developer_profile_when_first_install_points_to_release(self):
        self.database(self.release)
        connection = self.database(self.developer)
        connection.executemany("INSERT INTO moz_cookies VALUES (?, ?, ?, ?)", [
            (".example.com", "LEETCODE_SESSION", "different-domain", int(time.time()) + 1000),
            (".leetcode.com", "LEETCODE_SESSION", "expired-cookie", int(time.time()) - 1000),
            (".leetcode.com", "unrelated", "different-cookie", int(time.time()) + 1000),
            (".leetcode.com", "LEETCODE_SESSION", TOKEN, int(time.time()) + 1000),
        ])
        connection.commit()
        self.assertEqual(session.firefox_sessions(None), [(TOKEN, self.developer)])

    def test_reads_recent_cookie_still_in_firefox_write_ahead_log(self):
        connection = self.database(self.developer, wal=True)
        connection.execute("INSERT INTO moz_cookies VALUES (?, ?, ?, ?)", (
            ".leetcode.com", "LEETCODE_SESSION", TOKEN, int(time.time()) + 1000,
        ))
        connection.commit()
        self.assertGreater(Path(str(self.developer) + "-wal").stat().st_size, 0)
        self.assertEqual(session.firefox_sessions(str(self.developer)), [(TOKEN, self.developer)])

    def test_checks_profile_registered_outside_standard_profile_directory(self):
        custom = self.home / "custom-profile" / "cookies.sqlite"
        custom.parent.mkdir()
        self.database(custom)
        with (self.root / "profiles.ini").open("a") as config:
            config.write(f"[Profile2]\nIsRelative=0\nPath={custom.parent}\n")
        self.assertIn(custom, session.firefox_cookie_files(None))

    def test_permission_error_is_reported_as_access_problem(self):
        with patch.object(session.Path, "open", side_effect=PermissionError):
            with self.assertRaisesRegex(session.SessionError, "permission problem, not a missing login"):
                session.firefox_cookie_files(None)

    def test_tries_next_saved_session_when_leetcode_rejects_first(self):
        output = io.StringIO()
        with patch.object(session, "firefox_sessions", return_value=[("old-session", self.release), (TOKEN, self.developer)]), \
             patch.object(session, "account_username", side_effect=[session.SessionError("Expired"), "marten"]), \
             contextlib.redirect_stdout(output):
            self.assertEqual(session.browser_account(None, "firefox", None), (TOKEN, "marten"))
        self.assertNotIn(TOKEN, output.getvalue())
        self.assertIn(self.developer.parent.name, output.getvalue())


if __name__ == "__main__":
    unittest.main()
