#!/usr/bin/env python
"""Automation script for making a release. Must be run from the root for the
repository"""
# Note: Version scheme according to https://www.python.org/dev/peps/pep-0440
import datetime
import json
import os
import re
import shutil
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from subprocess import DEVNULL, CalledProcessError, run

import click
import git
import pytest
from packaging.version import parse as parse_version


RX_VERSION = re.compile(
    r'^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'
    r'(?P<prepost>\.post\d+|-(dev|a|b|rc)\d+)?'
    r'(?P<devsuffix>[+-]dev)?$'
)


def make_release(package_name):
    """Interactively create and publish a new release for the package"""
    click.confirm("Do you want to make a release?", abort=True)
    check_git_clean()
    new_version = ask_for_release_version(package_name)
    set_version('pyproject.toml', new_version)
    edit_changelog(new_version)
    while not check_dist():
        click.confirm(
            "Fix errors manually! Continue?", default=True, abort=True
        )
    make_release_commit(new_version)
{%- if cookiecutter.sphinx_docs == 'y' %}
    check_docs()
{%- endif %}
    run_tests()
    push_release_commit()
    make_upload(test=True)
    make_upload(test=False)
    make_and_push_tag(new_version)
    next_dev_version = new_version + '+dev'
    set_version('pyproject.toml', next_dev_version)
    add_unreleased_heading()
    make_next_dev_version_commit(next_dev_version)


###############################################################################


class ReleaseError(ValueError):
    pass


def get_package_name():
    """Find and return the package name from src"""
    for name in os.listdir('src'):
        if 'egg-info' in name:
            continue
        if os.path.isdir(os.path.join('src', name)):
            return name
    raise ReleaseError("Cannot find package name")


def get_pypi_versions(package_name):
    """Return list of versions for the given package on PyPI"""
    url = "https://pypi.python.org/pypi/%s/json" % (package_name,)
    data = json.load(urllib.request.urlopen(urllib.request.Request(url)))
    versions = list(data["releases"].keys())
    versions.sort(key=parse_version)
    return versions


def get_local_versions():
    """Return list of versions based on local tags

    For every version, there must be a tag "v<version>"
    """
    repo = git.Repo(os.getcwd())
    return [tag.name[1:] for tag in repo.tags if tag.name.startswith('v')]


def get_version(filename):
    """Extract the package version, as a str"""
    with open(filename) as in_fh:
        for line in in_fh:
            if line.startswith('version'):
                return line.split('=')[1].strip()[1:-1]
    raise ReleaseError("Cannot extract version from %s" % filename)


def edit(filename):
    """Open filename in EDITOR."""
    editor = os.getenv('EDITOR', 'vi')
    if click.confirm("Open %s in %s?" % (filename, editor), default=True):
        run([editor, filename])


def check_git_clean():
    """Ensure that a given git.Repo is clean."""
    repo = git.Repo(os.getcwd())
    if repo.is_dirty():
        run(['git', 'status'])
        raise ReleaseError("Repository must be in a clean state")
    if repo.untracked_files:
        click.echo("WARNING: there are untracked files:")
        for filename in repo.untracked_files:
            click.echo("\t%s" % filename)
        click.confirm("Continue?", default=False, abort=True)


def run_tests():
    """Run 'make test'."""
    success = False
    while not success:
        try:
            run(['make', 'test'], check=True)
        except CalledProcessError as exc_info:
            print("Failed tests: %s\n" % exc_info)
            print("Fix the tests and ammend the release commit.")
            print("Then continue.\n")
            click.confirm("Continue?", default=True, abort=True)
        else:
            success = True


def split_version(version, base=True):
    """Split `version` into a tuple

    If `base` is True, only return (<major>, <minor>, <patch>) as a tuple of
    ints, stripping out pre/post/dev release tags. Otherwise, the are included
    as a possible fourth and fifth element in the tuple (as strings)
    """
    version = str(version)
    if not RX_VERSION.match(version):
        raise ValueError("Invalid version: %s" % version)
    if base:
        return tuple(
            [
                int(v)
                for v in str(parse_version(version).base_version).split(".")
            ]
        )
    else:
        m = RX_VERSION.match(version)
        if m:
            res = [
                int(m.group('major')),
                int(m.group('minor')),
                int(m.group('patch')),
            ]
            if m.group('prepost') is not None:
                res.append(m.group('prepost'))
            if m.group('devsuffix') is not None:
                res.append(m.group('devsuffix'))
            return tuple(res)
        else:
            raise ValueError("Invalid version string: %s" % version)


