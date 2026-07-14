#!/bin/bash
# Forensic Audit: Post-Test Analysis
# Targeted at: Pip Cache resolution, Source file integrity, and CI/CD environment drift.

echo "=========================================================="
echo "          Forensic Audit: Pipeline Environment            "
echo "=========================================================="

# 1. Diagnostics: Pip Cache & Environment
echo "[DIAGNOSTIC] Checking cache state..."
if [ -d "/home/runner/.cache/pip" ]; then
    echo "SUCCESS: Cache directory exists."
    ls -lah /home/runner/.cache/pip
else
    echo "WARNING: /home/runner/.cache/pip does not exist."
    echo "Current working directory contents:"
    ls -F
fi

echo "[DIAGNOSTIC] Python Environment Info:"
python3 -m pip --version
python3 -m pip list | grep -E "scipy|numpy|jsonschema"

echo "[DIAGNOSTIC] Searching for 'punycode' (Deprecation Warning source)..."
grep -r "punycode" . --exclude-dir=.git

echo -e "\n=========================================================="
echo "          Forensic Audit: Smoking-Gun Source Audits       "
echo "=========================================================="

# 2. Source Audits: Pinpointing logic failures in core files
echo "[AUDIT] Examining src/main.py (Pipeline Orchestrator)..."
cat -n src/main.py

echo -e "\n[AUDIT] Examining src/config/config_loader.py (Config Validation)..."
cat -n src/config/config_loader.py

echo -e "\n=========================================================="
echo "          Forensic Audit: Automated Repairs (Sed)         "
echo "=========================================================="

# 3. Automated Repairs: Uncomment to apply patches
# If you need to force-disable cache requirements in code or patch config paths:

# # Repair: Use sed to point to a validated environment path if the cache directory is misidentified
# sed -i 's|/home/runner/.cache/pip|/tmp/pip_cache|g' src/main.py

# # Repair: Strip deprecated modules if they are causing CI pipeline aborts
# # sed -i '/punycode/d' src/requirements.txt

# # Repair: Fix hardcoded paths in the orchestrator if they drift during CI
# # sed -i 's|/home/runner/work/bernoulli_solver|/github/workspace|g' src/main.py

echo "[FORENSIC AUDIT COMPLETE]"