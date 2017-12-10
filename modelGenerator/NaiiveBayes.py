
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
import pickle
fake_data = pd.read_csv('https://s3.amazonaws.com/assets.datacamp.com/production/course_3629/fake_or_real_news.csv',
                        low_memory=True
                        )
fake_data.head()
response = fake_data.label
count_vectorizer = CountVectorizer(stop_words="english",
                                   ngram_range=(1,4))
X_train, X_test, Y_train, Y_test = train_test_split(fake_data["text"],
                                                    response,
                                                    test_size=0.33,
                                                    random_state=53)
count_train = count_vectorizer.fit_transform(X_train)
count_test = count_vectorizer.transform(X_test)
nb_classifier = MultinomialNB()
nb_classifier.fit(count_train, Y_train)
pred = nb_classifier.predict(count_test)
score = metrics.accuracy_score(Y_test, pred)
cm = metrics.confusion_matrix(Y_test,
                              pred,
                              labels=["FAKE",  "REAL"]
                             )

pickle.dump(nb_classifier, open('naiiveBayes.pkl', 'wb'))
pickle.load(open('naiiveBayes.pkl', 'rb'))

