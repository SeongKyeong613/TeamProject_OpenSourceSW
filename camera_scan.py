# 202534804 박성경
# camera.py

import cv2
from qr_utils import decode_codes_multi, draw_results


def camera_scan():
    # 기본 카메라(0번) 사용
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Camera not found!")
        return

    print("[INFO] Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Cannot read frame.")
            break

        # QR 코드 인식
        results = decode_codes_multi(frame)

        # 결과를 화면에 표시
        frame_with_boxes = draw_results(frame, results)

        # 화면 출력
        cv2.imshow("QR Scanner - Camera", frame_with_boxes)

        # q 키 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
