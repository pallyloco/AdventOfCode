# https://open.kattis.com/problems/nodup
line = input()
words = line.split(" ")
hash_words = set()
for word in words:
    if word in hash_words:
        print("no")
        exit()
    hash_words.add(word)
print("yes")
