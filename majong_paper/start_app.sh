#!/bin/bash

echo "Launching iOS Simulator..."
open -a Simulator

echo "Waiting for Simulator to launch (give it a few seconds)..."
sleep 10 # Give the simulator some time to fully launch

echo "Running Flutter application..."
flutter run
