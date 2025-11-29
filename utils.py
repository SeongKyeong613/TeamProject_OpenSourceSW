"""
202534724 권지우
"""

import cv2
from pyzbar.pyzbar import decode


def load_image(path):
   
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Cannot read image from path: {path}")
    return image


def decode_codes(image):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    decoded = decode(gray)
    results = []

    for d in decoded:
        data = d.data.decode("utf-8", errors="ignore")
        code_type = d.type
        rect = d.rect  # (left, top, width, height)

        results.append({
            "data": data,
            "type": code_type,
            "rect": (rect.left, rect.top, rect.width, rect.height),
        })

    return results