def list_versions(package_name):
    """List previously released versions

    This prints each released version on a new line, and returns the list of
    all released versions (based on PyPI and local tags)
    """
    try:
        pypi_versions = get_pypi_versions(package_name)
    except OSError:
        click.echo("PyPI versions no available")
        pypi_versions = []
    local_versions = get_local_versions()
    normalized_local_versions = set(
        [str(parse_version(v)) for v in local_versions]
    )
    versions = local_versions.copy()
    for version in pypi_versions:
        if version not in normalized_local_versions:
            versions.append(version)
    versions = sorted(versions, key=parse_version)
    for version in versions:
        normalized_version = str(parse_version(version))
        if (
            normalized_version in pypi_versions
            and normalized_version in normalized_local_versions
        ):
            status = 'PyPI/local'
        elif normalized_version in pypi_versions:
            status = 'PyPI only!'
        elif normalized_version in normalized_local_versions:
            status = 'local only!'
        click.echo("%-20s %s" % (version, status))
    return versions


def version_ok(version, dev_version, released_versions=None):
    """Check that `version` is a valid version for an upcoming release

    The `version` must be newer than the `dev_version` (from __version__, which
    should end in '-dev' or '+dev')
    """
    if released_versions is None:
        released_versions = []
    m = RX_VERSION.match(version)
    if m:
        if m.group('devsuffix') is not None:
            click.echo("Version %s contains a development suffix" % version)
            return False
        if version in released_versions:
            click.echo("Version %s is already released" % version)
            return False
        if parse_version(version) > parse_version(dev_version):
            return True
        else:
            click.echo("Version %s not newer than %s" % (version, dev_version))
            return False
    else:
        click.echo("Invalid version: %s" % version)
        return False


def propose_next_version(dev_version):
    """Return the most likely release version based on the current
    __version__"""
    dev_version = str(dev_version)
    if parse_version(dev_version).is_prerelease:
        return parse_version(dev_version).base_version
    else:
        base_version = parse_version(dev_version).base_version
        v = split_version(base_version)
        return "%d.%d.%d" % (v[0], v[1], v[2] + 1)


def ask_for_release_version(package_name):
    """Ask for the version number of the release.

    The version number is checked to be a valid next release
    """
    dev_version = get_version('pyproject.toml')
    proposed_version = propose_next_version(dev_version)
    released_versions = list_versions(package_name)
    new_version = click.prompt(
        "What version would you like to release?", default=proposed_version
    )
    while not version_ok(new_version, dev_version, released_versions):
        new_version = click.prompt(
            "What version would you like to release?", default=proposed_version
        )
    click.confirm("Confirm version %s?" % new_version, abort=True)
    return str(new_version)


def set_version(filename, version):
    """Set the package version (in pyproject.toml)"""
    shutil.copyfile(filename, filename + '.bak')
    click.echo("Modifying %s to set version %s" % (filename, version))
    with open(filename + '.bak') as in_fh, open(filename, 'w') as out_fh:
        found_version_line = False
        for line in in_fh:
            if line.startswith('version'):
                found_version_line = True
                line = line.split('=')[0].rstrip() + ' = "' + version + '"\n'
            out_fh.write(line)
    if get_version(filename) == version:
        os.remove(filename + ".bak")
    else:
        # roll back
        shutil.copyfile(filename + ".bak", filename)
        msg = "Failed to set version in %s (restored original)" % filename
        if not found_version_line:
            msg += ". Does not contain a line starting with 'version'."
        raise ReleaseError(msg)


def get_changelog_repo_base(text):
    """Return the ``https://github.com/<owner>/<repo>`` base for the project.

    The base is extracted from the first ``https://github.com`` URL in a
    reference-style link definition of CHANGELOG.md.
    """
    m = re.search(
        r'^\[[^\]]+\]:\s*(https://github\.com/[^/\s]+/[^/\s]+)',
        text,
        re.MULTILINE,
    )
    if m:
        return m.group(1)
    raise ReleaseError(
        "Cannot determine the GitHub repository from CHANGELOG.md links"
    )


