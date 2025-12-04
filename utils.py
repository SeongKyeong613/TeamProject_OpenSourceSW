#202534724 권지우

import cv2


def load_image(path):
    
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Cannot read image from path: {path}")
    return image


def decode_codes(image):
    
    detector = cv2.QRCodeDetector()

    data, points, _ = detector.detectAndDecode(image)

    results = []

    if data and points is not None:
        pts = points.reshape(-1, 2)
        
        xs = [int(p[0]) for p in pts]
        ys = [int(p[1]) for p in pts]

        x, y = min(xs), min(ys)
        w, h = max(xs) - x, max(ys) - y

        results.append({
            "data": data,
            "type": "QRCODE",
            "rect": (x, y, w, h),
        })

    return results
