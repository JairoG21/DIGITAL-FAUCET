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
    dna = {"speed": 0.02, "particle_count": 100, "hue_start": 180, "history": []}

if "history" not in dna:
    dna["history"] = []

# 2. INTRODUCE VARIATIONS (Mutate drastically)
dna["speed"] = round(random.uniform(0.01, 0.06), 4)
dna["particle_count"] = random.randint(40, 180)
dna["hue_start"] = random.randint(0, 360)

art_styles = ["spiral", "waves", "hypnotic_star", "cosmic_ring"]
color_modes = ["rainbow", "neon_pulse", "duotone", "monochrome"]

chosen_style = random.choice(art_styles)
chosen_color = random.choice(color_modes)
saturation = random.randint(70, 100)

# Save this generation's completely unique traits
new_generation = {
    "id": len(dna["history"]) + 1,
    "particle_count": dna["particle_count"],
    "speed": dna["speed"],
    "hue_start": dna["hue_start"],
    "style": chosen_style,
    "color_mode": chosen_color,
    "saturation": saturation,
    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
}
dna["history"].append(new_generation)

with open(dna_file, "w") as f:
    json.dump(dna, f)

# 3. BUILD THE GALLERY
js_history_data = json.dumps(dna["history"])

# 4. GENERATE GRID ART WITH FIXED DIMENSIONS (CRASH PROOF)
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/2.3.2/p5.js"></script>
    <style>
        body {{
            margin: 0;
            background: #07070a;
            font-family: system-ui, -apple-system, sans-serif;
            color: #fff;
            padding: 30px;
        }}
        h1 {{
            text-align: center;
            font-size: 28px;
            margin-bottom: 5px;
            letter-spacing: 1px;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 14px;
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(auto-fill, 300px);
            gap: 25px;
            justify-content: center;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .art-card {{
            background: #111116;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #22222a;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            width: 300px;
        }}
        .canvas-container {{
            width: 300px;
            height: 300px;
            background: #050505;
        }}
        .info-panel {{
            padding: 16px;
            font-size: 13px;
            border-top: 1px solid #22222a;
            background: #14141c;
            color: #999;
        }}
        .gen-title {{
            font-weight: 700;
            color: #fff;
            font-size: 15px;
            margin-bottom: 6px;
            display: flex;
            justify-content: space-between;
        }}
        .badge {{
            background: #2a2a3a;
            padding: 2px 8px;
            border-radius: 20px;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
    </style>
</head>
<body>

    <h1>🧬 Evolving Agentic Art Museum</h1>
    <div class="subtitle">Run python agent.py to birth a completely unpredictable new generation</div>
    <div class="grid-container" id="gallery"></div>

<script>
    const artHistory = {js_history_data};

    const createArtSketch = (genes) => {{
        return function(p) {{
            let t = 0;
            
            p.setup = function() {{
                // Explicit sizes remove layout load failures entirely
                p.createCanvas(300, 300);
                p.strokeWeight(1.5);
                p.noFill();
                p.colorMode("HSB", 360, 100, 100, 100);
            }};

            p.draw = function() {{
                p.background(7, 7, 10, 12);
                p.translate(150, 150); // Direct center of 300x300

                let numLines = genes.particle_count;
                let speedMultiplier = genes.speed;
                let baseHue = genes.hue_start;
                let style = genes.style;
                let colorMode = genes.color_mode;
                let sat = genes.saturation;

                for (let i = 0; i < numLines; i++) {{
                    let angle = i * 0.15 + t * speedMultiplier;
                    let radius;
                    let sizeX = 6 + (i * 0.08);
                    let sizeY = 6 + (i * 0.08);

                    if (style === "spiral") {{
                        radius = (i * 0.7) + p.sin(angle) * 20;
                    }} else if (style === "waves") {{
                        radius = p.sin(angle * 2) * 100;
                        sizeX = 4 + p.cos(angle) * 10;
                    }} else if (style === "hypnotic_star") {{
                        radius = 80 * p.sin(angle * 4);
                        sizeY = sizeX * 1.5;
                    }} else {{ 
                        radius = 90 + p.cos(angle) * 12;
                    }}

                    let x = p.cos(angle) * radius;
                    let y = p.sin(angle) * radius;
                    
                    let currentHue;
                    if (colorMode === "rainbow") {{
                        currentHue = (baseHue + (i * 2)) % 360;
                    }} else if (colorMode === "neon_pulse") {{
                        currentHue = (baseHue + p.sin(t * 0.02) * 50) % 360;
                    }} else if (colorMode === "duotone") {{
                        currentHue = i % 2 === 0 ? baseHue : (baseHue + 180) % 360;
                    }} else {{ 
                        currentHue = baseHue;
                    }}

                    p.stroke(currentHue, sat, 95, 80);
                    
                    if (style === "hypnotic_star") {{
                        p.rect(x, y, sizeX, sizeY);
                    }} else {{
                        p.ellipse(x, y, sizeX, sizeY);
                    }}
                }}
                t += 1;
            }};
        }};
    }};

    const gallery = document.getElementById('gallery');
    
    [...artHistory].reverse().forEach(genes => {{
        const card = document.createElement('div');
        card.className = 'art-card';
        
        // Setup direct mounting target container 
        const canvasId = `canvas-${{genes.id}}`;
        card.innerHTML = `
            <div class="canvas-container" id="${{canvasId}}"></div>
            <div class="info-panel">
                <div class="gen-title">
                    <span>Gen #${{genes.id}}</span>
                    <span class="badge" style="background: hsl(${{genes.hue_start}}, 50%, 25%); color: #fff">${{genes.style}}</span>
                </div>
                <div>Palette: <strong>${{genes.color_mode}}</strong></div>
                <div>Elements: ${{genes.particle_count}} | Speed: ${{genes.speed}}</div>
            </div>
        `;
        gallery.appendChild(card);
        
        // Instantiate the sketch immediately inside its target ID element
        new p5(createArtSketch(genes), canvasId);
    }});
</script>
</body>
</html>"""

with open("index.html", "w") as f:
    f.write(html_content)

print(f"🧬 New Variant Spawned! Gen #{len(dna['history'])} | Style: {chosen_style} | Colors: {chosen_color}")

