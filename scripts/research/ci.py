"""The checks of a pull request, run in this repository's Actions.

The heavy checks (the gate comparison, the full render check, the selftests, the harness selftest on Linux and on
Windows, the parity check) run in the Actions of the repository named by settings.json `ci_repo`, whose workflow
`ci_workflow` runs `scripts/research/ci-checks.sh` and prints only a PASS, FAIL or SKIP line per check, never a
check's output: the log of a public repository is public. The workflow runs on a push by a collaborator and on a
manual dispatch; it has no pull_request trigger, so a pull request opened by anyone outside the team starts nothing.
A push starts the run on the head it pushed; a dispatch names the branch (`--ref`) and the base (`-f base=...`).
A run is found by its head commit (`gh run list --commit`), never by its title: the workflow sets no run-name, and a
run of another event on the same head is the same head. It is green only when its jobs `ci_jobs` (gate,
harness-windows, parity) all succeeded: a run whose jobs were skipped reports success too, and proves nothing.
`rq land` notes the run a push started; `rq merge` waits for the run on the head it merges. The light checks (the
text of the commits and of the pull request, and the baseline rows) run here, in the merge session's process: a few
git calls and one hook per commit.

A failed check names itself; its output is in no log. The merge session reproduces that one check in its own clone
(never in the research checkout, AGENTS.md section 2 rule 14), for the gate `scripts/rq gatecmp --base origin/main`.
"""

import json
import os
import shutil
import subprocess
import time

import track
from common import BASH, REPO, SETTINGS, Fail, git, rq_home

CI_REPO = SETTINGS.get("ci_repo")
CI_WORKFLOW = SETTINGS.get("ci_workflow")
CI_REF = SETTINGS.get("ci_ref", "main")
# the jobs a run of the workflow must finish with success; a job that is skipped or missing is not green
CI_JOBS = tuple(SETTINGS.get("ci_jobs") or ("gate", "harness-windows", "parity"))
LABEL_BASELINE = "rq:baseline"


def remote():
    """True when the heavy checks run in a repository's Actions (settings.json names it)."""
    return bool(CI_REPO and CI_WORKFLOW)


def pushed_to_ci(repo=REPO):
    """True when a push of a run branch lands in the CI repository, which starts the run by itself. A push to a fork
    starts nothing. The remote's URL is reduced to owner/name first, so a fork whose name merely contains the CI
    repository's name is not mistaken for it."""
    from common import REMOTE, repo_slug
    url = (git(repo, "remote", "get-url", REMOTE, check=False) or "").strip()
    if not url or not CI_REPO:
        return False
    return bool(url) and repo_slug(url) == CI_REPO.lower()


def runs_url():
    return "https://github.com/%s/actions/workflows/%s" % (CI_REPO, CI_WORKFLOW)


class Unanswered(Fail):
    """gh did not answer (a timeout, the network, an error status): the caller may ask again."""


def find(head, repo=REPO):
    """The newest run of the workflow on head: a run of another head is never this one. -> dict(id, status,
    conclusion, url) or None. Fail without gh; Unanswered when gh did not answer, so a silent CI is never read as no
    run."""
    rc, out = track.gh_run(["run", "list", "--repo", CI_REPO, "--workflow", CI_WORKFLOW, "--commit", head,
                            "--limit", "100", "--json",
                            "databaseId,headSha,status,conclusion,url,createdAt,event,headBranch"], repo)
    if rc is None and not out and (os.environ.get("RQ_NO_GITHUB") or not shutil.which("gh")):
        raise Fail("the remote CI cannot be read: gh is missing or RQ_NO_GITHUB is set (%s)" % runs_url(), 1)
    try:
        rows = json.loads(out) if rc == 0 and out else None
    except ValueError:
        rows = None
    if rows is None:
        raise Unanswered("gh could not list the runs of %s in %s (exit %s)" % (CI_WORKFLOW, CI_REPO, rc), 1)
    mine = [x for x in rows if x.get("headSha") == head]
    if not mine:
        return None
    # a cancelled run is the answer only when it is the only one: a run of the same head that finished is newer news
    done = [x for x in mine if x.get("conclusion") != "cancelled"]
    x = max(done or mine, key=lambda y: y.get("createdAt") or "")
    return {"id": x.get("databaseId"), "status": x.get("status"), "conclusion": x.get("conclusion"), "url": x.get("url")}


def dispatch(head, base, branch, repo=REPO):
    """Ask the CI repository for a run of branch against base. -> True when GitHub took the request. A push that
    lands in the CI repository starts the run, so nothing is dispatched for a run branch."""
    if pushed_to_ci(repo):
        return False
    rc, _ = track.gh_run(["workflow", "run", CI_WORKFLOW, "--repo", CI_REPO, "--ref", branch or CI_REF,
                          "-f", "base=%s" % base], repo)
    return rc == 0


