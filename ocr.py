import cv2
import pytesseract
import api
import re

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
cap = cv2.VideoCapture(0) 

def ocr_setup(frame):
    color = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #not needed rn
    #x, y, w, h = 100, 100, 300, 300
    #roi = thresh[y:y+h, x:x+w]

    # reduces noise 
    # blurred = cv2.GaussianBlur(color, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        color, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    text = pytesseract.image_to_string(processed, lang='eng')
    return text

def camera_setup():
    W=600
    H=600
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) # doesnt work without this for me
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
    cap.set(cv2.CAP_PROP_FPS, 60)

# this displays the preprocessed frame
def preprocess_frame(frame):
    color = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # reduces noise 
    # blurred = cv2.GaussianBlur(color, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        color, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return processed


def main():
    camera_setup()
    if not cap.isOpened():
        print("cam not found")
        return

    frame_count = 0
    process_every_n_frames = 30

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # preprocessed frame so you can se what it looks like
        processed_frame = preprocess_frame(frame)
        
        cv2.imshow('Original Camera', frame)
        cv2.imshow('Processed Camera', processed_frame)

        # OCR process_every_n_frames 
        if frame_count % process_every_n_frames == 0:
            text = ocr_setup(frame)
            print("text detected:" + text)
            #api.autocomplete(text) # PoC of what i intend to do

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()