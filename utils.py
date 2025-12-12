#202534724 권지우

import cv2


def load_image(path: str):
    """이미지 파일을 읽어오는 함수. 실패하면 FileNotFoundError 발생."""
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Cannot read image from path: {path}")
    return image


def decode_codes(image):
    """
    입력 이미지에서 QR 코드를 디코딩하는 함수.
    반환 형식: dict 리스트
    [
        {
            "data": "decoded string",
            "type": "QRCODE",
            "rect": (x, y, w, h)
        }
    ]
    """
    detector = cv2.QRCodeDetector()

    data, points, _ = detector.detectAndDecode(image)

    results = []
    if data and points is not None:
        pts = points.reshape(-1, 2)  # (4, 2)
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
