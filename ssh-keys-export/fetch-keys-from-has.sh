#!/bin/bash
# Fetch SSH keys from HAS server
# Usage: ./fetch-keys-from-has.sh

set -euo pipefail

HAS_HOST="root@192.168.0.58"
HAS_PORT="2222"
HAS_KEYS_DIR="/root/.ssh/ecosystem-keys"
LOCAL_KEYS_DIR="$HOME/.ssh"

echo "🔑 Fetching SSH keys from HAS..."

# Check if HAS is reachable
if ! ping -c 1 -W 2 192.168.0.58 &>/dev/null; then
    echo "❌ HAS server (192.168.0.58) is not reachable"
    exit 1
fi

# Fetch keys
echo "📥 Downloading keys from HAS:${HAS_KEYS_DIR}..."
scp -P ${HAS_PORT} "${HAS_HOST}:${HAS_KEYS_DIR}/unified_ecosystem_key" "${LOCAL_KEYS_DIR}/" || {
    echo "❌ Failed to download keys"
    exit 1
}

# Set correct permissions
echo "🔒 Setting correct permissions..."
chmod 600 "${LOCAL_KEYS_DIR}/unified_ecosystem_key"

echo "✅ Keys fetched successfully to ${LOCAL_KEYS_DIR}/"
echo "📝 Key fingerprint:"
ssh-keygen -lf "${LOCAL_KEYS_DIR}/unified_ecosystem_key"