def jobs(run_id, repo=REPO):
    """The jobs of a run: [{name, conclusion, steps}]. Unanswered when gh did not answer."""
    rc, out = track.gh_run(["run", "view", str(run_id), "--repo", CI_REPO, "--json", "jobs"], repo)
    try:
        got = (json.loads(out) or {}).get("jobs") if rc == 0 and out else None
    except ValueError:
        got = None
    if got is None:
        raise Unanswered("gh could not read the jobs of run %s in %s (exit %s)" % (run_id, CI_REPO, rc), 1)
    return got


def verdict(run, js):
    """-> (green, problems) for a completed run: green only when the run succeeded and every job of CI_JOBS is
    there and succeeded. A run whose jobs were all skipped also reports success, which proves nothing."""
    problems = []
    by = {j.get("name"): j for j in js}
    for name in CI_JOBS:
        j = by.get(name)
        if j is None:
            problems.append("%s: missing" % name)
        elif j.get("conclusion") != "success":
            steps = [s.get("name") for s in j.get("steps") or [] if s.get("conclusion") == "failure"]
            problems.append("%s: %s" % (name, ", ".join(steps) if steps else j.get("conclusion") or "not finished"))
    for j in js:
        if j.get("name") not in CI_JOBS and j.get("conclusion") not in ("success", "skipped", "neutral"):
            problems.append("%s: %s" % (j.get("name"), j.get("conclusion") or "not finished"))
    if run.get("conclusion") != "success" and not problems:
        problems.append("the run: %s" % run.get("conclusion"))
    return not problems, problems


def failed_lines(run_id, repo=REPO):
    """The FAIL and RED lines that scripts/research/ci-checks.sh printed in the failed jobs: check names, never a
    check's output (the script prints none). -> lines."""
    rc, out = track.gh_run(["run", "view", str(run_id), "--repo", CI_REPO, "--log-failed"], repo)
    got = []
    for ln in (out or "").splitlines() if rc == 0 else []:
        text = ln.split("\t")[-1]
        text = text.split(" ", 1)[1] if text[:4].isdigit() and " " in text else text  # the timestamp gh puts first
        if text.startswith(("FAIL ", "RED: ")) and text.strip() not in got:
            got.append(text.strip())
    return got


def ensure(head, base, branch, repo=REPO, register=120, poll=10):
    """The run on head: the one that exists (a failed one too: its failure is the answer), or a new one when there is
    none. -> the run dict; Fail when none registers. A cancelled run stays the answer: GitHub cancelled it, and a
    head that is pushed again gets a new run."""
    got = find(head, repo)
    if got and got.get("conclusion") != "cancelled":
        return got
    if pushed_to_ci(repo):
        if got:
            raise Fail("the run of %s was cancelled and the push that started it is spent: push the branch again, and "
                       "the push starts the next run (%s)" % (head[:10], runs_url()), 1)
        raise Fail("no run of %s exists in %s, and nothing is dispatched there: the push did not start a run - the "
                   "workflow has no push trigger, or Actions is off (%s)" % (head[:10], CI_REPO, runs_url()), 1)
    if not dispatch(head, base, branch, repo):
        raise Fail("the remote CI was not started: gh workflow run %s --repo %s --ref %s failed (the network, the gh "
                   "login, a workflow that is not on %s, or a branch that %s lacks: origin here is not %s, so the push "
                   "went elsewhere, and only a push to %s gets the head checked)"
                   % (CI_WORKFLOW, CI_REPO, branch, CI_REPO, CI_REPO, CI_REPO, CI_REPO), 1)
    t0 = time.time()
    while True:
        try:
            got = find(head, repo)
        except Unanswered:
            got = None
        if got and got.get("conclusion") != "cancelled":
            return got
        if time.time() - t0 > register:
            raise Fail("the remote CI took the request for %s but no run registered within %d s (%s)"
                       % (head[:10], register, runs_url()), 1)
        time.sleep(poll)  # wait: poll, GitHub registers a pushed or dispatched run after a few seconds