def prepare_changelog(version, filename='CHANGELOG.md', today=None):
    """Turn the ``## [Unreleased]`` section into a release section.

    Rename the topmost ``## [Unreleased]`` heading to ``## [v<version>] -
    <YYYY-MM-DD>`` and update the reference-style version links at the bottom
    of the file: point ``[Unreleased]`` at ``…/compare/v<version>..HEAD`` and
    add a ``[v<version>]: …/releases/tag/v<version>`` definition.

    The tagged release commit must not contain an ``## [Unreleased]`` section,
    so no fresh heading is added here; `add_unreleased_heading` re-opens the
    changelog in the subsequent ``+dev`` version-bump commit.

    This is safe to re-run: if a ``## [v<version>]`` heading already exists,
    the file is left unchanged.
    """
    if today is None:
        today = datetime.date.today().isoformat()
    with open(filename) as in_fh:
        text = in_fh.read()

    version_heading = "## [v%s]" % version
    if version_heading in text:
        click.echo(
            "%s already has a %s section; leaving it unchanged"
            % (filename, version_heading)
        )
        return

    base = get_changelog_repo_base(text)

    # Rename the top '## [Unreleased]' heading to the release heading. The
    # fresh '## [Unreleased]' heading is intentionally *not* added here: the
    # tagged release commit must not contain an '## [Unreleased]' section.
    # `add_unreleased_heading` re-opens the changelog for the '+dev' commit.
    heading_rx = re.compile(r'^##[ \t]+\[Unreleased\][ \t]*$', re.MULTILINE)
    if not heading_rx.search(text):
        raise ReleaseError(
            "%s has no '## [Unreleased]' heading to release" % filename
        )
    text = heading_rx.sub(
        "%s - %s" % (version_heading, today),
        text,
        count=1,
    )

    # Point '[Unreleased]' at the new compare range and add the release link.
    link_rx = re.compile(r'^\[Unreleased\]:.*$', re.MULTILINE)
    if not link_rx.search(text):
        raise ReleaseError(
            "%s has no '[Unreleased]' link definition" % filename
        )
    new_links = (
        "[Unreleased]: %s/compare/v%s..HEAD\n" "[v%s]: %s/releases/tag/v%s"
    ) % (base, version, version, base, version)
    text = link_rx.sub(lambda _: new_links, text, count=1)

    with open(filename, 'w') as out_fh:
        out_fh.write(text)
    click.echo(
        "Updated %s: released [Unreleased] as %s - %s"
        % (filename, version_heading, today)
    )


def add_unreleased_heading(filename='CHANGELOG.md'):
    """Re-open the changelog for the next development cycle.

    Insert a fresh empty ``## [Unreleased]`` heading above the topmost
    ``## [vX.Y.Z]`` release heading. This runs for the ``+dev`` version-bump
    commit, so the just-tagged release commit stays free of an
    ``## [Unreleased]`` section.

    No-op if an ``## [Unreleased]`` heading is already present.
    """
    with open(filename) as in_fh:
        text = in_fh.read()

    if re.search(r'^##[ \t]+\[Unreleased\][ \t]*$', text, re.MULTILINE):
        click.echo(
            "%s already has an '## [Unreleased]' heading; leaving it unchanged"
            % filename
        )
        return

    m = re.search(r'^##[ \t]+\[v[0-9]+\.[0-9]+\.[0-9]+\]', text, re.MULTILINE)
    if not m:
        raise ReleaseError(
            "%s has no '## [vX.Y.Z]' heading to insert '## [Unreleased]' above"
            % filename
        )
    text = text[: m.start()] + "## [Unreleased]\n\n" + text[m.start() :]

    with open(filename, 'w') as out_fh:
        out_fh.write(text)
    click.echo(
        "Re-opened %s with a fresh '## [Unreleased]' heading" % filename
    )


