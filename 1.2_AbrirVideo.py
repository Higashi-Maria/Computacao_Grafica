import cv2
# FUnção VideoCapture

cap = cv2.VideoCapture("videos\dog.mp4")

while(True):
    ret, frame = cap.read()

    cv2.imshow("Video do dog", frame)

    # waitKey para videos
    if cv2.waitKey(20) & 0xFF == ord('d'):
        break
    #215 assertion failed

cap.released()
cv2.destroyAllWindows()