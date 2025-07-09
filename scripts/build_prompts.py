import yaml, pandas as pd, textwrap, re
from ace_tools import display_dataframe_to_user

# --- Sample: minimal YAML snippet with two characters (use your full file path in real pipeline) ---
yaml_text = """
kang_junhyuk:
  signature:
    hair:
      style: "loose slick-back"
    outfit:
      jacket: "midnight-charcoal suit"
      inner_shirt: "deep-V black silk shirt"
    accessories:
      lapel_pin:
        type: "mini brushed-silver origami rose"
park_siljang:
  signature:
    hair:
      style: "curtain bangs covering eyes"
    outfit:
      suit: "matte-black tailored suit"
    accessories:
      cufflinks:
        led: "tiny crimson LED"
"""

characters = yaml.safe_load(yaml_text)

# --- Example storyboard rows (cut list) ---
storyboard = [
    {
        "CUT": "1-A",
        "Description": "CU Kang Junhyuk half-lit face, cobalt-blue lapel-pin pulse",
        "Characters": ["kang_junhyuk"],
        "BG": "dark library"
    },
    {
        "CUT": "2-B",
        "Description": "Low-angle silhouette: Park Siljang enters, cufflink LED blinks",
        "Characters": ["park_siljang"],
        "BG": "dim doorway"
    },
    {
        "CUT": "3-C",
        "Description": "Two-shot: Junhyuk & Siljang confront each other",
        "Characters": ["kang_junhyuk", "park_siljang"],
        "BG": "marble corridor"
    },
]

def build_prompt(row):
    base = f"{row['Description']}, background {row['BG']}."
    details = []
    for cid in row["Characters"]:
        sig = characters.get(cid, {}).get("signature", {})
        hair = sig.get("hair", {}).get("style", "")
        outfit = sig.get("outfit", {})
        outfit_str = ", ".join(v for v in outfit.values() if isinstance(v, str))
        pieces = [cid.replace('_', ' ').title(), hair, outfit_str]
        details.append(" | ".join(filter(None, pieces)))
    return base + " -- " + " || ".join(details)

prompts = [build_prompt(r) for r in storyboard]

df = pd.DataFrame({
    "CUT": [r["CUT"] for r in storyboard],
    "Prompt": prompts
})

display_dataframe_to_user("AI_Prompts", df)
