#!/bin/bash
# ==============================================================================
# requirements.sh - Unified Environmental Provisioning
# ==============================================================================
set -e

echo "📦 Layer 1: Provisioning Runtime Core..."
pip install --no-cache-dir -r requirements.txt

# Only install dev tools if we are in a CI environment
if [ "$CI" = "true" ]; then
    echo "📦 Layer 2: Provisioning Dev/CI Tooling..."
    pip install --no-cache-dir -r requirements-dev.txt
fi

echo "✅ Environment Ready."