def extract_release_notes(version, filename='CHANGELOG.md'):
    """Return the release notes for a version from CHANGELOG.md.

    Extracts the body of the ``## [v<version>]`` section: everything between
    that heading and the next ``##`` heading (or the reference-link definition
    block at the bottom of the file), with surrounding blank lines stripped.
    """
    with open(filename) as in_fh:
        lines = in_fh.read().splitlines()
    heading_rx = re.compile(r'^##[ \t]+\[v%s\][ \t]' % re.escape(version))
    definition_rx = re.compile(r'^\[[^\]]+\]:')
    start = None
    for i, line in enumerate(lines):
        if heading_rx.match(line):
            start = i + 1
            break
    if start is None:
        raise ReleaseError(
            "No '## [v%s]' section found in %s" % (version, filename)
        )
    body = []
    for line in lines[start:]:
        if line.startswith('## ') or definition_rx.match(line):
            break
        body.append(line)
    notes = '\n'.join(body).strip()
    if not notes:
        raise ReleaseError(
            "The '## [v%s]' section in %s is empty" % (version, filename)
        )
    return notes


def edit_changelog(version):
    """Prepare CHANGELOG.md for the release, then edit it interactively.

    `prepare_changelog` does the mechanical transformation (renaming the
    ``## [Unreleased]`` heading to the release heading and updating the version
    links); the editor is opened afterwards so the release notes can be
    reviewed and refined before the file is validated.
    """
    prepare_changelog(version)
    click.echo(
        "Review and refine the release notes for %s in CHANGELOG.md" % version
    )
    edit('CHANGELOG.md')
    run(['make', 'check-changelog'], check=True)
    click.confirm("Is CHANGELOG.md up to date?", default=True, abort=True)


def check_dist():
    """Quietly make dist and check it. This is mainly to ensure that the README
    and CHANGELOG metadata are well-formed"""
    click.echo("Making and verifying dist and metadata...")
    try:
        run(['make', 'dist'], check=True, stdout=DEVNULL)
        run(['make', 'dist-check'], check=True)
        return True
    except CalledProcessError as exc_info:
        click.echo("ERROR: %s" % str(exc_info))
        return False


def check_docs():
    """Verify the documentation (interactively)"""
    click.echo("Making the documentation....")
    run(['make', 'docs'], check=True, stdout=DEVNULL)
    click.echo(
        "Check documentation in file://"
        + os.getcwd()
        + "/docs/_build/html/index.html"
    )
    click.confirm(
        "Does the documentation look correct?", default=True, abort=True
    )


def make_release_commit(version):
    """Commit Release."""
    click.confirm("Make release commit?", default=True, abort=True)
    run(
        ['git', 'commit', '-a', '-m', "Release %s" % version],
        check=True,
    )


def make_upload(test=True):
    """Upload to PyPI or test.pypi"""
    if test:
        cmd = ['make', 'test-upload']
        url = 'https://test.pypi.org'
    else:
        url = 'https://pypi.org'
        cmd = ['make', 'upload']
    click.confirm(
        "Ready to upload release to %s?" % url, default=True, abort=True
    )
    success = False
    while not success:
        try:
            run(cmd, check=True)
        except CalledProcessError as exc_info:
            click.confirm(
                "Failed to upload: %s. Try again?" % str(exc_info),
                default=True,
                abort=(not test),
            )
            success = False
        else:
            success = True
            click.confirm(
                "Please check release on %s. Continue?" % url,
                default=True,
                abort=True,
            )


def push_release_commit():
    """Push local commits to origin."""
    click.confirm("Push release commit to origin?", default=True, abort=True)
    run(['git', 'push', 'origin', '{{ cookiecutter.main_branch }}'], check=True)
    click.confirm(
        "Please check Continuous Integration success. Continue?",
        default=True,
        abort=True,
    )


