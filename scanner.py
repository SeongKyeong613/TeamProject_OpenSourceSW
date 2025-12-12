
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
        
def scan_camera():
    """
    웹캠 실시간 QR 코드 스캔 (OpenCV QRCodeDetector 사용)
    """
    detector = cv2.QRCodeDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Cannot open camera.")
        return

    print("[INFO] Webcam QR scan started. (Press 'q' to quit)")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to read frame.")
            break

        # QR 코드 디코딩 (OpenCV 전용)
        data, bbox, _ = detector.detectAndDecode(frame)

        if bbox is not None and data:
            # QR 박스 그리기
            bbox = bbox.astype(int)
            cv2.polylines(frame, [bbox], True, (0, 255, 0), 2)

            # 텍스트 표시
            cv2.putText(
                frame, data, 
                (bbox[0][0][0], bbox[0][0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 255, 0), 2
            )

            print(f"[QR] {data}")

        cv2.imshow("Webcam QR Scanner", frame)

        # q 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def parse_args():
    
    parser = argparse.ArgumentParser(
        description="Barcode / QR code scanner (image mode)"
    )
    parser.add_argument(
        "--image",
        required=True,
        help="Path to input image file"
    ) 
    parser.add_argument(
        "--camera",
        action="store_true",
        help="Use webcam realtime QR scanner"
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
