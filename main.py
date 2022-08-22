from concurrent.futures import thread
import tkinter as tk
import tkinter.font as font
from pytube import YouTube,Playlist
import time
from threading import Thread
import os
from tkinter import messagebox as mb
from tkinter import ttk

root = tk.Tk()
root.resizable(0,0)
root.geometry("800x500+50+50")
root.title("YouTube Downloader")

type_var = tk.StringVar(root,value="360")
downloading = False
main_urls_yt = []
main_urls_streams = []

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_label["text"] = str(round(percentage_of_completion))+"%"
    progressbar["value"] = percentage_of_completion

def download_the_videos() :
    global downloading,switch_btn
    download_path = os.getcwd()+"\\YT_Download"
    if not os.path.exists(download_path) :
        os.mkdir(download_path)
    while len(main_urls_yt) > 0 and downloading :

        current_download_label["text"] = video_name_list.get(0)

        if type_var.get() == "Audio" :
            video = main_urls_streams[0].get_audio_only()
        elif type_var.get() == "Highest" :
            video = main_urls_streams[0].get_highest_resolution()
        elif type_var.get() == "Lowest" :
            video = main_urls_streams[0].get_lowest_resolution()
        elif type_var.get() == "360" :
            video = main_urls_streams[0].get_by_resolution("360p")
        elif type_var.get() == "480" :
            video = main_urls_streams[0].get_by_resolution("480p")

        main_urls_yt[0].register_on_progress_callback(on_progress)
        video.download(download_path)

        video_name_list.delete(0)
        video_link_list.delete(0)
        del main_urls_yt[0]
        del main_urls_streams[0]
        current_download_label["text"] = "waiting for URLs..."
        progress_label["text"] = "0%"
        progressbar["value"] = 0

        time.sleep(1)
    downloading = False
    switch_btn["text"] = "Start"

def add_url(url) :
    video = YouTube(url)
    stream_video = video.streams
    main_urls_yt.append(video)
    main_urls_streams.append(stream_video)
    video_name_list.insert(tk.END,stream_video.first().default_filename.replace(".3gpp",""))
    video_link_list.insert(tk.END,url)

def add_video_url():
    global url_entry
    add_url(url_entry.get())
    url_entry.delete(0,tk.END)

tk.Label(root,text="Video URL").place(x=10,y=5)
media_type = tk.OptionMenu(root,type_var,"Highest","480","360","Lowest","Audio")
media_type["bd"] = 1
media_type.place(x=700,y=57.5,width=90,height=35)

url_entry = tk.Entry(root,font=font.Font(size=10))
url_entry.place(x=10,y=30,width=300,height=20)

add_video_btn = tk.Button(root,text="Add",command=add_video_url)
add_video_btn.place(x=320,y=30,width=75,height=20)

tk.Label(root,text="Playlist URL").place(x=405,y=5)
playlist_entry = tk.Entry(root,font=font.Font(size=10))
playlist_entry.place(x=405,y=30,width=300,height=20)

def get_video_from_playlist () :
    url = playlist_entry.get()
    playlist_entry.delete(0,tk.END)

    playlist = Playlist(url)
    ls = playlist.video_urls
    for l in ls :
        print(l)
        add_url(l)

add_videos_btn = tk.Button(root,text="Get Videos",command=get_video_from_playlist)
add_videos_btn.place(x=715,y=30,width=75,height=20)

video_name_list = tk.Listbox(root)
video_name_list.place(x=10,y=175,width=350,height=315)

video_link_list = tk.Listbox(root)
video_link_list.place(x=370,y=175,width=420,height=315)

def switch () :
    global downloading,switch_btn
    downloading = not downloading
    switch_btn["text"] = "Stop" if downloading else "Start"
    if downloading :
        Thread(target=download_the_videos,daemon=True).start()
    time.sleep(0.1)

switch_btn = tk.Button(root,text="Start",command=switch)
switch_btn.place(x=10,y=60,width=480,height=30)

def clear():
    global main_urls_streams,main_urls_yt
    video_name_list.delete(0,tk.END)
    video_link_list.delete(0,tk.END)
    main_urls_streams = []
    main_urls_yt = []

clear_btn = tk.Button(root,text="Clear",command=clear)
clear_btn.place(x=500,y=60,width=90,height=30)

def delete_seleted() :
    if video_name_list.selection_get() in video_name_list.get(0,tk.END) :
        indx = list(video_name_list.get(0,tk.END)).index(video_name_list.selection_get())
    elif video_link_list.selection_get() in video_link_list.get(0,tk.END) :
        indx = list(video_link_list.get(0,tk.END)).index(video_link_list.selection_get())
    video_name_list.delete(indx)
    video_link_list.delete(indx)
    del main_urls_streams[indx]
    del main_urls_yt[indx]

delete_btn = tk.Button(root,text="Delete",command=delete_seleted)
delete_btn.place(x=600,y=60,width=90,height=30)

current_download_label = tk.Label(root,text="waiting for URLs...")
current_download_label.place(x=10,y=100)


progress_label = tk.Label(root,text="0%")
progress_label.place(x=760,y=120)

progressbar = ttk.Progressbar(root)
progressbar.place(x=10,y=120,width=750)

root.mainloop()