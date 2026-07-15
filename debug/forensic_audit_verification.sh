#!/usr/bin/env bash
# ==============================================================================
# Pipeline Forensic Audit & Verification Utility
# Designed to run post-test in GitHub Actions to root out structural deviations.
# ==============================================================================
set -euo pipefail

echo "========================================================================"
echo "🔍 STARTING FORENSIC AUDIT: DIAGNOSING CI BREAKAGES"
echo "========================================================================"

# --- 1. AUDIT RUN_SOLVER() SIGNATURE ---
echo -e "\n=== [STEP 1] Auditing run_solver() and main() signatures in src/main.py ==="
if [ -f "src/main.py" ]; then
    echo "• Found src/main.py. Locating function definitions:"
    grep -n -E "def run_solver|def main" src/main.py || true
    echo -e "\n• Showing run_solver context:"
    grep -A 5 "def run_solver" src/main.py || true
else
    echo "⚠️ src/main.py not found!"
fi

# --- 2. AUDIT ARGPARSE / SYSTEMEXIT CODES ---
echo -e "\n=== [STEP 2] Auditing CLI Argument Parsing in main() ==="
if [ -f "src/main.py" ]; then
    # Look for how argparse is set up and exit codes are handled
    grep -n -C 5 "ArgumentParser" src/main.py || true
    grep -n -C 5 "sys.exit" src/main.py || true
fi

# --- 3. AUDIT OUTPUT SCHEMA VS FLAT CONTAINER STRUCTURE ---
echo -e "\n=== [STEP 3] Auditing Schema Top-Level Properties ==="
for schema_file in "schema/bernoulli_input.schema.json" "schema/bernoulli_output.schema.json"; do
    if [ -f "$schema_file" ]; then
        echo "• Fields in $schema_file:"
        grep -oE '"properties":\s*\{' -A 10 "$schema_file" | grep -E '"[a-zA-Z0-9_]+"' || true
    else
        echo "⚠️ Schema file $schema_file not found!"
    fi
done

# --- 4. SMOKING-GUN SOURCE CODE AUDITS ---
echo -e "\n=== [STEP 4] Smoking-Gun Code Audits (cat -n) ==="
echo "• Examining failing orchestrator tests calling run_solver():"
if [ -f "tests/orchestrator/test_pipeline_orchestrator.py" ]; then
    cat -n tests/orchestrator/test_pipeline_orchestrator.py | grep -C 3 "run_solver(" || true
fi

echo -e "\n• Examining CLI test blocks in orchestrator tests:"
if [ -f "tests/orchestrator/test_pipeline_orchestrator.py" ]; then
    cat -n tests/orchestrator/test_pipeline_orchestrator.py | grep -C 5 "test_main_" || true
fi

# --- 5. SUGGESTED AUTOMATED REPAIRS (Commented out) ---
echo -e "\n=== [STEP 5] Automated Sed Repairs (Comment out to run or execute as dry-run) ==="

# Issue A: test_run_solver_full_path and test_run_solver_schema_validation_error are calling
# run_solver() with only 1 positional argument, but it requires 2 (input and output file names).
echo "# [REPAIR A] Updating orchestrator test calls to pass output paths:"
echo "# sed -i 's/run_solver(\"input.json\")/run_solver(\"input.json\", \"bernoulli_solver_output.json\")/g' tests/orchestrator/test_pipeline_orchestrator.py"
echo "# sed -i 's/run_solver(\"dummy_path.json\")/run_solver(\"dummy_path.json\", \"bernoulli_solver_output.json\")/g' tests/orchestrator/test_pipeline_orchestrator.py"

# Issue B: test_solver_refuses_execution_if_validation_fails calls run_solver() with no arguments,
# which triggers a TypeError because it requires positional arguments.
echo -e "\n# [REPAIR B] Patching contract validation test to pass dummy paths to run_solver():"
echo "# sed -i 's/run_solver()/run_solver(\"invalid_input.json\", \"invalid_output.json\")/g' tests/contract/test_no_computation_before_validation.py"

# Issue C: CLI tests assert SystemExit(1) on failure, but argparse naturally exits with code 2.
echo -e "\n# [REPAIR C Option 1] Patching main() inside src/main.py to catch argparse errors and exit with 1:"
echo "# Note: Modify the error handler block inside src/main.py's main() to use sys.exit(1) on parsing failures."
echo "# [REPAIR C Option 2] Alternatively, update tests to expect argparse's standard exit code (2):"
echo "# sed -i 's/assert e.value.code == 1/assert e.value.code == 2/g' tests/orchestrator/test_pipeline_orchestrator.py"
echo "# sed -i 's/assert cm.value.code == 1/assert cm.value.code == 2/g' tests/orchestrator/test_pipeline_orchestrator.py"

# Issue D: Schema mapping expects flat matching, but the output schema defines nested fields ('results', 'config', 'inputs').
echo -e "\n# [REPAIR D] Fixing Schema Field Types & State Mapping Mismatch:"
echo "# If your system output is structurally nested, patch test_type_validation.py and test_schema_state_mapping.py"
echo "# to audit nested fields rather than treating the nested top-level blocks as direct properties."

echo "========================================================================"
echo "🎯 FORENSIC AUDIT SCAN COMPLETE"
echo "========================================================================"