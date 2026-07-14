#!/bin/bash
# src/debug/forensic_audit.sh
# Run this after a failed test to diagnose Exit Code 2 (CLI Contract Violation)

echo "--- 🔍 FORENSIC AUDIT STARTING ---"
echo "--- Working Directory: $(pwd) ---"

# --- SECTION 1: ENVIRONMENTAL DIAGNOSTICS ---
echo "--- [1/3] DIAGNOSTIC: Filesystem & Config Presence ---"
find . -maxdepth 3 -name "*.json" | grep -E "schema|config"
ls -lah data/testing-input-output/

echo "--- [2/3] DIAGNOSTIC: CLI Flag Definition Audit ---"
# Check if required flags exist in main.py
grep -C 5 "required=True" src/main.py

# Check for presence of the file the script is trying to load
ls -l data/testing-input-output/bernoulli_solver_input.json

# --- SECTION 2: SMOKING-GUN SOURCE AUDIT ---
echo "--- [3/3] AUDIT: main.py CLI Logic (Line Numbers) ---"
# Check the lines where arguments are defined
cat -n src/main.py | sed -n '170,200p'

echo "--- Forensic Audit Complete. If 'required=True' is present, it is likely the culprit. ---"

# --- SECTION 3: AUTOMATED REPAIRS (COMMENTED) ---
# Uncomment only one block at a time to test individual hypotheses.

# REPAIR A: Relax argparse constraints (Remove required=True)
# sed -i 's/required=True/required=False/g' src/main.py
# echo "Applied Repair A: Relaxed required=True to False."

# REPAIR B: Force log level to DEBUG to see hidden argparse errors
# sed -i 's/level=logging.INFO/level=logging.DEBUG/g' src/main.py
# echo "Applied Repair B: Set logging to DEBUG."

# REPAIR C: Force hardcoded path fallback (if env variables are failing)
# sed -i "s|args.input_output_folder|'data/testing-input-output/'|g" src/main.py
# echo "Applied Repair C: Bypassed CLI folder argument."

echo "--- 🛑 FORENSIC AUDIT FINISHED ---"