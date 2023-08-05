import nltk

nltk.download()

def main():

    # Tokenization - Breaking text into words or sentences
    text = "Natural language processing is a challenging field, but it can also be very rewarding."
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)

    pos_tags = nltk.pos_tag(words)

    print(
        "Post tagged:",
        pos_tags
    )

    # Named Entity Recognition - Identifying named entities (such as names, places, and organizations) in text
    ner_tags = nltk.ne_chunk(pos_tags)

    print(
        "Named Entity Recognition:",
        ner_tags
    )
    
    
if __name__ == "__main__":
    main()