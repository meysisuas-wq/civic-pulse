#!/bin/bash
set -euo pipefail
echo "Seeding CivicPulse database..."
python src/db/seeds.py
echo "Database seeded!"
