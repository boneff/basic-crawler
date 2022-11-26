# Sentiment analysis with Python

Python has a great community when it comes to NLP - more precisely the [Natural Language Toolkit](https://www.nltk.org/).
There are also multiple 3rd party providers concentrated on providing either a platform or a toolkit related to NLP.
Below we are going to demo both approaches.

We are going to be running those examples in Docker, running Python in interactive mode. You're free to run them however suits you.
Running an interactive shell is as simple as (using a slimmed down version, which is good enough for simple playground):
```docker
docker run --rm -it -w /app python:3.10-slim bash
```


## Using VADER from NLTK

For simple cases, in Python, we can use VADER (Valence Aware Dictionary for Sentiment Reasoning) that is available in the NLTK package and can be applied directly to unlabeled text data. As an example, let’s get all sentiment scores of the lines spoken by characters in a TV show.

First, we wrangle a dataset available on [Kaggle](https://www.kaggle.com/datasets/ekrembayar/avatar-the-last-air-bender), then with VADER we calculate the score of each line spoken. All of this is stored in the df_character_sentiment dataframe.

Get the test data first.
Install required Unix packages:
```bash
apt-get update && apt-get install vim curl -y
```
Download the file via cURL. Nevermind the `iconv`, using it to skip some bad data in the CSV.
```bash
curl -L https://raw.githubusercontent.com/ifrankandrade/data-science-projects/main/datasets/avatar.csv | iconv -c -f UTF-8 -t UTF-8 > /app/avatar.csv
```


Install required packages along with NLTK data(https://www.nltk.org/data.html):
```bash
pip install pandas nltk && python -m nltk.downloader -d /usr/local/share/nltk_data all
```

Running the below code can be done either via an interactive session or adding the example below to a file named `sentiment.py`.
Adding the code can be done via Vim:
```bash
vim sentiment.py
```
Type `i` to go into interactive mode, paste the code snippet, hit `Esc`, type `:wq`, then hit `Enter`. File saved and exited.
Running sentiment analysis would be `python sentiment.py` or following the steps below to run and interactive session.


Start an interactive session:
```bash
python
```

Run the actual sentiment analysis:
```python
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# reading and wragling data
df_avatar = pd.read_csv('/app/avatar.csv', encoding = 'unicode_escape', engine='python')
df_avatar_lines = df_avatar.groupby('character').count()
df_avatar_lines = df_avatar_lines.sort_values(by=['character_words'], ascending=False)[:10]
top_character_names = df_avatar_lines.index.values
# filtering out non-top characters
df_character_sentiment = df_avatar[df_avatar['character'].isin(top_character_names)]
df_character_sentiment = df_character_sentiment[['character', 'character_words']]

# calculating sentiment score
sid = SentimentIntensityAnalyzer()
df_character_sentiment.reset_index(inplace=True, drop=True)
df_character_sentiment[['neg', 'neu', 'pos', 'compound']] = df_character_sentiment['character_words'].apply(sid.polarity_scores).apply(pd.Series)
print(df_character_sentiment)
```

Source: https://towardsdatascience.com/7-nlp-techniques-you-can-easily-implement-with-python-dc0ade1a53c2

## Using 3rd party pre-trained sentiment snalysis models

In the [HuggingFaceHub](https://huggingface.co/models), you can find more than 27,000 models shared by the AI community with state-of-the-art performances on tasks such as sentiment analysis, object detection, text generation, speech recognition and more. The Hub is free to use and most models have a widget that allows to test them directly on your browser!

There are more than 215 sentiment analysis models publicly available on the Hub and integrating them with Python just takes 5 lines of code.
Using the `transformers` package requires either Tensorflow or Pytorch. We'll make sure we have Pytorch.

```bash
pip install -q transformers torch
```

```python
from transformers import pipeline
sentiment_pipeline = pipeline("sentiment-analysis")
data = ["I love you", "I hate you", "bruh, I don't care", "baby, one more time"]
print(sentiment_pipeline(data))
```

Source: https://huggingface.co/blog/sentiment-analysis-python

## Bonus section - debugging file encoding issues

Sometimes, when working with files, you may get errors such as:

```python
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa0 in position <random-int-here>: invalid start byte
```

This usually means you should double check what is the encoding of the files you're trying to open (whether CSVs or other).

If you're running Linux, your best bet is:
```bash
file -i <file-name-here>
```

You may end up with something like:

```bash
root@f394d0e49eff:/app# file -i avatar.csv 
avatar.csv: application/csv; charset=unknown-8bit
```

The `unknown-8bit` means the detection failed.
You could then try `enca`.

```bash
enca <file-name-here>
```

If that also fails - while risking data corruption, you could just use `iconv` and convert to whatever encoding you see fit. 

# Read more
 - more examples: https://www.nltk.org/howto/sentiment.html 