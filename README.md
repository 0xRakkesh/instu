# Instagram Post Scraper & Media Fetcher

A comprehensive guide and reference documentation for fetching Instagram post images and media in Python using free, open-source tooling.

---

## 📌 Overview

This project provides an approach to fetch public Instagram post images (including single images and multi-image carousels/sidecars) using Python without requiring paid API services or complex official Facebook App review approval.

---

## 🛠 Recommended Library: `instaloader`

[`instaloader`](https://instaloader.github.io/) is an open-source, free Python library that interacts with Instagram's public endpoints.

### Key Capabilities
- **Zero Cost**: No paid API keys or subscriptions required.
- **No Login Required for Public Posts**: Can fetch images and media from public posts anonymously.
- **Carousel Support**: Automatically detects and extracts all slide images from multi-photo posts.
- **Flexible**: Allows either extracting raw CDN image URLs or downloading the files directly to your storage.

---

## 🚀 Quick Setup & Installation

Ensure you have Python 3.8+ installed.

```bash
pip install instaloader
```

*(Optional) If you are using a virtual environment:*
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/WSL
pip install instaloader
```

---

## 💻 Code Reference

Below is a complete, modular script (`fetch_instagram.py`) to extract media URLs or download images from any Instagram post:

```python
import re
import instaloader

def extract_shortcode(url_or_code: str) -> str:
    """
    Extracts the shortcode from standard Instagram URLs.
    Supports /p/, /reel/, or raw shortcode strings.
    Example: https://www.instagram.com/p/C_abc123XYZ/ -> C_abc123XYZ
    """
    match = re.search(r"instagram\.com/(?:p|reel)/([A-Za-z0-9_-]+)", url_or_code)
    if match:
        return match.group(1)
    return url_or_code.strip("/ ")


def fetch_instagram_images(post_url_or_shortcode: str, download_to_folder: bool = False):
    """
    Fetches image URLs for a given Instagram post or carousel.
    
    Args:
        post_url_or_shortcode (str): The full URL or shortcode of the post.
        download_to_folder (bool): If True, downloads the files to disk.
    
    Returns:
        list[str]: A list of direct image URLs.
    """
    # Initialize Instaloader with extraneous features disabled for speed
    L = instaloader.Instaloader(
        download_pictures=download_to_folder,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_history=False,
    )

    shortcode = extract_shortcode(post_url_or_shortcode)
    print(f"Fetching post shortcode: {shortcode}...")

    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        image_urls = []

        # Case 1: Carousel / Multi-item post
        if post.mediacount > 1:
            print(f"Detected Carousel Post with {post.mediacount} slides:")
            for idx, node in enumerate(post.get_sidecar_nodes(), start=1):
                if not node.is_video:
                    image_urls.append(node.display_url)
                    print(f"  [Slide {idx}] {node.display_url}")
                else:
                    print(f"  [Slide {idx}] Video slide (skipped)")
        # Case 2: Single image post
        else:
            if not post.is_video:
                image_urls.append(post.url)
                print(f"Single Image URL: {post.url}")
            else:
                print("Note: This post is a video/reel, not a static image.")

        # Download to disk if requested
        if download_to_folder and image_urls:
            target_dir = f"instagram_{shortcode}"
            print(f"\nDownloading to disk under '{target_dir}'...")
            L.download_post(post, target=target_dir)
            print("Download complete.")

        return image_urls

    except instaloader.exceptions.ProfileNotExistsException:
        print("Error: Account or post is private, deleted, or does not exist.")
    except instaloader.exceptions.QueryReturnedBadRequestException:
        print("Error: Instagram returned 400 Bad Request (rate limit or IP challenge).")
    except Exception as err:
        print(f"Error fetching post: {err}")
        return []


if __name__ == "__main__":
    # Test with a public Instagram post URL
    sample_url = "https://www.instagram.com/p/SAMPLE_SHORTCODE/"
    
    # Set download_to_folder=True if you want local JPG files
    results = fetch_instagram_images(sample_url, download_to_folder=False)
```

---

## ⚠️ Important Considerations & Best Practices

### 1. Temporary Nature of Direct CDN URLs
Instagram's direct image URLs (`https://scontent...cdninstagram.com/...`) contain signed authorization query parameters (`?_nc_cat=...&oh=...`).
* These links **expire within a few hours or days**.
* **Best practice**: If you are displaying these images in your application permanently, download the image and store it in your own storage (local disk, AWS S3, Cloudinary, etc.).

### 2. Rate Limits & IP Throttling (HTTP 429)
Instagram enforces strict anti-bot protections:
* Avoid aggressive scraping or querying dozens of posts in rapid succession.
* Add delays between requests:
  ```python
  import time
  time.sleep(3)  # Wait 3-5 seconds between requests
  ```
* Cloud servers (AWS, GCP, DigitalOcean) are frequently blocked by Instagram. Running locally or using residential proxies avoids this.

### 3. Login Sessions (If Needed)
For private accounts you follow or if Instagram starts demanding authentication:
* Log in once using the terminal:
  ```bash
  instaloader --login=your_instagram_username
  ```
* Load the session in code:
  ```python
  L.load_session_from_file("your_instagram_username")
  ```

---

## 📊 Comparison with Alternatives

| Method | Cost | Setup Complexity | Longevity / Stability | When to Use |
| :--- | :--- | :--- | :--- | :--- |
| **`instaloader` (Python)** | Free | Very low | Moderate (dependent on IG frontend) | Best for free personal projects & quick image fetching |
| **Official Instagram Graph API** | Free | High (Meta App review, Business account required) | Very high | Best for enterprise apps & managing your own brand accounts |
| **Managed Scraper (Apify / RapidAPI)** | Paid | Low | High (handles rotating proxies) | Best for commercial apps scraping competitor data at scale |
