#!/bin/bash

# Entities - split into 3 files
echo "# Key Entities: Core System" > architecture/entities-core.md
echo "" >> architecture/entities-core.md
echo "**Scope**: Testing, Resilience, Simple Workflow entities" >> architecture/entities-core.md
echo "" >> architecture/entities-core.md
sed -n '721,785p' spec.md >> architecture/entities-core.md

echo "# Key Entities: Dynamic Catalog & Spec-Driven Workflow" > architecture/entities-dynamic-sdd.md
echo "" >> architecture/entities-dynamic-sdd.md
echo "**Scope**: Dynamic node catalog and spec-driven workflow entities" >> architecture/entities-dynamic-sdd.md
echo "" >> architecture/entities-dynamic-sdd.md
sed -n '753,785p' spec.md >> architecture/entities-dynamic-sdd.md

echo "# Key Entities: P2 Learning System" > architecture/entities-p2.md
echo "" >> architecture/entities-p2.md
echo "**Priority**: P2 (Deferred to Phase 2)" >> architecture/entities-p2.md
echo "" >> architecture/entities-p2.md
sed -n '785,830p' spec.md >> architecture/entities-p2.md

# Success Criteria
sed -n '831,930p' spec.md > success-criteria.md

# Assumptions
sed -n '913,1035p' spec.md > assumptions.md

# Dependencies
sed -n '1036,1115p' spec.md > dependencies.md

# Out of Scope
sed -n '1116,1210p' spec.md > out-of-scope.md

echo "Remaining files created:"
ls -lh architecture/*.md success-criteria.md assumptions.md dependencies.md out-of-scope.md | awk '{print $9, $5}'
