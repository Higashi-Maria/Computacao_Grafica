import cv2
import time

# Ativa a câmera
cap = cv2.VideoCapture(0)
prev_time = time.time()

# (ret) Variável que não ocupa espaço de memória
while True:
    ret, frame = cap.read()
    if not ret:
        break

    curr_time = time.time()
    fps = 1.0/(curr_time - prev_time) if curr_time != prev_time \
        else 0.0
    prev_time = curr_time

    # Captura FPS e limita eles
    cv2.putText(frame, f'FPS: {fps:.1f}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Camera Aberta: ', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

                