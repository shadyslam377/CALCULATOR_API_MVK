#!/usr/bin/env bash
set -euo pipefail

BASE_VERSION="$(tr -d '[:space:]' < VERSION)"
MAJOR="$(echo "$BASE_VERSION" | cut -d. -f1)"
MINOR="$(echo "$BASE_VERSION" | cut -d. -f2)"
PATCH="$(echo "$BASE_VERSION" | cut -d. -f3)"

COMMIT_MSG="$(git log -1 --pretty=%B 2>/dev/null || echo "")"

if printf '%s' "$COMMIT_MSG" | grep -q '\[major\]'; then
  MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0
elif printf '%s' "$COMMIT_MSG" | grep -q '\[minor\]'; then
  MINOR=$((MINOR + 1)); PATCH=0
else
  PATCH=$((PATCH + 1))
fi

NEW_BASE="${MAJOR}.${MINOR}.${PATCH}"

BUILD_ID="${GITHUB_RUN_NUMBER:-$(git rev-parse --short=7 HEAD 2>/dev/null || echo local)}"
APP_VERSION="${NEW_BASE}-build.${BUILD_ID}"
IMAGE_TAG="${APP_VERSION}"

echo "BASE_VERSION=${NEW_BASE}"
echo "BUILD_ID=${BUILD_ID}"
echo "APP_VERSION=${APP_VERSION}"
echo "IMAGE_TAG=${IMAGE_TAG}"