def make_and_push_tag(version):
    """Tag the release commit and push that tag to origin.

    The signed, annotated tag's message is built automatically from the
    ``## [v<version>]`` section of CHANGELOG.md (a ``Release <version>`` title
    followed by that section's release notes), so the notes never have to be
    retyped. After the tag is pushed, a matching GitHub release is created from
    the same notes.
    """
    tag = "v%s" % version
    notes = extract_release_notes(version)
    message = "Release %s\n\n%s\n" % (version, notes)
    click.echo("Tag message for %s (from CHANGELOG.md):\n" % tag)
    click.echo(message)
    click.confirm(
        "Create signed tag %s with this message and push to origin?" % tag,
        default=True,
        abort=True,
    )
    fd, msg_file = tempfile.mkstemp(suffix='.md', text=True)
    with os.fdopen(fd, 'w') as fh:
        fh.write(message)
    try:
        try:
            run(['git', 'tag', '-s', '-F', msg_file, tag], check=True)
        except CalledProcessError as exc_info:
            click.echo(
                "Failed to create signed tag '%s': %s" % (tag, str(exc_info))
            )
            click.echo(
                "Please create the signed tag manually (git tag -s %s)" % tag
            )
            click.confirm("Continue with pushing tag to origin?", default=True)
    finally:
        os.remove(msg_file)
    try:
        run(['git', 'push', '--tags', 'origin'], check=True)
    except CalledProcessError as exc_info:
        click.confirm(
            (
                "Failed to push tags: %s. "
                "Please push manually (git push --tags origin). "
                "Continue?"
            )
            % str(exc_info),
            default=True,
        )
    create_github_release(version, notes)


def create_github_release(version, notes):
    """Create a GitHub release for the tag, reusing the CHANGELOG notes.

    Uses the `gh` CLI (which infers the repository from the git remote). If
    `gh` is not installed, prints the URL for creating the release by hand.
    """
    tag = "v%s" % version
    if shutil.which('gh') is None:
        click.echo(
            "The `gh` CLI is not available; create the GitHub release for %s "
            "manually at %s" % (tag, github_release_url(tag))
        )
        return
    if not click.confirm(
        "Create the GitHub release for %s from the CHANGELOG notes?" % tag,
        default=True,
    ):
        return
    fd, notes_file = tempfile.mkstemp(suffix='.md', text=True)
    with os.fdopen(fd, 'w') as fh:
        fh.write(notes + "\n")
    try:
        run(
            [
                'gh',
                'release',
                'create',
                tag,
                '--verify-tag',
                '--title',
                tag,
                '--notes-file',
                notes_file,
            ],
            check=True,
        )
    except CalledProcessError as exc_info:
        click.echo("Failed to create the GitHub release: %s" % str(exc_info))
        click.echo("Create it manually at %s" % github_release_url(tag))
        click.confirm("Continue?", default=True, abort=True)
    finally:
        os.remove(notes_file)


def github_release_url(tag):
    """Return the "new release" URL for `tag`, derived from CHANGELOG.md."""
    try:
        with open('CHANGELOG.md') as in_fh:
            base = get_changelog_repo_base(in_fh.read())
    except (OSError, ReleaseError):
        return "the project's GitHub releases page"
    return "%s/releases/new?tag=%s" % (base, tag)


def make_next_dev_version_commit(version):
    """Commit 'Bump version to xxx'."""
    click.confirm(
        "Make commit for bumping to %s?" % version, default=True, abort=True
    )
    run(
        ['git', 'commit', '-a', '-m', "Bump version to %s" % version],
        check=True,
    )


###############################################################################


# Run the tests below with `uv run pytest -s scripts/release.py`.


def test_list_versions():
    print("")
    versions = list_versions(get_package_name())
    print(versions)
    assert isinstance(versions, list)


def test_split_version():
    # fmt: off
    assert split_version('0.1.0') == (0, 1, 0)
    assert split_version('0.1.0', base=False) == (0, 1, 0)
    assert split_version('0.1.0-dev1', base=True) == (0, 1, 0)
    assert split_version('0.1.0-dev1', base=False) == (0, 1, 0, '-dev1')
    assert split_version('0.1.0.post1', base=True) == (0, 1, 0)
    assert split_version('0.1.0.post1', base=False) == (0, 1, 0, '.post1')
    assert split_version('0.1.0-rc1', base=True) == (0, 1, 0)
    assert split_version('0.1.0-rc1', base=False) == (0, 1, 0, '-rc1')
    assert split_version('0.1.0-rc1-dev', base=True) == (0, 1, 0)
    assert split_version('0.1.0-rc1-dev', base=False) == (0, 1, 0, '-rc1', '-dev')
    assert split_version('0.1.0-rc1+dev', base=True) == (0, 1, 0)
    assert split_version('0.1.0-rc1+dev', base=False) == (0, 1, 0, '-rc1', '+dev')
    assert split_version('0.1.0-dev', base=True) == (0, 1, 0)
    assert split_version('0.1.0-dev', base=False) == (0, 1, 0, '-dev')
    assert split_version('0.1.0+dev', base=True) == (0, 1, 0)
    assert split_version('0.1.0+dev', base=False) == (0, 1, 0, '+dev')
    with pytest.raises(ValueError):
        split_version('0.1.0.rc1')
    with pytest.raises(ValueError):
        split_version('0.1.0rc1')
    with pytest.raises(ValueError):
        split_version('0.1.0.1')
    with pytest.raises(ValueError):
        split_version('0.1')
    with pytest.raises(ValueError):
        split_version('0.1.0+dev1')
    # fmt: on


