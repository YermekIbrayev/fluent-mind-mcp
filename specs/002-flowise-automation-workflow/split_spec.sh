#!/bin/bash

# Extract sections from spec.md

# Functional Requirements P1 (lines 441-510: FR-000 to FR-040, FR-106-115)
sed -n '441,510p; 571,582p' spec.md > requirements/functional-p1.md

# Functional Requirements P2 (lines 496-570: FR-041 to FR-105)
echo "# Functional Requirements: P2 Learning System" > requirements/functional-p2.md
echo "" >> requirements/functional-p2.md
echo "**Priority**: P2 (Deferred to Phase 2)" >> requirements/functional-p2.md
echo "" >> requirements/functional-p2.md
sed -n '496,570p' spec.md >> requirements/functional-p2.md

# NFR P1 (lines 583-653)
sed -n '583,660p' spec.md > requirements/nfr-p1.md

# NFR P2 (lines 596-720)
echo "# Non-Functional Requirements: P2 Learning System" > requirements/nfr-p2.md
echo "" >> requirements/nfr-p2.md
echo "**Priority**: P2 (Deferred to Phase 2)" >> requirements/nfr-p2.md
echo "" >> requirements/nfr-p2.md
sed -n '596,608p; 634,677p' spec.md >> requirements/nfr-p2.md

echo "Files created in requirements/"
ls -lh requirements/
