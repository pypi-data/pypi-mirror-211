#!/usr/bin/env python3

"""
Skulk.

A tool to help get your repo in good shape before pushing.

It works for packages intended for PyPi.

It has 2 public functions:

1. main() : A wizard that guides you to choosing a version that does not conflict with any git tags
   or PyPi versions.

If no pre-push hook exists in the repo, skulk will prompt and help to make one.

2. run_pre_push_checks() : A function that is designed to be called from a git pre-push hook.

Assumptions: 1. You have a file named VERSION at the top level of the repo. It should contain a
simple semver such as 1.2.3 2. You have a CHANGELOG.md  at the top level of the repo.


WIZARD MESSAGES:

1. Nothing will happen until the end. You can exit at any time.
2. Do you want to simply push your code(0), deploy a pre-release(1), or deploy a release(2)?
3. If pre-release(1) or release(2):
    a. You'll be shown the current version and the latest version on PyPi.
    b. You'll be asked to choose a new version from the options.


"""

from __future__ import print_function
from builtins import input
import datetime
import os
import sys
from . import util
from .bumper import Bumper


class Skulk(object):
    """A wizard to guide the user to a good version and changelog."""

    def __init__(self):
        self.repo = util.get_repo()
        self.branch = self.repo.active_branch
        self.branch_name = self.branch.name
        self.working_dir = self.repo.working_dir
        self.hook_filename = os.path.join(self.working_dir, ".git", "hooks", "pre-push")
        self.changelog_filename = os.path.join(self.working_dir, "CHANGELOG.md")
        self.version_filename = os.path.join(self.working_dir, "VERSION")
        self.pip_name = util.get_pip_name(self.repo)
        self.bumper = None
        self.edit_changelog = False
        self.changelog_addition = None

    def run(self):
        """
        Guide the user to ensure version and changelog are valid.
        """

        # wizard.check_pre_push_hook()
        self.check_clean()
        self.bumper = Bumper(self.repo, self.pip_name)
        if self.ask_do_tag_release():
            self.bumper.run()

        self.ask_changelog_additions()

        # Now we do the actual work.
        # CHANGELOG
        if self.edit_changelog:
            self.resolve_changelog()
 
        next_version = self.bumper.next_version
        if next_version:
            # VERSION FILE
            with open(self.version_filename, "w", encoding="utf-8") as vf:
                vf.write(next_version)

            # COMMIT CHANGES
            if self.repo.is_dirty():
                self.repo.index.add([self.changelog_filename, self.version_filename])
                self.repo.index.commit(
                    f"Update changelog and sets version to {next_version}"
                )
                print("Committed Version and Changelog\n")

        elif self.edit_changelog:
            # COMMIT CHANGES
            if self.repo.is_dirty():
                self.repo.index.add([self.changelog_filename])
                self.repo.index.commit("Update changelog")
                print("Committed Changelog\n")

        # GIT TAG

        origin = self.repo.remote("origin")
        if next_version:
            label = "Pre-release" if self.bumper.is_prerelease() else "Release"
            tag = self.repo.create_tag(next_version, message=f"{label}: {next_version}")

            # PUSH
            do_push = util.yes_no(
                f"Do you want me to push the branch and tag: {self.branch_name} + {tag.name}` for you?"
            )

            if do_push:
                origin.push(self.branch)
                origin.push(tag)
                print("Pushed branch and tag.\n")
            else:
                print(
                    "No worries. Use the following command to push the branch and tag later. Bye\n"
                )
                print(f"git push --atomic origin {self.branch_name} {tag.name}")

        else:
            do_push = util.yes_no(
                f"Do you want me to push the branch: {self.branch_name} for you?"
            )
            if do_push:
                origin.push(self.branch)
                print("Pushed branch.\n")
            else:
                print(
                    "No worries. Use the following command to push the branch later. Bye\n"
                )
                print(f"git push origin {self.branch_name}")

        sys.exit(0)

    def check_clean(self):
        """Check that the repo is clean.

        User can continue with a dirty repo, but we at least want to warn them.
        """
        if not self.repo.is_dirty():
            print("Repo clean. Good to go.")
            return

        mods = [item.a_path for item in self.repo.index.diff(None)]
        untracked = self.repo.untracked_files
        if mods:
            print(util.magenta("Modified files:\n{}".format("\n".join(mods))))
        if untracked:
            print(util.magenta("Untracked files:\n{}".format("\n".join(untracked))))

        print(
            "----------\nAttention: Repo is dirty. Uncommitted changes won't be included. Is this ok?"
        )
        print("If you want to include them, please commit them now.")
        cont = input(
            util.green(
                "When you are happy, press enter to continue or type 'exit' to exit."
            )
        )
        if cont == "exit":
            sys.stderr.write("Exited.\n")
            sys.exit(0)

    def ask_do_tag_release(self):
        """Ask the user if he wants to make a pre-release from this branch."""
        return util.yes_no(
            "Do you want to tag and deploy from this branch?",
            "No, push only",
            "Yes, push and deploy a taged release.",
        )

    def ask_changelog_additions(self):
        """Generate the reference additions to the changelog.

        Do not write anything to the changelog file yet."""
        block = ""
        write_block = self.bumper.next_version or self.changelog_needs_unreleased_stub()
        if self.bumper.next_version:
            self.edit_changelog = True
            date_string = datetime.date.today().strftime("%d %b %Y")
            block = f"## Version:{self.bumper.next_version} -- {date_string}\n\n"
        else:
            self.edit_changelog = util.yes_no(
                "No version bump. Do you want to add entries in the changelog anyway?"
            )
            block = "## Unreleased\n\n"
        sections = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]
        block += "\n".join([f"### {s}\n" for s in sections])

        if self.edit_changelog:
            commits = self.get_commits()
            commit_messages = ["\n# Raw commit messages for reference.\n"]
            commit_messages.extend([f"* {c.summary} [{c.hexsha[:7]}]" for c in commits])
            commit_block = "\n".join(commit_messages) or ""

            print(commit_block)

            self.changelog_addition = commit_block
            if write_block:
                self.changelog_addition = commit_block + "\n\n" + block

    def resolve_changelog(self):
        """Help the user to get the changelog file up-to-date."""
        with open(self.changelog_filename, "r", encoding="utf-8") as clog:
            content = clog.read() or "--"

        content = self.changelog_addition + "\n\n" + content

        with open(self.changelog_filename, "w", encoding="utf-8") as clog:
            clog.write(content)

        print("Resolve CHANGELOG:")
        print("Edit and save the changelog now.")

        input(
            util.green(
                "Please EDIT and SAVE your CHANGELOG (There's no need to commit), then press enter to continue."
            )
        )

    def changelog_needs_unreleased_stub(self):
        with open(self.changelog_filename, "r", encoding="utf-8") as f:
            datafile = f.readlines()

        for line in datafile:
            if line.startswith("## Unreleased"):
                return False
            elif line.startswith("## Version"):
                return True
        return True

    # PRIVATE

    def get_commits(self):
        """Get commits that are on the active branch but not on the master branch."""
        result = []
        master_shas = set(
            [c.hexsha for c in self.repo.iter_commits(rev=self.repo.branches.master)]
        )
        for commit in self.repo.iter_commits(rev=self.branch):
            if commit.hexsha in master_shas:
                continue
            result.append(commit)
        return result

def main():
    """Run the wizard."""
    wizard = Skulk()
    wizard.run()


if __name__ == "__main__":
    main()
