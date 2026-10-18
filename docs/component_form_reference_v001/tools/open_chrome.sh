#!/usr/bin/env bash
set -euo pipefail
task_ref=refs/remotes/origin/evidence/component-form-reference-v001
task_root=$(git rev-parse --show-toplevel)
task_target="$(dirname "$task_root")/wanfo-component-form-reference-v001"
task_sha=$(git rev-parse "$task_ref^{commit}")
if [ -e "$task_target" ]; then
  test -f "$task_target/.git" || { echo "审核目录已存在但不是worktree，停止。"; exit 1; }
  test "$(git -C "$task_target" rev-parse --show-toplevel)" = "$task_target" || exit 1
  task_common=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
  task_review_common=$(cd "$task_target" && cd "$(git rev-parse --git-common-dir)" && pwd -P)
  test "$task_review_common" = "$task_common" || { echo "审核目录不属于当前仓库，停止。"; exit 1; }
  test -z "$(git -C "$task_target" status --porcelain)" || { echo "审核目录有未提交修改，停止，不覆盖。"; exit 1; }
  git -C "$task_target" merge-base --is-ancestor HEAD "$task_sha" || { echo "审核目录不在本分支快进链上，停止。"; exit 1; }
  git -C "$task_target" checkout --detach "$task_sha"
else
  git worktree add --detach "$task_target" "$task_sha"
fi
task_html="$task_target/docs/component_form_reference_v001/index.html"
test -f "$task_html"
if [ "$(uname)" = Darwin ]; then
  open -a "Google Chrome" "$task_html"
else
  echo "已准备好：$task_html"
  echo "请在Google Chrome打开上述本地文件。"
fi
