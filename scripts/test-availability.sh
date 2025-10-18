#!/bin/bash

# Availability Testing Script for EB Deployments
# Usage: ./test-availability.sh <URL>

# Configuration
URL="${1}"
LOG_FILE="availability-test-$(date +%Y%m%d-%H%M%S).log"

if [ -z "$URL" ]; then
    echo "Usage: $0 <URL>"
    echo "Example: $0 http://your-env.elasticbeanstalk.com/health"
    exit 1
fi

echo "======================================"
echo "Availability Testing for EB Deployment"
echo "======================================"
echo "Testing URL: $URL"
echo "Log file: $LOG_FILE"
echo "Press Ctrl+C to stop"
echo "======================================"
echo ""

# Counters
TOTAL=0
SUCCESS=0
FAILED=0

# Start time
START_TIME=$(date +%s)

while true; do
    TOTAL=$((TOTAL + 1))
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$URL" 2>&1)
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    ELAPSED=$(($(date +%s) - START_TIME))

    if [ "$RESPONSE" = "200" ]; then
        SUCCESS=$((SUCCESS + 1))
        printf "[$TIMESTAMP] ✓ Available (200) | Success: %3d | Failed: %3d | Total: %3d | Elapsed: %ds\n" $SUCCESS $FAILED $TOTAL $ELAPSED
        echo "[$TIMESTAMP] SUCCESS 200" >> "$LOG_FILE"
    else
        FAILED=$((FAILED + 1))
        printf "[$TIMESTAMP] ✗ UNAVAILABLE (%s) | Success: %3d | Failed: %3d | Total: %3d | Elapsed: %ds\n" "$RESPONSE" $SUCCESS $FAILED $TOTAL $ELAPSED
        echo "[$TIMESTAMP] FAILED $RESPONSE" >> "$LOG_FILE"
    fi

    sleep 1
done