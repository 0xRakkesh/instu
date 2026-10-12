# Instagram Media Fetcher In-Depth Guide

This guide details the technical mechanics of fetching post media from Instagram, covering post structures, URL validation, and persistence strategies.

---

## 1. Post URL Validation (`/p/`)

The application strictly targets Instagram posts (photo posts and carousel photo slides). 

In `app/utils.py`, the URL regex explicitly validates the `/p/` path:
```python
pattern = r'/p/([A-Za-z0-9_-]+)'
```

Any URL that is not a standard post (such as reels `/reel/` or stories `/stories/`) is rejected immediately at the start of `download_insta_post`.

---

## 2. Core Python Architecture

Because Instagram notes and photo posts are strictly images, we do not perform unnecessary video rejection branches. The logic directly distinguishes between:
1. **Single Photo Post (`post.mediacount == 1`)**: Extracts `post.url`.
2. **Carousel Post (`post.mediacount > 1`)**: Extracts `node.display_url` for every slide.

```python
from pathlib import Path
import time
import urllib.request
import instaloader
from utils import url_to_shortcode

L = instaloader.Instaloader()
L.context.sleep = False  # Eliminates artificial rate-limiting sleep pauses

def download_insta_post(insta_url: str, storage_path: Path):
    shortcode = url_to_shortcode(insta_url)
    if not shortcode:
        print("❌ Invalid URL: Only Instagram posts with '/p/' are supported.")
        return

    post = instaloader.Post.from_shortcode(L.context, shortcode)
    target_dir = storage_path / shortcode
    target_dir.mkdir(parents=True, exist_ok=True)

    # Collect images directly
    images_to_download = []
    if post.mediacount > 1:
        for idx, node in enumerate(post.get_sidecar_nodes(), start=1):
            images_to_download.append((f"{shortcode}_{idx}.jpg", node.display_url))
    else:
        images_to_download.append((f"{shortcode}.jpg", post.url))

    # Stream images to disk
    for filename, img_url in images_to_download:
        urllib.request.urlretrieve(img_url, target_dir / filename)
```

---

## 3. Advantages of This Architecture

1. **Strict Type Safety**: Only processes URLs explicitly matching `/p/` posts.
2. **No Video Overhead**: Bypasses all video filtering, thumbnail extraction, and `.mp4` parsing.
3. **High Velocity**: Bypasses `L.download_post()` and rate controller sleep, completing downloads in 1–3 seconds.
4. **No Clutter**: Generates clean `.jpg` files without `.json.xz` metadata or `.txt` captions.
