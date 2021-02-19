 #HumAIn_usecase

# **`XGBOOST TEAM MEMBERS`**
<br>• Naomi Thiru **(Project Manager)**
<br>• Selma Esen
<br>• Sara Silvente
<br>• Dilara Parry

# <br>``What Is The Project?``
<br>The XGBOOST team take on the HumAIn project is to make an explanatory analysis with data science approach for HumAIn to showcase the pre-COVID and post-COVID trends filtered by the industry. Our goal is here to extract useful information from AI news between 1997 and 2021 to get AI usecase trends to lead new inwestments for businesses.

# <br>``Who Is The Project For?``
<br>It is directly for HumAIn to be used for their active or potential clientele.

# <br>``Business or Data Science Approach``
<br>The finished product will offer a comprehensive analysis to get new business insights.
<br>The graphs will be shown in the presentation.

# <br> ``Project Steps``
## <br>**1) Data Collecting (Parsing):**
<br>News articles and research papers have been collected from numerous sources to build a sufficient model for the project.
<br>‣ Libraries used: Beautifulsoup & Newspaper
<br>‣ Raw data figure: (+/-2200,10)

## <br>**2) The NLP Process:**
### <br>*Ⓐ Data Preprocessing:*
<br>We assembeled the data that we scraped different sources and made them clear and usable for our NLP process. 
<br>In order to identify the trends and the industries efficiently, we ellimineted the stop words and tokenize the news texts. 


### <br>*Ⓑ Keyword Extraction:*
<br>From the parsed data, it is crucial to extract keywords to categorize the trends. We have used textrank method to extract the keywords and afterwards we have chacked keyword bigrams.


### <br>*Ⓒ Model Initiation:*
<br>Our model is calculating the cosine similarities between the keywords and AI usecases and Indursries together. We have used for that process the pretrained NLP models. 

#### <br>*Used Libraries:*
➼ nltk
<br> ➼ flair
<br> ➼ spacy
<br> ➼ sklearn


### <br>*Ⓓ Visualization:*
<br>We have used Dash to create a Dashboard and Seaborn and Matplotlib to generate graphs to show the AI trends in the pre and post Covid AI news. 

## <br>**4) Deployment:**
<br>After the results of the model are presented in a dashboard, deployment is handled with Heroku https://aitrends.herokuapp.com/

