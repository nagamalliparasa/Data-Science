import re

import pandas as pd


def change_timeframe(item):
    items=item.split()
    tm=items[-2]
    hr=int(items[1].split(":")[0])
    if(tm=='pm' and hr<12):
        t=items[1].split(':')
        num=int(t[0])+12
        t[0]=str(num)
        items[1]=":".join(t)
    return " ".join(items[:2])

def get_user(item):
    s=item.split(":")
    if len(s)>1:
        return s[0];
    return ""
def get_message(item):
    s=item.split(":")
    if len(s)>=2:
        return ":".join(s[1:]);
    return s[0]
def preprocessing(data):
    # f=open(text_file,'r',encoding='utf-8')
    # data=f.read()
    pattern=r'\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s[ap]m -'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)

    data=pd.DataFrame({'user_message':messages,'message_date':dates})
    
    data['time']=data['message_date'].apply(change_timeframe)
    data['time']=pd.to_datetime(data['time'],format='%d/%m/%Y, %H:%M')
    data.drop(columns=['message_date'],inplace=True)
    data.rename(columns={'time':'date'},inplace=True)

    data['user']=data['user_message'].apply(get_user)
    data['message']=data['user_message'].apply(get_message)
    data.drop(columns=['user_message'],inplace=True)

    data['year']=data['date'].dt.year
    data['month']=data['date'].dt.month_name()
    data['day']=data['date'].dt.day
    data['hour']=data['date'].dt.hour
    data['minute']=data['date'].dt.minute

    data=data[data['message']!=' Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.\n']
    # data.drop(columns=['date'],inplace=True)
    return data[data['message']!=" <Media omitted>\n"]
