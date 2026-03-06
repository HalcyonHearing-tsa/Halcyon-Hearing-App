import cv2
from PIL import Image, ImageTk
import customtkinter
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

class RealTimeASLApp():
    def __init__(self):
        super().__init__()
        
        model_id = "prithivMLmods/Alphabet-Sign-Language-Detection" 
        self.processor = AutoImageProcessor.from_pretrained(model_id)
        self.model = AutoModelForImageClassification.from_pretrained(model_id)
        self.labels = self.model.config.id2label 
        
        self.cap = cv2.VideoCapture(0) 
    def helperFunction(self,callback):
        self.callback = callback
        self.update_frame()
        
    def update_frame(self):
        """Captures webcam frams, creates an ROI to reduce compute load,
        runs the ASL-Interpreter-Alphabet model to translate ASL gestures."""
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1) 
            height, width, color_channels = frame.shape
            
            #Creating valid coordinates for an ROI
            roi_width = 250   
            roi_height = 250
            x1 = width - roi_width
            x2 = width-50
            y1 = 50
            y2 = y1 + roi_height
                       
            roi_image = frame[y1:y2, x1:x2] 
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            roi_rgb = cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB)
            pil_roi = Image.fromarray(roi_rgb)

            inputs = self.processor(images=pil_roi, return_tensors="pt")
            #Disables gradiant tracking/Not being used for training
            with torch.no_grad():
                    outputs = self.model(**inputs)
                    idx = outputs.logits.argmax(-1).item()
                    letter =self.labels[idx]
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(img_rgb)
            img_tk = customtkinter.CTkImage(light_image=pil_image,dark_image=pil_image,size=(990,770))
            self.callback(letter,img_tk)


        
    