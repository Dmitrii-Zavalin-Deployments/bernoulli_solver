#!/bin/bash

# ==============================================================================
# Bernoulli Solver Forensic Audit
# Purpose: Diagnose Contract-Implementation Mismatch for SolverConfig
# ==============================================================================

echo "--- 1. DIAGNOSTICS: Inspecting SolverConfig Constructor ---"
grep -A 5 "class SolverConfig" src/config/config_interface.py 

echo -e "\n--- 2. DIAGNOSTICS: Inspecting Test Fixture Instantiation ---"
grep -A 10 "def valid_config" tests/contract/test_pipeline_deterministic_consistency.py

echo -e "\n--- 3. SOURCE AUDIT: Config Interface Definition ---"
cat -n src/config/config_interface.py

echo -e "\n--- 4. SOURCE AUDIT: Test Fixture Implementation ---"
cat -n tests/contract/test_pipeline_deterministic_consistency.py

echo -e "\n--- 5. REPAIR SUGGESTIONS (Automated Injection Commands) ---"
echo "To fix the missing 'precision' argument, you can apply one of the sed patterns below."
echo "Uncomment the line corresponding to your preferred fix."

# REPAIR: Inject precision=1e-6 into the SolverConfig call in the test file.
# Since it is a multiline definition, this sed appends it after 'g=9.81,':
# sed -i '/g=9.81,/a \            precision=1e-6,' tests/contract/test_pipeline_deterministic_consistency.py

# REPAIR: Alternative - Replace the entire SolverConfig instantiation block if the above fails
# # sed -i 's/SolverConfig(/SolverConfig(precision=1e-6, /g' tests/contract/test_pipeline_deterministic_consistency.py