
# coding: utf-8

# ### Import sections

# In[72]:


import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import roc_curve
from sklearn.naive_bayes import MultinomialNB
import pickle 


# In[4]:


fake_data = pd.read_csv('https://s3.amazonaws.com/assets.datacamp.com/production/course_3629/fake_or_real_news.csv',
            low_memory=True
           )


# In[8]:


fake_data.head()


# In[15]:


response = fake_data.label


# In[48]:


count_vectorizer = CountVectorizer(stop_words="english",
                                   ngram_range=(1,4))


# In[49]:


X_train, X_test, Y_train, Y_test = train_test_split(fake_data["text"],
                                                   response,
                                                   test_size=0.33,
                                                   random_state=53)


# In[50]:


count_train = count_vectorizer.fit_transform(X_train)


# In[51]:


count_train


# In[52]:


count_test = count_vectorizer.transform(X_test)


# In[53]:


count_test


# #### Naiive Bayes

# In[54]:


nb_classifier = MultinomialNB()


# In[55]:


nb_classifier.fit(count_train, Y_train)


# In[56]:


pred = nb_classifier.predict(count_test)


# In[57]:


score = metrics.accuracy_score(Y_test, pred)


# In[59]:


score


# In[61]:


cm = metrics.confusion_matrix(Y_test,
                              pred,
                              labels=["FAKE",  "REAL"]
                             )


# In[71]:


cm


# In[73]:


pickle.dump(nb_classifier, open('naiiveBayes.pkl', 'wb'))


# In[76]:


pickle.load(open('naiiveBayes.pkl', 'rb'))

