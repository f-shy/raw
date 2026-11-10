"""Shared helpers for the research harness (scripts/rq). Standard library only.

Nothing here knows about any model or agent harness: the harness is files, a few commands and
mechanical checks that any agent, in any tool, can run.

One working tree (AGENTS.md section 2 rule 14). Every research agent on the machine works in the same checkout, the
research checkout, so nothing here makes a git worktree, a clone or a copy of the tree, and nothing here changes the
checkout's branch, index, tracked files or git configuration. A run branch rq/<run> exists only as git objects and a
ref: TreeView reads a commit without a checkout, Overlay holds the changes of one unit, and commit_on writes them as
a commit with git plumbing and moves the ref with a compare-and-set. Every git command goes through git(), which
refuses anything outside an allowlist. Every file an agent makes goes under .tmp/<id>/.
"""
import datetime as dt
import gzip
import hashlib
import html
import importlib.util
import json
import os
import re
import subprocess
import shutil
import sys
import time
import unicodedata
import zlib
from urllib.parse import urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
with open(os.path.join(HERE, "settings.json"), encoding="utf-8") as _f:
    SETTINGS = json.load(_f)
REMOTE, BASE = SETTINGS["remote"], SETTINGS["base_branch"]
UPSTREAM = "%s/%s" % (REMOTE, BASE)  # the short name, for messages only
# every comparison with main resolves a full refname: a local branch refs/heads/origin/main or a tag main would win
# over the remote-tracking ref in git's short-name lookup, and git only warns on stderr (G7-03)
UPSTREAM_REF = "refs/remotes/%s/%s" % (REMOTE, BASE)
BASE_REF = "refs/heads/%s" % BASE
GITHUB_REPO = SETTINGS.get("github_repo")


def harness_env(repo=REPO):
    """The environment every harness process and its children run with: a plain `git status` cannot take the index
    lock and rewrite the shared index, and Python writes its bytecode under .tmp/rq/pycache, never beside the
    scripts (section 1.2 of the one-tree design)."""
    os.environ["GIT_OPTIONAL_LOCKS"] = "0"
    # a fetch or a push never waits for a person: no terminal prompt and no credential dialog (a token that expired
    # fails the call at once instead of holding the fetch lock that every other process waits on), and git's
    # messages are English, which the harness reads (a rejected push, a ref lock file) (G3-07)
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    os.environ["GCM_INTERACTIVE"] = "never"
    os.environ["LANGUAGE"] = "C"
    pc = os.path.join(repo, ".tmp", "rq", "pycache")
    os.environ["PYTHONPYCACHEPREFIX"] = pc
    try:
        sys.pycache_prefix = pc
    except Exception:
        pass


harness_env()


def find_bash():
    """gate.sh and broker.sh are bash scripts, and `sh` is dash on Debian and Ubuntu. $RQ_BASH wins. On Windows,
    bash on PATH can be the WSL launcher (System32) or a Store stub, which would run the gate inside WSL on a
    Windows path, so the bash of Git for Windows (beside git.exe) comes first."""
    if os.environ.get("RQ_BASH"):
        return os.environ["RQ_BASH"]
    if os.name == "nt":
        g = shutil.which("git")
        d = os.path.dirname(os.path.realpath(g)) if g else ""
        for _ in range(3):
            if not d:
                break
            for c in (os.path.join(d, "bin", "bash.exe"), os.path.join(d, "usr", "bin", "bash.exe")):
                if os.path.exists(c):
                    return c
            d = os.path.dirname(d)
        b = shutil.which("bash")
        if b and not any(x in b.lower() for x in ("system32", "windowsapps")):
            return b
    return shutil.which("bash") or "sh"


BASH = find_bash()
LADDER = ["unverified", "inferred", "reported", "documented", "measured"]  # weakest first
KINDS = ["discover", "verify", "reconcile", "audit"]  # unit kinds; a run kind (RUN_KINDS in units.py) is another list
OPS = ["set", "confirm", "append_evidence", "drop_evidence", "add_record", "dead", "relate", "open_question"]
CAUSES = ["dead-service", "registration-closed", "free-tier-removed", "revoked", "acquired"]
RELATIONS = ["duplicate_of", "variant_of", "successor_of", "same_offer_as"]
SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
RID_RE = re.compile(r"^[a-z0-9-]+/[a-z0-9]+(-[a-z0-9]+)*$")
# a run that is over: its folder and ref wait only for the wipe; `landed` is the old name of `merged`
DONE_PHASES = ("landed-empty", "merged", "landed", "closed")


class Fail(Exception):
    def __init__(self, msg, code=1):
        super().__init__(msg)
        self.code = code


def utc_now():
    if os.environ.get("RQ_TEST_NOW"):
        return dt.datetime.fromtimestamp(float(os.environ["RQ_TEST_NOW"]), dt.timezone.utc)
    return dt.datetime.now(dt.timezone.utc)


class TestStop(BaseException):
    """The selftest's kill at a named point, raised in-process when RQ_TEST_STOP_RAISE is set."""


def test_stop(point):
    """The selftest kills a command at a named point (RQ_TEST_STOP_AFTER) to test what the next command finds. In a
    subprocess the kill is os._exit, as a real kill would be; in-process (RQ_TEST_STOP_RAISE) it raises TestStop."""
    if os.environ.get("RQ_TEST_STOP_AFTER") == point:
        if os.environ.get("RQ_TEST_STOP_RAISE"):
            raise TestStop(point)
        os._exit(9)


def now_ts():
    """Seconds since the epoch; RQ_TEST_NOW moves the clock in the selftest."""
    return float(os.environ.get("RQ_TEST_NOW") or time.time())


