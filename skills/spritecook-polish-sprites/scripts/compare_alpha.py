"""Compare SpriteCook binary-alpha cutoffs offline. Requires Pillow; makes no network calls."""

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


def apply_cutoff(source, cutoff):
    if type(cutoff) is not int or not 0 <= cutoff <= 255:
        raise ValueError("Cutoffs must be integers from 0 to 255.")
    result = source.convert("RGBA").copy()
    result.putalpha(result.getchannel("A").point(lambda value: 255 if value >= cutoff else 0))
    return result


def load_rgba(path):
    with Image.open(path) as image:
        if getattr(image, "n_frames", 1) != 1:
            raise ValueError("Use the horizontal PNG spritesheet for animations, not an animated preview.")
        if image.width * image.height > 16_777_216:
            raise ValueError("Image exceeds the local comparison limit of 16 million pixels.")
        return image.convert("RGBA")


def validate_layout(source, editing):
    layout = editing.get("source_layout")
    if layout == "horizontal_spritesheet":
        values = [editing.get(key) for key in ("frame_count", "frame_width", "frame_height")]
        if any(type(value) is not int or value < 1 for value in values):
            raise ValueError("Animation frame layout is missing.")
        count, width, height = values
        if source.size != (count * width, height):
            raise ValueError("Source dimensions do not match the advertised animation layout.")
    elif layout != "image":
        raise ValueError("Unknown source layout. Refresh the asset metadata.")


def preview_image(image, editing):
    crop = editing.get("preview_crop")
    if editing.get("source_layout") != "image" or not crop:
        return image
    bounds = tuple(crop[key] for key in ("left", "top", "right", "bottom"))
    left, top, right, bottom = bounds
    if not (0 <= left < right <= image.width and 0 <= top < bottom <= image.height):
        raise ValueError("Preview crop is outside the preserved source.")
    return image.crop(bounds)


def compare(metadata, source_path, output_dir, *, cutoffs=None, current_path=None, scale=4):
    editing = metadata.get("alpha_editing") or {}
    if not editing.get("available"):
        raise ValueError("This asset has no available preserved source for edge cleanup.")
    if editing.get("processing") != "binary_alpha_v1":
        raise ValueError("This helper supports binary_alpha_v1. Tileset color tolerance needs its dedicated editor.")
    if type(scale) is not int or not 1 <= scale <= 8:
        raise ValueError("Preview scale must be an integer from 1 to 8.")
    current_cutoff = editing.get("current_cutoff")
    if cutoffs is None:
        center = current_cutoff if type(current_cutoff) is int else 96
        cutoffs = [max(1, min(255, center + delta)) for delta in (-48, -24, 0, 24, 48)]
    cutoffs = sorted(set(cutoffs))
    if not 1 <= len(cutoffs) <= 9:
        raise ValueError("Choose between one and nine cutoffs.")
    if any(type(cutoff) is not int or not 0 <= cutoff <= 255 for cutoff in cutoffs):
        raise ValueError("Cutoffs must be integers from 0 to 255.")
    source = load_rgba(source_path)
    validate_layout(source, editing)
    source_alpha = source.getchannel("A").histogram()
    soft_pixels = sum(source_alpha[1:255])
    out = Path(output_dir)
    if out.exists() and any(out.iterdir()):
        raise ValueError("Choose an empty output directory to preserve earlier comparisons.")
    out.mkdir(parents=True, exist_ok=True)
    previews = []
    if current_path:
        current = load_rgba(current_path)
        if editing.get("source_layout") == "horizontal_spritesheet":
            validate_layout(current, editing)
        if current.size == source.size:
            current = preview_image(current, editing)
        previews.append(("Current saved output", current))
    previews.append(("Preserved soft-alpha source", preview_image(source, editing)))
    candidates = []
    for cutoff in cutoffs:
        result = apply_cutoff(source, cutoff)
        filename = f"cutoff-{cutoff}.png"
        result.save(out / filename)
        previews.append((f"Cutoff {cutoff}", preview_image(result, editing)))
        candidates.append({"cutoff": cutoff, "file": filename, "opaque_pixels": result.getchannel("A").histogram()[255]})

    # Bound the contact sheet while keeping full-resolution candidates intact.
    width = max(160, min(768, max(image.width * scale for _, image in previews)))
    height = min(768, max(image.height * scale for _, image in previews))
    row_height = height + 28
    sheet = Image.new("RGB", (width * 2 + 24, row_height * len(previews)), "#777777")
    draw = ImageDraw.Draw(sheet)
    for row, (label, image) in enumerate(previews):
        factor = min(scale, width / image.width, height / image.height)
        thumb = image.resize((max(1, round(image.width * factor)), max(1, round(image.height * factor))), Image.Resampling.NEAREST)
        draw.text((8, row * row_height + 5), label + " | light / dark", fill="white")
        for column, background in enumerate(("#eeeeee", "#222222")):
            panel = Image.new("RGBA", (width, height), background)
            panel.alpha_composite(thumb, ((width - thumb.width) // 2, (height - thumb.height) // 2))
            sheet.paste(panel.convert("RGB"), (8 + column * (width + 8), row * row_height + 24))
    sheet.save(out / "comparison.png")
    warnings = []
    if not soft_pixels:
        warnings.append("The source has no soft-alpha pixels. All positive cutoffs produce the same alpha; compare that result with the current output.")
    if 0 in cutoffs:
        warnings.append("Cutoff 0 makes even zero-alpha pixels opaque; inspect it carefully.")
    report = {
        "asset_id": metadata.get("asset_id") or metadata.get("id"),
        "processing": editing["processing"],
        "source_sha256": hashlib.sha256(Path(source_path).read_bytes()).hexdigest(),
        "source_size": list(source.size),
        "current_cutoff": current_cutoff,
        "soft_alpha_pixels": soft_pixels,
        "candidates": candidates,
        "warnings": warnings,
        "comparison": "comparison.png",
    }
    # Signed URLs and local source paths are deliberately omitted from this report.
    (out / "comparison.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, required=True, help="Saved get_asset_metadata object containing alpha_editing")
    parser.add_argument("--source", type=Path, required=True, help="Downloaded alpha_editing.source_url PNG")
    parser.add_argument("--current", type=Path, help="Optional current sprite PNG or animation spritesheet PNG")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cutoffs", type=int, nargs="+")
    parser.add_argument("--scale", type=int, default=4)
    args = parser.parse_args()
    try:
        report = compare(json.loads(args.metadata.read_text(encoding="utf-8-sig")), args.source, args.output_dir,
                         cutoffs=args.cutoffs, current_path=args.current, scale=args.scale)
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(2, f"{exc}\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
