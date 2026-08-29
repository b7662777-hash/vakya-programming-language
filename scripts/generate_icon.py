"""Script to generate professional multi-resolution application icons for Vākya."""

import os
from PIL import Image, ImageDraw, ImageFont


def create_vakya_icon(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Padding & corner radius
        pad = max(1, int(size * 0.06))
        radius = max(2, int(size * 0.22))
        
        # Outer glowing / gold border
        draw.rounded_rectangle(
            [pad, pad, size - pad, size - pad],
            radius=radius,
            fill=(20, 24, 40, 255),
            outline=(245, 158, 11, 255),  # Amber gold
            width=max(1, int(size * 0.04)),
        )

        # Inner subtle gradient / accent block
        inner_pad = pad + max(2, int(size * 0.08))
        draw.rounded_rectangle(
            [inner_pad, inner_pad, size - inner_pad, size - inner_pad],
            radius=max(1, radius - 2),
            fill=(30, 36, 60, 255),
            outline=(217, 119, 6, 180),
            width=1,
        )

        # Draw stylized Sanskrit / Roman 'V' Monogram
        # Use geometric coordinates to guarantee crisp rendering across all sizes
        cx = size / 2.0
        cy = size / 2.0
        w = size * 0.38
        h = size * 0.44

        # Coordinate points for sharp modern V glyph
        top_y = cy - h / 2.0
        bottom_y = cy + h / 2.0
        left_x = cx - w / 2.0
        right_x = cx + w / 2.0
        thick = max(1.5, size * 0.08)

        # Left diagonal
        draw.line([(left_x, top_y), (cx, bottom_y)], fill=(251, 191, 36, 255), width=int(thick))
        # Right diagonal
        draw.line([(cx, bottom_y), (right_x, top_y)], fill=(245, 158, 11, 255), width=int(thick))
        # Top crown bar (Sanskrit Shirorekha style accent)
        draw.line([(left_x - thick * 0.5, top_y), (right_x + thick * 0.5, top_y)], fill=(252, 211, 77, 255), width=max(1, int(thick * 0.6)))

        images.append(img)

    # Save highest resolution PNG
    png_path = os.path.join(output_dir, "vakya.png")
    images[-1].save(png_path, format="PNG")
    print(f"Generated PNG icon: {png_path}")

    # Save multi-resolution ICO
    ico_path = os.path.join(output_dir, "vakya.ico")
    images[-1].save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[:-1],
    )
    print(f"Generated ICO icon: {ico_path}")


if __name__ == "__main__":
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    resources_dir = os.path.join(repo_root, "resources")
    create_vakya_icon(resources_dir)
