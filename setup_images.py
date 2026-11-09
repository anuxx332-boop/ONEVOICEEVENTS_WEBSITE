"""
Run this script once to copy the team photos into the website assets folder.
Double-click this file OR run: python setup_images.py
"""
import shutil, os, base64

src_dir = r"C:\Users\PASAN\.gemini\antigravity\brain\1ce97fb2-c3a1-4f44-89d5-62a7617f8294\.user_uploaded"
dest_dir = r"C:\Users\PASAN\OneDrive\Desktop\one voice events web\assets\images"
js_dir   = r"C:\Users\PASAN\OneDrive\Desktop\one voice events web\js"

os.makedirs(dest_dir, exist_ok=True)

mapping = {
    "media_1794216286994_73185d49.jpg": "lochana.jpg",
    "media_1794216286994_ba802ca3.jpg": "anusara.jpg",
}

copied = []
for src_name, dst_name in mapping.items():
    src_path = os.path.join(src_dir, src_name)
    dst_path = os.path.join(dest_dir, dst_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        copied.append(dst_name)
        print(f"[OK] Copied {dst_name}")
    else:
        print(f"[ERR] Not found: {src_path}")

# Also create a JS file with base64 fallback if copy fails
if len(copied) < 2:
    print("Trying base64 embed fallback...")
    js_lines = ["// Auto-generated team photo fallback\n(function(){\n"]
    ids = {"lochana.jpg": "lochana-img", "anusara.jpg": "anusara-img"}
    
    for src_name, dst_name in mapping.items():
        src_path = os.path.join(src_dir, src_name)
        if os.path.exists(src_path):
            with open(src_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            elem_id = ids[dst_name]
            js_lines.append(f'  document.querySelectorAll("img[data-team=\'{dst_name}\']").forEach(function(el){{ el.src="data:image/jpeg;base64,{b64}"; }});\n')
    
    js_lines.append("})();\n")
    
    out_js = os.path.join(js_dir, "team_photos.js")
    with open(out_js, "w") as f:
        f.writelines(js_lines)
    print(f"[OK] Created fallback JS: {out_js}")

print("\nDone.")
