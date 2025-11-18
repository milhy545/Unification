#!/bin/bash
# Upload SSH keys to HAS server
# Usage: ./upload-keys-to-has.sh

set -euo pipefail

HAS_HOST="root@192.168.0.58"
HAS_PORT="2222"
HAS_KEYS_DIR="/root/.ssh/ecosystem-keys"
LOCAL_KEYS_DIR="./ssh-keys-export"

echo "🔑 Uploading SSH keys to HAS..."

# Check if keys exist locally
if [ ! -f "${LOCAL_KEYS_DIR}/unified_ecosystem_key" ]; then
    echo "❌ Keys not found in ${LOCAL_KEYS_DIR}/"
    exit 1
fi

# Check if HAS is reachable
if ! ping -c 1 -W 2 192.168.0.58 &>/dev/null; then
    echo "❌ HAS server (192.168.0.58) is not reachable"
    exit 1
fi

# Create directory on HAS
echo "📁 Creating directory on HAS..."
ssh -p ${HAS_PORT} ${HAS_HOST} "mkdir -p ${HAS_KEYS_DIR} && chmod 700 ${HAS_KEYS_DIR}"

# Upload keys
echo "📤 Uploading keys to HAS:${HAS_KEYS_DIR}..."
scp -P ${HAS_PORT} \
    "${LOCAL_KEYS_DIR}/unified_ecosystem_key" \
    "${LOCAL_KEYS_DIR}/unified_ecosystem_key.pub" \
    "${HAS_HOST}:${HAS_KEYS_DIR}/"

# Set correct permissions on HAS
echo "🔒 Setting permissions on HAS..."
ssh -p ${HAS_PORT} ${HAS_HOST} "chmod 600 ${HAS_KEYS_DIR}/unified_ecosystem_key && chmod 644 ${HAS_KEYS_DIR}/unified_ecosystem_key.pub"

echo "✅ Keys uploaded successfully to HAS:${HAS_KEYS_DIR}/"
echo "🔐 Verifying..."
ssh -p ${HAS_PORT} ${HAS_HOST} "ls -la ${HAS_KEYS_DIR}/"
