 #HumAIn_usecase

# **`XGBOOST TEAM MEMBERS`**
<br>• [Naomi Thiru](https://github.com/naomithiru) **(Project Manager)**
<br>• [Selma Esen](https://github.com/selmaesen)
<br>• [Sara Silvente](https://github.com/silventesa)
<br>• [Dilara Parry](https://github.com/trickydaze)

# <br>``What Is The Project?``
<br>The XGBOOST team approach on the HumAIn project is to make an exploratory analysis with data science approach for HumAIn to showcase the pre-COVID and post-COVID AI trends filtered by the industry. Our goal is here to extract useful information from AI news between 1997 and 2021 to get AI usecase trends to lead new investments for businesses.

# <br>``Who Is The Project For?``
<br>This product is designed to support HumAIn's Technology Evangelization vertical, to demonstrate to potential and/or ongoing clients the different AI trends, and usecases as they are currently adopted in various industries.

# <br>``Business or Data Science Approach``
<br>The finished product will offer a comprehensive analysis to get new business insights.
<br>The final results will be demonstrated on an interactive dashboard.

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

