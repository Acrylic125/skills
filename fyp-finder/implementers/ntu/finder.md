# Find NTU projects

Use the working directory confirmed by the main skill for all findings.

Apply the main skill's existing-artifact checkpoint to this phase: `projects.html`, `stats.html`, `projects.index.json`, and `projects.headers.json`. Reuse valid artifacts when selected; create missing artifacts or restart the selected step. Open the browser only when page collection is needed.

Use computer use in the user's **existing active browser** throughout this phase. Inspect the open browsers and tabs through the computer-use tools, then use the browser the user is currently using, preserving its profile and session.

**Do not use the preview browser, any `preview_*` tools, an in-app browser, or a separate automation browser.** If the active browser cannot be identified or controlled through computer use, ask the user to identify or enable it before proceeding; do not substitute another browser.

1. Open <https://sso.wis.ntu.edu.sg/webexe88/owa/sso_login1.asp?t=1&p2=https://wis.ntu.edu.sg/webexe/owa/fyp_filter_student.main&pg=>.
2. Bring the user's active browser window to the foreground and select the NTU login tab so the login page is visible and ready for interaction. Then ask the user to log in themselves and tell you when they are done. Wait for their response before continuing.
3. Select **Final Year Project**.
4. Select **Main list of projects for selection**. Preserve **all** existing criteria; do not add filters. Download the resulting HTML page as `projects.html` in the confirmed directory.
5. Go back and select **View current selection statistics**. Download that HTML page as `stats.html` in the confirmed directory.
6. Verify that both saved files exist and contain the intended pages, rather than a login page or an error page.

7. Run the index script after verifying the saved pages:

   ```sh
   python3 <skill-directory>/implementers/ntu/scripts/index_projects.py <working-directory>/projects.html
   ```

   Quote paths containing spaces. The script uses only the Python standard library and writes `projects.index.json` beside the input by default. Use `--output <path>` to override it. Resolve parsing errors before continuing.

8. Retrieve project headers for analysis with `scripts/find_headers.py`:

   ```sh
   python3 <skill-directory>/implementers/ntu/scripts/find_headers.py <working-directory>/projects.html
   ```

   This writes `projects.headers.json` beside the input; `--output <path>` overrides it. The script defines the header schema and returns one header per project.
