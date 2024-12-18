def letter_freq(sentence):
    freq = {}
    for char in sentence:
        if char.isspace():
            continue
        if char not in freq:
            freq[char] = 1
        else:
            freq[char] += 1

    return freq

sent = input("Enter a sentence: ")
print("Frequencies: ")
freq = letter_freq(sent)
for char in freq:
    print(f"{char}: {freq[char]}")
