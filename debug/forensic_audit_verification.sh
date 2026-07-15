#!/usr/bin/env bash
# ==============================================================================
# CI Forensic Audit & Automated Repair Script (Robust Version)
# ==============================================================================

set -euo pipefail

echo "============================================================"
echo "🔍 DIAGNOSTICS: Locating Orchestrator Definition"
echo "============================================================"

# Read all matching files into an array safely
mapfile -t ORCHESTRATOR_FILES < <(grep -rl "class BernoulliPipelineOrchestrator" src/ || true)

if [ ${#ORCHESTRATOR_FILES[@]} -eq 0 ]; then
    echo "❌ ERROR: Could not find 'class BernoulliPipelineOrchestrator' in src/"
    exit 1
else
    echo "Found orchestrator class in:"
    printf "  - %s\n" "${ORCHESTRATOR_FILES[@]}"
fi

echo ""
echo "Files attempting to import from src.main:"
grep -rn "src.main" tests/ || true

echo "============================================================"
echo "📄 SMOKING-GUN AUDIT: Inspecting Source Files"
echo "============================================================"

# Loop through and inspect each file found
for file in "${ORCHESTRATOR_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "--- First 40 lines of: $file ---"
        cat -n "$file" | head -n 40
        echo "------------------------------------------------------------"
    fi
done

echo "============================================================"
echo "🛠️ AUTOMATED REPAIRS: Aligning Imports and Modules"
echo "============================================================"
# (Your remaining repair/pytest logic goes here...)