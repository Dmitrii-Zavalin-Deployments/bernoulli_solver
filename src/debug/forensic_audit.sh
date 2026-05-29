#!/bin/bash
# Description: Forensic audit for method signature mismatch in S0 Classifier.

ORCHESTRATOR="src/bernoulli_pipeline_orchestrator.py"
STEP_S0="src/steps/step_s0_filled_unfilled_classifier.py"

echo "--- 🔍 Starting Forensic Audit: S0 Method Signature Mismatch ---"

# 1. Diagnostic: Inspect the line in the orchestrator that failed
echo "Auditing Orchestrator line 70..."
cat -n "$ORCHESTRATOR" | grep -C 3 70

# 2. Diagnostic: List available methods in the failing step file
echo "--- 🔍 Checking available methods in $STEP_S0 ---"
grep "def " "$STEP_S0"

# 3. Diagnostic: Inspect the interface for the 'Truth'
echo "--- 🔍 Checking Interface Definition ---"
cat src/interfaces/step_interfaces/step_s0_filled_unfilled_classifier_interface.py

echo "--- 🛠️  Automated Repair Strategy ---"
echo "If the interface defines 'classify' but the orchestrator calls 'classify_fields',"
echo "use the following sed command to align the orchestrator with the interface:"
echo "# sed -i 's/classify_fields/classify/g' $ORCHESTRATOR"
echo "--- 🔍 Audit Complete. ---"
exit 0