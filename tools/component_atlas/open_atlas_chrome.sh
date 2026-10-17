#!/usr/bin/env bash
# Run from the existing repository. Only GitHub fetches are used for syncing.
# No reset, clean, force checkout, local model conversion, or ZIP handling.
set -euo pipefail
atlas_branch='visualization/wanfo-component-atlas-v001-20261017'
atlas_repo="$(git rev-parse --show-toplevel)"
atlas_review="$(dirname "$atlas_repo")/万佛殿构件图库-V001"
atlas_remote="refs/remotes/origin/$atlas_branch"
if command -v git-proxy-auto >/dev/null 2>&1; then
  (cd "$atlas_repo" && git-proxy-auto fetch origin "refs/heads/$atlas_branch:$atlas_remote")
else
  git -C "$atlas_repo" fetch origin "refs/heads/$atlas_branch:$atlas_remote"
fi
if [ -d "$atlas_review" ]; then
  test "$(git -C "$atlas_review" rev-parse --show-toplevel)" = "$atlas_review"
  if [ -n "$(git -C "$atlas_review" status --porcelain)" ]; then
    printf '%s\n' '审核目录存在未提交修改；已停止，未覆盖任何文件。' >&2
    exit 1
  fi
  git -C "$atlas_review" switch --detach "$atlas_remote"
else
  git -C "$atlas_repo" worktree add --detach "$atlas_review" "$atlas_remote"
fi
atlas_entry="$atlas_review/docs/component_atlas_v001/index.html"
test -s "$atlas_entry"
if [ "$(uname -s)" = Darwin ]; then
  open -a 'Google Chrome' "$atlas_entry"
else
  printf '%s\n' "Chrome本地入口：$atlas_entry"
fi
