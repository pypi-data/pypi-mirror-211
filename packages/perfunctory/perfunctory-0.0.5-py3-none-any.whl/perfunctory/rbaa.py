
import geocoder #install required "geocoder"
import socket
import speedtest #install required "speedtest-cli"
from googlesearch import search #install required "googlesearch-python"
from PyDictionary import PyDictionary #install required "PyDictionary"
import speech_recognition #install required
import pyttsx3 #install required
import platform
import psutil #install required
import calendar
import datetime
import pprint
import os
import shutil


#import requests
#from bs4 import BeautifulSoup #install required

class XXX:
    @staticmethod
    def date():
        now = datetime.datetime.now()
        current_date = now.strftime("%A, %d %B %Y")
        print("Current date:", current_date)

    @staticmethod
    def calendar():
        current_year = datetime.datetime.now().year
        for month in range(1, 13):
            print(calendar.month_name[month], current_year)
            pprint.pprint(calendar.monthcalendar(current_year, month), width=30)
            print()

    @staticmethod
    def location():
        g = geocoder.ipinfo('me')
        if g.ok:
            current_location = g.city
            print("Current location:", current_location)
        else:
            print("Unable to determine current location.")

    @staticmethod
    def time():
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current time:", current_time)

    @staticmethod
    def machineSpecs():
        # Get machine specifications using platform and psutil libraries
        system = platform.system()
        processor = platform.processor()
        architecture = platform.machine()
        node = platform.node()
        release = platform.release()
        version = platform.version()
        memory = round(psutil.virtual_memory().total / (1024**3), 2)  # Convert to GB
        
        # Print machine specifications
        print("Machine Specifications:")
        print(f"System: {system}")
        print(f"Processor: {processor}")
        print(f"Architecture: {architecture}")
        print(f"Node: {node}")
        print(f"Release: {release}")
        print(f"Version: {version}")
        print(f"Memory: {memory} GB")
        # Call the machineSpecs function to print the machine specifications

    @staticmethod
    def machineHardDrive():
        total_space = psutil.disk_usage('/').total
        health = psutil.disk_usage('/').percent

        print("Total Hard Drive Space: {:.2f} GB".format(total_space / (1024 ** 3)))
        print("Hard Drive Health: {}%".format(health))



    @staticmethod
    def getIp():
        local_ip = socket.gethostbyname(socket.gethostname())
        public_ip = geocoder.ip('me').ip
        print("Local IP:", local_ip)
        print("Public IP:", public_ip)
    
    @staticmethod
    def speedTest():
        st = speedtest.Speedtest()
        download_speed = st.download() / 10**6  # Convert to Mbps
        upload_speed = st.upload() / 10**6  # Convert to Mbps
        server = st.get_best_server()
        ping = server['latency']

        print("Server:", server['host'])
        print("Download Speed: {:.2f} Mbps".format(download_speed))
        print("Upload Speed: {:.2f} Mbps".format(upload_speed))
        print("Ping: {:.2f} ms".format(ping))

    @staticmethod
    def googleSearch(query):
        print("Google Search Results:")
        for i, result in enumerate(search(query, num_results=10), start=1):
            print(f"{i}. {result}")

    @staticmethod
    def meaning(query):
        dictionary = PyDictionary()
        meanings = dictionary.meaning(query)

        if meanings:
            print("Meanings:")
            for pos, meaning in meanings.items():
                print(f"{pos}:")
                for idx, m in enumerate(meaning, start=1):
                    print(f"{idx}. {m}")
        else:
            print("No meanings found.")

    @staticmethod
    def allTasks():
        # Get a list of all running processes and their resource usage
        processes = []
        for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                pinfo = proc.info
                processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Sort the processes by CPU usage
        sorted_processes = sorted(processes, key=lambda x: x['cpu_percent'] if x['cpu_percent'] is not None else 0, reverse=True)

        # Print the sorted processes with resource usage information
        print("Running tasks sorted by CPU usage:")
        print("PID    \tNAME                 \tCPU %\tMEMORY %")
        for process in sorted_processes:
            pid = process['pid']
            name = process['name'][:20]
            cpu_percent = process['cpu_percent'] if process['cpu_percent'] is not None else 0
            memory_percent = process['memory_percent'] if process['memory_percent'] is not None else 0
            print(f"{pid}\t{name:<20}\t{cpu_percent:.2f}\t{memory_percent:.2f}")

    
    @staticmethod
    def say(text):
        # Create a Text-to-Speech engine object
        engine = pyttsx3.init()

        # Set the voice properties to use a woman's voice
        voices = engine.getProperty('voices')
        female_voice = None
        for voice in voices:
            if "female" in voice.name.lower():
                female_voice = voice
                break
        if female_voice:
            engine.setProperty('voice', female_voice.id)

        # Convert the text to speech
        engine.say(text)
        engine.runAndWait()
        # Call the function to convert text to speech

    @staticmethod
    def manageFiles(folder_path):
        # Create a new folder for sorted files
        sorted_folder = os.path.join(folder_path, 'Sorted')
        os.makedirs(sorted_folder, exist_ok=True)

        # Iterate over files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Skip directories
            if os.path.isdir(file_path):
                continue

            # Get the file extension
            file_ext = os.path.splitext(filename)[1]

            # Create a new folder for the file extension if it doesn't exist
            ext_folder = os.path.join(sorted_folder, file_ext[1:].lower())
            os.makedirs(ext_folder, exist_ok=True)

            # Copy the file to the corresponding folder
            new_file_path = os.path.join(ext_folder, filename)
            shutil.copyfile(file_path, new_file_path)

        print('Files sorted successfully!')













class YYY:
    @staticmethod
    def say(text):
        # Create a Text-to-Speech engine object
        engine = pyttsx3.init()

        # Set the voice properties to use a woman's voice
        voices = engine.getProperty('voices')
        female_voice = None
        for voice in voices:
            if "female" in voice.name.lower():
                female_voice = voice
                break
        if female_voice:
            engine.setProperty('voice', female_voice.id)

        # Convert the text to speech
        engine.say(text)
        engine.runAndWait()


    @staticmethod    
    def listen(keyword_functions):
        r = speech_recognition.Recognizer()

        with speech_recognition.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)

        try:
            print("Recognizing speech...")
            text = r.recognize_google(audio)
            print("You said:", text)

            for keyword, function in keyword_functions.items():
                if keyword.lower() in text.lower():
                    print(f"Keyword '{keyword}' found!")
                    function()
                    break  # Exit the loop after executing the first matching function

            else:
                print("No matching keyword found.")

        except speech_recognition.UnknownValueError:
            print("Unable to recognize speech.")
        except speech_recognition.RequestError as e:
            print(f"Error: {str(e)}")





























