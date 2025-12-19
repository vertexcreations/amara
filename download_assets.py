import os
import requests
import re

def download_file(url, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {save_path}")
        return response.content
    else:
        print(f"Failed to download: {url}")
        return None

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, 'static')

    # 1. Download Boxicons
    print("Downloading Boxicons...")
    boxicons_css_url = "https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css"
    boxicons_css_path = os.path.join(static_dir, 'vendor', 'boxicons', 'css', 'boxicons.min.css')
    
    css_content = download_file(boxicons_css_url, boxicons_css_path)
    
    if css_content:
        # Parse fonts from CSS
        css_text = css_content.decode('utf-8')
        font_urls = re.findall(r'url\([\'"]?(\.\./fonts/[^\'"\)]+)[\'"]?\)', css_text)
        
        for relative_url in font_urls:
            # The CSS refers to ../fonts/..., so we need to construct the full URL
            # Original CSS is at .../css/boxicons.min.css
            # Fonts are at .../fonts/
            
            # Extract filename and sanitize (remove query params and fragments)
            filename = os.path.basename(relative_url).split('?')[0].split('#')[0]
            
            # Construct source URL (unpkg structure)
            # https://unpkg.com/boxicons@2.1.4/fonts/boxicons.woff2
            # Note: The relative URL might have query params, but we want the clean file from unpkg usually, 
            # OR we need to fetch the exact URL but save as clean filename.
            # Let's try fetching the clean filename first as unpkg supports it.
            font_source_url = f"https://unpkg.com/boxicons@2.1.4/fonts/{filename}"
            
            # Construct local path
            # static/vendor/boxicons/fonts/filename
            font_save_path = os.path.join(static_dir, 'vendor', 'boxicons', 'fonts', filename)
            
            download_file(font_source_url, font_save_path)
            
            # We also need to update the CSS to point to the clean filename
            # But we are parsing the CSS content which we already wrote to disk? 
            # No, we wrote the original content. We should probably update the CSS file too.
            # However, the CSS refers to the file with query params. 
            # If we save it without them, the browser might not find it if we don't update the CSS.
            # But wait, the browser resolves the URL. If the file on disk is `boxicons.svg`, 
            # and CSS asks for `boxicons.svg?#boxicons`, the server (Flask) needs to serve `boxicons.svg`.
            # Flask static serving usually ignores query params for file lookup.
            # So saving as `boxicons.svg` should be fine.


    # 2. Download Google Fonts (Outfit)
    # We need to download the CSS first, then the font files referenced in it.
    # Note: Google Fonts serves different CSS based on User-Agent. We'll use a standard one.
    print("\nDownloading Google Fonts (Outfit)...")
    google_fonts_url = "https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap"
    fonts_css_path = os.path.join(static_dir, 'css', 'fonts.css')
    
    # Fake a user agent to get woff2
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(google_fonts_url, headers=headers)
    if response.status_code == 200:
        css_text = response.text
        
        # Find all font URLs
        # url(https://fonts.gstatic.com/s/outfit/v11/QGYyz_MVcBeNP4NjuGObqx1XmO1I4TC0C4G-FiU.woff2)
        font_matches = re.findall(r'url\((https://fonts\.gstatic\.com/[^)]+)\)', css_text)
        
        local_css_text = css_text
        
        for i, font_url in enumerate(set(font_matches)): # Use set to avoid duplicates
            filename = f"outfit-{i}.woff2"
            save_path = os.path.join(static_dir, 'fonts', 'outfit', filename)
            
            download_file(font_url, save_path)
            
            # Replace URL in CSS with local path
            # The CSS will be in static/css/fonts.css
            # The fonts will be in static/fonts/outfit/
            # So relative path is ../fonts/outfit/filename
            local_css_text = local_css_text.replace(font_url, f"../fonts/outfit/{filename}")
            
        with open(fonts_css_path, 'w', encoding='utf-8') as f:
            f.write(local_css_text)
        print(f"Saved local fonts CSS to {fonts_css_path}")
        
    else:
        print("Failed to download Google Fonts CSS")

if __name__ == "__main__":
    main()
