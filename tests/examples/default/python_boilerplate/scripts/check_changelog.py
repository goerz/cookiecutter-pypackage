#!/usr/bin/env python
"""Validate (and optionally fix) the reference-style links in CHANGELOG.md.

The default check mode is purely textual: it makes no network calls and
inspects no git state. It verifies that every reference used in the prose
(e.g. ``[#97]``, ``[v0.8.0]``) has a matching link definition, that no
definition is unused or duplicated, that each version link points to its own
release tag, and that the ``[Unreleased]`` link compares against the latest
version heading in the file (once a first release exists).

The ``--fix`` mode (only) may make network calls: any missing ``[#N]``
issue/pull-request link target is added, consulting the GitHub API to decide
whether ``#N`` is an issue or a pull request and to confirm it exists:

  * If the API confirms ``#N`` exists, the correct ``issues/`` or ``pull/`` URL
    is added.
  * If the API definitively reports that ``#N`` does not exist (HTTP 404),
    it is treated as a typo: no link is added and the reference is reported.
  * If the API cannot be reached (offline, rate-limited), verification is
    skipped and an ``issues/`` URL is added (GitHub redirects ``issues/N`` <->
    ``pull/N``, so it still resolves).

Reading issues/PRs of a public repository requires no special privileges, so
this works for any contributor (including from a fork): it uses the ``gh`` CLI
when available, and otherwise the unauthenticated public API via ``urllib``.

The repository is derived from the existing link definitions, falling back to
the ``origin`` git remote, so the script is not tied to a specific repository.

Run with ``python scripts/check_changelog.py [--fix] [path]`` (no
dependencies), or via ``make check-changelog`` / ``make changelog``. Exits
non-zero on any remaining problem.
"""

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request


DEFINITION = re.compile(r"^\[([^\]]+)\]:[ \t]*(\S+)[ \t]*$")
INLINE_LABEL = re.compile(
    r"\[([^\[\]]+)\]\("
)  # `[text](url)` -- not a reference
REFERENCE = re.compile(r"\[([^\[\]]+)\]")  # innermost `[label]`
VERSION_HEADING = re.compile(r"^##[ \t]+\[(v[0-9]+\.[0-9]+\.[0-9]+)\]")
ISSUE_LABEL = re.compile(r"^#([0-9]+)$")


def parse_changelog(lines):
    """Parse the file into its structural pieces.

    Returns a dict with the link definitions (``defs``: label -> url), the
    order in which labels first appear (``order``), duplicated labels
    (``dups``), the references used in the prose (``used``), and the latest
    version (``latest``: the topmost ``## [vX.Y.Z]`` heading).
    """
    defs = {}
    order = []
    dups = []
    body = []
    for line in lines:
        m = DEFINITION.match(line)
        if m is None:
            body.append(line)
        else:
            label = m.group(1)
            if label in defs:
                dups.append(label)
            else:
                order.append(label)
            defs[label] = m.group(2)
    prose = "\n".join(body)
    inline = set(m.group(1) for m in INLINE_LABEL.finditer(prose))
    used = set(
        m.group(1)
        for m in REFERENCE.finditer(prose)
        if m.group(1) not in inline
    )
    latest = None
    for line in lines:
        m = VERSION_HEADING.match(line)
        if m is not None:
            latest = m.group(1)
            break
    return {
        "defs": defs,
        "order": order,
        "dups": dups,
        "used": used,
        "latest": latest,
    }


