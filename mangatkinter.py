import tkinter
import json
import requests
from functools import partial
import os
import re


headers = {
    "Client-Id": "manga-android-app2",
    "Client-Secret": "9befba1243cc14c90e2f1d6da2c5cf9b252bfcbh",
    "Accept": "application/json,application/*+json",
    "enc": "No",
    "User-Agent": "okhttp/3.12.1"}

buttonsdict = {}
manga_dict = {}
window = tkinter.Tk()
window.title("Arabic-Manga")
window.geometry('800x500')
frame = tkinter.Frame(window)
frame.pack()


canvas = tkinter.Canvas(frame)
scrollbar = tkinter.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = tkinter.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="right", fill="both", expand=True)


def search(name):
    if len(buttonsdict) != 0 :
        canvas.delete("all")  # Delete all items
        #for i in buttonsdict:
         #   buttonsdict[i].destroy()
    url = "https://mangaslayer.com/manga-app-api/get-all-published-manga"
    params = {
        "list_type": "filter",
        "limit": "50",
        "offset": "0",
        "json": f'{{"manga_name":"{name}","sort_by_direction":"DESC","sort_by":"manga_id","manga_status":"All","genre_include_ids":""}}'
    }
    response = requests.get(url, headers=headers, params=params, verify=True)
    if response.status_code == 200:
        data = json.loads(response.json()['result'])
        manga_list = data.get("data", [])
        if len(manga_list) == 0:
            print("NO RESULTS FOUND , PLZ ENTER VALID MANGA NAME!!")
        else:
            print(f"{len(manga_list)} Results Found:")
            print(manga_list)
            for i, manga in enumerate(manga_list, start=1):
                manga_name = manga.get('manga_name', '')
                manga_id = manga.get('manga_id', '')
                manga_cover_image_url = manga.get('manga_cover_image_url' , '')
                manga_dict[i] = manga.get('manga_id', '')
                buttonsdict[i] = tkinter.Button(scrollable_frame, bg="orange", fg="black", text=f"{manga_name}",command=  partial(getchapters, manga_id))
                buttonsdict[i].pack(fill="x")
                print(f"{i}. {manga_name} {manga_cover_image_url} ")
            print(manga_dict)
            # print("Manga Dictionary:")
            # print(manga_dict)
            # print(len(manga_list))
def getchapters(mangaid) :
    for i in buttonsdict:
        buttonsdict[i].destroy()
    chapter_url = f"https://mangaslayer.com/manga-app-api/get-published-manga-details-info?manga_id={mangaid}&chapters=Yes"
    response = requests.get(chapter_url, headers=headers, verify=True)
    data = json.loads(response.json()['result'])
    chapters_list = list(reversed(data.get('data', [])))
    # print(chapters_list)
    # print(response.json())
    chapters_dict = {}
    for i, chapter in enumerate(chapters_list, start=1):
        chapter_name = chapter.get('chapter_name', '')
        chapter_id = chapter.get('chapter_id', '')
        chapters_dict[i] = chapter_id
        chapter_number = chapter.get('chapter_number', '')
        buttonsdict[i] = tkinter.Button(scrollable_frame, bg="orange", fg="black", text=f"{chapter_name}",
                                        command=partial(print , "hh"))
        buttonsdict[i].pack(fill="x")
        print(f"{i}. {chapter_name}  ")

label = tkinter.Label(frame, text="أدخل اسم المانغا للبحث " + ":", width=50)
label.pack(fill="both")
search_entery = tkinter.Entry(frame, width=500)
search_entery.pack()



search_button = tkinter.Button(frame, bg="black", fg="orange", text='البحث', command=lambda :search(search_entery.get()))
search_button.pack(fill="x")

window.mainloop()
