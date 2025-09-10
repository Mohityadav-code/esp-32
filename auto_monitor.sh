#!/bin/bash
echo "============================================"
echo "🔄 Waiting for upload to complete..."
echo "============================================"
echo ""
echo "This will automatically start monitoring after upload."
echo "Press Ctrl+C to stop monitoring."
echo ""
sleep 3
echo "📡 Starting serial monitor on /dev/cu.usbserial-230..."
echo "--------------------------------------------"
cat /dev/cu.usbserial-230 
