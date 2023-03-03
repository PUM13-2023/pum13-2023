# Contributing to GraphIt

To ensure a smooth workflow contributors should follow these guidelines.

## Table of Contents
- [Branch Structure](#branch-structure)
- [Commit Messages](#commit-messages)
- [Rebasing](#rebasing)
- [Pull Requests](#pull-request)
- [Example](#example)

## Branch Structure
The project uses the Gitflow workflow, meaning there are main, dev, and feature
branches. When adding a new feature branch, a feature branch is created with
`dev` as its source branch. Releases are handled with a release branch, created
from `dev`. After the release is finalized, the release branch is merged with
`main` and a release tag is created.

## Commit Messages
Commit messages begin with a short title, summarizing the changes made. The
title should be capitalized and use the imperative mood. For example, use "fix"
instead of "fixed". The title should not end with a period. For example:
``` 
Fix issue on login page
```

After the title follows a blank line and an explanation on *what* was done,
*why* it was done, and *how*. If the change is very small, all points may not
be needed. It may be useful to use bullet points. Example:
```
Short description in imperative mood

Longer description of changes. This commit fixes issue #31.
+ Add zapinator to transmogrifier.
* Fix light speed drive.
- Remove orcs from dungeon.
```

Commits should not contain *too* many changes. It is difficult to quantify the
right amount, but a guideline might be that one change is one commit. If you do
two things, i.e fix bug in A and add docstring to B, it should be two commits.
If you have done two things in the same file, these can be commited separately
with `git add --patch` or `git add -p`. This lets you interactively choose what
to add. Use `y` to add a hunk, `n` to not add a hunk. For more information see
[git documentation](https://git-scm.com/docs/git-add#_interactive_mode).

Since multiple lines are expected in a commit message, do *not* use
`git commit -m`. Omitting the `-m` flag will open an editor where the commit
message can be edited. The editor that is opened is configured either by
environment variables or git config. In the following examples replace
`<your favorite editor>` with your editor of choice, for example `vim`.

### Bash/zsh
`~/.bashrc` or `~/.zshrc`
```bash
export EDITOR=<your favorite editor>
```

### Git Config
```bash
git config core.editor <your favorite editor>
```

## Rebasing
To ensure a clean git history, a rebase may sometimes be needed. Sometimes
commits are made just to switch to another computer and sometimes commits are
made after running autoformatter or fixing a small issue. These commits do not
contribute to the overall git history and should not be visible in the `dev`
branch. To eliminate such commits there are a few options. Idelly these should
be addressed **before** pushing, since doing so after pushing requires a force
push.

### Using `git commit --amend`
If you fix a small error in your previous commit, use
```bash
git commit --amend
```
to update the previous commit with the fix. This can also be used to address
errors made in the commit message.

## Using `git rebase -i HEAD~<n>`
If you need to edit commits further back in history, use
```bash
git rebase -i HEAD~<n>
```
where n is the number of commits you want to edit. This command lets you edit
history in your editor. Different commands can be applied to commits, such as
`pick` which includes the selected commit in the amended history. This is the
default command. `squash` or `fixup` are used to combine commits that are not
to be included in the history. `fixup` disgards the commit's message, which is
often useful. The interactive rebase view includes a further tutorial.

If you need help with rebasing or git in general, @AxelMatstoms or @YouKnowBlom
may be able to help.

## Pull Requests
Pull requests are a way to ensure code is reviewed by another individual before
it is merged. They are an opportunity to get suggestions for improvements and
fixes. Before submitting a PR, run linter and tests on your machine. Ensure the
changes made are relevant to the PR as a whole. Making irrelevant changes to
code makes git history harder to follow.

The pull request template includes a checklist with common issues found in PRs.

## Example
Example on adding a feature.
Switch to the `dev` branch and ensure you have the latest version.
```bash
git switch dev
git pull
```
Create a new branch from dev, and switch to it.
```bash
git switch -c add-feature
```
Make changes, autoformat, lint and run tests.
```bash
vim src/...

nox -s fmt
nox -t lint
nox -t test
```
Stage changes and commit.
```bash
git add <path-to-changes>
git commit
```
Push to remote.
```bash
git push --set-upstream origin add-feature
```
Alternatively, configure git to auto-setup remote branch.
```bash
git config push.autoSetupRemote true
```

Open a PR, tag related individuals and await review.
