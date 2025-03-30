import pyttsx3
import os
import playsound
import speech_recognition as sr
import time
import sys
import ctypes
import wikipedia
import datetime
import json
import urllib.parse
import re
import webbrowser
import smtplib
import requests
import urllib
import subprocess
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch
from googlesearch import search
from googletrans import Translator
from fake_useragent import UserAgent
import tkinter as tk
from tkinter import scrolledtext
import threading

wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()

root = tk.Tk()
root.title("Jarvis Chat Interface")
root.geometry("500x600")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=25, width=60, state='normal')
chat_box.pack(pady=10)

def speak(text, chat_box=chat_box):
    chat_box.insert(tk.END, f"Jarvis: {text}\n")
    chat_box.see(tk.END)
    tts = gTTS(text=text, lang='vi', slow=False)
    filename = "sound.mp4"
    tts.save(filename)
    playsound.playsound(filename, False)
    os.remove(filename)

def get_audio(chat_box=chat_box):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        chat_box.insert(tk.END, "Listening...\n")
        chat_box.see(tk.END)
        try:
            audio = r.listen(source, phrase_time_limit=5)
            text = r.recognize_google(audio, language="vi-VN")
            chat_box.insert(tk.END, f"You: {text}\n")
            chat_box.see(tk.END)
            return text
        except sr.UnknownValueError:
            chat_box.insert(tk.END, "You: ... (No input detected)\n")
            chat_box.see(tk.END)
            return None
        
def stop():
    speak("Hẹn gặp lại bạn sau!", chat_box)

def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            speak("Jarvis không nghe rõ. Bạn nói lại được không!", chat_box)
            time.sleep(3)
    time.sleep(10)
    stop()
    return 0

def hello(name):
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng bạn {}. Chúc bạn một ngày tốt lành.".format(name), chat_box)
    elif 12 <= day_time < 18:
        speak("Chào buổi chiều bạn {}. Bạn đã dự định gì cho chiều nay chưa.".format(name), chat_box)
    else:
        speak("Chào buổi tối bạn {}. Bạn đã ăn tối chưa nhỉ.".format(name), chat_box)
    time.sleep(5)
    speak("bạn có khỏe không ?", chat_box)
    time.sleep(3)
    ans = get_audio()
    if ans:
        if "có" in ans:
            speak("Thật là tốt!")
        else:
            speak("Vậy à, bạn nên nghỉ ngời đi!", chat_box)

def open_website(text):
    try:
        regex = re.search('mở (.+)', text)
        if regex:
            domain = regex.group(1)
            url = f"https://{domain}"
            webbrowser.open(url)
            speak("Trang web của bạn đã được mở!", chat_box)
        else:
            speak("Không tìm thấy URL hợp lệ để mở!", chat_box)
    except Exception as e:
        speak(f"Có lỗi khi mở website: {e}", chat_box)

# def do_math(text):
    # speak("Bạn muốn tính phép toán gì?")
    # time.sleep(2)
    # user_input = get_text()
    # if user_input.lower() == 'thôi':
    #     speak("Dừng tính toán.")
    #     return
    # regex_matches = re.findall('(\d+ [+\-*/] \d+)', user_input)
    # if regex_matches:
    #     for match in regex_matches:
    #         regex = re.search('(\d+ [+\-*/] \d+)', match)
    #         math_expression = regex.group()
    #         speak(f"Bạn muốn tính phép toán: {math_expression}")
    #         time.sleep(2)
    #         result = eval(math_expression)
    #         speak(f"Kết quả của phép toán là {result}")
    # else:
    #     speak("Không tìm thấy phép toán trong đoạn văn bản bạn nhập.")

def google_search(text, chat_box):
    try:
        search_query = text.split("tìm kiếm", 1)[1].strip()
        search_query_encoded = urllib.parse.quote_plus(search_query)
        google_url = f"https://www.google.com/search?q={search_query_encoded}"
        webbrowser.open(google_url)
        speak(f"Tìm kiếm cho '{search_query}' đã được mở trong trình duyệt.", chat_box)
    except IndexError:
        speak("Tôi không hiểu nội dung bạn muốn tìm kiếm. Vui lòng nói lại!", chat_box)
    except Exception as e:
        speak(f"Có lỗi xảy ra khi tìm kiếm: {e}", chat_box)

def play_youtube():
    speak('Xin mời bạn chọn tên bài hát', chat_box)
    mysong = get_audio()
    while True:
        result = YoutubeSearch(mysong, max_results=10).to_dict()
        if result:
            break
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    webbrowser.open(url)
    speak("Bài hát bạn yêu cầu đã được mở. Hãy tận hưởng nó", chat_box)


def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak(f'Bây giờ là {now.hour} giờ {now.minute} phút', chat_box)
    elif "ngày" in text:
        speak(f"Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}", chat_box)
    else:
        speak("Bot chưa hiểu ý của bạn. Bạn nói lại được không?", chat_box)


