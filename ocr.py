import cv2
import pytesseract
import api

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
cap = cv2.VideoCapture(0) 

def ocr_setup(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #greyscale
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV) #threshold

    #x, y, w, h = 100, 100, 300, 300
    #roi = thresh[y:y+h, x:x+w]

    text = pytesseract.image_to_string(thresh, lang='eng') #ocr using pytesseract 
    return text

def camera_setup():
    W=1024
    H=1024
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) # doesnt work without this for me
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
    # cap.set(cv2.CAP_PROP_FPS, 30)

def main():
    camera_setup()
    if not cap.isOpened():
        print("cam not found")
        return

    frame_count = 0
    process_every_n_frames = 30 

    while True:
        ret, frame= cap.read()
        if not ret:
            break
        cv2.imshow('ocr-mtg', frame)

        # OCR process_every_n_frames 
        if frame_count % process_every_n_frames == 0:
            text = ocr_setup(frame)
            print("text detected:" + text)
            api.autocomplete(text) # PoC of what i intend to do
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()