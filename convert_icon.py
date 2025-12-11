from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
import os

def convert_svg_to_ico(svg_path, ico_path):
    print(f"Converting {svg_path} to {ico_path}...")
    
    # 1. Convert SVG to ReportLab Drawing
    drawing = svg2rlg(svg_path)
    
    # 2. Render to temporary PNG
    png_path = "temp_icon.png"
    renderPM.drawToFile(drawing, png_path, fmt="PNG")
    
    # 3. Convert PNG to ICO using Pillow
    img = Image.open(png_path)
    
    # Create a high-quality icon with multiple sizes
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save(ico_path, format='ICO', sizes=icon_sizes)
    
    # Clean up
    img.close()
    os.remove(png_path)
    print("Conversion complete!")

if __name__ == "__main__":
    svg_file = os.path.join("static", "store_ico.svg")
    ico_file = os.path.join("static", "icon.ico")
    
    if os.path.exists(svg_file):
        try:
            convert_svg_to_ico(svg_file, ico_file)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"File not found: {svg_file}")
