import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
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
                lookup = stack.enter_context(patch.object(session, "browser_session", side_effect=cookie_result))
            else:
                lookup = stack.enter_context(patch.object(session, "browser_session", return_value=cookie_result))
            hidden = stack.enter_context(patch.object(session.getpass, "getpass", return_value=TOKEN))
            stack.enter_context(patch.object(session, "account_username", return_value="marten"))
            upload = stack.enter_context(patch.object(session.subprocess, "run"))
            result = session.main()
        self.assertNotIn(TOKEN, output.getvalue())
        return result, upload, opening, setup, lookup, hidden

    def test_matching_username_uploads_token_through_stdin(self):
        result, upload, *_ = self.run_main(["marten"])
        self.assertEqual(result, 0)
        upload.assert_called_once()
        self.assertEqual(upload.call_args.kwargs["input"], TOKEN)
        self.assertNotIn(TOKEN, upload.call_args.args[0])
        self.assertIn("LeetCode Account", upload.call_args.args[0])

    def test_wrong_username_never_updates_secret(self):
        result, upload, *_ = self.run_main(["someone-else"])
        self.assertEqual(result, 1)
        upload.assert_not_called()

    def test_missing_session_can_cancel_without_uploading(self):
        result, upload, *_ = self.run_main(["cancel"], cookie_result=[session.SessionError("Signed out")])
        self.assertEqual(result, 1)
        upload.assert_not_called()

    def test_retry_rereads_cookie_after_browser_login(self):
        result, upload, _, _, lookup, _ = self.run_main(
            ["", "marten"], cookie_result=[session.SessionError("Signed out"), TOKEN],
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
            self.assertEqual(session.browser_session(["browser-cookie"], "firefox", "/profile/cookies.sqlite"), TOKEN)
        self.assertEqual(run.call_args.args[0], [
            "browser-cookie", "--firefox", "--cookie-file", "/profile/cookies.sqlite", "leetcode.com", "LEETCODE_SESSION",
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

    def test_signed_out_and_invalid_responses_are_rejected(self):
        for body in ('{"data":{"userStatus":{"isSignedIn":false,"username":null}}}', '{"errors":[]}', '<html>blocked</html>'):
            with self.subTest(body=body), patch.object(session.urllib.request, "urlopen", return_value=io.StringIO(body)):
                with self.assertRaises(session.SessionError) as error:
                    session.account_username(TOKEN)
                self.assertNotIn(TOKEN, str(error.exception))


if __name__ == "__main__":
    unittest.main()
