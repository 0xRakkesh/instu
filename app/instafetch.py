from pathlib import Path
import time
import urllib.request
import instaloader
from utils import url_to_shortcode  # type: ignore

# Configure Instaloader with sleep disabled for maximum speed
L = instaloader.Instaloader()
L.context.sleep = False


def download_insta_post(insta_url: str, storage_path: Path):
    
    start_total = time.perf_counter()

    # Ensure URL is strictly a post (/p/)
    shortcode = url_to_shortcode(insta_url)
    if not shortcode:
        print("Invalid URL: Only Instagram posts with '/p/' are supported.")
        return

    try:
        # Query post metadata
        print(f"\n[1/3] Fetching post info for: {shortcode}...")
        t_meta_start = time.perf_counter()
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        t_meta = time.perf_counter() - t_meta_start
        print(f"Metadata fetched in {t_meta:.2f} seconds")

        # Prepare target destination folder
        target_dir = storage_path / shortcode
        target_dir.mkdir(parents=True, exist_ok=True)

        # Collect image URLs 
        images_to_download = []
        if post.mediacount > 1:
            print(f"[2/3] Detected Carousel ({post.mediacount} slides)...")
            for idx, node in enumerate(post.get_sidecar_nodes(), start=1):
                images_to_download.append((f"{shortcode}_{idx}.jpg", node.display_url))
        else:
            images_to_download.append((f"{shortcode}.jpg", post.url))

        # Stream images directly via HTTP
        print(f"[3/3] Downloading {len(images_to_download)} images...")
        for filename, img_url in images_to_download:
            dest_file = target_dir / filename
            urllib.request.urlretrieve(img_url, dest_file)
            print(f"Saved {filename} ")

        total_time = time.perf_counter() - start_total

        print(f"\nAll images saved to: {target_dir}")
        print(f"Total time elapsed: {total_time:.2f} seconds")
        return target_dir

    except Exception as e:
        print(f"\nError downloading post: {e}")
