#necessary libraries

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from newspaper import Article


# scraping form MIT

# MIT AI news urls
links = []
url = "https://news.mit.edu/search?keyword=artificial%20intelligence%20&publication_date%5Bmin%5D=2020-02-08&publication_date%5Bmax%5D=2021-02-10"
for n in range(12):
    url = url+"&page="+str(n)
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    for article in soup.find_all("article"):
        link = article.find("a", class_="search-result-item--title--link")["href"]
        link = "https://news.mit.edu" + link
        links.append(link)

#Intialize list articles_info list
articles_info = []
for i in links:
    page = requests.get(i).text
    soup = BeautifulSoup(page, "lxml")
    article = soup.find("article")
    #Intialize dictionary
    article_dict = {}
    #Insert link "i" into the dictionary
    article_dict["link"] = i
    #Pass link into Article() function
    art = Article(i)
    #Download contents of art object
    art.download()
    
    #Try/except is included because not all articles can be parsed
    try:
        #If article can be successfully parsed then insert its text, title, publish_date, keywords
        #and summary into corresponding keys
        art.parse()
        article_dict["text"] = article.find("div", class_="news-article--content--body").text
        article_dict["title"] = art.title
        article_dict["date"] = article.find("div", class_="news-article--publication-date").time["datetime"].split("T")[0]
        article_dict["author"] = art.authors
        tag_list = []
        for n in article.find_all("li", class_="news-article--topics-list--item"):
            tag_list.append(n.a.text)
        article_dict["tags"] = '/'.join(tag_list)
        art.nlp()
        article_dict["keywords"] = art.keywords
        article_dict["summary"] = art.summary
        

    except ArticleException:
        #If article cannot be parse then insert null values for the following keys:
        #"text", "title", "date", "keywords", and "summary"
        article_dict["text"] = np.nan
        article_dict["title"] = np.nan
        article_dict["date"] = np.nan
        article_dict["author"] = np.nan
        article_dict["tags"] = np.nan
        article_dict["keywords"] = np.nan
        article_dict["summary"] = np.nan

        
    #Insert dictionary of article info into the articles_info list
    articles_info.append(article_dict)
#Pass the list of dictionaries into a pandas data frame
corpus = pd.DataFrame(articles_info)

corpus["author"] = corpus["author"].astype(str)

corpus["source"] = "Mit"

#store as a cvs file
corpus.to_csv('MIT_news.csv')

#---------------------------
# scraping form AInews

# AInews links from google search

