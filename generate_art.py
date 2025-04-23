from openai import OpenAI
import requests
import os
import hashlib
from utils.api_keys import OPENAI_API_KEY

print("[DEBUG] OpenAI key in use:", OPENAI_API_KEY[:8] + "..." if OPENAI_API_KEY else "None")

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_art_from_headline(headline, out_dir="./static/art/"):
    try:
        os.makedirs(out_dir, exist_ok=True)
    except Exception as e:
        print(f"[Error] Failed to create directory: {e}")
        return None

    # Ghibli-style art prompt
    prompt = (
        f"Create a peaceful and imaginative digital painting inspired by this news headline: '{headline}'. "
        f"This artwork is intended for a calming, educational media display that visualizes world events through the lens of beauty and storytelling. "
        f"Use the style of Studio Ghibli, with soft lighting, rich color palettes, dreamy landscapes, and painterly textures. "
        f"Do not depict real people or literal events—abstract the scene into something symbolic, whimsical, and emotionally resonant."
    )

    hash_name = hashlib.md5(prompt.encode()).hexdigest() + ".png"
    out_path = os.path.join(out_dir, hash_name)

    print("\n[Prompt being used]\n", prompt)
    print("[Expected output path]:", out_path)

    if os.path.exists(out_path):
        print("[Cache hit] Using existing art.")
        return out_path

    try:
        print("[Generating] Ghibli-style art using DALL·E 3...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        if not response or not hasattr(response, 'data') or not response.data:
            print("[Warning] OpenAI response was empty or invalid.")
            return None

        image_url = response.data[0].url
        print("[Image URL]:", image_url)

        img_data = requests.get(image_url).content
        with open(out_path, 'wb') as handler:
            handler.write(img_data)

        print("[Success] Image saved to:", out_path)
        return out_path

    except Exception as e:
        print("[Error] Failed to generate/save image:", type(e), e)
        return None
