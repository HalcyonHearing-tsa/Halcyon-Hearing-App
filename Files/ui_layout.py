import os
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import *
import customtkinter as ctk
from PIL import Image, ImageTk
from Transcription import Transcription 
from ASL_Interpreter import RealTimeASLApp 
import win32com.client as wincl
import win32com.client
import pygame
from Config_Loader import ConfigLoader

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_PATH = os.path.dirname(CURRENT_PATH)
ASSETS_PATH = os.path.join(PARENT_PATH, "Assets")

class AcknoledgmentsTopLevel(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")
        self.title("Acknowledgements")
        self.font  =  ctk.CTkFont(family="Helvetica now", size=20,weight='normal',slant='roman')
        self.resizable(False,False)
        self.credit_textbox = ctk.CTkTextbox(self, width=460,height=360,font=self.font)
        self.credit_textbox.pack(padx=20, pady=20)
        self.credit_textbox.focus_displayof
        self.credit_textbox.insert("0.0","Halcyon Hearing was developed for helping communication for the hearing impaired.\n"
                                   "This was possible to the open-source community,\n"
                                   "special thanks for the creators of CustomTkinter, OpenCV,OpenAI Whisper, Silero VAD,\n"
                                   "and Alphabet-Sign-Language-Detection. UI assets provided by:\n"
                                   "Light mode icon made by Any Icon from www.flaticon.com.\n"
                                    "Dark mode icon made by adriansyah from www.flaticon.com.\n"
                                    "Folder icon made by Freepik from www.flaticon.com.\n"
                                    "Notification icon made by Freepik from www.flaticon.com.\n"
                                    "Palm icon made by Icon Mart from www.flaticon.com.\n"
                                    "Microphone icon made by Freepik from www.flaticon.com.")
        self.credit_textbox.configure(state="disabled")
        self.focus()
        self.attributes('-topmost', True)



"""
Main Window Frames
"""
class MainWindowFrame1(ctk.CTkFrame):
    def __init__(self, master,height,width):
        super().__init__(master,height,width)
        self.grid_columnconfigure(0, weight=1)
        self.settings = ConfigLoader()
        
        
        self.font  =  ctk.CTkFont(family="Helvetica now", size=20,weight='normal',slant='roman')

        theme_image = ctk.CTkImage(light_image=Image.open(os.path.join(ASSETS_PATH,"light-mode.png")),
        dark_image=Image.open(os.path.join(ASSETS_PATH,"night-mode.png")),size=(30, 30))
        
        self.mode = ctk.CTkButton(master=self,image=theme_image,text='',command=lambda : self.changeTheme())
        self.mode.grid(row=1,column=0)
        self.grid_rowconfigure(1, weight=1)
        
        home_image = ctk.CTkImage(light_image=Image.open(os.path.join(ASSETS_PATH,"home.png")),size=(30,30))
        
        self.homeB =  ctk.CTkButton(self,text="",image = home_image, corner_radius=10)
        self.homeB.grid(row=2,column=0)
        self.grid_rowconfigure(2, weight=1)
        
        self.acknow =  ctk.CTkButton(self,text="Acknowledgments",width=30,font = self.font,command=self.open_toplevel)
        self.acknow.grid(row=3,column=0,sticky='we',padx =(40,40))
        self.grid_rowconfigure(3, weight=1)
        
        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AcknoledgmentsTopLevel(self)  
        else:
            self.toplevel_window.focus() 
        
    def changeTheme(self):
        is_light = self.settings.configs["is_light"]
        if(is_light):
            self.settings.configs["is_light"]=False
            self.settings.configs["current_mode"]=self.settings.configs["mode"][0]
            ctk.set_appearance_mode(self.settings.configs["current_mode"])
        else:
            self.settings.configs["is_light"]=True
            self.settings.configs["current_mode"]=self.settings.configs["mode"][1]
            ctk.set_appearance_mode(self.settings.configs["current_mode"])
        self.update()
        self.settings.save_settings()
class MainWindowFrame2(ctk.CTkFrame):
    def __init__(self, master,height,width):
        super().__init__(master,height,width)
        self.font  =  ctk.CTkFont(family="Helvetica now", size=30,weight='normal',slant='roman')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        fileT_image = ctk.CTkImage(light_image=Image.open(os.path.join(ASSETS_PATH,"folder.png")),size=(40, 40))
        self.file_transcription= ctk.CTkButton(master=self,image=fileT_image,text="Open a file",font=self.font)
        self.file_transcription.grid(row=0,column=0,pady=20,sticky='nsew',padx=20)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        liveT_image = ctk.CTkImage(light_image=Image.open(os.path.join(ASSETS_PATH,"microphone.png")),size=(40, 40))
        self.live_transcript= ctk.CTkButton(master=self,image=liveT_image,text="Live transcription",font=self.font)
        self.live_transcript.grid(row=2,column=0,pady=20,sticky='nsew',padx=20) 
        
        asl_image = ctk.CTkImage(light_image=Image.open(os.path.join(ASSETS_PATH,"palm.png")),size=(40, 40))
        self.ASL= ctk.CTkButton(master=self,image=asl_image,text="ASL Interpreter",font=self.font)
        self.ASL.grid(row=0,column=2,pady=20,sticky='nsew',padx=20)
        
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        emerP_image = ctk.CTkImage(light_image=Image.open(os.path.join(ASSETS_PATH,"notification.png")),size=(40, 40))
        self.emer_pharases= ctk.CTkButton(master=self,image=emerP_image,text="Emergency Phrases",font=self.font)
        self.emer_pharases.grid(row=2,column=2,pady=20,sticky='nsew',padx=20)

    def widgetConfig(self,transript_method,cancelMic_method,aslInt_method,emerPhrases_method):
        self.file_transcription.configure(command=lambda: transript_method())
        self.live_transcript.configure(command = lambda: cancelMic_method())
        self.ASL.configure(command = lambda: aslInt_method())
        self.emer_pharases.configure(command = lambda: emerPhrases_method())
"""
Main App Layout
"""
class UiLayout(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.settings = ConfigLoader()
        self.theme=self.settings.configs["current_mode"]
        ctk.set_appearance_mode(self.theme)
        self.font  =  ctk.CTkFont(family="Helvetica now", size=20,weight='normal',slant='roman')
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        pygame.mixer.init()
        self.curr_speaking = False
        self.wav_file = os.path.abspath("temp_speech.wav")

        self.screenWidth = self.winfo_screenwidth()
        self.screenLength = self.winfo_screenheight()
        self.title("Halcyon Hearing")
        
        self.audio_trans = Transcription()
        self.inter = RealTimeASLApp()
        self.mainWindow_frame1 = MainWindowFrame1(self,int(self.screenLength/3),int(self.screenWidth/3))
        self.mainWindow_frame1.grid(row=0,column=0, padx=10, pady=(10, 0), sticky="nsew")
        
        self.after(0,lambda: self.mainWindow())
    def mainWindow(self):
        
        self.state("zoomed")
        self.mainWindow_frame2 = MainWindowFrame2(self,int(self.screenLength*2/3),int(self.screenWidth*2/3))
        self.mainWindow_frame2.grid(row=0,column=1, padx=10, pady=(10, 0), sticky="nsew")
        self.mainWindow_frame2.widgetConfig(self.transcript,self.cancelMic,self.aslInt,self.emerPhrases)
        self.grid_columnconfigure(1, weight=9)
        self.mainWindow_frame1.homeB.configure(command=lambda: ...)
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())

    """
    Transcription UI
    """    
    def cancelMic(self):
        self.clearing()
        
        self.mainWindow_frame1.homeB.configure(command=lambda :self.stop_e())
        self.mainWindow_frame2.grid_rowconfigure(0, weight=1)
        self.mainWindow_frame2.grid_rowconfigure(1, weight=1)
        self.mainWindow_frame2.grid_columnconfigure((0,1,2), weight=1)
        
        self.text_Widget=ctk.CTkTextbox(master=self.mainWindow_frame2,width=int(self.screenWidth/1.3),
                                        height=int(self.screenLength/1.3),font=self.font)
        self.text_Widget.configure(state="disable")
        self.text_Widget.grid(row=0,column=0,pady=20,columnspan=3)
        
        clearB= ctk.CTkButton(master=self.mainWindow_frame2,text="Clear",command=lambda : self.clearText(),
                              font=self.font,width=250,height=50)
        clearB.grid(row=1,column=0,pady=20)
        
        self.strEndB= ctk.CTkButton(master=self.mainWindow_frame2,text="Start Recording",command=lambda : self.initialRecording(),
                                    font=self.font,width=250,height=50)
        self.strEndB.grid(row=1,column=1,pady=20)
        
        saveT= ctk.CTkButton(master=self.mainWindow_frame2,text="Save",command= lambda: self.saveText(self.text_Widget.get("1.0","end")),
                             font=self.font,width=250,height=50)
        saveT.grid(row=1,column=2,pady=20)
        saveT.focus_displayof
        
    def initialRecording(self):
        self.strEndB.configure(text="Stop Recording",command=lambda: self.stopRecording())
        self.audio_trans.helperTranscription(callback_function=self.tran_update)
    def startRecording(self):
        self.speech_buffer = []
        self.audio_trans.helperTranscription(callback_function=self.tran_update)
        self.strEndB.configure(text="Stop Recording",command=lambda: self.stopRecording())
    def stopRecording(self):  
        self.audio_trans.start_Trans=True
        self.strEndB.configure(text="Start Recording",command=lambda: self.startRecording())
        self.audio_trans.stop_event.set()
        
    def stop_e(self):
        self.audio_trans.stop_event.set()
        self.clearing()
        self.mainWindow()
    def tran_update(self,textVar):
        self.text_Widget.configure(state="normal")
        self.text_Widget.insert("end",textVar)
        self.text_Widget.see("end")
        self.text_Widget.configure(state="disable")
    def clearText(self):
        self.text_Widget.configure(state="normal")
        self.text_Widget.delete("1.0","end")
        self.text_Widget.see("end")
        self.text_Widget.configure(state="disable")

    def transcript(self):
        self.withdraw()
        self.clearing()
        filetypes_config = [
        ("Audio files", "*.wav"),("Audio files","*.mp3"),("Audio files", "*.m4a")]
        filename = filedialog.askopenfilename(
        title="Select a file",
        initialdir="/",  #Set initial directory
        filetypes=filetypes_config
        )
        if filename:
            self.mainWindow_frame1.homeB.configure(command=lambda :self.clearingMod())
        
            self.text_Widget=ctk.CTkTextbox(master=self.mainWindow_frame2,font=self.font)
            self.text_Widget.configure(state="disable")
            self.text_Widget.grid(row=0,column=0,padx=(20,20),pady=(20,20),sticky="nsew")
            self.mainWindow_frame2.grid_rowconfigure(0,weight=4)
            self.mainWindow_frame2.grid_columnconfigure(0,weight=1)
            
            saveT= ctk.CTkButton(master=self.mainWindow_frame2,text="Save",command= lambda: self.saveText(self.text_Widget.get("1.0","end")),
                                 font=self.font,width=250,height=50)
            saveT.grid(row=1,column=0,padx=(20,20),pady=(20,20))
            self.mainWindow_frame2.grid_rowconfigure(1,weight=1)
            
            saveT.focus_displayof
            
            audio=self.audio_trans.transcription(filename)
            self.tran_update(f"Transcript: {audio['text']}\n")

            self.deiconify()
        else:
            self.mainWindow()
        self.deiconify()
        self.state("zoomed")
    def clearing(self):
        for widget in self.mainWindow_frame2.winfo_children():
            widget.destroy()
        self.reset_all_weights()
    def clearingMod(self):
        for widget in self.mainWindow_frame2.winfo_children():
            widget.destroy()
        self.reset_all_weights()
        self.mainWindow()
    def saveText(self,text):
        self.withdraw()
        self.audio_trans.stop_event.set()
        files = [('All Files', '*.*'), 
             ('Word Document', '*.docx'),
             ('Text Document', '*.txt')]
        file_path = filedialog.asksaveasfilename(filetypes = files,initialdir="/",defaultextension=".txt")
        if file_path:
           with open(file_path, "w") as file:
               file.write(text)
        self.state("zoomed")
        self.deiconify()
    def reset_all_weights(self):
        columns, rows = self.mainWindow_frame2.grid_size()
        for col in range(columns):
            self.mainWindow_frame2.grid_columnconfigure(col, weight=0)    
        for row in range(rows):
            self.mainWindow_frame2.grid_rowconfigure(row, weight=0) 
    def aslInt(self):
        self.clearing()
        
        self.mainWindow_frame2.grid_rowconfigure(0, weight=1)
        self.mainWindow_frame2.grid_columnconfigure(0, weight=1)
        
        self.mainWindow_frame1.homeB.configure(command=lambda :self.stopFrame())
        
        self.label_video = ctk.CTkLabel(self.mainWindow_frame2,text="")
        self.label_video.grid(row=0,column=0,sticky="")
        
        self.mainWindow_frame2.grid_rowconfigure(1, weight=1)
        self.mainWindow_frame2.grid_columnconfigure(0, weight=1)
        
        self.label_result = ctk.CTkLabel(self.mainWindow_frame2, text="Waiting for hand...", font=self.font)
        self.label_result.grid(row=1,column=0,padx=(20,20),pady=(20,30))
        self.label_result.focus_displayof
        
        
        self.inter.helperFunction(self.updatingFrame)
    def updatingFrame(self,letter,img_tk):
        self.label_result.configure(text=f"Detected: {letter}")
        self.label_video.imgtk = img_tk
        self.label_video.configure(image=img_tk)
        self.after(10, self.inter.update_frame)

    def stopFrame(self):
        self.inter.cap.release()
        self.clearingMod()
        self.inter = RealTimeASLApp()


    def emerPhrases(self):
        self.clearing()
        self.mainWindow_frame1.homeB.configure(command=lambda :self.stopTTS())
        self.sel=tk.StringVar() 
        self.mainWindow_frame2.grid_rowconfigure(0, weight=1)
        self.mainWindow_frame2.grid_columnconfigure(0, weight=1)
        self.phrases = self.settings.configs["phrases"]
        self.combo_phrases = ctk.CTkComboBox(master=self.mainWindow_frame2,values=self.phrases,variable=self.sel,command= self.textToSpeech,font=self.font,width=250,height=50)
        self.combo_phrases.grid(row=0,column=1,sticky="",)
        self.mainWindow_frame2.grid_rowconfigure(1, weight=1)
        self.mainWindow_frame2.grid_columnconfigure(1, weight=1)
        self.mainWindow_frame2.grid_columnconfigure(2, weight=1)
        self.e1=ctk.CTkEntry(master=self.mainWindow_frame2,width=250,height=50,font=self.font)
        self.e1.grid(row=1,column=0)
        self.addB=ctk.CTkButton(master=self.mainWindow_frame2,text='Add',command=lambda: self.my_insert(),font=self.font,width=250,height=50)
        self.addB.grid(row=1,column=1)
        self.deleteB=ctk.CTkButton(master=self.mainWindow_frame2,text='Delete',command=lambda: self.my_delete(),font=self.font,width=250,height=50)
        self.deleteB.grid(row=1,column=2)
    def my_insert(self):
        my_new = self.combo_phrases.cget("values")
        if self.e1.get() not in my_new and (not self.e1.get().isspace() and not self.e1.get()==''): 
            my_new.append(self.e1.get())
            self.combo_phrases.configure(values=my_new)
            self.e1.delete(0,'end') 
            self.settings.configs["phrases"] = my_new
            self.phrases = self.settings.configs["phrases"]
            self.settings.save_settings()

    def my_delete(self): 
        my_new=[]
        for opt in self.combo_phrases.cget("values"): 
            if(opt != self.combo_phrases.get()): 
                my_new.append(opt)  
        self.combo_phrases.configure(values=my_new)
        self.settings.configs["phrases"] = my_new
        self.phrases = self.settings.configs["phrases"]
        self.settings.save_settings() 
        self.combo_phrases.set('')
    def textToSpeech(self,choice):
        if self.curr_speaking:
            return
        
        self.curr_speaking = True
        self.combo_phrases.configure(state="disable", values=[])
        self.update()

        try:
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            sapi_stream = win32com.client.Dispatch("SAPI.SpFileStream")
            sapi_stream.Open(self.wav_file, 3)
            
            for voice in speaker.GetVoices():
                if "Zira" in voice.GetDescription() or "Female" in voice.GetDescription():
                    speaker.Voice = voice
                    break
                    
            speaker.AudioOutputStream = sapi_stream
            speaker.Speak(choice)
            sapi_stream.Close()
            
        except Exception as e:
            print(f"File generation failed: {e}")
            self.unlock_ui()
            return
        pygame.mixer.music.load(self.wav_file)
        pygame.mixer.music.play()
        self.checkTTS()
    def checkTTS(self):
        """Asynchronously polls the Pygame mixer stream every 50ms to 
        prevent the Tkinter event loop from freezing during text-to-speech playback."""
        if pygame.mixer.music.get_busy():
            self.after(50, self.checkTTS)
        else:
            self.unlock_ui()
    def unlock_ui(self):
        pygame.mixer.music.unload()
        try:
            if os.path.exists(self.wav_file): 
                os.remove(self.wav_file)
        except Exception as e:
            pass
        self.combo_phrases.configure(state="normal",values=self.phrases)
        self.curr_speaking = False
    def stopTTS(self):
        self.clearingMod()

root  = UiLayout()
root.mainloop()