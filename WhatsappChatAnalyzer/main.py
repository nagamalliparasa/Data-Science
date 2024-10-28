import streamlit as st
import matplotlib.pyplot as plt

from analyzer.preprocess import preprocessing
from analyzer.helper import *


st.sidebar.title("Whatsapp Chat Analyzer")

upload_file=st.sidebar.file_uploader("Choose a File")



if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode("utf-8")
    
    file_name='files/'+upload_file.name

    with open(file_name,'w',encoding='utf-8') as file: 
        file.write(data)

    # print("Data is ",data)

    df=preprocessing(data)
    st.dataframe(df)


    user_list=df['user'].unique().tolist()
    # print(user_list)
    # user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages,words,media,links=fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Messages")
            st.title(media)
        with col4:
            st.header("Links Included")
            st.title(links)

     # finding the busiest users in the group (group level)
        if selected_user=="Overall":
            st.title("Most Busy Users")
            x,new_df=most_busiest(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns([2,2])
            
            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
            
    
        # create wordcloud
        st.title("Word Cloud")
        df_wc=create_word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most common words")
        most_common=most_common_words(selected_user,df)

        fig,ax=plt.subplots() 
        ax.bar(most_common['word'],most_common['freq'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # st.dataframe(most_common)

        # emoji analysis

        emoji_df=emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax=plt.subplots()
            ax.bar(emoji_df[0].head(15),emoji_df[1].head(15))
            st.pyplot(fig)



st.sidebar.text("Developed by ")
st.sidebar.header("Parasa Nagamalleswara Rao")
