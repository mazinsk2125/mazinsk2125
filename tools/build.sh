#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p fonts ../assets/projects
[ -f fonts/JBM-Regular.ttf ] || curl -sSL -o fonts/JBM-Regular.ttf https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf
[ -f fonts/JBM-Bold.ttf ]    || curl -sSL -o fonts/JBM-Bold.ttf    https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Bold.ttf
[ -f fonts/BSD.ttf ]         || curl -sSL -o fonts/BSD.ttf        "https://github.com/google/fonts/raw/main/ofl/bigshouldersdisplay/BigShouldersDisplay%5Bwght%5D.ttf"
for g in gen_hero gen_terminal gen_cp gen_projects; do python3 "$g.py"; done
