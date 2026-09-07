#!/bin/bash
cd /home/devoid_caliber/Desktop/DIGITAL-FAUCET

# 1. Run the Python Agent to evolve the art and update index.html
python3 agent.py

# 2. Push the updated code straight to GitHub
git add index.html art_dna.json
git commit -m "Agent evolved the art automatically"
git push origin main
