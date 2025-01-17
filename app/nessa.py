import PyPDF2
import os
import nltk
import string
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize 
import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from summa import keywords
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score


def CvAnalyser(cv_file_name=os.getcwd() + 'cv_file.pdf',
               job_file=os.getcwd() + 'datascience.csv'):
    with open(cv_file_name, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text() #this (+=) adds text extracted from each page of the doc into one single variable (text)
            # print(text)

        #splitting the text into lines for easier processing
        lines = text.split('\n')
        # print(lines)

        #variables where extracted information would be stored
        experience = ''
        skills = ''
        education = ''

        #specifying Boolean variables to track when to extract content from the text
        extract_experience = False
        extract_skills = False
        extract_education = False

        #looping through `lines` to extract information under each section
        for line in lines:
            #extracting info in the SKILLS section
            if 'SKILLS' in line.upper():
                extract_experience = False
                extract_skills = True
                extract_education = False
                continue  # Skip this line
            
            #extracting info in the EDUCATION section
            elif 'EDUCATION' in line.upper():
                extract_experience = False
                extract_skills = False
                extract_education = True
                continue  # Skip this line

            #extracting info in the EXPERIENCE section
            elif 'EXPERIENCE' in line.upper():
                extract_experience = True
                extract_skills = False
                extract_education = False
                continue  # Skip this line

            # print(extract_skills)
            # print(extract_education)
            # print(extract_experience)
            # Extract information based on the active section flag
            if extract_experience:
                experience += line + '\n'
            elif extract_skills:
                skills += line + '\n'
            elif extract_education:
                education += line + '\n'

        # # the extracted information for each file
        # print(f"Experience:{experience}\nSkills:{skills}\nEducation:{education}\n")

    experience = ' '.join(experience.split('\n'))
    # #(experience)


    #Education section
    education = ' '.join(education.split('\n'))
    #(education)

    #Skills section
    skills = ' '.join(skills.split('\n'))
    #(skills)


    # **Converting to lowercase**


    #experience section
    #splits the text into individual sentences or sections based on punctuations like "." or "●" and keeps it from repeating
    exp_section = [section.strip() for section in experience.split("●") if section.strip()]

    #this then converts each section to lowercase if it's a string, but ignores numbers
    experience = [str(item).lower() if isinstance(item, str) else item for item in exp_section]
    #(experience)

    #education section
    edu_section = [section.strip() for section in education.split("●") if section.strip()]
    education = [str(item).lower() if isinstance(item, str) else item for item in edu_section]
    #(education)

    #skills section
    skl_section = [section.strip() for section in skills.split("●") if section.strip()]
    skills = [str(item).lower() if isinstance(item, str) else item for item in skl_section]
    #(skills)


    # **Word tokenization**

    #downloading the `punkt` package which contains pre-trained models for text tokenization (like tokenize)
    nltk.download('punkt')

    #experience section
    #word tokenizes each string inside the list of strings (experience), with each individual string represented as `exp` instaed of the whole list (experience) at once (word_tokenize doesn't work on lists)
    exp_tokenized = [word_tokenize(exp) for exp in experience]
    #(exp_tokenized)

    #education section
    edu_tokenized = [word_tokenize(edu) for edu in education]
    #(edu_tokenized)

    #skills section
    skl_tokenized = [word_tokenize(skl) for skl in skills]
    #(skl_tokenized)


    # **Sentence tokenization**

    #experience section
    #sentence tokenizes each string inside the list of strings (experience), with each individual string represented as `exp` instaed of the whole list (experience) at once (sentence_tokenize doesn't work on lists)
    exp_sent_tokenized = [sent_tokenize(exp) for exp in experience]
    #(exp_sent_tokenized)

    #education section
    edu_sent_tokenized = [sent_tokenize(edu) for edu in education]
    #(edu_sent_tokenized)


    # In[ ]:


    #skills section
    skl_sent_tokenized = [sent_tokenize(skl) for skl in skills]
    #(skl_sent_tokenized)


    # **Punctuation removal**

    # In[ ]:


    #experience section

    #this code says: escape (skip) at every punctuation encountered
    reg_exprsn = re.compile('[%s]' % re.escape(string.punctuation))

    exp_tokenized_no_punct = []

    #for loop that automates the process
    for review in exp_tokenized:
        new_review_exp = []
        for token in review:
            new_token_exp = reg_exprsn.sub(u'', token)
            if not new_token_exp == u'': new_review_exp.append(new_token_exp)
        exp_tokenized_no_punct.append(new_review_exp)

    #(exp_tokenized_no_punct)


    # In[ ]:


    #education section
    edu_tokenized_no_punct = []

    for review in edu_tokenized:
        new_review_edu = []
        for token in review:
            new_token_edu = reg_exprsn.sub(u'', token)
            if not new_token_edu == u'': new_review_edu.append(new_token_edu)
        edu_tokenized_no_punct.append(new_review_edu)

    #(edu_tokenized_no_punct)


    # In[ ]:


    #skills section
    skl_tokenized_no_punct = []

    for review in skl_tokenized:
        new_review_skl = []
        for token in review:
            new_token_skl = reg_exprsn.sub(u'', token)
            if not new_token_skl == u'': new_review_skl.append(new_token_skl)
        skl_tokenized_no_punct.append(new_review_skl)

    #(skl_tokenized_no_punct)


    # **Stopword removal**

    nltk.download('stopwords')

    #experience section
    exp_tokenized_no_stopw = []

    for doc in exp_tokenized_no_punct:
        new_term_vector_exp = []
        for word in doc:
            if not word in stopwords.words('english'): new_term_vector_exp.append(word)
        exp_tokenized_no_stopw.append(new_term_vector_exp)

    #(exp_tokenized_no_stopw)
    #education section
    edu_tokenized_no_stopw = []

    for doc in edu_tokenized_no_punct:
        new_term_vector_edu = []
        for word in doc:
            if not word in stopwords.words('english'): new_term_vector_edu.append(word)
        edu_tokenized_no_stopw.append(new_term_vector_edu)

    #(edu_tokenized_no_stopw)

    #skills section
    skl_tokenized_no_stopw = []

    for doc in skl_tokenized_no_punct:
        new_term_vector_skl = []
        for word in doc:
            if not word in stopwords.words('english'): new_term_vector_skl.append(word)
        skl_tokenized_no_stopw.append(new_term_vector_skl)

    #(skl_tokenized_no_stopw)


    # **Stemming and Lemmantization**
    # (But only lemmantization was done, 'cause it's better.)


    #Lemmantization
    nltk.download('wordnet')  #Necessary for WordNetLemmatizer
    #experience section
    wordnet = WordNetLemmatizer()

    exp_preprocessed = []

    for doc in exp_tokenized_no_stopw:
        exp_final_doc = []
        for word in doc:
            exp_final_doc.append(wordnet.lemmatize(word))
        exp_preprocessed.append(exp_final_doc)

    print(exp_preprocessed)
    #education section
    edu_preprocessed = []

    for doc in edu_tokenized_no_stopw:
        edu_final_doc = []
        for word in doc:
            edu_final_doc.append(wordnet.lemmatize(word))
        edu_preprocessed.append(edu_final_doc)

    print(edu_preprocessed)

    #skills section
    skl_preprocessed = []

    for doc in skl_tokenized_no_stopw:
        skl_final_doc = []
        for word in doc:
            skl_final_doc.append(wordnet.lemmatize(word))
        skl_preprocessed.append(skl_final_doc)

    print(skl_preprocessed)
    #Saving each of the preprocessed sections into one variable

    CV = exp_preprocessed + edu_preprocessed + skl_preprocessed
    print(CV)


    # # Model Training using job descriptions

    # **Analysing and extracting features from the job description**

    ds = pd.read_csv(job_file)
    ds

    ds.isnull().sum()

    ds_needed = ds[['Job Title', 'Job Description']]
    ds_needed


    # **There are A LOT of rows in this dataset, thus it would take a lot of time for keywords to be extracted from it. So, instead of using all the job descriptions, I'll be training the model on just one.**
    #Let's take the needed job decription to be `b`

    b = ds_needed.head(1)
    b

    #CountVectorizer wouldn't work on a dataframe of two columns, so I concatentated the columns into one

    b_concat = b['Job Title'] + '' + b['Job Description']
    b_concat

    # **I would have used `TfidfVectrizer()` instead of `CountVectrizer()` because it both finds term frequency across documents, and then supresses the most occuring term/s in the docs to remove unnecessary considerations of repeating words and focus more on unique words, but the vocabulary of `CountVectrizer()` just seemed better**.

    #Turning CV (which is a list of lists) into a single list so it can be vectorized

    CV_list = [word for sublist in CV for word in sublist]
    print(CV_list)


    vectorizer = CountVectorizer()

    #model's vocab building and tokenizing

    X = vectorizer.fit_transform(CV_list)
    #vectorizer.transform(df['Keyword'])

    ##(vectorizer.transform(df['Keyword']))


    #Turning ds_concat to a string, since the `keywords` module only accepts strings and not DataFrames

    b_concat_text = ''.join(b_concat)
    b_concat_text


    # **TextRank is an algorithm that assigns importance scores to words in a text based on their relationships. The `summa` library in Python provides an implementation of TextRank for both summarizing text and exracting keywords. The documentation was really helpful: https://pypi.org/project/summa/**

    #Extracting keywords

    kw = keywords.keywords(b_concat_text)
    #(kw)


    #Turning kw into a list of strings, so it can be used in creating the DataFrame

    kw_list = kw.split('\n')
    kw_list


    # **Creating a binary indicator to score the CV against the job description.**
    #Changing CV_list to a string first, to make keywords in it more visible)

    CV_string = ' '.join(CV_list)
    CV_string


    #Creating the DF
    df = pd.DataFrame({'Keywords': kw_list})

    # Creating a binary indicator column, 'Match'
    #The lambda function checks if keywords x (from kw_list) is in CV_list for every keyword. It gives 1 if true and 0 if not, and then applies it column-wise to the created DF as 'Match'
    df['Match'] = df['Keywords'].apply(lambda x: 1 if x in CV_string else 0)
    df

    X.shape, df.shape

    #Making the values of X to be equal to those in in df['Match] using indexing (Sparse Matrix nnz Steps)

    select_num_samplesX = len(df['Match'])
    X_subset = X[:select_num_samplesX, :]


    X_train, X_test, y_train, y_test = train_test_split(X_subset, df['Match'], test_size=0.2, random_state=42)
    lr = LogisticRegression()
    lr.fit(X_train, y_train)


    #Testing

    lr_prediction = lr.predict(X_test)
    lr_prediction

    accuracy = lr.score(X_test, y_test)
    #(f"Model Accuracy: {accuracy}")


    #Importing modules for the evaluation metrics:


    #("Mean Squared Error =" , mean_squared_error(y_test, lr_prediction))
    #("Mean Absolute Error metric for LinearRegression =" , mean_absolute_error(y_test, lr_prediction))
    #("R-squared metric for LinearRegression = ", r2_score(y_test, lr_prediction))


    Total_kw = len(df['Keywords'])
    return [df['Match'].sum(), Total_kw]

    #('Your CV score is ' + str(df['Match'].sum()) + '/' + str(Total_kw) + '.')



# print(CvAnalyser())