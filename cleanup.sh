#!/usr/bin/env bash
set -euo pipefail

echo "Cleaning Paris Field Guide repository..."

# --------------------------------------------------------------------
# Remove obsolete top-level docs (only if they exist)
# --------------------------------------------------------------------

rm -f \
  BACKLOG.md \
  DEPLOY.md \
  SESSION.md \
  itinerary.md \
  logistics.md \
  tickets.md \
  transit-ledger.md

# --------------------------------------------------------------------
# Remove junk
# --------------------------------------------------------------------

rm -rf \
  tmp \
  generator/__pycache__

find . -name "__pycache__" -type d -prune -exec rm -rf {} +
find . -name "*.pyc" -delete
find . -name ".DS_Store" -delete

# --------------------------------------------------------------------
# Ensure knowledge folders exist
# --------------------------------------------------------------------

mkdir -p research/cafes
mkdir -p research/bakeries
mkdir -p research/neighborhoods

# --------------------------------------------------------------------
# Fix accidental filename
# --------------------------------------------------------------------

if [ -f "MASTER_ITINERARY.md." ]; then
    mv MASTER_ITINERARY.md. MASTER_ITINERARY.md
fi

# --------------------------------------------------------------------
# Verify required files
# --------------------------------------------------------------------

required=(
  README.md
  PROJECT_RULES.md
  MASTER_ITINERARY.md
)

for file in "${required[@]}"; do
    if [ ! -f "$file" ]; then
        echo "WARNING: Missing $file"
    fi
done

echo
echo "Repository cleaned."
echo
git status --short
