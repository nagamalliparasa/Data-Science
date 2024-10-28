from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

f=open("analyzer/stop_words.txt",'r',encoding='utf-8')
stop_words=f.read()

def get_links(msg):
    extractor=URLExtract()
    urls=extractor.find_urls(msg)
    return urls


def fetch_stats(user,data):
    if user!='Overall':
        data=data[data['user']==user]
    
    num_msgs=data.shape[0]
    words=[]
    for msg in data['message']:
        words.extend(msg.split())

    num_media_msgs=data[data['message']=='<Media omitted>\n'].shape[0]

    links=[]
    for msg in data['message']:
        urls=get_links(msg)
        if urls is not None:
            links.extend(urls)
        
    return num_msgs,len(words),num_media_msgs,len(links)
    # if user=='Overall':
    #     num_msgs=data.shape[0];
    #     words=[]
    #     for msg in data['message']:
    #         words.extend(msg.split())
    #     return num_msgs,len(words)
    # else:
    #     new_data=data[data['user']==user]
    #     num_msgs=new_data.shape[0]
    #     words=[]
    #     for msg in new_data['message']:
    #         words.extend(msg.split())
    #     return num_msgs,len(words)


def most_busiest(data):
    persons=data['user'].value_counts().head()
    df=round((data['user'].value_counts()/data.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return persons,df

def create_word_cloud(user,data):
    if(user!="Overall"):
        data=data[data['user']==user]
    temp=data[data['user']!='']
    temp=temp[temp['message']!=' <Media omitted>\n']
    def remove_stop_words(msg):
        words=msg.split()
        return " ".join([word for word in words if word not in stop_words])
    
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(data['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(user,data):
    if(user!='Overall'):
        data=data[data['user']==user]
    temp=data[data['user']!='']
    temp=temp[temp['message']!=' <Media omitted>\n']
    # stop_words=set(stopwords.words("english"))
    words=[]
    for msg in temp['message']:
        for word in msg.split():
            if word.lower() not in stop_words:
                words.append(word)
    df=pd.DataFrame(Counter(words).most_common(20),columns=['word','freq'])

    return df


def emoji_helper(user,data):
    if user!='Overall':
        data=data[data['user']==user]
    emojis=[]
    for msg in data['message']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df