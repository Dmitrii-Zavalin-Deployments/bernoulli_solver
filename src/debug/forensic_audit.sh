#!/bin/bash
# Description: Automated forensic audit for Bernoulli Pipeline Import Failures.

echo "--- 🔍 Starting Forensic Audit: Import Structure ---"

# 1. Verify Class Definition existence in the source file
TARGET_FILE="src/steps/step_s0_filled_unfilled_classifier.py"
EXPECTED_CLASS="StepS0FilledUnfilledClassifier"

echo "Auditing $TARGET_FILE for class definition: $EXPECTED_CLASS"
if ! grep -q "class $EXPECTED_CLASS" "$TARGET_FILE"; then
    echo "❌ [CRITICAL] Class '$EXPECTED_CLASS' not found in $TARGET_FILE."
    echo "--- 📋 Current file contents (smoking gun): ---"
    cat -n "$TARGET_FILE"
else
    echo "✅ Class definition found."
fi

# 2. Check for circular imports in the target file
if grep -q "from src.bernoulli_pipeline_orchestrator" "$TARGET_FILE"; then
    echo "❌ [CRITICAL] Circular dependency detected: $TARGET_FILE imports the orchestrator."
fi

# 3. Automated Repair Injection Strategy (Uncomment to apply)
# If the class name was wrong, this sed would fix it:
# # sed -i "s/class [A-Za-z0-9_]*/class $EXPECTED_CLASS/" "$TARGET_FILE"

# If an __init__.py is missing in src/steps:
# # touch src/steps/__init__.py

echo "--- 🔍 Audit Complete. Review logs for structural debt. ---"
exit 0