#!/usr/bin/env bash
echo "==============================================================="
echo "  Starting Vrusha Kamat Portfolio - Java Web Server"
echo "==============================================================="
echo ""
javac PortfolioServer.java
if [ $? -ne 0 ]; then
    echo "Compilation failed. Ensure JDK is installed."
    exit 1
fi
echo "Compiled successfully! Launching server..."
java PortfolioServer
