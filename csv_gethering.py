#libraries
import json
import pandas as pd
import numpy as np

# we have 4 different csv files:
# 1) contains ai news before 7th 2020 and preprocessed to extact keywords
# 2) contains ai news after 7th 2020 from MIT news
# 3) contains ai news after 7th 2020 from AInews
# 4) contains ai news after 7th 2020 from other sources (more than 10 different)


# df1:
news_data_df = pd.read_csv("news_data.csv")
news_data_df = news_data_df.drop(columns=["keywords", "word_count"])
news_data_df = news_data_df.rename({"keywords_8":"keywords"}, axis = 1)

# df2:
# MIT news
mit_df = pd.read_csv("MIT_news.csv")

#df3:
#AInews
ainews_df = pd.read_csv("AInews.csv")

# df4:
# other sources:
other_news = pd.read_csv("df_articles.csv")

def pre_clean(df):
    df.date = df.date.fillna("2020-01-01")
    df = df.rename({"link":"url"}, axis = 1)
    return df
csv_list = [news_data_df, mit_df, ainews_df, other_news]

for i in range(len(csv_list)):
    csv_list[i] = pre_clean(csv_list[i])

#concatnate all
news_df = pd.concat(csv_list)

#make the df prettier
news_df = news_df.dropna(subset=['text'])
news_df = news_df.drop(columns=["authors", "created_at", "updated_at", "Unnamed: 0"])
news_df['date'] = pd.to_datetime(news_df['date'],utc=True)
news_df = news_df.sort_values(by='date')

# store all the data in one csv:
news_df.to_csv('all_news.csv')