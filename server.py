import io
import re
import os
import sys
import random
import urllib.parse
import torch
import requests
from PIL import Image, ImageDraw, ImageFont
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer, util
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles

# ---------------------------------------------------------
# 1. Environment & Paths
# ---------------------------------------------------------
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.environ["HF_HOME"] = os.path.join(BASE_DIR, "hf_cache")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
FP_TYPE = torch.float16 if DEVICE == "cuda" else torch.float32

app = FastAPI(title="CaughtIn4K 1000-Anchor Meme Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 2. AI Model Loading
# ---------------------------------------------------------
print(f"[+] Loading Moondream2 on {DEVICE}...")
VISION_ID = "vikhyatk/moondream2"
vision_tok = AutoTokenizer.from_pretrained(VISION_ID, revision="2024-07-23")
vision_model = AutoModelForCausalLM.from_pretrained(
    VISION_ID,
    trust_remote_code=True,
    revision="2024-07-23",
    torch_dtype=FP_TYPE,
    low_cpu_mem_usage=True,
).to(DEVICE).eval()

print("[+] Loading Sentence-Transformers (all-MiniLM-L6-v2)...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2", device=DEVICE)

print("[+] Loading Qwen 0.5B...")
LLM_ID = "Qwen/Qwen2.5-0.5B-Instruct"
llm_tok = AutoTokenizer.from_pretrained(LLM_ID)
llm_model = AutoModelForCausalLM.from_pretrained(
    LLM_ID,
    torch_dtype=FP_TYPE,
    low_cpu_mem_usage=True,
).to(DEVICE).eval()

# ---------------------------------------------------------
# 3. 1,000+ Semantic Anchor Matrix Generation
# ---------------------------------------------------------
print("[+] Fetching Imgflip template registry...")
try:
    resp = requests.get("https://api.imgflip.com/get_memes", timeout=12).json()
    raw_memes = resp.get("data", {}).get("memes", [])
except Exception as err:
    print(f"[!] Imgflip fetch error: {err}")
    raw_memes = []

EXCLUDED = {"expanding brain", "drake hotline bling"}
BASE_MEMES = [m for m in raw_memes if not any(x in m["name"].lower() for x in EXCLUDED)]

# Categorized semantic clusters
CLUSTER_SEEDS = {
    "trauma_shock": [
        "paralyzed wide-eyed terror witnessing disaster",
        "staring in disbelief completely traumatized",
        "jaw unhinged dropped in pure horror",
        "catastrophic sudden realization of failure",
        "unfiltered panic after terrible mistake",
        "witnessing an unspeakable crime live",
        "blank white shock eyes popping out of skull"
    ],
    "smug_villain": [
        "arrogant sly side-eye smirk planning chaos",
        "wicked evil grin watching everything burn down",
        "condescending villain laughter holding beverage",
        "petty victory celebration toxic superiority",
        "narcissistic ego trip looking down on mortals",
        "sarcastic raised eyebrow mocking someone",
        "devious mischievous plot brewing behind eyes"
    ],
    "clueless_npc": [
        "zero thoughts completely blank static brain",
        "deadpan unblinking default character creation slider",
        "confused question marks floating above clueless head",
        "awkward bystander who has no idea what is happening",
        "glazed over eyes buffering 144p resolution",
        "standing awkwardly in the corner isolated weirdo",
        "smiling politely while having zero comprehension"
    ],
    "dead_inside": [
        "agonizing forced smile disguising internal suffering",
        "exhausted lifeless hollow eyes staring into void",
        "sitting lonely on a swing depressed and defeated",
        "decayed dusty skeleton waiting for an eternity",
        "spirit completely crushed by corporate existence",
        "silent screaming inside while smiling on outside",
        "burnt out drained hopeless staring at a monitor"
    ],
    "unhinged_panic": [
        "sweating profusely trying to make impossible decision",
        "hyperventilating frantic mania wide open pupils",
        "desperate pleading pathetic begging with open hands",
        "clown applying makeup escalating foolish decisions",
        "violent swerve bad decision impulsive madness",
        "pure unadulterated chaotic stress breakdown",
        "heart attack pulse panic after false sense of calm"
    ],
    "triumph_superiority": [
        "dominant gigachad flex looking down on pathetic weakling",
        "toddler clenched fist gritty beach victory",
        "two muscular arms locking in ultimate brotherly agreement",
        "self-congratulating arrogant cheers toast",
        "mocking superiority asking where are the bitches",
        "supreme big brain logic tapping the head temple"
    ]
}

SITUATIONAL_MODIFIERS = [
    "during a tense moment",
    "when caught completely red handed",
    "while being confronted by authority",
    "at 3 am under fluorescent lighting",
    "under extreme psychological interrogation",
    "pretending to understand complex explanations",
    "after realizing the microphone was unmuted",
    "witnessing their own downfall in real time",
    "after saying something completely unhinged",
    "in an awkward professional corporate meeting"
]

# Build 1000+ distinct semantic anchors
CATALOG_ENTRIES = []
SEMANTIC_TEXTS = []

print("[+] Generating and cross-vectorizing 1,000+ semantic anchors...")
for meme in BASE_MEMES:
    m_name = meme["name"].lower()

    # Route template to best fitting seed cluster
    if any(k in m_name for k in ["pikachu", "padme", "holy shit", "uncut"]):
        cluster_key = "trauma_shock"
    elif any(k in m_name for k in ["disaster", "leo", "kermit", "roll safe"]):
        cluster_key = "smug_villain"
    elif any(k in m_name for k in ["harold", "pablo", "skeleton", "waiting"]):
        cluster_key = "dead_inside"
    elif any(k in m_name for k in ["two buttons", "cat", "nick young", "math lady", "clown"]):
        cluster_key = "unhinged_panic"
    elif any(k in m_name for k in ["doge", "success", "handshake", "cheers"]):
        cluster_key = "triumph_superiority"
    else:
        cluster_key = "clueless_npc"

    # Generate multi-context variations for every single template
    seeds = CLUSTER_SEEDS[cluster_key]
    for seed in seeds:
        for mod in SITUATIONAL_MODIFIERS[:3]:  # Yields ~21 permutations per template
            entry_text = f"{meme['name']}: {seed} {mod}"
            CATALOG_ENTRIES.append((meme, cluster_key))
            SEMANTIC_TEXTS.append(entry_text)

# Vectorize all anchors
meme_embeddings = embed_model.encode(SEMANTIC_TEXTS, convert_to_tensor=True, show_progress_bar=False)
print(f"[✓] {len(SEMANTIC_TEXTS)} semantic anchors vectorized into VRAM.")

# ---------------------------------------------------------
# 4. Anti-Repetition Weighted Softmax Selector
# ---------------------------------------------------------
RECENT_MEMES = []

def select_dynamic_meme(user_desc: str, top_k: int = 15):
    global RECENT_MEMES
    u_embed = embed_model.encode(user_desc, convert_to_tensor=True)
    cos_scores = util.cos_sim(u_embed, meme_embeddings)[0]

    # Pick top K candidate anchors
    _, top_indices = torch.topk(cos_scores, k=min(top_k, len(CATALOG_ENTRIES)))
    candidate_indices = top_indices.tolist()

    # Discard templates seen in the last 10 requests
    valid_candidates = [
        idx for idx in candidate_indices 
        if CATALOG_ENTRIES[idx][0]["name"] not in RECENT_MEMES
    ]

    # History decay safeguard
    if not valid_candidates:
        RECENT_MEMES = RECENT_MEMES[-3:]
        valid_candidates = [
            idx for idx in candidate_indices 
            if CATALOG_ENTRIES[idx][0]["name"] not in RECENT_MEMES
        ]

    chosen_idx = random.choice(valid_candidates) if valid_candidates else candidate_indices[0]
    matched_meme, matched_cluster = CATALOG_ENTRIES[chosen_idx]

    RECENT_MEMES.append(matched_meme["name"])
    if len(RECENT_MEMES) > 10:
        RECENT_MEMES.pop(0)

    return matched_meme, matched_cluster

# ---------------------------------------------------------
# 5. Context-Matched Roast Vault & LLM Few-Shot Generation
# ---------------------------------------------------------
TEMPLATE_SPECIFIC_ROASTS = {
    "trauma_shock": [
        ("REGRET TASTES", "LIKE PURE ACID"),
        ("WITNESSING THE", "CONSEQUENCES OF ACTIONS"),
        ("SOUL EXITED", "THE ENTIRE BUILDING"),
        ("TRAUMA IN", "4K RESOLUTION"),
        ("MOMENT OF UNFILTERED", "HORROR CAPTURED")
    ],
    "smug_villain": [
        ("VILLAIN ORIGIN STORY", "ACTIVATED"),
        ("WATCHING THE WHOLE", "WORLD BURN DOWN"),
        ("UNPROVOKED AND", "COMPLETELY PETTY"),
        ("ZERO SHAME", "100% AUDACITY"),
        ("HEIR TO THE", "CHAOS THRONE")
    ],
    "clueless_npc": [
        ("ZERO THOUGHTS", "BEHIND THOSE EYES"),
        ("HEAD EMPTY", "JUST DIAL-UP STATIC"),
        ("BRO IS BUFFERING", "AT 144P QUALITY"),
        ("NPC SPAWNED", "IN THE WRONG ROOM"),
        ("DEFAULT CHARACTER", "CREATION SLIDER")
    ],
    "dead_inside": [
        ("SMILING THROUGH", "EXCRUCIATING PAIN"),
        ("CORPORATE SPIRIT", "OFFICIALLY CRUSHED"),
        ("5 SECONDS WITHOUT", "DOPAMINE HIT"),
        ("WAITING FOR", "THE EMBRACE OF SLEEP"),
        ("ALIVE EXTERNALLY", "DEAD INTERNALLY")
    ],
    "unhinged_panic": [
        ("ONE WRONG MOVE", "FROM TOTAL COLLAPSE"),
        ("SWEATING BULLETS", "FOR NO REASON"),
        ("ESCALATING CLOWN", "BEHAVIOR DETECTED"),
        ("WRONG ANSWER", "CHOSEN INSTANTLY"),
        ("CALM BEFORE", "THE MEGATON BLAST")
    ],
    "triumph_superiority": [
        ("LOOK AT ME", "I AM THE CAPTAIN NOW"),
        ("PEAK DELUSION", "MAXIMUM EGO"),
        ("BRO THINKS", "HE TRULY COOKED"),
        ("UNEARNED CONFIDENCE", "AT ALL COSTS"),
        ("DOMINANCE ASSERTED", "OVER NOBODY")
    ]
}

def generate_matched_roast(user_vibe: str, meme_name: str, cluster: str):
    system_prompt = (
        "You are an uncensored, savage internet comic. "
        "Write a hilarious 2-line roast caption that DIRECTLY matches the given face and meme template. "
        "Rules:\n"
        "1. NEVER use boomer tropes like 'when you', 'me when', 'pov', or 'that face when'.\n"
        "2. Keep lines short, devastating, and punchy.\n"
        "Format:\n"
        "TOP: [2-4 words]\n"
        "BOTTOM: [2-4 words]"
    )

    user_prompt = (
        f"Face Vibe: {user_vibe}\n"
        f"Matched Template: {meme_name} ({cluster.replace('_', ' ')})\n"
        "Write the roast:"
    )

    prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n"
    inputs = llm_tok(prompt, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        outputs = llm_model.generate(
            **inputs,
            max_new_tokens=42,
            temperature=0.92,
            top_p=0.9,
            do_sample=True,
            pad_token_id=llm_tok.eos_token_id
        )

    out = llm_tok.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()

    top_m = re.search(r"TOP:\s*(.*)", out, re.IGNORECASE)
    bot_m = re.search(r"BOTTOM:\s*(.*)", out, re.IGNORECASE)

    top_text = top_m.group(1).split("\n")[0].strip().upper() if top_m else ""
    bottom_text = bot_m.group(1).split("\n")[0].strip().upper() if bot_m else ""

    top_text = re.sub(r"[^A-Z0-9\s!?\']", "", top_text).strip()
    bottom_text = re.sub(r"[^A-Z0-9\s!?\']", "", bottom_text).strip()

    # If small LLM outputs an unusable caption, grab a matched joke from the exact emotion vault
    if not top_text or not bottom_text or len(top_text) > 28 or len(bottom_text) > 30:
        cluster_roasts = TEMPLATE_SPECIFIC_ROASTS.get(cluster, TEMPLATE_SPECIFIC_ROASTS["clueless_npc"])
        top_text, bottom_text = random.choice(cluster_roasts)

    return top_text, bottom_text

# ---------------------------------------------------------
# 6. Dynamic Non-Cropping Text Renderer
# ---------------------------------------------------------
def burn_caption(image: Image.Image, top_text: str, bottom_text: str) -> Image.Image:
    canvas = image.copy()
    draw = ImageDraw.Draw(canvas)
    width, height = canvas.size
    max_w = int(width * 0.88)

    font_path = r"C:\Windows\Fonts\impact.ttf"
    if not os.path.exists(font_path):
        font_path = "arial.ttf"

    def fit_text_lines(text: str, starting_size: int):
        cur_size = starting_size
        while cur_size >= 14:
            try:
                font = ImageFont.truetype(font_path, cur_size)
            except Exception:
                font = ImageFont.load_default()
                return [text], font

            bbox = draw.textbbox((0, 0), text, font=font)
            if (bbox[2] - bbox[0]) <= max_w:
                return [text], font

            words = text.split()
            if len(words) > 1:
                mid = len(words) // 2
                l1 = " ".join(words[:mid])
                l2 = " ".join(words[mid:])
                b1 = draw.textbbox((0, 0), l1, font=font)
                b2 = draw.textbbox((0, 0), l2, font=font)
                if (b1[2] - b1[0]) <= max_w and (b2[2] - b2[0]) <= max_w:
                    return [l1, l2], font

            cur_size -= 2
        return [text], ImageFont.load_default()

    def draw_lines(lines, font, anchor_y, is_bottom=False):
        line_heights = [draw.textbbox((0, 0), l, font=font)[3] - draw.textbbox((0, 0), l, font=font)[1] for l in lines]
        spacing = 4
        total_h = sum(line_heights) + (len(lines) - 1) * spacing
        cur_y = anchor_y - total_h if is_bottom else anchor_y
        stroke = max(2, getattr(font, "size", 20) // 12)

        for i, l in enumerate(lines):
            bbox = draw.textbbox((0, 0), l, font=font)
            line_w = bbox[2] - bbox[0]
            x = (width - line_w) // 2

            for dx in range(-stroke, stroke + 1):
                for dy in range(-stroke, stroke + 1):
                    draw.text((x + dx, cur_y + dy), l, font=font, fill="black")
            draw.text((x, cur_y), l, font=font, fill="white")
            cur_y += line_heights[i] + spacing

    start_size = max(20, int(width / 12))

    if top_text:
        t_lines, t_font = fit_text_lines(top_text, start_size)
        draw_lines(t_lines, t_font, int(height * 0.04), is_bottom=False)

    if bottom_text:
        b_lines, b_font = fit_text_lines(bottom_text, start_size)
        draw_lines(b_lines, b_font, int(height * 0.94), is_bottom=True)

    return canvas

# ---------------------------------------------------------
# 7. FastAPI Endpoint & Static Server
# ---------------------------------------------------------
@app.post("/generate-caught-meme")
async def generate_caught_meme(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        user_img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid camera frame.")

    v_prompt = (
        "Describe the exact facial emotion and expression of this person in 6 words. "
        "Highlight whether they look guilty, shocked, deadpan, bored, smug, stressed, or goofy."
    )
    with torch.no_grad():
        embeds = vision_model.encode_image(user_img)
        reaction_desc = vision_model.answer_question(embeds, v_prompt, vision_tok).strip()

    # 1. Pull from 1,000+ anchor matrix with duplicate lockout
    matched_meme, cluster = select_dynamic_meme(reaction_desc, top_k=15)

    # 2. Generate joke matched to the template's context
    top_cap, bot_cap = generate_matched_roast(reaction_desc, matched_meme["name"], cluster)

    # 3. Burn caption safely without cropping
    meme_resp = requests.get(matched_meme["url"], timeout=12)
    meme_img = Image.open(io.BytesIO(meme_resp.content)).convert("RGB")
    final_meme = burn_caption(meme_img, top_cap, bot_cap)

    buf = io.BytesIO()
    final_meme.save(buf, format="JPEG", quality=92)

    headers = {
        "X-Meme-Name": urllib.parse.quote(matched_meme["name"]),
        "X-User-Reaction": urllib.parse.quote(reaction_desc),
        "X-Top-Text": urllib.parse.quote(top_cap),
        "X-Bottom-Text": urllib.parse.quote(bot_cap),
        "Access-Control-Expose-Headers": "X-Meme-Name, X-User-Reaction, X-Top-Text, X-Bottom-Text"
    }

    return Response(content=buf.getvalue(), media_type="image/jpeg", headers=headers)

CLIENT_DIST = os.path.join(BASE_DIR, "client", "dist")
if os.path.exists(CLIENT_DIST):
    assets_dir = os.path.join(CLIENT_DIST, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    def serve_root():
        return FileResponse(os.path.join(CLIENT_DIST, "index.html"))

    @app.get("/{catchall:path}")
    def serve_spa(catchall: str):
        file_path = os.path.join(CLIENT_DIST, catchall)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(CLIENT_DIST, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)