def translate_text(text, target_language='vi'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# def weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ?")
    time.sleep(3)
    url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temp = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        sun_time = data["sys"]
        sun_rise = datetime.datetime.fromtimestamp(sun_time["sunrise"])
        sun_set = datetime.datetime.fromtimestamp(sun_time["sunset"])
        wther = data["weather"]
        weather_des = wther[0]["description"]
        now = datetime.datetime.now()

        # Additional weather advice based on conditions
        weather_advice = ""
        if "rain" in weather_des.lower():
            weather_advice = translate_text("Nên mang theo ô khi ra ngoài vì có dự báo mưa.")
        elif current_temp < 18:
            weather_advice = translate_text("Nên mặc áo ấm khi ra ngoài vì nhiệt độ thấp hơn 18 độ C.")
        elif 18 <= current_temp < 27:
            weather_advice = translate_text("Hôm nay nhiệt độ rất thích hợp để hoạt động thể thao và đi chơi. Bạn nên đi ra ngoài")
        else:
            weather_advice = translate_text("Nên đội mũ khi ra ngoài trời nắng để bảo vệ đầu khỏi tác động của tia UV.")

        content = f"""
        Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}
        Mặt trời mọc vào {sun_rise.hour} giờ {sun_rise.minute} phút
        Mặt trời lặn vào {sun_set.hour} giờ {sun_set.minute} phút
        Nhiệt độ trung bình là {current_temp} độ C
        Áp suất không khí là {current_pressure} héc tơ Pascal
        Độ ẩm là {current_humidity}%
        Trời hôm nay {translate_text(weather_des)}. {weather_advice}"""

        speak(content)
        time.sleep(25)

        # Ask if the user wants to know the weather for tomorrow
        speak("Bạn muốn xem thời tiết cho ngày mai không?")
        response_tomorrow = get_text().lower()
        if "có" in response_tomorrow or "đúng" in response_tomorrow:
            get_weather_for_tomorrow(city)
    else:
        speak("Không tìm thấy thành phố!")

# def get_weather_for_tomorrow(city):
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    tomorrow_date = tomorrow.strftime("%Y-%m-%d")

    url = "http://api.openweathermap.org/data/2.5/forecast?"
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()

    if data["cod"] != "404":
        # Find the forecast for tomorrow
        for entry in data["list"]:
            dt_txt = entry["dt_txt"]
            if dt_txt.startswith(tomorrow_date):
                # Extract relevant information
                temp = entry["main"]["temp"]
                weather_des = entry["weather"][0]["description"]
                speak(f"Thời tiết cho ngày mai tại {city}: {translate_text(weather_des)} và nhiệt độ khoảng {temp} độ C.")
                break
    else:
        speak("Không thể lấy dữ liệu thời tiết cho ngày mai.")

def open_application(text):
    try:
        if "google" in text:
            speak("Mở Google Chrome", chat_box)
            os.startfile('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
        elif "word" in text:
            speak("Mở Microsoft Word", chat_box)
            os.startfile('C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE')
        elif "excel" in text:
            speak("Mở Microsoft Excel", chat_box)
            os.startfile('C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\EXCEL.EXE')
        elif "powerpoint" in text:
            speak("Mở Microsoft PowerPoint", chat_box)
            os.startfile('C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\POWERPNT.EXE')
        else:
            speak("Ứng dụng không được cài đặt hoặc không tìm thấy.", chat_box)
    except Exception as e:
        speak(f"Có lỗi khi mở ứng dụng: {e}", chat_box)

def change_wallpaper():
    api_key = 'RF3LyUUIyogjCpQwlf-zjzCf1JdvRwb--SLV6iCzOxw'
    url = 'https://api.unsplash.com/photos/random?client_id=' + api_key
    response = requests.get(url)
    data = response.json()
    photo_url = data['urls']['full']
    filepath = os.path.join(os.getenv('TEMP'), 'wallpaper.jpg')
    with open(filepath, 'wb') as file:
        file.write(requests.get(photo_url).content)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 3)
    speak('Hình nền máy tính vừa được thay đổi.', chat_box)


def tell_me():
    try:
        speak("Bạn muốn nghe về gì ạ!", chat_box)
        text = get_audio()
        if not text:
            speak("Tôi không nghe rõ. Bạn có thể nói lại không?", chat_box)
            return

        contents = wikipedia.summary(text).split('\n')
        speak(contents[0], chat_box)
        time.sleep(3)

        for content in contents[1:]:
            speak("Bạn muốn nghe tiếp hay không?", chat_box)
            ans = get_audio()
            if ans and "không" in ans.lower():
                speak("Cảm ơn bạn đã lắng nghe!", chat_box)
                break
            speak(content, chat_box)
            time.sleep(3)
    except wikipedia.DisambiguationError as e:
        speak("Chủ đề bạn yêu cầu quá chung chung. Hãy cụ thể hơn. Ví dụ: " + ", ".join(e.options[:5]), chat_box)
    except Exception as e:
        speak("Jarvis không thể định nghĩa được ngôn ngữ hoặc xảy ra lỗi: " + str(e), chat_box)


def read_news():
    speak("Bạn muốn đọc tin về chủ đề gì?", chat_box)
    topic = get_audio()
    time.sleep(3)
    if not topic:
        speak("Không có thông tin về chủ đề bạn yêu cầu.", chat_box)
        return

    params = {
        'apiKey': 'a0958e3dca0d45748c61ca9ab342224f',
        'q': topic,
    }

    api_url = 'http://newsapi.org/v2/top-headlines?'

    try:
        api_result = requests.get(api_url, params=params)
        api_response = api_result.json()

        if 'articles' in api_response:
            articles = api_response['articles']
            for number, article in enumerate(articles[:3], start=1):
                title = article.get('title', 'Không có tiêu đề')
                description = article.get('description', 'Không có mô tả')
                speak(f"Tin {number}: {title}. {description}", chat_box)
                time.sleep(5)
        else:
            speak(f"Không tìm thấy tin tức nào về {topic}.", chat_box)
    except Exception as e:
        speak(f"Có lỗi xảy ra: {e}", chat_box)

# def send_email(text):
#     speak('Bạn gửi email cho ai nhỉ')
#     recipient = get_text()
#     if 'yến' in recipient:
#         speak('Nội dung bạn muốn gửi là gì')
#         content = get_text()
#         mail = smtplib.SMTP('smtp.gmail.com', 587)
#         mail.ehlo()
#         mail.starttls()
#         mail.login('điền email của bạn', 'mật khẩu email')
#         mail.sendmail('email của bạn',
#                       'email người nhận', content.encode('utf-8'))
#         mail.close()
#         speak('Email của bạn vùa được gửi. Bạn check lại email nhé hihi.')
#     else:
#         speak('Jarvis không hiểu bạn muốn gửi email cho ai. Bạn nói lại được không?')

def translate(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def speech_translation_en():
    speak("Bạn muốn nói điều gì?", chat_box)
    user_input = get_audio()
    if user_input:
        translated_text = translate_text(user_input, target_language='en')
        speak(f"Translation: {translated_text}", chat_box)

def speech_translation_vn():
    speak("What would you like to say?", chat_box)
    user_input = get_audio()
    if user_input:
        translated_text = translate_text(user_input, target_language='vi')
        speak(f"Bản dịch: {translated_text}", chat_box)

def help():
    commands = """Tôi có thể làm những việc sau:
    - Chào hỏi
    - Hiển thị giờ
    - Mở website, ứng dụng
    - Tìm kiếm trên Google
    - Phát nhạc
    - Đổi hình nền
    - Đọc báo
    - Định nghĩa khái niệm
    - Dịch thuật
    - Và nhiều hơn nữa!"""
    speak(commands, chat_box)
    time.sleep(10)

def call_jarvis(chat_box):
    speak("Xin chào, bạn tên là gì?", chat_box)
    time.sleep(3)
    name = get_text()
    if name:
        speak("Chào bạn {}".format(name))
        time.sleep(3)
        speak("Tôi là Jarvis. Tôi có thể giúp gì cho bạn!", chat_box)
        time.sleep(5)
        while True:
            text = get_text()
            if not text:
                break
            elif "trò chuyện" in text or "nói chuyện" in text:
                hello(name)
            elif "dừng" in text or "thôi" in text or "bye" in text:
                stop()
                break
            elif "ngày" in text or "giờ" in text:
                get_time(text)
            elif "chơi nhạc" in text or "nghe nhạc" in text:
                play_youtube()
            # elif "thời tiết hôm nay" in text:
            #     weather()
            elif "đổi hình nền" in text:
                change_wallpaper()
            elif "có thể làm gì" in text:
                help()
                time.sleep(10)
            elif "định nghĩa" in text:
                tell_me()
            elif "đọc báo" in text:
                read_news()
            # elif "làm toán" in text:
            #     do_math(text)
            # elif "email" in text or "mail" in text or "gmail" in text:
            #     send_email(text)
            elif "dịch" in text:
                if "dịch tiếng anh" in text or "dịch tiếng Anh" in text:
                    speech_translation_en()
                elif "dịch tiếng việt" in text or "dịch tiếng Việt" in text:
                    speech_translation_vn()
                else:
                    speak("Xin lỗi, ngôn ngữ này tôi không biết! Hãy chọn lại")
            elif "mở" in text:
                if "mở google và tìm kiếm" in text:
                    google_search(text, chat_box)
                elif "." in text:
                    open_website(text, chat_box)
                else:
                    open_application(text)
            else:
                speak("Bạn cần Jarvis giúp gì ạ?")



def create_ui():
    start_button = tk.Button(root, text="Start Jarvis", font=("Arial", 14),
                             command=lambda: threading.Thread(target=call_jarvis, args=(chat_box,), daemon=True).start())
    start_button.pack(pady=10)

    root.mainloop()

create_ui()