def test_version_ok():
    assert version_ok('0.1.0', '0.1.0-dev')
    assert version_ok('0.1.0-a1', '0.1.0-dev')
    assert version_ok('0.1.0-b1', '0.1.0-dev')
    assert version_ok('0.1.0-rc1', '0.1.0-dev')
    assert version_ok('0.2.0', '0.1.0+dev')
    assert version_ok('0.2.0-a1', '0.1.0+dev')
    assert version_ok('0.2.0-b1', '0.1.0+dev')
    assert version_ok('0.2.0-rc1', '0.1.0+dev')
    assert version_ok('0.2.0-dev1', '0.1.0+dev')
    assert version_ok('0.1.0.post1', '0.1.0+dev')
    assert version_ok('0.1.0.post1', '0.1.0')
    assert version_ok('0.2.0', '0.1.0')
    assert version_ok('0.2.0', '0.1.0+dev', ['0.1.0', '0.1.0.post1', '0.1.1'])
    print("")
    assert not version_ok('0.0.1-dev', '0.1.0-dev')
    assert not version_ok('0.1.0', '0.1.0')
    assert not version_ok('0.1.0', '0.1.0+dev')
    assert not version_ok('0.1.0+dev', '0.1.0')
    assert not version_ok('0.2.0-dev', '0.1.0+dev')
    assert not version_ok('0.1.0.1', '0.1.0-dev')
    assert not version_ok('0.1.0a1', '0.1.0-dev')
    assert not version_ok('0.1.0b1', '0.1.0-dev')
    assert not version_ok('0.1.0rc1', '0.1.0-dev')
    assert not version_ok('0.1.0dev1', '0.1.0-dev')
    assert not version_ok('0.1.0-post1', '0.1.0+dev')
    assert not version_ok('0.2.0', '0.1.0+dev', ['0.1.0', '0.2.0'])


def test_propose_next_version():
    assert propose_next_version('0.1.0') == '0.1.1'
    assert propose_next_version('0.1.0-dev') == '0.1.0'
    assert propose_next_version('0.1.0-rc1') == '0.1.0'
    assert propose_next_version('0.1.0-rc1+dev') == '0.1.0'
    assert propose_next_version('0.1.0+dev') == '0.1.1'
    assert propose_next_version('0.1.0.post1') == '0.1.1'
    assert propose_next_version('0.1.0.post1+dev') == '0.1.1'


def test_extract_release_notes(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        "# Changelog\n\n"
        "## [Unreleased]\n\n"
        "## [v0.2.0] - 2026-09-01\n\n"
        "* Added: a feature [[#12]]\n"
        "* Fixed: a crash [[#15]]\n\n"
        "## [v0.1.0] - 2026-07-07\n\n"
        "Initial release.\n\n"
        "[Unreleased]: https://github.com/o/r/compare/v0.2.0..HEAD\n"
        "[v0.2.0]: https://github.com/o/r/releases/tag/v0.2.0\n"
        "[v0.1.0]: https://github.com/o/r/releases/tag/v0.1.0\n"
    )
    f = str(changelog)
    # A middle version stops at the next '## ' heading.
    assert extract_release_notes('0.2.0', filename=f) == (
        "* Added: a feature [[#12]]\n* Fixed: a crash [[#15]]"
    )
    # The last version stops at the link-definition block.
    assert extract_release_notes('0.1.0', filename=f) == "Initial release."
    # A missing or empty section is an error.
    with pytest.raises(ReleaseError):
        extract_release_notes('9.9.9', filename=f)


