#!/usr/bin/env bash
# Fetch every raw source at the commit pinned in sources.lock.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p raw
grep -v '^#' sources.lock | while read -r name url commit; do
  [ -z "$name" ] && continue
  if [ ! -d "raw/$name/.git" ]; then git init -q "raw/$name"; git -C "raw/$name" remote add origin "$url"; fi
  git -C "raw/$name" fetch -q --depth 1 origin "$commit"
  git -C "raw/$name" checkout -q FETCH_HEAD
  echo "$name @ $(git -C raw/$name rev-parse HEAD)"
done
