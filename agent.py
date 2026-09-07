import random
import os
import json
from datetime import datetime

# 1. Load or initialize the Art Agent's "DNA"
dna_file = "art_dna.json"
if os.path.exists(dna_file):
    with open(dna_file, "r") as f:
        dna = json.load(f)
else:
    # Default starter genes
    dna = {"speed": 0.02, "particle_count": 100, "mutation_rate": 0.1, "hue_start": 180}

# 2. EVOLVE: Mutate the genes slightly for the new day
dna["speed"] = max(0.005, min(0.1, dna["speed"] + random.uniform(-0.01, 0.01)))
dna["particle_count"] = max(20, min(500, int(dna["particle_count"] + random.randint(-20, 20))))
dna["hue_start"] = (dna["hue_start"] + random.randint(-30, 30)) % 360

# Save the evolved DNA back to memory
with open(dna_file, "w") as f:
    json.dump(dna, f)

# 3. GENERATE THE ART CODE (HTML + p5.js)
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <script src="https://cloudflare.com"></script>
    <style> body {{ margin: 0; overflow: hidden; background: #050505; }} </style>
</head>
<body>
<script>
    let t = 0;
    function setup() {{
        createCanvas(windowWidth, windowHeight);
        strokeWeight(2);
        noFill();
    }}
    function draw() {{
        background(5, 20); // Creates a trailing blur effect
        translate(width / 2, height / 2);
        
        // Visual variables driven entirely by the agent's evolved DNA
        let numLines = {dna['particle_count']};
        let speedMultiplier = {dna['speed']};
        let baseHue = {dna['hue_start']};

        for (let i = 0; i < numLines; i++) {{
            let angle = i * 0.1 + t * speedMultiplier;
            let radius = sin(angle) * (width * 0.3) + (i * 0.5);
            let x = cos(angle) * radius;
            let y = sin(angle) * radius;
            
            // Shifting colors dynamically based on DNA
            stroke((baseHue + i) % 360, 80, 90);
            ellipse(x, y, 10 + (i * 0.2));
        }}
        t += 1;
    }}
    function windowResized() {{ resizeCanvas(windowWidth, windowHeight); }}
</script>
</body>
</html>"""

with open("index.html", "w") as f:
    f.write(html_content)

print(f"[{datetime.now()}] Art evolved successfully! Particles: {dna['particle_count']}, Speed: {dna['speed']:.4f}")
