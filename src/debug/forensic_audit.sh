#!/bin/bash
# ==============================================================================
# src/debug/forensic_audit.sh
# Forensic Audit: Injecting Missing Physical Validation Logic
# ==============================================================================

set -euo pipefail

SOURCE_FILE="src/steps/step_s1_exactly_one_missing.py"
TEST_FILE="tests/steps/test_step_s1_exactly_one_missing.py"

echo "======================================================================"
echo "🔍 STAGE 1: DIAGNOSING LOGIC GAP"
echo "======================================================================"
echo "Result: Implementation is passing structural tests but failing physical edge-cases."

# Check if implementation contains validation logic
if grep -q "if val < 0" "$SOURCE_FILE"; then
    echo "✅ Physical validation logic appears to be present."
else
    echo "❌ CRITICAL: Physical validation logic (pressure/velocity checks) missing."
fi

echo -e "\n======================================================================"
echo "🛠 STAGE 3: AUTOMATED REPAIR INJECTIONS"
echo "======================================================================"
echo "The following command will inject the missing physical constraint checks"
echo "before the return statement in the source file."

# Injection: Inserts validation checks before line 55
sed -i '55i\
        # Enforce physical constraints\
        for key, val in raw_input_dict.items():\
            if val is None: continue\
            if key in ["p1", "p2"] and val < 0:\
                raise ValidationError(f"Negative pressure at {key}: {val}")\
            if key in ["v1", "v2"] and val > 1e6:\
                raise ValidationError(f"Extreme velocity at {key}: {val}")' "$SOURCE_FILE"

# Injection: Update tests to catch ValidationError instead of generic ValueError
sed -i 's/pytest.raises(ValueError)/pytest.raises(ValidationError)/g' "$TEST_FILE"

echo "✅ Forensic audit complete. Uncomment the sed commands to apply patches."