def stamp():
    return utc_now().strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp_ms():
    t = utc_now()
    return t.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (t.microsecond // 1000)


def today():
    return utc_now().date().isoformat()


def tmp_root(repo=REPO):
    return os.path.join(repo, ".tmp")


def rq_home(repo=REPO):
    """.tmp/rq/: harness-owned and shared (state.db, the locks, the bytecode); it holds nothing an agent made."""
    return os.path.join(repo, ".tmp", "rq")


def run_dir(run, repo=REPO):
    """.tmp/<run>/: one run, its plan, its units and their lane folders."""
    if not run or "/" in run or "\\" in run or run.startswith(".") or run in ("rq", "fshy"):
        raise Fail("not a run id: %r" % run, 2)
    return os.path.join(repo, ".tmp", run)


def tmp_rel(path, repo=REPO):
    """path relative to .tmp/ when it lies in an id folder, .tmp/<id>/ or below: "<id>" or "<id>/...". None for a
    path outside .tmp/, .tmp/ itself, and the harness's own .tmp/rq/ and .tmp/fshy/ (and a hidden name). Every file
    a research agent makes goes into its id folder (AGENTS.md section 2 rule 14)."""
    try:
        rel = os.path.relpath(os.path.abspath(path), os.path.join(repo, ".tmp")).replace("\\", "/")
    except ValueError:  # another drive on Windows
        return None
    first = rel.split("/", 1)[0]
    if rel in (".", "..") or rel.startswith("../") or os.path.isabs(rel) or first in ("rq", "fshy") or first.startswith("."):
        return None
    return rel


def legacy_dirs(repo=REPO):
    """The folders of the harness before the one-tree change; while one exists, only status, wipe and close run."""
    return [p for p in (os.path.join(repo, ".tmp", "rq", "runs"), os.path.join(repo, ".tmp", "rq", "wt")) if os.path.isdir(p)]


def read_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def replace_file(tmp, path):
    """os.replace, tried again for about two seconds on Windows, where it is refused (WinError 5 or 32) while another
    process has the target open: a parallel rq status or collect that reads it, or a virus scanner (G-05)."""
    for i in range(40):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if os.name != "nt" or i == 39:
                raise
            time.sleep(0.05)  # wait: lock, another process holds the file open on Windows


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp-%d" % os.getpid()
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")
    replace_file(tmp, path)


def write_jsonl(path, rows):
    """Rewrite a JSON-lines file whole, through a temporary file and a rename: a kill leaves the old file or the new
    one, never a truncated one (G-10)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp-%d" % os.getpid()
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    replace_file(tmp, path)


def json_bytes(obj):
    """The bytes write_json writes, for a file that goes onto a run branch instead of the disk."""
    return (json.dumps(obj, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def utf8_problem(path):
    """None when the file is absent or UTF-8; else a problem line that names the first byte that is not. A lane that
    writes through a Windows code page (0x92 for a right quote in cp1252) would otherwise crash the reader."""
    try:
        with open(path, "rb") as f:
            b = f.read()
    except FileNotFoundError:
        return None
    try:
        b.decode("utf-8")
        return None
    except UnicodeDecodeError as e:
        return ("%s is not UTF-8: byte 0x%02x at line %d (offset %d); write the file again as UTF-8"
                % (os.path.basename(path), b[e.start], b.count(b"\n", 0, e.start) + 1, e.start))


def read_jsonl(path):
    out = []
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as f:
        return parse_jsonl(f.read())


def parse_jsonl(text):
    out = []
    for n, ln in enumerate((text or "").splitlines(), 1):
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except ValueError as e:
            out.append({"_bad": "line %d: %s" % (n, e)})
    return out


def append_jsonl(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def sha256_text(text):
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------------------------- git

class GitRefused(Fail):
    pass


GIT_READS = {"cat-file", "ls-tree", "rev-parse", "rev-list", "log", "show", "diff-tree", "merge-base",
             "for-each-ref", "version", "ls-files", "count-objects", "archive", "show-ref", "var"}
GIT_REF_PREFIXES = ("refs/heads/rq/", "refs/heads/intake/")
_GIT_VERSION = {}


def _ref_ok(name):
    if name.startswith(GIT_REF_PREFIXES):
        return True
    return bool(os.environ.get("RQ_SELFTEST")) and name.startswith("refs/heads/test-")


def repo_slug(url):
    """owner/name (lower case) of a git remote URL in any form (https, ssh://, git@host:owner/name, with or without
    .git), or "" when the text is not a URL of that shape (a path, a remote's name)."""
    url = (url or "").strip().replace("\\", "/")
    if "://" in url:
        url = url.split("://", 1)[1].split("/", 1)[-1]          # strip scheme and host
    elif ":" in url.split("/", 1)[0]:
        url = url.split(":", 1)[1]                              # git@host:owner/name
    else:
        return ""
    url = url.rstrip("/")
    url = url[:-4] if url.endswith(".git") else url
    owner, _, name = url.rpartition("/")
    owner = owner.rsplit("/", 1)[-1]
    return ("%s/%s" % (owner, name)).lower() if owner and name else ""


def _is_origin(remote, repo):
    """True when a push target is origin: its name, or the URL that origin has."""
    if remote == REMOTE:
        return True
    if not repo:
        return False
    try:
        url = subprocess.run(["git", "-C", repo, "remote", "get-url", REMOTE], capture_output=True, text=True).stdout.strip()
    except OSError:
        return False
    a, b = repo_slug(url), repo_slug(remote)
    if a and b:
        return a == b  # ssh and https forms of one repository are one
    norm = lambda u: u.replace("\\", "/").rstrip("/").removesuffix(".git").lower()
    return bool(url) and norm(url) == norm(remote)


def git_guard(args, merge_session=False, repo=None):
    """Refuse every git command that is not in the allowlist of the one-tree design (section 1.2): research writes git
    objects and the refs refs/heads/rq/* and refs/heads/intake/* with an old value, and fetches into
    refs/remotes/origin/*; it never writes the checkout's branch, index, files or configuration. The merge session's
    commands (rq sync, the legacy step of rq wipe, rq merge's push of the gated head to a pull request's branch) pass
    merge_session=True."""
    args = [str(a) for a in args]
    if not args:
        raise GitRefused("git with no subcommand", 2)
    cmd, rest = args[0], args[1:]
    flags = [a for a in rest if a.startswith("-")]
    pos = [a for a in rest if not a.startswith("-")]

    def no(why):
        raise GitRefused("refused: git %s (%s). Research writes the repository only through scripts/rq, with git "
                         "plumbing on a run branch (AGENTS.md section 2 rule 14)" % (" ".join(args)[:160], why), 2)
    if cmd in GIT_READS:
        return
    if cmd == "diff":
        # a diff against the working tree or the index refreshes the shared index when a file's stat data changed,
        # even with optional locks off; only a diff of two commits (A B, A..B or A...B) reads git objects alone
        revs = [a for a in (rest[:rest.index("--")] if "--" in rest else rest) if not a.startswith("-")]
        if "--cached" in rest or "--staged" in rest or "--no-index" in rest or not (
                len(revs) == 2 or (len(revs) == 1 and ".." in revs[0])):
            no("diff only between two commits (A B, A..B or A...B); a worktree diff can rewrite the shared index")
        return
    if cmd == "merge-tree":
        if "--write-tree" not in rest:
            no("merge-tree only with --write-tree")
        return
    if cmd == "status":
        if not any(a.startswith("--porcelain") for a in rest):
            no("status only with --porcelain")
        return
    if cmd == "config":
        if not rest or rest[0] not in ("--get", "--get-regexp", "--get-all", "-l", "--list"):
            no("config only reads")
        return
    if cmd == "remote":
        if rest[:1] != ["get-url"]:
            no("remote only get-url")
        return
    if cmd == "worktree":
        if rest[:1] == ["list"]:
            return
        if merge_session and (rest[:1] == ["prune"] or (rest[:1] == ["remove"] and "--force" in rest)):
            return
        no("research makes and removes no worktree")
    if cmd == "hash-object":
        if "-w" in rest and "--stdin" not in rest:
            no("hash-object writes only from --stdin")
        return
    if cmd in ("mktree", "commit-tree"):
        return
    if cmd == "update-ref":
        i, delete, out = 0, False, []
        while i < len(rest):
            a = rest[i]
            if a == "-m":
                i += 2
                continue
            if a == "-d":
                delete = True
            elif a.startswith("-"):
                no("update-ref option %s" % a)
            else:
                out.append(a)
            i += 1
        if not out or not (_ref_ok(out[0]) or (merge_session and delete and
                                               out[0].startswith("refs/remotes/%s/rq/" % REMOTE))):
            # the merge session's wipe deletes the remote-tracking ref of a done run (LIO3-05)
            no("only refs/heads/rq/* and refs/heads/intake/* are written")
        if (delete and len(out) != 2) or (not delete and len(out) != 3):
            no("update-ref needs the old value (compare-and-set)")
        return
    if cmd == "fetch":
        if "--no-write-fetch-head" not in rest:
            no("fetch needs --no-write-fetch-head")
        for a in flags:
            if a not in ("--no-write-fetch-head", "-q", "--quiet", "--no-tags"):
                no("fetch option %s" % a)
        for spec in pos[1:]:
            if ":" in spec and not spec.split(":", 1)[1].startswith("refs/remotes/"):
                no("fetch writes only refs/remotes/")
        return
    if cmd == "push":
        for a in flags:
            if a not in ("-q", "--quiet", "--delete", "--porcelain"):
                no("push option %s" % a)
        if len(pos) < 2:
            no("push names the remote and the refspec")
        for spec in pos[1:]:
            if spec.startswith("+"):
                no("no forced push")
            src, _, dst = spec.partition(":")
            if (merge_session and "--delete" not in flags and re.fullmatch(r"[0-9a-f]{40}", src)
                    and dst.startswith("refs/heads/")
                    and (dst != "refs/heads/" + BASE or not _is_origin(pos[0], repo))):
                continue  # rq merge: the gated head, fast-forward only, to the branch a pull request has as its head (main of a fork too, never origin's)
            dst = spec.split(":", 1)[-1]
            if not _ref_ok(dst):
                no("push only refs/heads/rq/* or refs/heads/intake/* to the same name")
        return
    if merge_session:
        if cmd == "merge" and "--ff-only" in rest:
            return
        if cmd == "reset" and "--hard" in rest and pos and pos[-1].startswith((REMOTE + "/", "refs/remotes/%s/" % REMOTE)):
            return
        if cmd == "update-index" and set(rest) <= {"-q", "--refresh"}:
            return
        if cmd == "maintenance" and rest[:1] == ["run"] and set(rest[1:]) <= {"--auto", "--quiet"}:
            return
    no("not in the allowlist")


def git_argv(repo, args, merge_session=False):
    git_guard(args, merge_session, repo)
    return ["git", "-C", repo, "-c", "gc.auto=0", "-c", "maintenance.auto=false"] + [str(a) for a in args]


def check_version():
    """git merge-tree --write-tree -X no-renames needs git 2.43 or later (-X came in 2.43); refuse an older git once,
    at the first merge-tree (land, plan's merge of main, resolve). Other commands do not start `git version` (LIO2-03)."""
    if "v" in _GIT_VERSION:
        return
    _GIT_VERSION["v"] = (0, 0)
    try:
        out = subprocess.run(["git", "version"], capture_output=True, text=True).stdout
    except FileNotFoundError:
        raise Fail("git is not on PATH", 3)
    m = re.search(r"(\d+)\.(\d+)", out or "")
    v = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    _GIT_VERSION["v"] = v
    if v < (2, 43):
        raise Fail("git %d.%d is too old: the harness needs git 2.43 or later (merge-tree --write-tree -X)" % v, 3)


def git(repo, *args, check=True, merge_session=False, input=None):
    """One git command, text mode, through the allowlist. Never use it for object bytes: a text-mode pipe on Windows
    turns \\n into \\r\\n (git_bytes and TreeView use binary pipes)."""
    r = subprocess.run(git_argv(repo, args, merge_session), capture_output=True, text=True, encoding="utf-8",
                       errors="replace", input=input)
    if check and r.returncode != 0:
        raise Fail("git %s failed: %s" % (" ".join(map(str, args)), (r.stderr or r.stdout).strip()[:400]))
    return (r.stdout or "").strip()


# a fetch or a push that has not ended after this many seconds hangs (a dead connection); it is a guard against a hang,
# not a pace: the call fails and the caller says so (G3-07)
NET_TIMEOUT = int(SETTINGS.get("git_network_timeout_s", 300))


def kill_tree(p):
    """Kill a process and every process it started. On Windows a killed git.exe leaves its transport helper
    (git-remote-https, an ext:: command) running with the pipes it inherited, so the whole tree goes (G5-01)."""
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, timeout=30)
        else:
            import signal
            os.killpg(p.pid, signal.SIGKILL)
    except Exception:
        pass
    try:
        p.kill()
    except Exception:
        pass


def bounded(argv, timeout, input=None, repo=REPO):
    """Run argv with a deadline that holds on every platform. -> (exit code, stdout bytes, stderr bytes), or None when
    the deadline passed. The output goes to files under .tmp/rq/tmp/, never to pipes: on Windows, subprocess.run with
    a timeout kills git.exe and then waits for the end of its pipes, which a transport helper that inherited them
    keeps open for as long as it runs (hours on a stalled HTTPS connection). The process tree is killed on expiry."""
    d = os.path.join(rq_home(repo), "tmp")
    os.makedirs(d, exist_ok=True)
    tag = "git-%d-%d" % (os.getpid(), time.monotonic_ns())
    paths = [os.path.join(d, "%s.%s" % (tag, n)) for n in ("in", "out", "err")]
    kw = {} if os.name == "nt" else {"start_new_session": True}  # taskkill /T follows the tree on Windows
    fin = None
    try:
        if input is not None:
            with open(paths[0], "wb") as f:
                f.write(input if isinstance(input, bytes) else input.encode("utf-8"))
            fin = open(paths[0], "rb")
        with open(paths[1], "wb") as fo, open(paths[2], "wb") as fe:
            p = subprocess.Popen(argv, stdin=fin or subprocess.DEVNULL, stdout=fo, stderr=fe, **kw)
            try:
                rc = p.wait(timeout=timeout)
            except BaseException as e:  # the deadline, or an interrupt: no helper outlives the call
                kill_tree(p)
                try:
                    p.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    pass
                if isinstance(e, subprocess.TimeoutExpired):
                    return None
                raise
        with open(paths[1], "rb") as f:
            out = f.read()
        with open(paths[2], "rb") as f:
            err = f.read()
        return rc, out, err
    finally:
        if fin is not None:
            fin.close()
        for x in paths:
            try:
                os.remove(x)
            except OSError:
                pass  # a helper still holds it on Windows; the merge session's wipe takes it


def net_argv(argv, timeout):
    """A fetch or a push that moves less than one byte a second for timeout seconds gives up inside git and its
    helper, on any platform (G5-01)."""
    if not timeout:
        return argv
    i = argv.index("-C") + 2 if "-C" in argv else 1
    return argv[:i] + ["-c", "http.lowSpeedLimit=1", "-c", "http.lowSpeedTime=%d" % max(1, int(timeout))] + argv[i:]


def git_ok(repo, *args, merge_session=False, timeout=None):
    argv = git_argv(repo, args, merge_session)
    if timeout is None:
        return subprocess.run(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    r = bounded(net_argv(argv, timeout), timeout, repo=repo)
    return r is not None and r[0] == 0


def git_run(repo, *args, merge_session=False, input=None, timeout=None):
    """-> (exit code, stdout, stderr) as text, for a caller that reads a non-zero exit (merge-tree exits 1 on a conflict).
    A call that outlives timeout exits 124 with a stderr that says so; its whole process tree is killed (G5-01)."""
    argv = git_argv(repo, args, merge_session)
    if timeout is None:
        r = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", input=input)
        return r.returncode, r.stdout or "", r.stderr or ""
    r = bounded(net_argv(argv, timeout), timeout, input=input, repo=repo)
    if r is None:
        return 124, "", "git %s did not end within %s s (a hung connection)" % (args[0] if args else "", timeout)
    def dec(b):
        return b.decode("utf-8", "replace").replace("\r\n", "\n")
    return r[0], dec(r[1]), dec(r[2])


def status_paths(repo, *args):
    """The paths `git status --porcelain` lists. git() strips its output, which would cut the first line's two status
    columns (" M path" -> "M path"), so this reads the output as it is."""
    rc, out, err = git_run(repo, "status", "--porcelain", *args)
    return [ln[3:].strip() for ln in out.splitlines() if len(ln) > 3]


def git_bytes(repo, *args, input=None, check=True):
    r = subprocess.run(git_argv(repo, args), capture_output=True, input=input)
    if check and r.returncode != 0:
        raise Fail("git %s failed: %s" % (" ".join(map(str, args)), r.stderr.decode("utf-8", "replace").strip()[:400]))
    return r.stdout


def has_remote(repo=REPO):
    return git_ok(repo, "remote", "get-url", REMOTE)


def rev(repo, name):
    """The commit a name points at, or None."""
    return git(repo, "rev-parse", "--verify", "-q", name + "^{commit}", check=False) or None


def is_ancestor(repo, a, b):
    return git_ok(repo, "merge-base", "--is-ancestor", a, b)


def upstream(repo=REPO):
    """refs/remotes/origin/main when the clone has it, else refs/heads/main: full refnames, never the short names a
    local branch or a tag of the same name would shadow (G7-03). short_ref() gives the name for a message."""
    return UPSTREAM_REF if rev(repo, UPSTREAM_REF) else BASE_REF


def short_ref(name):
    """refs/remotes/origin/main -> origin/main, refs/heads/main -> main: the name a message prints."""
    for pre in ("refs/remotes/", "refs/heads/"):
        if (name or "").startswith(pre):
            return name[len(pre):]
    return name


def upstream_shadowed(repo=REPO):
    """A ref that shadows origin/main or main in git's short-name lookup (a branch refs/heads/origin/main, a tag main),
    or None. The harness resolves full refnames, so this is a warning for rq status (G7-03)."""
    # git's lookup order for a short name: refs/NAME, refs/tags/NAME, refs/heads/NAME, refs/remotes/NAME; a ref earlier
    # in the order than the full one wins (and rev-parse --symbolic-full-name only says "ambiguous")
    shadows = {}
    for short, full in ((UPSTREAM, UPSTREAM_REF), (BASE, BASE_REF)):
        for pre in ("refs/", "refs/tags/", "refs/heads/", "refs/remotes/"):
            if pre + short == full:
                break
            shadows[pre + short] = (short, full)
    have = set(git(repo, "for-each-ref", "--format=%(refname)", *sorted(shadows), check=False).split())
    out = ["%s is %s, not %s" % (shadows[n][0], n, shadows[n][1]) for n in sorted(shadows) if n in have]
    return "; ".join(out) or None


def extra_worktrees(repo=REPO):
    """The linked worktrees of the checkout, the main working tree left out (git lists it first): [(path, branch)],
    branch "detached" when the worktree has none. In the research checkout each one is a full-tree copy made against
    AGENTS.md section 2 rule 14 (a subagent started with worktree isolation, the old harness's .tmp/rq/wt/) (LIO7-01)."""
    out, cur = [], None
    for ln in git(repo, "worktree", "list", "--porcelain", check=False).splitlines() + [""]:
        if ln.startswith("worktree "):
            cur = [ln[len("worktree "):].strip(), "detached"]
        elif ln.startswith("branch ") and cur:
            cur[1] = ln[len("branch "):].strip().replace("refs/heads/", "", 1)
        elif not ln.strip() and cur:
            out.append(tuple(cur))
            cur = None
    return out[1:]


def research_checkout(repo=REPO):
    """True in the one checkout where all research runs (git config rq.researchCheckout true, set by the merge session)."""
    return git(repo, "config", "--get", "rq.researchCheckout", check=False).strip().lower() == "true"


# ---------------------------------------------------------------------------------------------- locks

class Locked(Fail):
    pass


class FileLock:
    """An exclusive lock on a file that the operating system releases when the holder dies, so it is never stale.
    wait=True waits with no deadline (the build lock, the fetch lock); wait=False tries once (the run lock). On Windows,
    msvcrt.locking(LK_LOCK) gives up after about ten seconds, so the wait is a loop of LK_NBLCK. After it has the lock,
    the holder writes <lock>.holder: pid, UTC time, command line."""

    def __init__(self, path, wait=True, what="", on_wait=None):
        self.path, self.wait, self.what, self.on_wait = path, wait, what, on_wait
        self.fd = None

    def holder(self):
        try:
            with open(self.path + ".holder", encoding="utf-8") as f:
                return f.read().strip()
        except OSError:
            return ""

    def acquire(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        fd = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o644)
        told = False
        while True:
            try:
                if os.name == "nt":
                    import msvcrt
                    os.lseek(fd, 0, 0)
                    msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if not self.wait:
                    os.close(fd)
                    raise Locked("%s is locked by %s" % (self.what or os.path.basename(self.path),
                                                       self.holder() or "another process"), 1)
                if not told and self.on_wait:
                    self.on_wait(self.holder())
                    told = True
                if os.name != "nt":
                    import fcntl
                    fcntl.flock(fd, fcntl.LOCK_EX)  # wait: lock, with no deadline
                    break
                time.sleep(0.2)  # wait: lock, LK_NBLCK again (LK_LOCK gives up after about 10 s)
        self.fd = fd
        try:
            with open(self.path + ".holder", "w", encoding="utf-8", newline="\n") as f:
                f.write("pid %d since %s: %s\n" % (os.getpid(), stamp(), " ".join(sys.argv)[:300]))
        except OSError:
            pass
        _LOCKS.append(self)
        return self

    def release(self):
        if self.fd is None:
            return
        try:
            if os.name == "nt":
                import msvcrt
                os.lseek(self.fd, 0, 0)
                try:
                    msvcrt.locking(self.fd, msvcrt.LK_UNLCK, 1)
                except OSError:
                    pass
            else:
                import fcntl
                fcntl.flock(self.fd, fcntl.LOCK_UN)
        finally:
            os.close(self.fd)
            self.fd = None
            if self in _LOCKS:
                _LOCKS.remove(self)

    def __enter__(self):
        return self.acquire()

    def __exit__(self, *a):
        self.release()


_LOCKS = []


def run_lock(run, repo=REPO):
    """The one-writer lock of a run. It never waits: a second writer is a mistake to report, not a turn to wait for."""
    return FileLock(os.path.join(run_dir(run, repo), "lock"), wait=False, what="rq/%s" % run)


def fetch(repo=REPO, refspecs=(), quiet=True):
    """One fetch, joined with any fetch another process started after this one asked (the stamp holds the start time
    and the refspecs). Thirty processes that fetch at once otherwise race on the lock of refs/remotes/origin/main.
    This joins concurrent fetches; it is not a limit. -> True when origin answered."""
    if not has_remote(repo):
        return False
    # main by an explicit refspec: a clone whose remote.origin.fetch does not map main (a single-branch clone of
    # another branch) would otherwise update nothing and leave origin/main stale or absent (G2-08)
    refspecs = [base_refspec() if s == BASE else s for s in (list(refspecs) or [BASE])]
    asked = time.time()
    lockp = os.path.join(rq_home(repo), "locks", "fetch.lock")
    stampp = os.path.join(rq_home(repo), "locks", "fetch.stamp")
    def told(holder):
        print("rq: waiting for the fetch lock (%s); a fetch ends within %d s" % (holder or "another process", NET_TIMEOUT),
              file=sys.stderr)
    with FileLock(lockp, wait=True, what="the fetch lock", on_wait=told):
        st = read_json(stampp, None) if os.path.exists(stampp) else None
        if isinstance(st, dict) and st.get("ok") and st.get("start", 0) >= asked and set(refspecs) <= set(st.get("refspecs") or []):
            return True
        start = time.time()
        args = ["fetch", "--no-write-fetch-head", "-q", REMOTE] + refspecs
        ok = git_ok(repo, *args, timeout=NET_TIMEOUT)
        try:
            write_json(stampp, {"start": start, "refspecs": refspecs, "ok": ok})
        except OSError:
            pass
    return ok


def base_refspec():
    return "+refs/heads/%s:refs/remotes/%s/%s" % (BASE, REMOTE, BASE)


def run_refspec(run):
    return "+refs/heads/rq/%s:refs/remotes/%s/rq/%s" % (run, REMOTE, run)


# ---------------------------------------------------------------------------------------------- objects

class CatFile:
    """One `git cat-file --batch` process per repository and command, on binary pipes (a text-mode pipe on Windows
    would turn \\n into \\r\\n on the way in and back on the way out)."""

    def __init__(self, repo):
        self.repo = repo
        self.p = None

    def get(self, spec):
        """-> (type, bytes) of an object id or a <rev>:<path> spec, or None when it is missing."""
        if self.p is None or self.p.poll() is not None:
            self.p = subprocess.Popen(git_argv(self.repo, ["cat-file", "--batch"]), stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.p.stdin.write(spec.encode("utf-8") + b"\n")
        self.p.stdin.flush()
        head = self.p.stdout.readline()
        if not head:
            raise Fail("git cat-file stopped while reading %s" % spec, 3)
        parts = head.split()
        if len(parts) < 3 or parts[-1] == b"missing" or parts[1] == b"missing":
            return None
        size = int(parts[2])
        data = self.p.stdout.read(size)
        self.p.stdout.read(1)
        return parts[1].decode(), data

    def close(self):
        if self.p is not None:
            try:
                self.p.stdin.close()
                self.p.wait(timeout=10)
            except Exception:
                try:
                    self.p.kill()
                except Exception:
                    pass
            self.p = None


_CAT = {}


def catfile(repo=REPO):
    if repo not in _CAT:
        _CAT[repo] = CatFile(repo)
    return _CAT[repo]


def close_git():
    """Close every cat-file process and lock this process holds (the wipe lets go of .tmp/ before it renames it)."""
    for c in list(_CAT.values()):
        c.close()
    _CAT.clear()
    for lk in list(_LOCKS):
        lk.release()


class TreeView:
    """A commit's files, read without a checkout: tree objects by id, cached, and blobs by id, through one cat-file
    process per command. listdir(dir) -> {name: (mode, oid)}; read(path) -> bytes or None; advance(new) moves the view
    to a new commit (the cache is by tree id, so an unchanged subtree is not read again)."""

    def __init__(self, repo, revname):
        self.repo = repo
        # a full commit id is taken as it is (advance reads it and checks it is a commit): a caller that resolved the
        # name already does not start a second rev-parse (LIO7-03)
        c = revname if re.match(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$", revname or "") else rev(repo, revname)
        if not c:
            raise Fail("no commit %s" % revname, 1)
        self.cat = catfile(repo)
        self._trees = {}
        self._blobs = {}
        self.commit = None
        self.tree = None
        self.advance(c)

    def advance(self, new, changed=None):
        got = self.cat.get(new)
        if not got or got[0] != "commit":
            raise Fail("no commit %s" % new, 1)
        self.commit = new
        self.tree = got[1].split(b"\n", 1)[0].split()[1].decode()
        self.parents = [ln.split()[1].decode() for ln in got[1].split(b"\n\n", 1)[0].split(b"\n") if ln.startswith(b"parent ")]
        return self

    def tree_entries(self, oid):
        if oid not in self._trees:
            got = self.cat.get(oid)
            if not got or got[0] != "tree":
                raise Fail("no tree %s" % oid, 1)
            self._trees[oid] = parse_tree(got[1], len(oid) // 2)
        return self._trees[oid]

    def entry(self, path, root=None):
        """(mode, oid) of a path under the view's tree (or another root tree), or None."""
        oid, mode = root or self.tree, "40000"
        for part in [p for p in (path or "").strip("/").split("/") if p]:
            if mode != "40000":
                return None
            e = self.tree_entries(oid).get(part)
            if e is None:
                return None
            mode, oid = e
        return mode, oid

    def listdir(self, d, root=None):
        e = self.entry(d, root)
        if not e or e[0] != "40000":
            return None
        return self.tree_entries(e[1])

    def ls(self, d):
        """[(name, is_dir)] of a directory, for render.py's source layer."""
        return [(n, m == "40000") for n, (m, _) in sorted((self.listdir(d) or {}).items())]

    def blob(self, oid):
        if oid not in self._blobs:
            got = self.cat.get(oid)
            if not got or got[0] != "blob":
                return None
            if len(got[1]) < 1 << 20:
                self._blobs[oid] = got[1]
            return got[1]
        return self._blobs[oid]

    def read(self, path, root=None):
        e = self.entry(path, root)
        if not e or e[0] == "40000":
            return None
        return self.blob(e[1])

    def text(self, path):
        b = self.read(path)
        return None if b is None else b.decode("utf-8")

    def exists(self, path):
        return self.entry(path) is not None

    def isdir(self, path):
        e = self.entry(path)
        return bool(e) and e[0] == "40000"

    def close(self):
        pass


def parse_tree(data, rawlen=20):
    out, i, n = {}, 0, len(data)
    while i < n:
        sp = data.index(b" ", i)
        nul = data.index(b"\0", sp)
        mode = data[i:sp].decode()
        name = data[sp + 1:nul].decode("utf-8", "surrogateescape")
        oid = data[nul + 1:nul + 1 + rawlen].hex()
        out[name] = (mode, oid)
        i = nul + 1 + rawlen
    return out


class Overlay:
    """A view plus the change set of the unit being built ({path: bytes, or None for a removal}). Every read inside a
    unit goes through it, so a second operation sees what the unit has decided already."""

    def __init__(self, view, changes=None):
        self.view = view
        self.changes = {} if changes is None else changes

    def read(self, path):
        if path in self.changes:
            return self.changes[path]
        return self.view.read(path)

    def text(self, path):
        b = self.read(path)
        return None if b is None else b.decode("utf-8")

    def exists(self, path):
        if path in self.changes:
            return self.changes[path] is not None
        return self.view.exists(path)

    def names(self, d):
        """The file names directly under d, with the unit's additions and removals."""
        d = d.strip("/")
        have = {n for n, (m, _) in (self.view.listdir(d) or {}).items() if m != "40000"}
        pre = d + "/"
        for p, v in self.changes.items():
            if p.startswith(pre) and "/" not in p[len(pre):]:
                (have.add if v is not None else have.discard)(p[len(pre):])
        return sorted(have)

    def set(self, path, data):
        self.changes[path] = data.encode("utf-8") if isinstance(data, str) else data

    def remove(self, path):
        if self.exists(path):
            self.changes[path] = None


_OBJDIR = {}


def _objects_dir(repo):
    if repo not in _OBJDIR:
        fmt = git(repo, "rev-parse", "--show-object-format", check=False) or "sha1"
        p = git(repo, "rev-parse", "--git-path", "objects")
        _OBJDIR[repo] = (fmt, p if os.path.isabs(p) else os.path.join(repo, p))
    return _OBJDIR[repo]


def blob_id(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def write_blob(repo, data):
    """A blob as a loose object written by Python (zlib into a temporary file, then a rename); one git process per
    blob would cost about 34 ms each. A target that exists holds the same object and is kept. Falls back to
    `git hash-object -w --stdin` in a repository whose objects are not SHA-1."""
    fmt, objdir = _objects_dir(repo)
    if fmt != "sha1":
        return git_bytes(repo, "hash-object", "-w", "--stdin", input=data).decode().strip()
    oid = blob_id(data)
    d = os.path.join(objdir, oid[:2])
    p = os.path.join(d, oid[2:])
    if os.path.exists(p):
        # freshen it as git does (freshen_loose_object): an old unreachable copy would otherwise be pruned by a
        # concurrent gc between this write and the update-ref that makes it reachable (G-08)
        try:
            os.utime(p, None)
        except OSError:
            pass
        return oid
    os.makedirs(d, exist_ok=True)
    tmp = os.path.join(d, "tmp_obj_rq_%d_%d" % (os.getpid(), time.perf_counter_ns()))
    with open(tmp, "wb") as f:
        f.write(zlib.compress(b"blob %d\0" % len(data) + data, 1))
    try:
        os.rename(tmp, p)
    except OSError:
        if not os.path.exists(p):
            os.remove(tmp)
            raise
        os.remove(tmp)
    return oid


# the extensions eol_convert never touches: these, and every `*.EXT binary` line of the checkout's .gitattributes
_BINARY_EXT = (".gz", ".png", ".jpg", ".pdf", ".zip", ".dat", ".ico", ".wasm", ".sqlite", ".db")
_BINARY = {}


def binary_exts(repo=REPO):
    """The binary extensions: _BINARY_EXT and the `*.EXT binary` lines of .gitattributes, read once (G6-08)."""
    if repo not in _BINARY:
        exts = set(_BINARY_EXT)
        try:
            with open(os.path.join(repo, ".gitattributes"), encoding="utf-8") as f:
                for ln in f:
                    m = re.match(r"^\*(\.[A-Za-z0-9_]+)\s+(?:.*\s)?(?:binary|-text)(?:\s|$)", ln.strip() + " ")
                    if m:
                        exts.add(m.group(1).lower())
        except OSError:
            pass
        _BINARY[repo] = tuple(sorted(exts))
    return _BINARY[repo]


def is_binary_path(path):
    return path.lower().endswith(binary_exts())


def eol_convert(path, data, base):
    """The line-ending convention of scripts/research/eol.py per path: a path keeps the endings its base blob has
    (CRLF when more than half of its line ends are CRLF), a new path is LF. Text with no carriage return for a CRLF
    path is converted; text with CRLF for a path that has none is refused."""
    if data is None or is_binary_path(path):
        return data
    crlf = base is not None and base.count(b"\r\n") * 2 > base.count(b"\n")
    if b"\r\n" in data:
        if base is None or b"\r" not in base:
            raise Fail("%s: the new text has CRLF line ends, and the path stores LF; write LF" % path, 1)
        return data
    if crlf and b"\n" in data:
        return data.replace(b"\n", b"\r\n")
    return data


# the code points HFS+ ignores in a name, which git's is_hfs_dotgit drops before it compares a segment with .git
_HFS_IGNORABLE = dict.fromkeys(map(ord, "\u200c\u200d\u200e\u200f\u202a\u202b\u202c\u202d\u202e"
                                        "\u206a\u206b\u206c\u206d\u206e\u206f\ufeff"))


def is_dotgit(seg):
    """git fsck's hasDotgit for one segment: '.git' in any case, with trailing dots or spaces (NTFS), with an NTFS
    alternate data stream ('.git::$INDEX_ALLOCATION'), as the NTFS short name 'git~1', or with code points that HFS+
    ignores (G3-09)."""
    s = seg.translate(_HFS_IGNORABLE).lower()
    return s.split(":", 1)[0].rstrip(". ") in (".git", "git~1")


def bad_path(path):
    """Why git fsck (and GitHub's receive.fsckObjects) would refuse a tree entry on this path, or None: an empty, '.'
    or '..' segment, or a segment that is .git to NTFS or HFS+ (hasDot, hasDotdot, hasDotgit; is_dotgit). A run
    branch is never rewritten, so such an entry would keep its run from landing for good (G2-03)."""
    for seg in path.split("/"):
        if seg in ("", ".", ".."):
            return "the path %r has an empty, '.' or '..' segment" % path
        if is_dotgit(seg):
            return "the path %r has a .git segment" % path
    return None


def write_tree(repo, view, base_tree, changes):
    """-> (tree id, the changes that were not no-ops). No-op entries (bytes equal to the base blob, None for a path
    that is absent) are dropped first. Trees are rebuilt bottom-up, only for the directories that hold a change,
    through one `git mktree --batch -z` process; a directory left empty is dropped, a new one is made. A path that
    git fsck would refuse stops the call before any object is written."""
    for path in changes:
        why = bad_path(path.replace("\\", "/").strip("/"))
        if why:
            raise Fail("%s; nothing written" % why, 2)
    kept = {}
    for path, data in sorted(changes.items()):
        path = path.replace("\\", "/").strip("/")
        if isinstance(data, str):
            data = data.encode("utf-8")
        e = view.entry(path, base_tree)
        if e is not None and e[0] == "40000":
            raise Fail("%s is a directory on the run branch" % path, 1)
        if data is None:
            if e is None:
                continue
            kept[path] = None
            continue
        base = view.blob(e[1]) if e is not None and not is_binary_path(path) else None
        data = eol_convert(path, data, base)
        if e is not None and blob_id(data) == e[1]:
            continue
        kept[path] = data
    if not kept:
        return base_tree, {}
    files, dirs = {}, {}
    for path, data in kept.items():
        d, _, name = path.rpartition("/")
        files.setdefault(d, {})[name] = data
        while d:
            parent, _, sub = d.rpartition("/")
            dirs.setdefault(parent, set()).add(sub)
            d = parent
    todo = sorted(set(files) | set(dirs) | {""}, key=lambda x: (-x.count("/") - (1 if x else 0), x))
    built = {}
    p = subprocess.Popen(git_argv(repo, ["mktree", "--batch", "-z"]), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    try:
        for d in todo:
            base_e = view.entry(d, base_tree)
            entries = dict(view.tree_entries(base_e[1])) if base_e and base_e[0] == "40000" else {}
            for name, data in files.get(d, {}).items():
                if data is None:
                    entries.pop(name, None)
                else:
                    mode = entries[name][0] if name in entries and entries[name][0] != "40000" else "100644"
                    entries[name] = (mode, write_blob(repo, data))
            for sub in dirs.get(d, ()):
                key = (d + "/" + sub) if d else sub
                if built.get(key) is None:
                    entries.pop(sub, None)
                else:
                    entries[sub] = ("40000", built[key])
            if not entries:
                built[d] = None
                continue
            rec = b"".join(("%s %s %s\t" % (m, "tree" if m == "40000" else ("commit" if m == "160000" else "blob"), o)).encode()
                           + n.encode("utf-8", "surrogateescape") + b"\0" for n, (m, o) in sorted(entries.items()))
            p.stdin.write(rec + b"\0")
            p.stdin.flush()
            line = p.stdout.readline().strip().decode()
            if not re.match(r"^[0-9a-f]{40,64}$", line):
                raise Fail("git mktree gave no tree id for %s: %s" % (d or "the root", p.stderr.read(400).decode("utf-8", "replace")), 3)
            built[d] = line
    finally:
        try:
            p.stdin.close()
        except OSError:
            pass
        p.wait()
    if built.get("") is None:
        raise Fail("the change set would leave the tree empty", 1)
    return built[""], kept


# commit_on tries update-ref this many times, 0.2 s apart, while the ref still holds the expected commit; a ref lock
# older than STALE_LOCK_MIN minutes is left over from a killed git
REF_TRIES = 10
STALE_LOCK_MIN = 10


class RefNotMoved(Fail):
    """update-ref failed and the ref still holds the expected commit: a ref lock (a killed git, a pack-refs of git
    maintenance), not another writer. Nothing was moved, and the same command can run again (G2-06)."""


class RefMoved(Fail):
    """update-ref failed because the ref no longer holds the commit the changes were read from."""


# GitHub closes an issue that a pull request body, or a commit message that reaches the default branch, names right
# after one of these words, with an optional colon: "closes #70", "Fixes: owner/repo#70", "resolved
# https://github.com/o/r/issues/70". A per-topic issue closed that way on the merge of its first run (F-10).
CLOSING_RE = re.compile(r"\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b(\s*:?\s*)((?:[\w.-]+/[\w.-]+)?#(\d+)\b|GH-(\d+)\b|"
                        r"https?://github\.com/[\w.-]+/[\w.-]+/(?:issues|pull)/(\d+))", re.I)


def no_close(text, keep=()):
    """text with every closing keyword taken away from the issue it names ("closes #70" becomes "closes issue #70"),
    so that no merge closes an issue by accident: GitHub closes one only when the reference follows the word. keep:
    the numbers of the issues the text means to close with a bare "#N" (a run's own rq:run issue). Every text the
    harness writes to GitHub or into a commit goes through it, the text it copies from issues and lanes too."""
    if not text:
        return text
    keep = {int(k) for k in keep if k}

    def sub(m):
        if m.group(3).startswith("#") and int(m.group(4)) in keep:
            return m.group(0)
        return "%s%sissue %s" % (m.group(1), m.group(2) or " ", m.group(3))
    return CLOSING_RE.sub(sub, text)


def clean_subject(message):
    """The commit-msg hook that rq merge runs on every commit of a pull request refuses a subject over 100 characters (dash
    counts bytes) or one that ends in a full stop, and a run branch is never rewritten, so every harness commit's
    subject is cut to 100 bytes and loses its trailing full stops and spaces here (G2-04)."""
    first, sep, rest = message.partition("\n")
    first = " ".join(first.split()).encode("utf-8")[:100].decode("utf-8", "ignore").rstrip(" .")
    return (first or "rq: a change") + sep + rest


def commit_on(repo, ref, old, changes, message, extra_parents=(), base_tree=None, ref_old=None, view=None):
    """Write `changes` on top of commit `old` (the commit they were computed from) and move `ref` there with a
    compare-and-set. base = base_tree or old's tree. When nothing changes and there is no extra parent, no commit is
    made and `old` is returned. `git diff-tree` between the base and the new tree must list exactly the changed paths,
    else the ref is not moved (a defect of the tree writer). ref_old="" makes a ref that must not exist yet. -> the
    new commit."""
    v = view if view is not None else TreeView(repo, old)
    got = v.cat.get(old)
    old_tree = got[1].split(b"\n", 1)[0].split()[1].decode()
    base = base_tree or old_tree
    tree, kept = write_tree(repo, v, base, changes)
    if tree == old_tree and not extra_parents and ref_old is None:
        return old
    args = ["commit-tree", tree, "-p", old]
    for p in extra_parents:
        args += ["-p", p]
    message = clean_subject(no_close(message))
    if ref.startswith("refs/heads/rq/") and ref[len("refs/heads/rq/"):] not in message:
        # the subject carries a short run id; the body carries the whole one, so `git log --grep RUN` finds every
        # commit of the run (W2-16)
        message = message.rstrip("\n") + "\n\nrun " + ref[len("refs/heads/rq/"):] + "\n"
    new = git_bytes(repo, *args, "-F", "-", input=message.encode("utf-8")).decode().strip()
    listed = set(x for x in git_bytes(repo, "diff-tree", "-r", "-z", "--no-renames", "--name-only", base, tree)
                 .decode("utf-8", "surrogateescape").split("\0") if x)
    if listed != set(kept):
        raise Fail("internal: the new tree changes %s, not the %d path(s) of the change set; %s was not moved"
                   % (", ".join(sorted(listed ^ set(kept))[:6]), len(kept), ref), 1)
    expect = old if ref_old is None else ref_old
    for attempt in range(REF_TRIES):
        rc, out, err = git_run(repo, "update-ref", "-m", message.split("\n", 1)[0][:200], ref, new, expect)
        if rc == 0:
            return new
        if ref_old == "":
            raise Fail("%s exists already: %s" % (ref, err.strip()[:200]), 1)
        now_at = rev(repo, ref) or ""
        if now_at == new:
            # the update-ref wrote the ref and then reported an error (a lock it could not delete): the commit of this
            # call is on the branch, so it is not a lost race (G7-07)
            return new
        if now_at != expect:
            break
        # the ref still holds the expected commit: its lock is held for a moment (a pack-refs, another update-ref of
        # the same ref), and the next try usually gets it (G6-04)
        if attempt + 1 < REF_TRIES:
            time.sleep(0.2)  # wait: lock, held by another git for a moment
    name = ref.replace("refs/heads/", "")
    if (rev(repo, ref) or "") == expect:
        m = re.search(r"'([^']+\.lock)'", err or "")
        lockf = m.group(1) if m else os.path.join(repo, ".git", *ref.split("/")) + ".lock"
        try:
            age = "%d s old" % (time.time() - os.path.getmtime(lockf))
        except OSError:
            age = "gone now"
        raise RefNotMoved("%s did not move: its lock file %s exists (%s) and stayed for %d tries. Run the same command "
                          "again. Delete the lock file only when it is older than %d minutes: no git command holds a ref "
                          "lock that long, and deleting a lock that a running git holds can lose an update (git: %s)"
                          % (name, lockf, age, REF_TRIES, STALE_LOCK_MIN, err.strip()[:200]), 1)
    raise RefMoved("%s moved under this command (%s); run it again" % (name, err.strip()[:200]), 1)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def module_from_source(name, source, filename):
    """A module executed from text (a file read from a commit), with no file written and no process started."""
    import types
    mod = types.ModuleType(name)
    mod.__file__ = filename
    code = compile(source, filename, "exec")
    exec(code, mod.__dict__)
    return mod


_FR = {}


def fr():
    """The fr module: its writer keeps untouched bytes, validates against the schema and owns the clock."""
    if "m" not in _FR:
        _FR["m"] = load_module("rq_fr", os.path.join(REPO, "scripts", "fshy", "fr.py"))
    return _FR["m"]


_VAL = {}


def validator_of(view):
    """(validate module, schema) from a commit: a run whose base has a newer schema than the checkout's HEAD validates
    against its own schema. Cached by the blob ids of the two files."""
    vs = view.entry("scripts/dossier/validate.py")
    ss = view.entry("scripts/dossier/schema.json")
    if not vs or not ss:
        return fr().load_validate(REPO)
    key = (vs[1], ss[1])
    if key not in _VAL:
        mod = module_from_source("rq_validate_%s" % vs[1][:12], view.blob(vs[1]).decode("utf-8"),
                                 "<%s:scripts/dossier/validate.py>" % view.commit[:12])
        _VAL[key] = (mod, json.loads(view.blob(ss[1]).decode("utf-8")))
    return _VAL[key]


def validate_in(view, rec):
    mod, schema = validator_of(view)
    v = mod.Validator(schema)
    v.validate(rec)
    return v.errors


_FSHY = {}


def fshy(name):
    """A module of scripts/fshy (entity, project, derive)."""
    if name not in _FSHY:
        d = os.path.join(REPO, "scripts", "fshy")
        if d not in sys.path:
            sys.path.insert(0, d)
        _FSHY[name] = __import__(name)
    return _FSHY[name]


# ---------------------------------------------------------------------------------------------- text

_PUNCT = {ord(c): " " for c in "\"'`*_#|>~[](){}<>:;,!?‘’“”«»「」『』"}


def norm_text(s):
    """Case, width, entity, link and punctuation folding used for quote matching (measured: 0 false accepts)."""
    s = html.unescape(s or "")
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("–", "-").replace("—", "-").replace("−", "-").replace(" ", " ").replace("​", "")
    s = s.casefold()
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = s.translate(_PUNCT)
    return re.sub(r"\s+", " ", s).strip()


def quote_found(quote, capture_text):
    """-> (verdict, score). verdict: exact | fragments | fuzzy | miss. Fuzzy needs >= 0.9 of tokens in order."""
    import difflib
    q = norm_text(quote)
    if len(q) < 3:
        return "miss", 0.0
    hay = norm_text(capture_text)
    if q in hay:
        return "exact", 1.0
    frags = [norm_text(x) for x in re.split(r"\.\.\.|…|\[\s*\.\.\.\s*\]", quote)]
    frags = [f for f in frags if len(f) >= 3]
    if len(frags) >= 2 and all(f in hay for f in frags):
        return "fragments", 1.0
    qt, ht = q.split(), hay.split()
    if len(qt) < 4:
        return "miss", 0.0
    sm = difflib.SequenceMatcher(None, qt, ht, autojunk=False)
    got = sum(b.size for b in sm.get_matching_blocks()) / len(qt)
    return ("fuzzy", got) if got >= 0.9 else ("miss", got)


_ISO = re.compile(r"\b\d{4}-\d{2}-\d{2}(?:T[\d:.]+Z?)?\b")
_NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:[,  ]\d{3})+(?:\.\d+)?|\d+(?:[.,]\d+)?)(?:\s?(k|thousand|m|million|b|billion)\b)?", re.I)
_MULT = {"k": 1e3, "thousand": 1e3, "m": 1e6, "million": 1e6, "b": 1e9, "billion": 1e9}


def _to_float(raw):
    raw = raw.replace(" ", "").replace(" ", "")
    if re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", raw):
        raw = raw.replace(",", "")
    elif re.fullmatch(r"\d+,\d{1,2}", raw):
        raw = raw.replace(",", ".")
    else:
        raw = raw.replace(",", "")
    return float(raw)


def numbers(s, lenient=False):
    """Numeric values in text, ISO dates removed. lenient adds unscaled variants (the capture side)."""
    s = _ISO.sub(" ", s or "")
    out = set()
    for m in _NUM.finditer(s):
        try:
            v = _to_float(m.group(1))
        except ValueError:
            continue
        sfx = m.group(2)
        if sfx:
            out.add(v * _MULT[sfx.lower()])
            if lenient:
                out.add(v)
        else:
            out.add(v)
    return out


def claim_numbers(s):
    """Numbers a claim asserts: ISO dates and bare years removed, values below 2 ignored (ordinals, '1 account')."""
    vals = set()
    s2 = _ISO.sub(" ", s or "")
    for m in _NUM.finditer(s2):
        raw = m.group(1)
        if re.fullmatch(r"(19|20)\d{2}", raw) and not m.group(2):
            continue
        try:
            v = _to_float(raw)
        except ValueError:
            continue
        if m.group(2):
            v *= _MULT[m.group(2).lower()]
        if v >= 2:
            vals.add(v)
    return vals


def missing_numbers(claim, *sources):
    have = set()
    for s in sources:
        have |= numbers(s, lenient=True)
    return sorted(v for v in claim_numbers(claim) if not any(abs(v - h) <= 0.005 * max(abs(h), 1e-9) for h in have))


def norm_url(u):
    p = urlsplit((u or "").strip())
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host + p.path.rstrip("/") + (("?" + p.query) if p.query else "")


def psl():
    if "_psl" not in _FSHY:
        _FSHY["_psl"] = fshy("entity").PSL()
    return _FSHY["_psl"]


def domain_of(url):
    h = urlsplit(url or "").netloc.lower().split("@")[-1].split(":")[0]
    if h.startswith("www."):
        h = h[4:]
    return psl().registrable(h) if h else None


def core_name(p):
    return fshy("entity").core_name(p)


# a tier value that names no tier: a placeholder or a status, not the vendor's label of a plan
NO_TIER = {"", "none", "n a", "na", "unknown", "unverified", "not stated", "unstated", "dead", "closed", "tbd"}
TIER_FILLER = re.compile(r"\b(?:tier|tiers|plan|plans)\b")


def tier_key(tier):
    """The tier of a record as a comparison key: casefolded, every run of whitespace and punctuation one space, the
    words tier and plan left out ('Free plan' is 'free'). A placeholder ('none', 'n/a', 'unknown') is no tier: ''."""
    if not isinstance(tier, str):
        return ""
    k = " ".join(TIER_FILLER.sub(" ", re.sub(r"[\W_]+", " ", tier.casefold())).split())
    return "" if k in NO_TIER else k


def other_tier(a, b):
    """True when both sides name a tier and the tiers differ. The schema's `tier`: a provider with two materially
    different tiers is two records, so two such drafts or records are two offers, whatever their name, domain and pages
    share. A missing tier on either side decides nothing."""
    ka, kb = tier_key(a), tier_key(b)
    return bool(ka and kb and ka != kb)


# ---------------------------------------------------------------------------------------------- captures

def capture_rel(sha):
    h = sha.split(":", 1)[1]
    return "sources/c/%s/%s.md.gz" % (h[:2], h), "sources/c/%s/%s.json" % (h[:2], h)


def probe_rel(sha, ext=".json"):
    """sources/p/<aa>/<sha><ext>.gz and its sidecar <sha>.json: a probe record that a `measured` claim cites,
    registered with `rq capture --probe` and copied here by the integrator (or by fr with --capture). The name is
    the sha256 of the record's text, as for every file of sources/p/; a file there with no sidecar has a row in
    sources/MANIFEST.tsv instead."""
    h = sha.split(":", 1)[1]
    return "sources/p/%s/%s%s.gz" % (h[:2], h, ext), "sources/p/%s/%s.json" % (h[:2], h)


def capture_store(repo=REPO):
    return os.path.join(repo, "sources", "c")


def capture_paths(sha, repo=REPO):
    return tuple(os.path.join(repo, *r.split("/")) for r in capture_rel(sha))


def probe_dir(sha, repo=REPO):
    return os.path.join(repo, "sources", "p", sha.split(":", 1)[1][:2])


def probe_paths(sha, repo=REPO, ext=".json"):
    return tuple(os.path.join(repo, *r.split("/")) for r in probe_rel(sha, ext))


class DiskReader:
    """The working tree as a reader with the interface of TreeView and Overlay (read, exists)."""

    def __init__(self, repo):
        self.repo = repo

    def read(self, rel):
        p = os.path.join(self.repo, *rel.split("/"))
        if not os.path.isfile(p):
            return None
        with open(p, "rb") as f:
            return f.read()

    def exists(self, rel):
        return os.path.exists(os.path.join(self.repo, *rel.split("/")))


_LIVE = {}


def live_runs(repo=REPO, fresh=False):
    """The ids of the runs of this checkout that are not done, from one `for-each-ref` per command: their branches may
    hold captures that the working tree does not have yet. fresh=True reads them again."""
    if fresh or repo not in _LIVE:
        out = git(repo, "for-each-ref", "--format=%(refname)", "refs/heads/rq/", check=False)
        runs = []
        for ln in out.splitlines():
            run = ln.strip()[len("refs/heads/rq/"):]
            try:
                r = read_json(os.path.join(run_dir(run, repo), "run.json"), None)
            except Fail:
                r = None
            if isinstance(r, dict) and r.get("phase") not in DONE_PHASES:
                runs.append(run)
        _LIVE[repo] = runs
    return _LIVE[repo]


def _readers(repo, view=None):
    out = []
    if view is not None:
        out.append(view)
    out.append(DiskReader(repo))
    for run in live_runs(repo):
        try:
            out.append(_RunReader(repo, run))
        except Fail:
            pass
    return out


def run_or_ref_tree(repo, name):
    """A run id, rq/RUN, a ref or a commit -> (TreeView, run id or None): the run branch of this clone, else origin's
    (fetched once when this clone lacks it), else the name as a commit. A merge session in its own clone reads a run
    it did not run this way (W-03)."""
    run = name[3:] if name.startswith("rq/") else name
    cands = ["refs/heads/rq/" + run, "refs/remotes/%s/rq/%s" % (REMOTE, run)]
    # each name is resolved once and the view is made from the commit, not from the name again (LIO7-03)
    for c in cands:
        got = rev(repo, c)
        if got:
            return TreeView(repo, got), run
    got = rev(repo, name)
    if got:
        return TreeView(repo, got), None
    if re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]*$", run) and has_remote(repo):
        fetch(repo, [run_refspec(run)])
        got = rev(repo, cands[1])
        if got:
            return TreeView(repo, got), run
    raise Fail("no run branch rq/%s here or on %s, and no commit %s" % (run, REMOTE, name), 2)


class _RunReader:
    def __init__(self, repo, run):
        self.repo, self.ref = repo, "refs/heads/rq/" + run

    def read(self, rel):
        got = catfile(self.repo).get("%s:%s" % (self.ref, rel))
        return got[1] if got and got[0] == "blob" else None

    def exists(self, rel):
        return self.read(rel) is not None


def _probe_hit_in(reader, sha):
    """A probe record that a run stored: <sha>.json.gz or <sha>.txt.gz with a <sha>.json sidecar of kind probe.
    The other files of sources/p/ (page snapshots, process output with a MANIFEST.tsv row) are not probe records.
    -> the relative path of the .gz, or None."""
    meta_rel = probe_rel(sha)[1]
    raw = reader.read(meta_rel)
    try:
        meta = json.loads(raw.decode("utf-8")) if raw else None
    except ValueError:
        meta = None
    if not isinstance(meta, dict) or meta.get("kind") != "probe":
        return None
    for ext in (".json", ".txt"):
        rel = probe_rel(sha, ext)[0]
        if reader.exists(rel):
            return rel
    return None


def _stored(sha, repo, view=None):
    """The durable copy of a capture or a probe record: on the run branch a caller reads (view), in the working tree,
    or on the branch of a live run that has integrated it and not landed yet (content-addressed, so any copy is the
    same text). -> (reader, relative path, kind) or None."""
    for rd in _readers(repo, view):
        rel = capture_rel(sha)[0]
        if rd.exists(rel):
            return rd, rel, "page"
        hit = _probe_hit_in(rd, sha)
        if hit:
            return rd, hit, "probe"
    return None


def probe_targets(sha, repo=REPO, lane_dir=None, view=None):
    """The probe: URLs a probe record was registered for (its sidecar), from the lane or the durable stores."""
    h = sha.split(":", 1)[1]
    if lane_dir:
        info = read_json(os.path.join(lane_dir, "captures", h + ".json"), None) \
            if os.path.isfile(os.path.join(lane_dir, "captures", h + ".json")) else None
        if isinstance(info, dict) and info.get("kind") == "probe":
            return list(info.get("targets") or ([info["url"]] if info.get("url") else []))
    for rd in _readers(repo, view):
        raw = rd.read(probe_rel(sha)[1])
        try:
            info = json.loads(raw.decode("utf-8")) if raw else None
        except ValueError:
            info = None
        if isinstance(info, dict) and info.get("kind") == "probe":
            return list(info.get("targets") or ([info["url"]] if info.get("url") else []))
    return []


def capture_kind(sha, repo=REPO, lane_dir=None, view=None):
    """page (a page text) or probe (a probe record) for a capture hash; None when no copy exists."""
    if not SHA_RE.match(sha or ""):
        return None
    h = sha.split(":", 1)[1]
    if lane_dir and os.path.exists(os.path.join(lane_dir, "captures", h + ".md")):
        meta = read_json(os.path.join(lane_dir, "captures", h + ".json"), {}) or {}
        return "probe" if meta.get("kind") == "probe" else "page"
    got = _stored(sha, repo, view)
    return got[2] if got else None


def read_capture(sha, repo=REPO, lane_dir=None, view=None):
    """Capture text by hash: the lane's own captures first, then the durable stores (sources/c/, sources/p/) of the
    view, the working tree and the live run branches."""
    if not SHA_RE.match(sha or ""):
        return None
    h = sha.split(":", 1)[1]
    if lane_dir:
        p = os.path.join(lane_dir, "captures", h + ".md")
        if os.path.exists(p):
            with open(p, encoding="utf-8", newline="") as f:
                text = f.read()
            # a file whose text is not its name is no capture: an edit after the registration changed it
            return text if sha256_text(text) == sha else None
    got = _stored(sha, repo, view)
    if got:
        return gzip.decompress(got[0].read(got[1])).decode("utf-8")
    return None


def promote_files(sha, lane_dir, overlay):
    """The files that copy a lane capture into sources/c/, or a probe record into sources/p/, on a run branch
    (content-addressed: two runs that store one page write the same body and each its own sidecar, with the url and
    fetched_at of its read; land and merge take main's sidecar, land.SIDECAR_RE).
    -> (relative path, {path: bytes}); ({}, when the branch holds it already), or (None, {}) when the lane lacks it."""
    h = sha.split(":", 1)[1]
    m = os.path.join(lane_dir, "captures", h + ".json")
    info = read_json(m, {}) if os.path.exists(m) else {}
    have = capture_rel(sha)[0]
    if overlay.exists(have):
        return have, {}
    hit = _probe_hit_in(overlay, sha)
    if hit:
        return hit, {}
    src = os.path.join(lane_dir, "captures", h + ".md")
    if not os.path.exists(src):
        return None, {}
    with open(src, encoding="utf-8", newline="") as f:
        text = f.read()
    if sha256_text(text) != sha:
        raise Fail("capture %s does not hash to its name" % sha)
    if info.get("kind") == "probe":
        gz, meta = probe_rel(sha, ".json" if info.get("format") == "json" else ".txt")
    else:
        gz, meta = capture_rel(sha)
    info["sha256"] = sha
    info["bytes"] = len(text.encode("utf-8"))
    return gz, {gz: gzip.compress(text.encode("utf-8"), 9, mtime=0), meta: json_bytes(info)}


def promote_capture(sha, lane_dir, repo):
    """The working-tree form of promote_files, for a hand change with scripts/fr in an own clone (never in the
    research checkout, where fr's writes refuse). -> the relative path or None when absent."""
    rel, files = promote_files(sha, lane_dir, DiskReader(repo))
    for p, data in files.items():
        full = os.path.join(repo, *p.split("/"))
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as f:
            f.write(data)
    return rel
