# encoding: utf-8

def is_key_or_isbn(word):
    key_or_isbn = "key"
    if len(word) == 13 and word.isdigit():
        key_or_isbn = "isbn"
    short_word = word.replace("-", "")
    if "-" in word and len(short_word) == 10 and short_word.isdigit():
        key_or_isbn = "isbn"
    return key_or_isbn
