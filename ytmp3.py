from tkinter import Tk,Button,Label,Entry,DISABLED,NORMAL,NSEW
import youtube_dl
import sys,os
from threading import Thread
import socket

SAVE_PATH=r"C:\Users\sou22\Downloads"
ydl_opts = {
    'format': 'bestaudio/best',
    'extractaudio':True,
    'audioformat':'mp3',
    'noplaylist': True,
    'nocheckcertificate':True,
    'outtmpl':SAVE_PATH + '/%(title)s (%(id)s).%(ext)s',
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
    ],
}

root=Tk()
root.title("YouTube to mp3 (Made by Sourabh Sathe)")
root.geometry("700x70")
root.config(bg="white")

def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def is_supported(url):
    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(url) and e.IE_NAME != 'generic':
            return True
    return False


def downloadtoMP3():
    downloadbtn.config(state=DISABLED)
    if is_connected():
        if is_supported(urlbox.get()):
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                urlbox.config(fg="green")
                status.config(text="Downloading...")    
                try:
                    ydl.download([urlbox.get()])
                except youtube_dl.utils.DownloadError as e:
                    print(e)
                    downloadbtn.config(state=NORMAL)
                    status.config(text="Error.Please retry")
        else:
            downloadbtn.config(state=NORMAL)
            status.config(text="Not a valid URL")
            urlbox.config(fg="red")
            root.focus_force()
            return
    else:
        status.config(text="Unable to connect to internet. Connect to internet and restart this application")
        urlbox.config(state=DISABLED)
        return

    status.config(text="Downloaded Successfully (Saved to Downloads folder)")
    print("downloaded")
    urlbox.delete(0, "end")
    urlbox.config(fg = 'grey')
    urlbox.insert(0, 'Enter the URL')
    root.focus_force()

def on_entry_click(event):
    downloadbtn.config(state=NORMAL)
    urlbox.delete(0, "end")
    urlbox.config(fg = 'black')
    status.config(text="")

title=Label(text="YouTube to MP3!",bg="white")
title.grid(row=0,columnspan=2,sticky=NSEW)

status=Label(text="",bg="white")
status.grid(row=2,columnspan=2,sticky=NSEW)

urlbox=Entry(width=100)
urlbox.grid(row=1,column=0,padx=10,ipady=3)

urlbox.insert(0, 'Enter the URL')
urlbox.config(fg = 'grey')
urlbox.bind('<FocusIn>', on_entry_click)


downloadbtn=Button(text="Download",relief="groove",bg="white",command=lambda:Thread(target=downloadtoMP3).start())
downloadbtn.grid(row=1,column=1)
downloadbtn.config(state=DISABLED)

if not is_connected():
    status.config(text="Unable to connect to internet. Connect to internet and restart this application")
    downloadbtn.config(state=DISABLED)
    urlbox.config(state=DISABLED)
else:
    status.config(text="Internet connection available")

root.mainloop()
