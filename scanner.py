
import argparse
import cv2

from utils import load_image, decode_codes


def draw_results(image, results):
    """디코딩 결과를 이미지 위에 박스/텍스트로 시각화."""
    for r in results:
        x, y, w, h = r["rect"]

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        text = f'{r["type"]}: {r["data"]}'
        cv2.putText(
            image,
            text,
            (x, max(0, y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )
    return image


def scan_image(path, show=True, save_path=None):
    """단일 이미지 파일에서 QR 코드를 스캔."""
    image = load_image(path)
    results = decode_codes(image)

    if not results:
        print("[INFO] No QR codes found.")
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

def scan_camera():
    """
    (A2 담당) 웹캠 실시간 스캔 함수 자리.
    A2가 구현하면 main()에서 바로 호출되도록 설계.
    """
    print("[INFO] Camera mode is selected. (A2 will implement scan_camera())")


def parse_args():
    """--image 또는 --camera 중 하나를 받는 옵션 파서."""
def parse_args():
    
    parser = argparse.ArgumentParser(
        description="QR code scanner (image/camera mode)"
    )
    parser.add_argument(
        "--image",
        default=None,
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
        help="Path to save result image (image mode only)"
    )
    parser.add_argument(
        "--camera",
        action="store_true",
        help="Use webcam for real-time scanning"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # 카메라 모드 우선
    if args.camera:
        scan_camera()
        return

    # 이미지 모드
    if args.image:
        scan_image(args.image, show=True, save_path=args.output)
        return

    # 옵션 없을 때
    print("[ERROR] You must provide --image <path> or --camera")


if __name__ == "__main__":
    main()
