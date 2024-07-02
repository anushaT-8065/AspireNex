import re
import requests as rq
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext as st

rules = [
    (r'hello|hey|hi',"Hi there! How can I help you?"),
    (r'what is your name',"Myself Helpy - your chatbot!"),
    (r'what is your (favourite)',"I'm a rule-based chatbot. I don't think I can answer that."),
    (r'bye', "Goodbye! I hope you have a nice day!"),
    (r'how are you', "I'm good , thanks!"),
    (r'what is the weather in ([a-zA-Z\s]+)', "weather"),
    (r'what is the local time|what time is it|what time is it|what is the time' , "time"),
    (r'name a few countries',"India, Nepal, Thailand, Bhutan,Singapore, etc."),
    (r'who (are|is) you',"I am a chatbot!"),
    (r'what (is|are) (.+)',"Sorry, I'm not sure about that.")
]

openweather_api='bd5e378503939ddaee76f12ad7a97608'
weather_url='http://api.openweathermap.org/data/2.5/weather'

def weather(city):
    try:
        res=rq.get(weather_url,params={'q': city, 'appid': openweather_api,'units':'metric'})
        data=res.json()
        if data.get('cod')!=200:
            return "I couldn't find the weather of this city. Please try a different input."
        
        descrip= data['weather'][0]['description']
        temp=data['main']['temp']
        return f"The current weather in {city} is {descrip} with a temperatue of {temp}°C. "
    except Exception as e:
        return "There was an error fetching the information."

def time_func():
    try:
        local_time=datetime.now().strftime('%H:%M:%S')
        return f"The current local time is {local_time}"
    except Exception as e:
        return "There was an error fetching the information."


def handle_query(query):
    match=None
    resp=None

    for pattern,resp_type in rules:
        match=re.search(pattern,query.lower())
        if match:
            if resp_type == "weather":
                city=match.group(1)
                resp=weather(city)
            elif resp_type == "time":
                resp=time_func()
            else:
                resp=resp_type
            break
    
    if not resp:
        resp="I'm sorry , I couldn't understand that. You can try asking something else."
    return resp


def msg(event=None):
    inp=entry.get().strip()
    if inp=="":
        return
    
    chat_wind.configure(state=tk.NORMAL)
    chat_wind.insert(tk.END, f"You: {inp}\n")
    resp=handle_query(inp)
    chat_wind.insert(tk.END, f"ChatBot: {resp}\n")
    chat_wind.configure(state=tk.DISABLED)

    entry.delete(0,tk.END)

root = tk.Tk()
root.title("Chatbot")
root.geometry("500x500")

chat_wind=st.ScrolledText(root,wrap=tk.WORD)
chat_wind.pack(padx=10,pady=10,fill=tk.BOTH, expand=True)
chat_wind.configure(state = tk.DISABLED)

entry=tk.Entry(root,width=80)
entry.pack(padx=10,pady=5,side=tk.LEFT,expand=True)

entry.bind('<Return>',msg)
send = tk.Button(root,text="Send ->",command=msg)
send.pack(padx=10,pady=5,side=tk.RIGHT)

chat_wind.configure(state=tk.NORMAL)
chat_wind.insert(tk.END,"Chatbot: Hi there! How can I help you? \n")
chat_wind.insert(tk.END,"Try asking me the following questions - \n 1.How are you? \n 2.What is the weather in Bengaluru? \n 3.Name a few countries\n")
chat_wind.insert(tk.END,"Type 'bye' to end the chat\n")
chat_wind.configure(state=tk.DISABLED)

root.mainloop()