main_urls = ["https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk024CroNXGfBbu47BL_HBqbrShDAmQ:1613135593077&ei=6X4mYO2aBKePlwS-hJzYAg&start=0&sa=N&ved=2ahUKEwits_-vtuTuAhWnx4UKHT4CBys4ChDy0wN6BAgFEDU&biw=1440&bih=789",
              "https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk03_0S6MP9mrO3q6eQpFBrB9NhsNcg:1613136050114&ei=soAmYNygBoWWafzPoMgN&start=10&sa=N&ved=2ahUKEwjcwfaJuOTuAhUFSxoKHfwnCNkQ8tMDegQIERA3&biw=885&bih=789",
              "https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk02WyIrlwVREIbSwHQT5l9SWpVefGw:1613144634470&ei=OqImYPyDHI2maNWVrvAO&start=20&sa=N&ved=2ahUKEwj8iKKH2OTuAhUNExoKHdWKC-44ChDw0wN6BAgDEEo&biw=885&bih=789",
              "https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk03aCzKqLF5FXL0Pl0wIX7mUHBirzQ:1613144761830&ei=uaImYOmmMs_0aM7ntNgM&start=30&sa=N&ved=2ahUKEwip5__D2OTuAhVPOhoKHc4zDcs4FBDy0wN6BAgEEDw&biw=885&bih=789",
              "https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk01ZyzS0rus5HBWwjN1ffhGFwy8ezw:1613144790896&ei=1qImYO2UNseblwTuzYywAQ&start=40&sa=N&ved=2ahUKEwjt1-3R2OTuAhXHzYUKHe4mAxY4HhDy0wN6BAgFED0&biw=885&bih=789",
              "https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk00ZOWS4RQjJcXMxFAGPwewG4M8EIw:1613144828764&ei=_KImYILvLayZlwSzhpHoCg&start=50&sa=N&ved=2ahUKEwiC3fTj2OTuAhWszIUKHTNDBK04KBDy0wN6BAgFED8&biw=885&bih=789",
              "https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk02EQDwzhFTljdE-qZQBzQjMK6bRKw:1613144856834&ei=GKMmYKepMo2MlwSUuqa4DA&start=60&sa=N&ved=2ahUKEwinlabx2OTuAhUNxoUKHRSdCcc4MhDy0wN6BAgFEEA&biw=885&bih=789",
              "https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk02DbiUSJiaMWVCDy1g7W-LvpoyNMw:1613145060353&ei=5KMmYNCJFe-TlwSetoGgCw&start=70&sa=N&ved=2ahUKEwjQi6zS2eTuAhXvyYUKHR5bALQ4PBDy0wN6BAgFEEA&biw=885&bih=789",
              "https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk01daC74Jcugl6sTWnvthIIQK5o_HA:1613145122839&ei=IqQmYM3VMumKlwTtyoTwDQ&start=80&sa=N&ved=2ahUKEwjN7pHw2eTuAhVpxYUKHW0lAd44RhDy0wN6BAgFEEA&biw=885&bih=789",
              "https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk011Debk7ytzwh2RKNsXLOd7fLFNwg:1613145140210&ei=NKQmYJCjDMP4aPyUifAE&start=90&sa=N&ved=2ahUKEwiQjbb42eTuAhVDPBoKHXxKAk44UBDy0wN6BAgFEEA&biw=885&bih=789",
              "https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk01JwvgtsLH8QX7U0diPdJZu-5tswQ:1613145161951&ei=SaQmYM26OYuoa6iPi9AB&start=100&sa=N&ved=2ahUKEwiNg-WC2uTuAhUL1BoKHajHAho4WhDy0wN6BAgFEEA&biw=885&bih=789",
              "https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk00HSVPhdfOGYjh1X1TPZo1LsIS8WA:1613145183527&ei=X6QmYL_HH5HeavethKAN&start=110&sa=N&ved=2ahUKEwj_8omN2uTuAhURrxoKHfcWAdQ4ZBDy0wN6BAgFEEI&biw=885&bih=789",
              "https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk03qDj9NgQfLv0pQ_fFqxE5BVeDTcQ:1613145202818&ei=cqQmYPqjMcjolwTgyJLgAg&start=120&sa=N&ved=2ahUKEwj6pKOW2uTuAhVI9IUKHWCkBCw4bhDy0wN6BAgFEEQ&biw=885&bih=789",
              "https://www.google.com/search?q=AI+site:https://artificialintelligence-news.com/&lr=&hl=en&tbs=qdr:y&sxsrf=ALeKk00kxP2rvoFLWkZ_OvnIp7tVKcEjPg:1613145218623&ei=gqQmYJvDJcuIae2onrgE&start=130&sa=N&ved=2ahUKEwibjOid2uTuAhVLRBoKHW2UB0c4eBDy0wN6BAgFEEY&biw=885&bih=789"
            ]

link_list = []
for url in main_urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    links = soup.find_all("a")
    for link in links:
        link = str(link["href"]).split("&")[0]
        if "/url?q=" in str(link) and "accounts.google" not in str(link):
            link_list.append(link.replace("/url?q=", ""))
        


#Intialize list articles_info list
articles_info = []
for i in link_list:
    page = requests.get(i).text
    soup = BeautifulSoup(page, "lxml")
    article = soup.find("article")
    #Intialize dictionary
    article_dict = {}
    #Insert link "i" into the dictionary
    article_dict["link"] = i
    #Pass link into Article() function
    art = Article(i)
    #Download contents of art object
    art.download()
    
    #Try/except is included because not all articles can be parsed
    try:
        #If article can be successfully parsed then insert its text, title, publish_date, keywords
        #and summary into corresponding keys
        art.parse()
        article_dict["text"] = article.text
        article_dict["title"] = art.title
        article_dict["date"] = art.publish_date
        article_dict["author"] = art.authors
        tag_list = []
        art.nlp()
        article_dict["keywords"] = art.keywords
        article_dict["summary"] = art.summary
        

    except ArticleException:
        #If article cannot be parse then insert null values for the following keys:
        #"text", "title", "date", "keywords", and "summary"
        article_dict["text"] = np.nan
        article_dict["title"] = np.nan
        article_dict["date"] = np.nan
        article_dict["author"] = np.nan
        article_dict["keywords"] = np.nan
        article_dict["summary"] = np.nan

        
    #Insert dictionary of article info into the articles_info list
    articles_info.append(article_dict)
#Pass the list of dictionaries into a pandas data frame
corpus2 = pd.DataFrame(articles_info)

corpus2["source"] = "AInews"

#store as a cvs file
corpus2.to_csv('AInews.csv')

#---------------------------
# scraping articles from other sources

