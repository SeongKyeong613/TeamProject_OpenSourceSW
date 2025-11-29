#202534724 권지우

import argparse
import cv2

from utils import load_image, decode_codes


def draw_results(image, results):
    """
    디코딩된 결과를 기반으로 이미지 위에 박스와 텍스트를 그려주는 함수.
    """
    for r in results:
        x, y, w, h = r["rect"]

        cv2.rectangle(image, (x, y), (x + w, y + h),
                      (0, 255, 0), 2)

        text = f'{r["type"]}: {r["data"]}'
        cv2.putText(image, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 1)

    return image


def scan_image(path, show=True, save_path=None):
    """
    단일 이미지 파일에서 바코드/QR 코드를 스캔하는 메인 함수.
    """
    image = load_image(path)
    results = decode_codes(image)

    if not results:
        print("[INFO] No barcodes/QR codes found.")
    else:
        print("[INFO] Detected codes:")
        for idx, r in enumerate(results, start=1):
            print(f"  #{idx} [{r['type']}]: {r['data']}")

    image_with_boxes = draw_results(image, results)

    if save_path:
        cv2.imwrite(save_path, image_with_boxes)
        print(f"[INFO] Saved output image to: {save_path}")

    if show:
        cv2.imshow("Scan Result", image_with_boxes)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def parse_args():
    """
    커맨드라인 옵션 파서.
    A2가 나중에 --camera 옵션 추가할 수 있도록 구조 유지.
    """
    parser = argparse.ArgumentParser(
        description="Barcode / QR code scanner (image mode)"
    )
    parser.add_argument(
        "--image",
        required=True,
        help="Path to input image file"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to save result image"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    scan_image(args.image, show=True, save_path=args.output)


if __name__ == "__main__":
    main()

    main()