def wait(head, base, branch, repo=REPO, timeout=3600, poll=20, register=120, tries=6):
    """Wait for the run on head (started when there is none) and pass only when verdict() is green. A failure names
    the failed jobs, steps and checks; a cancelled run, a skipped or missing job, gh that does not answer `tries`
    times in a row, or no end within timeout, is not green."""
    t0, errors = time.time(), 0
    while True:
        try:
            got = ensure(head, base, branch, repo, register=register, poll=min(poll, 10))
            break
        except Unanswered as e:
            errors += 1
            if errors >= tries:
                raise Fail("%s, %d times in a row; the merge stops" % (e, errors), 1)
            time.sleep(poll)  # wait: poll, gh did not answer
    errors = 0
    while True:
        if got.get("status") == "completed":
            try:
                green, problems = verdict(got, jobs(got.get("id"), repo))
            except Unanswered as e:
                green, problems = None, [str(e)]
                errors += 1
                if errors >= tries:
                    raise Fail("%s, %d times in a row; the merge stops (%s)" % (e, errors, got.get("url")), 1)
            if green:
                return got
            if green is False:
                lines = failed_lines(got.get("id"), repo) if got.get("conclusion") == "failure" else []
                raise Fail("the remote CI is not green on %s (%s): %s. Its log prints no check output: read a failed "
                           "check in an own clone, never in the research checkout (for the gate: scripts/rq gatecmp "
                           "--base origin/main). Once the cause is fixed, a new head gets a new run; a run that failed "
                           "for a passing reason runs again with gh run rerun %s --failed --repo %s"
                           % (head[:10], got.get("url"), "; ".join(problems + lines), got.get("id"), CI_REPO), 1)
        if time.time() - t0 > timeout:
            raise Fail("the remote CI on %s did not finish within %d s: %s" % (head[:10], timeout, got.get("url")), 1)
        time.sleep(poll)  # wait: poll, the remote run is queued or running, or gh did not answer
        try:
            got = find(head, repo) or got
            errors = 0
        except Unanswered as e:
            errors += 1
            if errors >= tries:
                raise Fail("%s, %d times in a row; the merge stops (%s)" % (e, errors, got.get("url")), 1)


def describe(head, repo=REPO):
    """One line on the run of head, for rq ci and for the land notes."""
    got = find(head, repo)
    if not got:
        return "remote CI: no run on %s yet (%s)" % (head[:10], runs_url())
    line = "remote CI on %s: %s (%s)" % (head[:10], got.get("conclusion") or got.get("status"), got.get("url"))
    if got.get("status") == "completed":
        green, problems = verdict(got, jobs(got.get("id"), repo))
        line += "; green" if green else "; not green: %s" % "; ".join(problems + failed_lines(got.get("id"), repo))
    return line


# ------------------------------------------------------------------------------------------------- the light checks

def hook(text, repo=REPO):
    """.githooks/commit-msg on one message. -> (ok, what it printed)."""
    path = os.path.join(rq_home(repo), "tmp", "ci-msg-%d.txt" % os.getpid())
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text if text.endswith("\n") else text + "\n")
    try:
        r = subprocess.run([BASH or "sh", os.path.join(repo, ".githooks", "commit-msg"), path], cwd=repo,
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def reason(said):
    """The hook's own reason (its line that starts "commit-msg:"), else its last line."""
    lines = [ln for ln in (said or "").splitlines() if ln.strip()]
    mine = [ln for ln in lines if ln.startswith("commit-msg:")]
    return (mine or lines or ["refused by the commit hook"])[-1]


def commits(base, head, repo=REPO):
    """The commits of base..head, merges aside."""
    return (git(repo, "rev-list", "--no-merges", "%s..%s" % (base, head)) or "").split()


def text_problems(base, head, title_, body, repo=REPO, cs=None):
    """The pr-text check: each commit message of base..head (merges aside) and the pull request's title and body pass
    the commit hook (no tool credit, no subject over 100 characters or ending in a full stop). -> lines."""
    out = []
    for c in commits(base, head, repo) if cs is None else cs:
        good, said = hook(git(repo, "log", "-1", "--format=%B", c) or "", repo)
        if not good:
            out.append("commit %s: %s" % (c[:10], reason(said)))
    if title_:
        good, said = hook("%s\n\n%s\n" % (title_, body or ""), repo)
        if not good:
            out.append("the pull request title or body: %s" % reason(said))
    return out


def light(pr, base, head, repo=REPO):
    """The checks that cost almost nothing, in this process: the text of the commits and of the pull request, and
    the baseline rows (a row added only with the label a merge session applies). Fail on the first that fails."""
    import land
    raw = track.gh(["pr", "view", pr, "--json", "title,body,labels"], repo)
    try:
        v = json.loads(raw) if raw else None
    except ValueError:
        v = None
    if v is None:
        raise Fail("gh could not read the title, body and labels of %s; the light checks did not run" % pr, 1)
    cs = commits(base, head, repo)
    bad = text_problems(base, head, v.get("title"), v.get("body"), repo, cs)
    if bad:
        raise Fail("the text check failed: %s" % "; ".join(bad), 1)
    added = land.baseline_added(base, head, repo)
    labels = {x.get("name") for x in v.get("labels") or []}
    if added and LABEL_BASELINE not in labels:
        raise Fail("the baseline gains %d row(s) and the pull request does not carry %s: a merge session reviews the "
                   "rows first (%s)" % (len(added), LABEL_BASELINE, "; ".join(added[:5])), 1)
    return ["light checks: the text of %d commit(s) and of the pull request, and the baseline (%d added row(s)%s)"
            % (len(cs), len(added), ", labelled" if added else "")]
