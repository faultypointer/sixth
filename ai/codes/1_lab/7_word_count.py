def word_count(sentence):
    return len(sentence.split())

sentence = input("Enter a sentence: ")
print(f"No of words: {word_count(sentence)}")
