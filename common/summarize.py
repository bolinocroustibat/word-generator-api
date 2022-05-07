import heapq
from typing import List

import nltk
from fastapi import HTTPException


async def summarize(lang: str, text: str, sentences_nb: int) -> str:
    """
    Heavily inspired by https://www.analyticsvidhya.com/blog/2020/12/tired-of-reading-long-articles-text-summarization-will-make-your-task-easier/
    """

    # Break down sentences into words so that we have separate entities
    sentence_list = nltk.sent_tokenize(text)

    # Find weighted frequencies of occurrences of each word, except the stop words
    if lang == "en":
        stopwords = nltk.corpus.stopwords.words("english")
    elif lang == "fr":
        stopwords = nltk.corpus.stopwords.words("french")
    else:
        raise HTTPException(status_code=400, detail="Language not supported.")
    word_frequencies: dict = {}
    for word in nltk.word_tokenize(text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    # Calculate the most frequent word
    maximum_frequency = max(word_frequencies.values())

    # Change the frequencies values according to the most frequent word
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / maximum_frequency

    # print(word_frequencies)  # DEBUG

    # Calculate the sentence scores
    # Iterate over all the sentences, tokenize all the words in a sentence. If the word exists in word_frequences and also if the sentence exists in sentence_scores then increase its count by 1 else insert it as a key in the sentence_scores and set its value to 1. We are not considering longer sentences hence we have set the sentence length to 30.
    sentence_scores: dict = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(" ")) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    # Get the 'sentences_nb' sentences with the best scores
    summary_sentences: List[str] = heapq.nlargest(
        sentences_nb, sentence_scores, key=sentence_scores.get
    )

    # Join the list of sentences into a text
    return " ".join(summary_sentences)
