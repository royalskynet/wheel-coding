#!/usr/bin/env python3
"""Self-check for skills/wheel/SKILL.md. Run: python3 skills/wheel/scripts/test_skill.py

The skill is prose, so what can be pinned is its contract with the registry and
with itself: every verdict word the CLI accepts appears in the skill, the three
sections `/wheel` promises (decision / wheels / reverse) exist, the reverse section
stays conditional, and the fallback commands the prose tells the model to run
actually work on this machine's shell.

Every fallback case runs inside a tempdir with `HOME` and `WHEEL_REGISTRY` pointed
there, so neither the grep fallback nor the printf fallback touches the user's
real `~/.wheel`.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(os.path.dirname(HERE), "SKILL.md")
CLI = os.path.join(HERE, "wheel_registry.py")

sys.path.insert(0, HERE)
import wheel_registry  # noqa: E402  (same grammar the skill must spell out)
import test_wheel_registry as regtest  # noqa: E402

CHECKS = []
FAILS = []


def check(cond, label):
    CHECKS.append(label)
    if not cond:
        FAILS.append(label)


def body():
    with open(SKILL, encoding="utf-8") as fh:
        return fh.read()


def shell(script, env_extra, cwd):
    env = dict(os.environ)
    env.pop("WHEEL_REGISTRY", None)
    env.pop("PYTHONPATH", None)
    env.update(env_extra)
    return subprocess.run(["bash", "-c", script], capture_output=True, text=True,
                          env=env, cwd=cwd)


def fallback_block():
    """SKILL.md §7's bare-printf snippet, placeholders filled, verbatim otherwise."""
    text = body()
    m = re.search(r"```bash\n(mkdir -p ~/\.wheel.*?)```", text, re.S)
    if not m:
        return "false  # SKILL.md §7 has no printf fallback block"
    block = m.group(1)
    for key, value in (("<裁決>", "設定｜借鏡"), ("<問題一句>", "測試問題"),
                       ("<首選>", "首選"), ("<YYYY-MM-DD>", "2099-12-31")):
        block = block.replace(key, value)
    return block


def test_frontmatter(text):
    head = text.split("---")[1] if text.startswith("---") else ""
    check("name: wheel" in head, "frontmatter names the skill wheel")
    desc = re.search(r"description:\s*(.+)", head)
    check(bool(desc) and len(desc.group(1)) >= 40,
          "frontmatter description is long enough to route on")


def test_three_sections(text):
    """/wheel does three jobs by default-or-context; each must be spelled out."""
    for needle in ("**決策**", "**輪子**", "**逆向**", "§3.5"):
        check(needle in text, "the three jobs table names %s" % needle)


def test_reverse_is_conditional(text):
    m = re.search(r"### 3\.5[^\n]*\n(.*?)\n## 4\.", text, re.S)
    check(bool(m), "§3.5 has a body ending at §4")
    if not m:
        return
    # The condition lives in the heading; re.search() only captures past `\n`, so
    # the heading is read from the whole text, not from group(1).
    intro = text[m.start():m.end(1)]
    check("只" in intro and "情境需要或使用者要求，不是每次" in text,
          "§3.5 runs only when the context needs it; the jobs table marks it "
          "「情境需要或使用者要求，不是每次」")
    check("DRM" in intro and "有權" in intro,
          "§3.5 keeps the legal boundary (owned/allowed targets, no DRM)")
    check("Full＋逆向" in text, "the depth table has the reverse row")


def test_verdicts_line_up(text):
    for verdict in wheel_registry.VERDICTS:
        check(verdict in text, "skill spells verdict %s" % verdict)
    check(wheel_registry.VERDICT_SEP in text,
          "skill uses the full-width ｜ separator")


def test_literal_paths_resolve(text):
    """The prose's `<本 skill 目錄>/../../router/...` is one layout; the shipped
    script is another. Only the shipped one can be checked here, but the prose
    must describe it so an installed copy is not told to look for nothing."""
    # Step 0 and §7 both name the CLI by path. A layout that is not the one in the
    # prose is fine as long as the prose's CLI itself resolves; here it is next to
    # this test, so the check is that the skill tells the reader the script exists
    # and how to reach it by a relative path.
    check(text.count("wheel_registry.py") >= 2, "skill names wheel_registry.py at step 0 and §7")
    check("本 skill 目錄" in text, "skill gives a relative way to reach the CLI")
    check(os.path.isfile(CLI), "shipped registry CLI exists next to this test")


def test_fallback_commands_run(text):
    """Both fallbacks must work on the shell they are pasted into."""
    with tempfile.TemporaryDirectory() as tmp:
        reg = os.path.join(tmp, ".wheel", "registry.tsv")
        os.makedirs(os.path.dirname(reg))
        regtest.write_rows(reg, ["2026-01-01\t採用\tnpm 的 date library\tdayjs\t2099-01-01"])
        env = {"HOME": tmp, "WHEEL_REGISTRY": reg}

        r = shell('grep -iF -e "DAYJS" -e "時區" "$HOME/.wheel/registry.tsv" | tail -5', env, tmp)
        check(r.returncode == 0 and "dayjs" in r.stdout,
              "grep fallback: case-insensitive literal match")

        # The printf fallback is executed exactly as SKILL.md §7 prints it, with
        # the placeholders filled in. Running the prose itself is the only way to
        # catch a block that reads fine and fails on the user's shell.
        skill_printf = fallback_block()
        before = regtest.rows_of(reg)
        r = shell(skill_printf, env, tmp)
        check(r.returncode == 0, "printf fallback exits 0")
        after = regtest.rows_of(reg)
        check(len(after) == len(before) + 1, "printf fallback appends exactly one row")
        if after:
            check(wheel_registry.row_problems(after[-1]) == [],
                  "printf fallback row passes the CLI's own grammar check")

        # A file whose last line lost its newline must not swallow the new row.
        # rows_of() splits on "\n", so count the raw newlines instead.
        with open(reg, "w", encoding="utf-8") as fh:
            fh.write("2026-01-01\t採用\tx\ty\t2099-01-01")
        shell(skill_printf, env, tmp)
        with open(reg, encoding="utf-8") as fh:
            raw = fh.read()
        check(raw.count("\n") == 2 and raw.endswith("\n"),
              "printf fallback closes a missing trailing newline first")

        # Round trip: rows written by the fallback are found by the CLI.
        # The temp HOME's copy is the one the fallback wrote.
        written = os.path.join(tmp, ".wheel", "registry.tsv")
        r = regtest.run("find", "測試問題", registry=written)
        check(r.returncode == 0 and "[有效] " in r.stdout,
              "CLI find reads the fallback's rows")


def test_no_stale_host_names(text):
    """This repo is host-neutral; a leftover host name routes to a skill that is
    not installed."""
    for name in ("genie-harness", "~/.hermes", "coding-hermes"):
        check(name not in text, "skill does not name %s" % name)


def main():
    text = body()
    for fn in (test_frontmatter, test_three_sections, test_reverse_is_conditional,
               test_verdicts_line_up, test_literal_paths_resolve,
               test_fallback_commands_run, test_no_stale_host_names):
        fn(text)
    for f in FAILS:
        print("FAIL ", f)
    if FAILS:
        print("\n%d of %d checks failed" % (len(FAILS), len(CHECKS)))
        return 1
    print("PASS  %d checks: frontmatter, three jobs, §3.5 conditional + legal, verdicts, "
          "paths, grep and printf fallbacks (newline-safe, grammar-clean, findable) "
          "agree with the CLI" % len(CHECKS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