def test_get_changelog_repo_base():
    text = (
        "# Changelog\n\n"
        "[Unreleased]: https://github.com/o/r/compare/v0.1.0..HEAD\n"
        "[v0.1.0]: https://github.com/o/r/releases/tag/v0.1.0\n"
    )
    assert get_changelog_repo_base(text) == "https://github.com/o/r"
    with pytest.raises(ReleaseError):
        get_changelog_repo_base("# Changelog\n\nno links here\n")


CHANGELOG_BEFORE_RELEASE = (
    "# Changelog\n\n"
    "## [Unreleased]\n\n"
    "* Added: a feature [[#12]]\n\n"
    "## [v0.1.0] - 2026-07-07\n\n"
    "Initial release.\n\n"
    "[Unreleased]: https://github.com/o/r/compare/v0.1.0..HEAD\n"
    "[v0.1.0]: https://github.com/o/r/releases/tag/v0.1.0\n"
)


def test_prepare_changelog(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(CHANGELOG_BEFORE_RELEASE)
    f = str(changelog)
    prepare_changelog('0.2.0', filename=f, today='2026-09-01')
    text = changelog.read_text()
    # The '[Unreleased]' heading becomes the release heading; no fresh
    # '[Unreleased]' heading is added yet (that is a separate '+dev' step).
    assert "## [v0.2.0] - 2026-09-01" in text
    assert "## [Unreleased]" not in text
    # The entry is carried over verbatim under the new heading.
    assert "* Added: a feature [[#12]]" in text
    # The version links are updated.
    assert "[Unreleased]: https://github.com/o/r/compare/v0.2.0..HEAD" in text
    assert "[v0.2.0]: https://github.com/o/r/releases/tag/v0.2.0" in text
    assert "[v0.1.0]: https://github.com/o/r/releases/tag/v0.1.0" in text
    # Re-running is a no-op (the '## [v0.2.0]' heading already exists).
    prepare_changelog('0.2.0', filename=f, today='2099-01-01')
    assert changelog.read_text() == text
    # With no '[Unreleased]' heading left, releasing another version errors.
    with pytest.raises(ReleaseError):
        prepare_changelog('0.3.0', filename=f, today='2026-10-01')


def test_add_unreleased_heading(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(CHANGELOG_BEFORE_RELEASE)
    f = str(changelog)
    # A release followed by re-opening round-trips to a valid next-cycle file.
    prepare_changelog('0.2.0', filename=f, today='2026-09-01')
    add_unreleased_heading(filename=f)
    text = changelog.read_text()
    assert "## [Unreleased]\n\n## [v0.2.0] - 2026-09-01" in text
    # Exactly one '## [Unreleased]' heading, above the latest release.
    assert text.count("## [Unreleased]") == 1
    # Idempotent: a heading already present is left untouched.
    add_unreleased_heading(filename=f)
    assert changelog.read_text() == text
    # A file with no version heading cannot be re-opened.
    empty = tmp_path / "EMPTY.md"
    empty.write_text("# Changelog\n\nnothing here\n")
    with pytest.raises(ReleaseError):
        add_unreleased_heading(filename=str(empty))


def test_set_version(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname = "x"\nversion = "0.1.0+dev"\n')
    f = str(pyproject)
    assert get_version(f) == '0.1.0+dev'
    set_version(f, '0.2.0')
    assert get_version(f) == '0.2.0'
    # Other lines are untouched and the '.bak' file is cleaned up on success.
    assert 'name = "x"' in pyproject.read_text()
    assert not (tmp_path / "pyproject.toml.bak").exists()
    # A file without a version line is a ReleaseError (original restored).
    noversion = tmp_path / "noversion.toml"
    noversion.write_text('[project]\nname = "x"\n')
    with pytest.raises(ReleaseError):
        set_version(str(noversion), '0.2.0')
    assert noversion.read_text() == '[project]\nname = "x"\n'


###############################################################################


@click.command(help=__doc__)
@click.help_option('--help', '-h')
def main():
    try:
        make_release(get_package_name())
    except Exception as exc_info:
        click.echo(str(exc_info))
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
