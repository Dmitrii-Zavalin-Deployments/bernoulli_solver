#!/usr/bin/env bash
# ==============================================================================
# Pipeline Forensic Audit & Verification Utility
# Designed to run post-test in GitHub Actions to root out contract & validation errors.
# ==============================================================================
set -euo pipefail

echo "========================================================================"
echo "🔍 STARTING DETAILED CONTRACT AND VALIDATION FORENSIC AUDIT"
echo "========================================================================"

# --- STEP 1: SCAN SCHEMAS FOR STRUCTURAL NESTING ---
echo -e "\n### [DIAGNOSTIC] Scanning Output Schema Structure ###"
if [ -f "schema/bernoulli_output.schema.json" ]; then
    echo "• Found schema/bernoulli_output.schema.json. Top-level keys:"
    grep -n -E '"properties"\s*:' -A 5 schema/bernoulli_output.schema.json || true
else
    echo "⚠️ schema/bernoulli_output.schema.json not found!"
fi


# --- STEP 2: SMOKING-GUN SOURCE AUDITS (cat -n) ---
echo -e "\n### [SMOKING GUN] 1. Excess Field Validation Audit ###"
if [ -f "tests/contract/test_excess_field_validation.py" ]; then
    cat -n tests/contract/test_excess_field_validation.py | sed -n '22,35p' || true
else
    echo "⚠️ tests/contract/test_excess_field_validation.py not found!"
fi

echo -e "\n### [SMOKING GUN] 2. No Computation Before Validation Audit ###"
if [ -f "tests/contract/test_no_computation_before_validation.py" ]; then
    cat -n tests/contract/test_no_computation_before_validation.py | sed -n '18,30p' || true
else
    echo "⚠️ tests/contract/test_no_computation_before_validation.py not found!"
fi

echo -e "\n### [SMOKING GUN] 3. Type Validation Audit ###"
if [ -f "tests/contract/test_type_validation.py" ]; then
    cat -n tests/contract/test_type_validation.py | sed -n '45,61p' || true
else
    echo "⚠️ tests/contract/test_type_validation.py not found!"
fi

echo -e "\n### [SMOKING GUN] 4 & 5. Schema-State Mapping Audits ###"
if [ -f "tests/validation/test_schema_state_mapping.py" ]; then
    cat -n tests/validation/test_schema_state_mapping.py | sed -n '19,32p' || true
else
    echo "⚠️ tests/validation/test_schema_state_mapping.py not found!"
fi


# --- STEP 3: PIPELINE REPAIR INJECTIONS (Commented-out sed Commands) ---
echo -e "\n========================================================================"
echo "🛠️ AUTOMATED REPAIR PLAYBOOK"
echo "========================================================================"

# --- Repair 1: Excess Field Validation ---
# Explanation: Flattens the properties map by extracting nested keys inside "inputs" and "results".
echo "# [REPAIR 1] Traverse nested fields instead of checking the schema root:"
echo "# sed -i 's/properties = json.load(f).get(\"properties\", {})/schema_props = json.load(f).get(\"properties\", {}); properties = {sub_k: sub_v for k in [\"inputs\", \"results\"] if k in schema_props for sub_k, sub_v in schema_props[k].get(\"properties\", {}).items()}/' tests/contract/test_excess_field_validation.py"

# --- Repair 2: No Computation Before Validation (run_solver signature) ---
# Explanation: Passes the missing directory path and expected outputs to satisfy run_solver's 3-parameter signature.
echo -e "\n# [REPAIR 2] Update run_solver calls to match its 3-argument signature:"
echo "# sed -i 's/run_solver(invalid_path)/run_solver(\".\", invalid_path, \"bernoulli_solver_output.json\")/g' tests/contract/test_no_computation_before_validation.py"

# --- Repair 3: Type Validation (nested vs flat matching) ---
# Explanation: Maps typed evaluation dynamically to inner properties inside "inputs" and "results".
echo -e "\n# [REPAIR 3] Track types of nested JSON objects rather than root keys:"
echo "# sed -i 's/properties = schema.get(\"properties\", {})/schema_props = schema.get(\"properties\", {}); properties = {sub_k: sub_v for k in [\"inputs\", \"results\"] if k in schema_props for sub_k, sub_v in schema_props[k].get(\"properties\", {}).items()}/' tests/contract/test_type_validation.py"

# --- Repair 4 & 5: Schema State Mapping ---
# Explanation: Flattens nested keys under "inputs" and "results" so both the completeness and excess mappings evaluate successfully.
echo -e "\n# [REPAIR 4 & 5] Flatten schema mapping verification outputs:"
echo "# sed -i 's/output_fields = set(output_schema.get(\"properties\", output_schema).keys())/out_props = output_schema.get(\"properties\", {}); output_fields = {sub_k for k in [\"inputs\", \"results\"] if k in out_props for sub_k in out_props[k].get(\"properties\", {}).keys()}/' tests/validation/test_schema_state_mapping.py"

echo -e "\n========================================================================"
echo "🎯 FORENSIC AUDIT COMPLETE"
echo "========================================================================"