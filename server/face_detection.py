import cv2

def detect_and_draw_features(image_path):
    print("🟡 מתחיל לעבד את התמונה...")

    image = cv2.imread(image_path)
    if image is None:
        print("❌ לא ניתן לקרוא את הקובץ:", image_path)
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # טוענים את הקלאסיפיירים
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
    mouth_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

    # מזהים פנים
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    print(f"🧑‍🦰 נמצאו {len(faces)} פנים")

    for (x, y, w, h) in faces:
        face_roi_gray = gray[y:y+h, x:x+w]
        face_roi_color = image[y:y+h, x:x+w]

        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # עיניים
        eyes = eye_cascade.detectMultiScale(face_roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
        print(f"👁️ נמצאו {len(eyes)} עיניים")
        for (ex, ey, ew, eh) in eyes:
            center = (x + ex + ew // 2, y + ey + eh // 2)
            radius = int(round((ew + eh) * 0.25))
            cv2.circle(image, center, radius, (0, 255, 0), 2)

        # אף - סינון תוצאות כפולות, זיהוי רק את האף הגדול ביותר
        noses = nose_cascade.detectMultiScale(face_roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        print(f"👃 נמצאו {len(noses)} אפים")
        if len(noses) > 0:  # אם נמצאו אפים
            largest_nose = max(noses, key=lambda n: n[2] * n[3])  # בחר את האף הגדול ביותר
            nx, ny, nw, nh = largest_nose
            center = (x + nx + nw // 2, y + ny + nh // 2)
            radius = int(round((nw + nh) * 0.25))
            cv2.circle(image, center, radius, (0, 0, 255), 2)

        # פה - סינון פיות קטנים מדי
        mouths = mouth_cascade.detectMultiScale(face_roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        print(f"👄 נמצאו {len(mouths)} פיות")
        for (mx, my, mw, mh) in mouths:
            if mh > 30 and mw > 30:  # סינון דינמי
                center = (x + mx + mw // 2, y + my + mh // 2)
                radius = int(round((mw + mh) * 0.25))
                cv2.circle(image, center, radius, (255, 0, 255), 2)


    # שומרים ומציגים
    cv2.imwrite(image_path, image)
    print("✅ התמונה המקורית עודכנה ונשמרה שוב כ:", image_path)

    cv2.imshow('Processed Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# קריאה לפונקציה
detect_and_draw_features("captured_image.jpg")
