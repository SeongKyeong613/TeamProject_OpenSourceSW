import argparse
import cv2
from utils import load_image, decode_codes


def draw_results(image, results):
    """
    디코딩된 결과를 기반으로 이미지 위에 박스와 텍스트를 그려주는 함수.
    """
    for r in results:
        x, y, w, h = r["rect"]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = f'{r["type"]}: {r["data"]}'
        cv2.putText(image, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
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

def scan_camera():
    """
    OpenCV QRCodeDetector를 사용한 웹캠 실시간 QR 스캔
    """
    detector = cv2.QRCodeDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Cannot open camera.")
        return

    print("[INFO] Webcam QR scan started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data, bbox, _ = detector.detectAndDecode(frame)

        if bbox is not None and data:
            bbox = bbox.astype(int)
            cv2.polylines(frame, [bbox], True, (0, 255, 0), 2)
            cv2.putText(frame, data, (bbox[0][0][0], bbox[0][0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            print(f"[QR] {data}")

        cv2.imshow("Webcam QR Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def parse_args():
    """
    커맨드라인 옵션 파서.
    --camera 옵션 추가
    """
    parser = argparse.ArgumentParser(
        description="Barcode / QR code scanner (image mode / camera mode)"
    )
    parser.add_argument("--image", help="Path to input image file")
    parser.add_argument("--camera", action="store_true",
                        help="Use webcam realtime QR scanner")
    parser.add_argument("--output", default=None, help="Path to save result image")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.camera:
        scan_camera()
    elif args.image:
        scan_image(args.image, show=True, save_path=args.output)
    else:
        print("[ERROR] Provide either --image or --camera option.")


if __name__ == "__main__":
    main()
