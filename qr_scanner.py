import cv2
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

class QRCodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")

        self.video_source = 0  # Default camera

        # Create video capture object
        self.cap = cv2.VideoCapture(self.video_source)

        # Create a canvas for displaying the video feed
        self.canvas = tk.Canvas(root, width=self.cap.get(3), height=self.cap.get(4))
        self.canvas.pack()

        # Create a label for displaying QR code information
        self.label_qr_info = ttk.Label(root, text="")
        self.label_qr_info.pack(pady=10)

        # Button to exit the application
        self.exit_button = ttk.Button(root, text="Exit", command=self.exit_application)
        self.exit_button.pack(pady=10)

        # Start the video feed
        self.update()

    def update(self):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        # Scan for QR codes in the frame
        frame_with_qr = self.scan_qr_code(frame)

        # Convert the frame to RGB format for displaying in Tkinter
        img = cv2.cvtColor(frame_with_qr, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(image=img)

        # Update the canvas with the new frame
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.img_tk = img_tk

        # Schedule the next update
        self.root.after(10, self.update)

    def scan_qr_code(self, frame):
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Use pyzbar to decode QR codes
        barcodes = decode(gray)

        # Iterate through detected QR codes
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type

            # Draw a rectangle around the QR code
            rect_points = barcode.polygon
            if rect_points and len(rect_points) == 4:
                rect_points = [tuple(point) for point in rect_points]
                cv2.polylines(frame, [np.array(rect_points)], isClosed=True, color=(0, 255, 0), thickness=2)

            # Display QR code information
            self.label_qr_info.config(text=f'Type: {barcode_type}\nData: {barcode_data}')

        return frame

    def exit_application(self):
        # Release the camera and close the Tkinter window
        self.cap.release()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = QRCodeScannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