def github_base(defs, changelog):
    """Return the ``https://github.com/owner/repo`` base for the project.

    Derived from the existing link definitions, falling back to the ``origin``
    git remote.
    """
    for url in defs.values():
        m = re.match(r"^(https://github\.com/[^/]+/[^/]+)", url)
        if m is not None:
            return m.group(1)
    try:
        out = subprocess.run(
            [
                "git",
                "-C",
                os.path.dirname(changelog) or ".",
                "remote",
                "get-url",
                "origin",
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        out = ""
    m = re.search(r"github\.com[:/](.+?)(?:\.git)?\s*$", out)
    if m is not None:
        return "https://github.com/" + m.group(1).strip()
    raise SystemExit(
        "could not determine the GitHub repository "
        "(no link definitions, no github.com `origin`)"
    )


def classify_gh(slug, n):
    """Classify ``#n`` via the ``gh`` CLI.

    Returns one of ``'pull'``, ``'issue'``, ``'missing'``, ``'network'``, or
    ``'unavailable'`` (gh not installed or not authenticated -- try another
    method).
    """
    jq = 'if has("pull_request") then "pull" else "issue" end'
    try:
        proc = subprocess.run(
            ["gh", "api", "repos/%s/issues/%s" % (slug, n), "--jq", jq],
            capture_output=True,
            text=True,
        )
    except OSError:
        return "unavailable"
    if proc.returncode == 0:
        kind = proc.stdout.strip()
        if kind in ("pull", "issue"):
            return kind
        return "network"
    err = proc.stderr
    if "HTTP 404" in err or "Not Found" in err:
        return "missing"
    if "HTTP 401" in err or re.search(r"auth", err, re.IGNORECASE):
        return "unavailable"
    return "network"


def classify_urllib(slug, n):
    """Classify ``#n`` via the unauthenticated public REST API."""
    url = "https://api.github.com/repos/%s/issues/%s" % (slug, n)
    req = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return "missing"
        return "network"
    except OSError:
        return "network"
    return "pull" if "pull_request" in payload else "issue"


def classify_issue(slug, n):
    """Determine whether ``#n`` is an issue or PR (or missing / unknown)."""
    result = classify_gh(slug, n)
    if result != "unavailable":
        return result
    result = classify_urllib(slug, n)
    return "network" if result == "unavailable" else result


def fix_missing(lines, changelog):
    """Append missing ``[#N]`` link targets.

    Returns ``(modified, problems)``.
    """
    parsed = parse_changelog(lines)
    missing = sorted(
        int(ISSUE_LABEL.match(ref).group(1))
        for ref in parsed["used"]
        if ISSUE_LABEL.match(ref) and ref not in parsed["defs"]
    )
    if not missing:
        return (False, [])

    base = github_base(parsed["defs"], changelog)
    slug = base.replace("https://github.com/", "")
    nonissue = []
    issues = {}
    for label in parsed["order"]:
        m = ISSUE_LABEL.match(label)
        if m is None:
            nonissue.append((label, parsed["defs"][label]))
        else:
            issues[int(m.group(1))] = parsed["defs"][label]

    problems = []
    added = 0
    for n in missing:
        kind = classify_issue(slug, n)
        if kind == "missing":
            problems.append(
                "reference [#%d] does not exist on GitHub (typo?); "
                "no link added" % n
            )
            continue
        issues[n] = (
            "%s/pull/%d" % (base, n)
            if kind == "pull"
            else "%s/issues/%d" % (base, n)
        )
        note = (
            " (could not verify via GitHub; assuming issue)"
            if kind == "network"
            else ""
        )
        print("Added link target [#%d]: %s%s" % (n, issues[n], note))
        added += 1
    if added == 0:
        return (False, problems)

    # Rebuild: prose (trailing blanks trimmed), one blank separator, then all
    # definitions -- non-issue defs in original order, then `#N` defs sorted.
    prose_lines = [line for line in lines if not DEFINITION.match(line)]
    while prose_lines and prose_lines[-1].strip() == "":
        prose_lines.pop()
    out = list(prose_lines)
    out.append("")
    for label, url in nonissue:
        out.append("[%s]: %s" % (label, url))
    for n in sorted(issues):
        out.append("[#%d]: %s" % (n, issues[n]))
    with open(changelog, "w") as fh:
        fh.write("\n".join(out) + "\n")
    return (True, problems)


def validate(lines):
    """Return a list of problems found in the changelog (empty if valid)."""
    parsed = parse_changelog(lines)
    defs = parsed["defs"]
    used = parsed["used"]
    latest = parsed["latest"]
    errors = []

    for u in sorted(used):
        if u not in defs:
            errors.append(
                "reference [%s] is used but has no link definition" % u
            )
    for d in sorted(defs):
        # `[Unreleased]` is structural and may be defined without a
        # corresponding heading (e.g. immediately after a release).
        if d == "Unreleased":
            continue
        if d not in used:
            errors.append("link definition [%s] is never used" % d)
    for d in sorted(set(parsed["dups"])):
        errors.append("link definition [%s] is duplicated" % d)

    # Each version link should point to its own release tag.
    for label, url in defs.items():
        if not label.startswith("v"):
            continue
        if not url.endswith("/releases/tag/%s" % label):
            errors.append(
                "[%s] should point to `…/releases/tag/%s`, not `%s`"
                % (label, label, url)
            )

    # The `[Unreleased]` link should compare the latest version against HEAD.
    if "Unreleased" not in defs:
        errors.append("missing the [Unreleased] link definition")
    elif latest is None:
        # Before the first release there is no version heading to compare
        # against; any `[Unreleased]` link (e.g. `…/commits/main`) is fine.
        pass
    elif not defs["Unreleased"].endswith("/compare/%s..HEAD" % latest):
        errors.append(
            "[Unreleased] should compare against the latest version `%s` "
            "(expected `…/compare/%s..HEAD`), not `%s`"
            % (latest, latest, defs["Unreleased"])
        )

    return errors


def main(argv):
    fix = "--fix" in argv
    positional = [a for a in argv if a != "--fix"]
    changelog = (
        positional[0]
        if positional
        else os.path.join(os.path.dirname(__file__), "..", "CHANGELOG.md")
    )

    if not os.path.isfile(changelog):
        print("Not found: %s" % changelog, file=sys.stderr)
        return 1

    with open(changelog) as fh:
        lines = fh.read().splitlines()

    if fix:
        _, problems = fix_missing(lines, changelog)
        for p in problems:
            print("WARNING: %s" % p, file=sys.stderr)
        with open(changelog) as fh:
            lines = fh.read().splitlines()

    errors = validate(lines)
    if not errors:
        n = sum(1 for line in lines if DEFINITION.match(line))
        print("CHANGELOG.md: OK (%d link definitions)" % n)
        return 0
    print(
        "CHANGELOG.md has %d problem(s):\n  %s"
        % (len(errors), "\n  ".join(errors)),
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