def linkstolist(links,list):
    for i in links:
        article_dict = {}
        article_dict["link"] = i
        art = Article(i)
        art.download()
        try:
            art.parse()
            article_dict["title"] = art.title
            article_dict["date"] = art.publish_date
            article_dict["text"] = art.text
            art.nlp()
            article_dict["keywords"] = art.keywords
            article_dict["summary"] = art.summary
        except ArticleException:
        # If article cannot be parse then insert null values for the following keys:
        # "text", "title", "date", "keywords", and "summary"
            article_dict["text"] = np.nan
            article_dict["title"] = np.nan
            article_dict["date"] = np.nan
            article_dict["keywords"] = np.nan
            article_dict["summary"] = np.nan
        list.append(article_dict)


def datatolist(data,keys):
    for i in data.keywords:
        for x in i:
            s= keys.append(x)
    return s

articles=['https://www.marktechpost.com/2021/02/13/microsoft-azure-ai-is-bringing-iconic-characters-to-life-with-the-help-of-custom-neural-voice-and-5g-network/','https://venturebeat.com/2021/02/13/ai-progress-depends-on-us-using-less-data-not-more/','https://towardsdatascience.com/classification-in-security-operations-dc6f43adcae8','https://www.forbes.com/sites/hannahmayer/2021/02/14/from-mission-control-to-mission-connect-how-nasa-is-repositioning-itself-with-digital-transformation/','https://www.finanzen.at/nachrichten/aktien/wellai-scientists-to-present-research-based-on-the-covid-19-research-tool-at-the-global-ifcc-conference-1030079873','https://www.wsj.com/articles/ai-emerges-as-crucial-tool-for-groups-seeking-justice-for-syria-war-crimes-11613228401','https://www.varesenews.it/2021/02/laboratory-automation-serving-scientific-research/1306918/','https://aithority.com/technology/analytics/realpage-presents-new-data-reinforcing-the-value-of-ai-screening/','https://microcapdaily.com/major-move-on-plyz-plyzer-technologies-plyzer-intelligence-ai-machine-learning-product-matching/130317/','https://www.dailystar.co.uk/news/latest-news/real-life-minority-report-ai-23496623','https://analyticsindiamag.com/how-machine-learning-streamlines-risk-management/','http://www.tribtown.com/2021/02/13/ap-hkn-nhl-tech-upgrade/','https://www.analyticsinsight.net/unfortunately-commercial-ai-is-failing-heres-why/','https://indiaeducationdiary.in/artificial-intelligence-for-dementia-prevention/','https://towardsdatascience.com/introducing-transformers-interpret-explainable-ai-for-transformers-890a403a9470','https://micky.com.au/ai-can-now-learn-to-manipulate-human-behaviour/','https://techcrunch.com/2021/02/13/9-investors-discuss-challenges-opportunities-and-the-impact-of-cloud-vendors-in-enterprise-data-lakes/','https://analyticsindiamag.com/a-birds-eye-view-on-use-of-ai-ml-in-airlines-industry/','https://www.forbes.com/sites/tomtaulli/2021/02/13/aiops-how-to-get-started/','https://towardsdatascience.com/forecasting-of-periodic-events-with-ml-5081db493c46','https://towardsdatascience.com/the-ai-ml-fda-plan-efb384c9bf31','https://www.marktechpost.com/2021/02/12/baidu-team-introduces-ernie-m-a-multilingual-model-that-learns-96-languages-from-monolingual-corpora/','https://towardsdatascience.com/deepmind-releases-a-new-state-of-the-art-image-classification-model-nfnets-75c0b3f37312','https://venturebeat.com/2021/02/13/ai-progress-depends-on-us-using-less-data-not-more/','https://venturebeat.com/2021/02/13/michael-hurlston-how-synaptics-pivoted-from-mobile-pc-sensors-to-the-internet-of-things/','https://www.sciencedaily.com/releases/2021/02/210211113917.htm','https://venturebeat.com/2021/02/13/thought-detection-ai-has-infiltrated-our-last-bastion-of-privacy/','https://techbullion.com/how-ai-technology-makes-manufacturing-smarter/','https://newscenter.lbl.gov/2021/02/12/applying-quantum-computing-to-a-particle-process/','https://siliconangle.com/2021/02/12/future-compute-will-big-small-smart-way-edge/','https://towardsdatascience.com/a-data-science-perspective-to-automated-valuation-models-435a19326dbc','https://towardsdatascience.com/cognitive-risk-management-7c7bcfe84219','https://www.navsea.navy.mil/Media/News/SavedNewsModule/Article/2502702/nswc-dahlgren-division-automates-target-detection-and-tracking-for-armys-next-g/','https://syncedreview.com/2021/02/12/deepmind-ucls-alchemy-is-a-best-of-both-worlds-3d-video-game-for-meta-rl/','https://uk.finance.yahoo.com/news/worldwide-automotive-artificial-intelligence-industry-110300294.html','https://europeangaming.eu/portal/latest-news/2021/02/12/86619/agechecked-and-rdentify-partner-to-help-identify-vulnerable-players/','https://www.wfmz.com/news/pr_newswire/pr_newswire_technology/quantiphi-named-as-an-idc-innovator-in-artificial-intelligence-services/article_c228db75-a2a3-553e-93fb-fc8273fcec96.html','https://www.tvtechnology.com/news/nhl-selects-aws-for-cloud-infrastructure','https://towardsdatascience.com/synthetic-data-applications-in-data-privacy-and-machine-learning-1078bb5dc1a7','https://www.analyticsinsight.net/a-new-ai-algorithm-detecting-asymptomatic-carriers-of-covid-19/','https://venturebeat.com/2021/02/12/ai-weekly-techno-utopianism-in-the-workplace-and-the-threat-of-excessive-automation/','https://towardsdatascience.com/facebook-detr-transformers-dive-into-the-object-detection-world-39d8422b53fa','https://www.mcknights.com/blogs/guest-columns/how-we-used-machine-learning-to-reduce-rehospitalizations/','https://www.wired.com/story/microsoft-win-quantum-computing-error/','https://phys.org/news/2021-02-tackles-central-powerful-quantum.html','https://www.smartcitiesworld.net/opinions/opinions/reviving-smart-cities-with-edge-computing-and-5g','https://towardsdatascience.com/a-primer-on-the-sources-of-biases-in-data-mining-for-machine-learning-d82e89604693','https://www.miragenews.com/artificial-intelligence-can-boost-disaster-513730/','https://www.prweb.com/releases/quantiphi_named_as_an_idc_innovator_in_artificial_intelligence_services/prweb17721733.htm','https://www.iotforall.com/automotive-manufacturing-and-advanced-artificial-intelligence','http://www.hedgeweek.com/2021/02/12/295869/ex-jp-morgan-strategist-unveils-machine-learning-us-equity-hedge-fund-falcon','https://www.smartcitiesworld.net/news/news/start-up-helps-turin-to-optimise-healthcare-and-covid-19-vaccine-spaces-6092','https://techcrunch.com/2021/02/12/swedens-data-watchdog-slaps-police-for-unlawful-use-of-clearview-ai/','https://www.analyticsinsight.net/artificial-intelligence-redefining-and-innovating-the-textile-industry/','https://pulse2.com/machine-learning-cloud-infrastructure-company-pinecone-raises-10-million/','https://venturebeat.com/2021/02/11/quantum-venture-funding-dipped-12-in-2020-but-quantum-investments-rose-46/','https://www.discovermagazine.com/the-sciences/quantum-computer-chips-manufactured-using-mass-market-industrial-fabrication','http://www.nextplatform.com/2021/02/11/the-billion-dollar-ai-problem-that-just-keeps-scaling/','https://phys.org/news/2021-02-machine-stellar-tess.html','https://www.businessinsider.com/labelbox-40m-seriesc-funding-data-labeling-machine-learning-2021-2','https://aithority.com/technology/analytics/piano-software-elevates-flagship-product-composer-with-new-data-and-machine-learning-capabilities-for-more-powerful-customer-journey-design/','https://screenrant.com/star-wars-episode-10-artificial-intellegence-parody-video/','https://analyticsindiamag.com/how-genpact-uses-ai-to-automate-vehicle-insurance-claims-process/','https://venturebeat.com/2021/02/11/researchers-propose-platform-for-evaluating-ai-disease-forecasting-methods/','https://siliconangle.com/2021/02/11/labelbox-raises-40m-automate-data-labeling-ai-model-development/','https://www.techrepublic.com/article/aws-ibm-google-and-microsoft-are-taking-ai-from-1-0-to-2-0-according-to-forrester/','https://www.aitrends.com/ai-trends-insider-on-executive-leadership/ai-holistic-adoption-for-manufacturing-and-operations-ethics/','https://www.sciencedaily.com/releases/2021/02/210210133407.htm','https://www.aitrends.com/ai-and-space-exploration/scientists-pursue-a-range-of-projects-employing-ai-for-space-exploration/','https://venturebeat.com/2021/02/11/bowery-cto-injong-rhee-on-the-grand-challenge-of-ai-for-indoor-farming/','https://venturebeat.com/2021/02/11/nvidia-researchers-train-ai-to-reward-dogs-for-responding-to-commands/','https://petapixel.com/2021/02/11/canons-new-app-culls-photos-with-artificial-intelligence/','https://www.privateinternetaccess.com/blog/code-is-law-why-software-openness-and-algorithmic-transparency-are-vital-for-privacy/','https://www.itproportal.com/features/key-data-trends-for-2021-and-beyond/','https://www.information-age.com/qa-helping-government-singapore-improve-virtual-agents-123493801/','https://www.zdnet.com/article/ibm-and-exxonmobil-are-building-quantum-algorithms-to-solve-this-giant-optimization-problem/','https://www.forbes.com/sites/sap/2021/02/11/how-big-data-predictive-analytics-and-machine-learning-changed-the-railway-industry/','https://www.eureporter.co/general/2021/02/11/how-artificial-intelligence-is-used-in-online-casinos/','https://techobserver.in/2021/02/11/sebi-to-bank-on-ai-based-technology-for-inspections-and-surveillance-of-mutual-funds/','https://venturebeat.com/2021/02/11/immunai-raises-60-million-to-analyze-the-immune-system-with-ai/','https://venturebeat.com/2021/02/11/labelbox-raises-40-million-for-its-data-labeling-and-annotation-tools/','https://www.marktechpost.com/2021/02/11/fda-gives-landmark-clearance-to-clews-ai-driven-icu-predictive-tool/','https://www.analyticsinsight.net/a-look-at-5-ai-startups-empowering-defence-and-security-industry/','http://www.medicaldesignandoutsourcing.com/cardiologs-touts-results-of-afib-study/','https://techcrunch.com/2021/02/11/base-operations-raises-2-2-million-to-modernize-physical-enterprise-security/','http://aiweekly.co/issues/200','https://techcrunch.com/2021/02/11/intenseye-raises-4m-to-boost-workplace-safety-through-computer-vision/','https://www.sciencedaily.com/releases/2021/02/210210142049.htm','https://venturebeat.com/2021/02/10/neureality-emerges-from-stealth-to-accelerate-ai-workloads-at-scale/','https://www.medtechintelligence.com/column/quantum-computing-makes-inroads-in-life-sciences/','https://metrology.news/machine-learning-fault-detection-to-deliver-on-smart-factory-aerospace-fasteners-production-line/','https://www.rtinsights.com/6q4-nlp-expert-neta-snir-on-how-ai-can-save-lives/','https://www.theengineer.co.uk/new-study-uses-wireless-signals-for-emotion-detection/','https://www.techgenyz.com/2021/02/10/google-cloud-finds-verloop-ios/','https://economictimes.indiatimes.com/tech/startups/vernacular-ai-makes-key-hires-to-leadership-team-ramps-up-headcount/articleshow/80830313.cms','https://techcrunch.com/2021/02/10/scalarr-series-a/','https://customerthink.com/2021-emerging-ai-trends-in-the-telecom-industry/','https://www.information-age.com/the-3-ai-startups-revolutionising-the-defence-sector-123493776/','https://www.medianama.com/2021/02/223-sebi-upgrading-it-infrastructure/','https://www.businessinsider.in/science/health/news/ai-in-healthcare-is-set-to-open-up-a-range-of-futuristic-job-profiles-in-healthcare/articleshow/80833859.cms','https://www.cnet.com/news/experience-synesthesia-google-tool-lets-you-hear-colors-and-shapes/','https://www.news-medical.net/news/20210210/Metabolomics-and-machine-learning-used-to-identify-possible-COVID-19-biomarkers.aspx','https://www.enterpriseai.news/2021/02/10/where-to-expect-enterprise-ai-growth-in-2021-more-predictions-from-our-ai-experts/','https://www.miragenews.com/lab-researchers-explore-learn-by-calibration-512516/','https://www.hpcwire.com/2021/02/10/chinese-company-launches-origin-pilot-os-for-quantum-computing/','https://techcrunch.com/2021/02/10/lang-ai-snags-2m-to-remove-technical-burden-of-implementing-ai-for-businesses/','https://www.forbes.com/sites/davidteich/2021/02/10/ecommerce-delivery-and-the-gig-economy-create-opportunities-for-both-fraud-and-the-artificial-intelligence-to-detect-it/','https://www.techrepublic.com/article/study-robots-are-trusted-more-than-people-when-it-comes-to-money-management/','https://techcrunch.com/2021/02/09/with-ai-translation-service-that-rivals-professionals-lengoo-attracts-new-20m-round/','https://www.sciencedaily.com/releases/2021/02/210210091126.htm','https://venturebeat.com/2021/02/10/cye-raises-120-million-for-security-that-uses-hackers-and-ai/','https://venturebeat.com/2021/02/10/bighat-raises-19-million-for-an-ai-powered-antibody-design-platform/','https://www.sciencedaily.com/releases/2021/02/210205104219.htm','https://venturebeat.com/2021/02/10/salesforce-brings-intelligent-document-automation-to-health-cloud/','https://venturebeat.com/2021/02/10/vivun-raises-35-million-to-advance-presales-engineering-platform/','https://venturebeat.com/2021/02/10/rhino-health-emerges-from-stealth-to-bring-hospital-data-to-federated-learning/','https://venturebeat.com/2021/02/09/theator-raises-15-5-million-to-analyze-surgical-footage-with-computer-vision/','https://www.enterpriseai.news/2021/02/09/ai-tool-emerges-to-hasten-vaccine-development/','https://techcrunch.com/2021/02/09/sentinelone-acquires-high-speed-logging-startup-scalyr-for-155m/','https://techcrunch.com/2021/02/05/orwellian-ai-lie-detector-project-challenged-in-eu-court/','https://research.aimultiple.com/voice-recognition-applications/','https://www.aitrends.com/security/solarwinds-hack-likely-assisted-by-ai-suggests-microsofts-smith/','https://www.aitrends.com/ai-in-government/ai-applied-to-tax-systems-can-help-discover-shelters-support-equality/','https://www.aitrends.com/startups/startup-mojo-vision-eyes-a-future-in-smart-contact-lenses/','https://techcrunch.com/2021/02/03/evinced-raises-17m-to-speed-up-accessibility-testing-for-the-web/','https://techcrunch.com/2021/02/02/trustlayer-raises-6m-seed-to-become-the-carta-for-insurance/','https://research.aimultiple.com/self-driving-cars-stats/','https://www.sciencedaily.com/releases/2021/01/210130092754.htm','https://www.aitrends.com/security/cybersecurity-tools-gaining-an-edge-from-ai/','https://www.aitrends.com/financial-services/financial-firms-turning-to-ai-to-fight-fraud-in-2021/','https://www.aitrends.com/transportation/ai-seen-helping-to-reduce-pollution-save-fuel-ease-traffic/','https://www.aitrends.com/ai-insider/ai-autonomous-cars-as-drug-mules-for-narco-dealers-is-a-bad-prescription/','https://www.theguardian.com/science/2021/jan/26/us-has-moral-imperative-to-develop-ai-weapons-says-panel','https://research.aimultiple.com/chatbot-best-practices/','https://www.sciencedaily.com/releases/2021/01/210121132127.htm','https://www.theguardian.com/environment/2021/jan/15/how-ai-helped-find-millions-of-trees-in-the-sahara-aoe','https://techcrunch.com/2021/02/03/deep-science-ais-with-high-class-and-higher-altitudes/','https://www.sciencedaily.com/releases/2021/02/210204192543.htm','https://www.sciencedaily.com/releases/2021/02/210208125357.htm','https://techcrunch.com/2021/02/09/nextmv-raises-8m-series-a-to-increase-accessibility-to-its-automation-optimization-tech/','https://techcrunch.com/2021/02/09/with-ai-translation-service-that-rivals-professionals-lengoo-attracts-new-20m-round/','https://news.mit.edu/2021/language-learning-efficiency-0210','https://thenextweb.com/neural/2021/02/10/anti-trashbug-ai-scours-sky-snaps-to-spot-sea-plastic/','https://www.analyticsinsight.net/are-psychologists-the-next-target-for-ai-machine-learning/','https://analyticsindiamag.com/from-being-broke-to-creating-a-leading-chatbot-how-these-two-ex-fractalites-created-ori/','https://www.eetimes.com/israeli-ai-chip-startup-raises-seed-funding/','https://www.prnewswire.com/news-releases/oracle-brings-new-level-of-intelligence-to-construction-projects-301225453.html','https://venturebeat.com/2020/08/23/the-term-ethical-ai-is-finally-starting-to-mean-something/','https://venturebeat.com/2020/05/04/plotmachines-ai-long-form-stories/','https://www.aimagazine.com/data-and-analytics/data-poisoning-new-front-ai-cyber-war','https://www.aimagazine.com/ai-strategy/saudi-arabia-launches-dollar20bn-ai-strategy-bid','https://www.aimagazine.com/ai-applications-1/darpa-seeks-improve-ai-standards-dollar1m-ditto-project','https://www.aimagazine.com/ai-strategy/wef-ai-automation-cost-17m-jobs-year','https://www.aimagazine.com/ai-strategy/ai-transformation-global-trade-ecosystem-underway','https://www.aimagazine.com/machine-learning/baidu-debuts-latest-version-ai-platform-baidu-brain','https://www.aimagazine.com/machine-learning/ai-and-ml-ace-healthcare-industrys-sleeve','https://www.aimagazine.com/machine-learning/eagle-eye-ai-transforming-expense-management-heres-how','https://www.aimagazine.com/data-and-analytics/datarobots-enterprise-ai-and-ml-cloud-platform','https://www.aimagazine.com/technology-9/graphcores-intelligent-processing-unit-ai-and-ml','https://www.aimagazine.com/ai-applications-1/intel-and-esa-launch-experimental-ai-satellite-phisat-1','https://www.aimagazine.com/ai-applications-1/beyond-limits-partners-nvidia-ai-energy-sector','https://www.aimagazine.com/machine-learning/sabre-corporation-develops-travel-ai-platform-google','https://www.aimagazine.com/interviews/michael-kanaan-usafmit-ai-accelerator','https://www.aimagazine.com/ai-strategy/interview-pascal-bornet-intelligent-automation','https://www.aimagazine.com/machine-learning/machine-learning-music-googles-tone-transfer','https://www.aimagazine.com/top10/top-10-cars-ai-features','https://www.aimagazine.com/technology-9/demystifying-role-rpa-among-automation-solutions','https://www.aimagazine.com/ai-applications/startup-extend-robotics-launches-vr-controlled-robot-arm','https://www.aimagazine.com/ai-applications-1/uber-sells-atg-self-driving-unit-aurora','https://www.aimagazine.com/machine-learning/cambridge-university-build-ai-chemical-research-lab','https://www.aimagazine.com/data-and-analytics/starburst-becomes-latest-enterprise-data-unicorn','https://www.aimagazine.com/technology-9/how-unilever-driving-digital-transformation-manufactur-intelligent-powder-towers-are-keeping-its-manufacturing-powder-dry-during-pandemic','https://www.aimagazine.com/interviews/satyan-abraham-digital-transformation-journey-dubai','https://www.aimagazine.com/interviews/panasonic-using-technology-address-customer-challenges','https://www.aimagazine.com/company/cellcard-delivering-cambodias-5g-digital-transformation','https://www.aimagazine.com/data-and-analytics/get-data-science-out-it-departments-and-boardrooms','http://aiweekly.co/issues/186','http://aiweekly.co/issues/185','http://aiweekly.co/issues/183','http://aiweekly.co/issues/182','http://aiweekly.co/issues/180','http://aiweekly.co/issues/179','http://aiweekly.co/issues/177','http://aiweekly.co/issues/175','http://aiweekly.co/issues/174','http://aiweekly.co/issues/172','http://aiweekly.co/issues/170','http://aiweekly.co/issues/168','http://aiweekly.co/issues/167','http://aiweekly.co/issues/166','http://aiweekly.co/issues/164','http://aiweekly.co/issues/163','http://aiweekly.co/issues/162','http://aiweekly.co/issues/160','http://aiweekly.co/issues/158','http://aiweekly.co/issues/156','http://aiweekly.co/issues/149','http://aiweekly.co/issues/146','https://www.aitrends.com/healthcare/google-move-into-healthcare-leveraging-its-ai-getting-more-pronounced/','https://www.aitrends.com/2021-ai-predictions/2021-predictions-rise-of-glocalization-model-monitoring-focus-on-supply-chain/','https://www.aitrends.com/startups/startup-truera-raising-money-to-get-ai-explainability-solution-to-market/','https://www.aitrends.com/ai-insider/ai-autonomous-cars-might-not-know-they-were-in-a-car-crash/','https://www.aitrends.com/healthcare/how-ai-is-helping-with-covid-19-vaccine-rollout-and-tracking/','https://www.aitrends.com/ai-in-marine-industry/first-harvest-selects-sea-machines-to-launch-autonomous-hybrid-cargo-vessel/','https://www.aitrends.com/workforce/itserve-alliance-wins-court-ruling-on-h-1b-visa-prevailing-wages/','https://www.aitrends.com/ai-insider/ai-autonomous-cars-to-ultimately-bolster-the-christmas-holidays/','https://www.aitrends.com/ethics-and-social-issues/google-wades-into-controversy-with-dismissal-of-ai-ethicist-timnit-gebru/','https://www.aitrends.com/ai-in-business/new-ai-chips-managed-services-among-flood-from-aws-at-reinvent-2020/','https://www.aitrends.com/ai-research/fords-use-of-ai-an-example-of-shaping-of-innovation-in-mit-future-of-work-session/','https://www.aitrends.com/ai-insider/complexities-when-ai-autonomous-cars-attempt-zipper-merging/','https://www.aitrends.com/ai-in-industry/construction-industry-beginning-to-use-ai-powered-robots-and-drones-on-site/','https://www.aitrends.com/security/cryptographic-breakthrough-on-io-said-to-be-a-crown-jewel-for-security/','https://www.aitrends.com/ai-in-business/kdp-using-ai-to-fuel-expansion-strategy-with-sales-boosted-during-pandemic/','https://www.aitrends.com/ai-insider/prospects-of-empty-roaming-ai-autonomous-cars-aplenty/','https://www.aitrends.com/cloud-2/power-of-ai-with-cloud-computing-is-stunning-to-microsofts-nadella/','https://www.aitrends.com/ai-and-business-strategy/it-departments-find-timing-is-good-to-modernize-legacy-systems-ai-can-help/','https://www.aitrends.com/ai-insider/ai-autonomous-cars-contending-with-human-bullying-drivers/','https://www.aitrends.com/ai-and-business-strategy/ai-applied-to-aquaculture-aims-for-improved-efficiency-healthier-fish/','https://www.aitrends.com/healthcare/startup-cognoa-seeks-fda-approval-for-device-with-ai-to-help-diagnose-autism/','https://www.aitrends.com/robotics/recycling-robots-with-ai-helping-to-improve-financial-viability-of-recycling/','https://www.aitrends.com/ai-in-business/ai-hybrid-cloud-and-quantum-computing-seen-by-ibms-krishna-as-shaping-it/','https://www.aitrends.com/ai-insider/consequences-of-bike-riding-kids-amidst-ai-autonomous-cars/','https://www.aitrends.com/ethics-and-social-issues/compute-power-concentration-creating-a-digital-divide-in-ai-research-study-finds/','https://www.aitrends.com/ai-in-business/amazon-beefs-up-ai-in-alexa-and-gets-charged-by-eu-with-unfair-practices/','https://www.aitrends.com/healthcare/internet-of-medical-things-is-beginning-to-transform-healthcare/','https://www.aitrends.com/ai-in-science/scientists-employing-chemputers-in-efforts-to-digitize-chemistry/','https://www.aitrends.com/ai-trends-insider-on-executive-leadership/ai-holistic-adoption-for-manufacturing-and-operations-data/','https://www.aitrends.com/ai-world-government/hhs-automating-hiring-with-help-of-ai-faa-planning-for-role-of-ai-in-modernizing/','https://research.aimultiple.com/supply-chain-automation/','https://research.aimultiple.com/ap-ai/','https://research.aimultiple.com/ecm-case-studies/','https://research.aimultiple.com/rpa-insurance/','https://research.aimultiple.com/ecm-applications/','https://www.sciencedaily.com/releases/2020/12/201215112009.htm','https://www.sciencedaily.com/releases/2020/12/201215142218.htm','https://www.sciencedaily.com/releases/2020/12/201215131236.htm','https://www.sciencedaily.com/releases/2020/12/201211115457.htm','https://www.sciencedaily.com/releases/2020/12/201211100627.htm','https://www.sciencedaily.com/releases/2020/12/201211083041.htm','https://www.sciencedaily.com/releases/2020/12/201211100646.htm','https://www.sciencedaily.com/releases/2020/11/201118080758.htm','https://www.sciencedaily.com/releases/2020/11/201117144539.htm','https://www.sciencedaily.com/releases/2020/11/201103104723.htm','https://www.sciencedaily.com/releases/2020/10/201012152055.htm','https://www.sciencedaily.com/releases/2020/10/201006165746.htm','https://www.sciencedaily.com/releases/2020/09/200930144426.htm','https://www.sciencedaily.com/releases/2020/09/200916113601.htm','https://www.sciencedaily.com/releases/2020/08/200812144008.htm','https://www.sciencedaily.com/releases/2020/08/200811120120.htm','https://www.sciencedaily.com/releases/2020/07/200727194721.htm','https://www.sciencedaily.com/releases/2020/06/200624120434.htm','https://www.sciencedaily.com/releases/2020/06/200617091024.htm','https://www.sciencedaily.com/releases/2020/06/200611183906.htm','https://www.sciencedaily.com/releases/2020/06/200610102726.htm','https://www.sciencedaily.com/releases/2020/06/200601113315.htm','https://www.sciencedaily.com/releases/2020/04/200430091255.htm','https://www.sciencedaily.com/releases/2020/04/200429134018.htm','https://www.sciencedaily.com/releases/2020/04/200423130508.htm']

articles_list=[]
linkstolist(articles,articles_list)
df_articles = pd.DataFrame(articles_list)
 
#store the data in a csv file:
df_articles.to_csv("df_articles.csv")
