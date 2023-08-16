import json
import requests
import os
import re
url = "https://mangaslayer.com/manga-app-api/get-all-published-manga"
headers = {
    "Client-Id": "manga-android-app2",
    "Client-Secret": "9befba1243cc14c90e2f1d6da2c5cf9b252bfcbh",
    "Accept": "application/json,application/*+json",
    "enc": "No",
    "User-Agent": "okhttp/3.12.1"
}
while True :
    print(""" ▄▄▄       ██▀███        ███▄ ▄███▓ ▄▄▄       ███▄    █   ▄████  ▄▄▄         
▒████▄    ▓██   ██       ██ ▀█▀ ██  ████▄     ██ ▀█   █  ██  ▀█  ████▄       
▒██  ▀█▄  ▓██  ▄█       ▓██    ▓██  ██  ▀█▄  ▓██  ▀█ ██▒ ██ ▄▄▄  ██  ▀█▄     
░██▄▄▄▄██ ▒██▀▀█▄       ▒██    ▒██ ░██▄▄▄▄██ ▓██▒  ▐▌██ ░▓█  ██  ██▄▄▄▄██    
 ▓█   ▓██▒░█▓  ██▒ ██  ▒██▒   ░██▒ ▓█   ▓██▒▒██░   ▓██░░▒▓███▀▒ ▓█   ▓██▒   By ProMast3r
 ▒▒   ▓▒█░░▒▓  ██░     ░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒  ░▒   ▒  ▒▒   ▓▒█░   https://github.com/PM035
  ▒   ▒▒ ░ ░▒ ░ ▒░     ░  ░      ░  ▒   ▒▒ ░░ ░░   ░ ▒░  ░   ░   ▒   ▒▒ ░   https://t.me/ProMast3r """)
    search = input("أدخل اسم المانغا للبحث:")

    params = {
        "list_type": "filter",
        "limit": "50",
        "offset": "0",
        "json": f'{{"manga_name":"{search}","sort_by_direction":"DESC","sort_by":"manga_id","manga_status":"All","genre_include_ids":""}}'
    }

    response = requests.get(url, headers=headers, params=params, verify=True)
    if response.status_code == 200:
        data = json.loads(response.json()['result'])
        manga_list = data.get("data", [] )
        manga_dict = {}
        if len(manga_list) > 0 :


            print(f"{len(manga_list)} Results Found:")
            for i, manga in enumerate(manga_list, start=1):
                manga_name = manga.get('manga_name', '')
                manga_id = manga.get('manga_id', '')
                manga_dict[i] = manga_id
                print(f"{i}. {manga_name}")
            #print("Manga Dictionary:")
            #print(manga_dict)
            #print(len(manga_list))

            choice = input("أدخل رقم المانغا من القائمة :")
            if choice.isdigit() and int(choice) in manga_dict:
                manga_id = manga_dict[int(choice)]
                manga_list_ar_dict = {'manga_name': 'الاسم:', 'manga_theater': 'المؤلف:',
                                      'manga_genres': 'التصنيف:', 'manga_status': 'الحالة:',
                                      'manga_rank': 'الترتيب:',
                                      'manga_rating': 'التقييم:', 'manga_rating_user_count': 'عدد المصوتين:',
                                      'manga_updated_at': 'اخر تحديث:'}
                manga_list_ar_dict2 = {'manga_release_date': 'تاريخ الاصدار', 'manga_age_rating': 'التصنيف العمري:',
                                       'manga_description': 'الوصف:'}
                if manga_list[int(choice) - 1]['manga_status'] == 'Ongoing':
                    manga_list[int(choice) - 1]['manga_status'] = 'مستمر'
                if manga_list[int(choice) - 1]['manga_status'] == 'Completed':
                    manga_list[int(choice) - 1]['manga_status'] = 'مكتمل'
                for i in manga_list_ar_dict:
                    print(manga_list_ar_dict[i], end=" ")
                    print(manga_list[int(choice) - 1].get(i, "غير معروف"))
                chapter_url = f"https://mangaslayer.com/manga-app-api/get-published-manga-details-info?manga_id={manga_id}&chapters=Yes"
                response = requests.get(chapter_url, headers=headers, verify=True)
                if response.status_code == 200:
                    data = json.loads(response.json()['result'])
                    chapters_list = list(reversed(data.get('data', [])))
                    # print(chapters_list)
                    # print(response.json())
                    print(f"عدد الفصول:{len(chapters_list)}")
                info_url = f"https://mangaslayer.com/manga-app-api/get-published-manga-details-info?manga_id={manga_id}&chapters=No"
                response = requests.get(info_url, headers=headers, verify=True)
                if response.status_code == 200:
                    manga_info = json.loads(response.json()['result'])
                    for i in manga_list_ar_dict2:
                        print(manga_list_ar_dict2[i], end=" ")
                        print(manga_info.get(i, "غير معروف"))
                manga_cover_url = manga_list[int(choice) - 1]['manga_cover_image_url']
                confirm = input("اضغط للاستمرار")
                chapters_dict = {}
                for i, chapter in enumerate(chapters_list, start=1):
                    chapter_name = chapter.get('chapter_name', '')
                    chapter_id = chapter.get('chapter_id', '')
                    chapters_dict[i] = chapter_id
                    chapter_number = chapter.get('chapter_number', '')
                    print(f"{i}. {chapter_name} ")
                    chapter_id = ""
                    pages_url = f"https://mangaslayer.com/manga-app-api/get-published-manga-chapter-pages?manga_id={manga_id}&chapter_id={chapter_id}&device_id=0ea8e795d423caf2"
                    manga_name_str = re.sub(r'[^\w\- ]', '_', manga_list[int(choice) - 1]['manga_name'])
                while True:
                    choice = input("أدخل رقم الفصل من القائمة--أدخل * لتحديد الكل--")
                    if (choice.isdigit() and int(choice) in chapters_dict) or choice == "*":
                        folder_path = f"./{manga_name_str}" #create poster in manga folder
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)
                        poster = os.path.join(folder_path, 'Poster.png')
                        response = requests.get(manga_cover_url)
                        response.raise_for_status()  # Raise an exception for any request error
                        with open(poster, 'wb') as file:
                            file.write(response.content)
                        if choice.isdigit():
                            loop_mode = False
                            x = choice
                            print(f"LoOp Mode = {loop_mode}")
                        if choice == "*":
                            loop_mode = True
                            print(f"LoOp Mode = {loop_mode}")
                        for x in chapters_dict:
                            chapter_id = chapters_dict[int(x)]
                            pages_url = f"https://mangaslayer.com/manga-app-api/get-published-manga-chapter-pages?manga_id={manga_id}&chapter_id={chapter_id}&device_id=0ea8e795d423caf2"
                            response = requests.get(pages_url, headers=headers, verify=True)
                            if response.status_code == 200:
                                data = json.loads(response.json()['result'])
                                url_dict = {}
                                url_dict['Poster'] = manga_cover_url
                                chapter_name = chapters_list[int(x) - 1]['chapter_name']
                                chapter_name = re.sub(r'[^\w\- ]', '_', chapter_name)  # to filer bad path charecters
                                folder_path = f"./{manga_name_str}/{chapter_name}"
                                pages_list = data.get('data', [])
                                for i, page in enumerate(pages_list, start=1):
                                    url_dict[i] = page.get('page_image_url', '')
                                print(chapter_name)
                                print("عدد الصفحات :", end="")
                                print(data['total'])
                                print("جاري التنزيل...")
                                # print(url_dict)
                                if not os.path.exists(folder_path):
                                    os.makedirs(folder_path)
                                for key, url in url_dict.items():
                                    file_name = os.path.join(folder_path, str(key) + '.png')
                                    response = requests.get(url)
                                    response.raise_for_status()  # Raise an exception for any request error
                                    with open(file_name, 'wb') as file:
                                        file.write(response.content)
                                    print(f"Downloaded photo {file_name}")

            else:
                print("الرجاء ادخال رقم من القائمة")
        else:
            print("NO RESULTS FOUND , PLZ ENTER VALID MANGA NAME!!")
    else:
        print(response.status_code)
