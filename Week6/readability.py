from cs50 import get_string


def grade_sentence(grade):
    if grade < 1:
        return "Before Grade 1"
    elif grade >= 16:
        return "Grade 16+"
    else:
        return "Grade " + str(round(grade))


def evaluate_grade(n_letters, n_words, n_sentences):
    L = (n_letters / n_words) * 100
    S = (n_sentences / n_words) * 100
    index = 0.0588 * L - (0.296 * S) - 15.8
    return index


sentence = get_string("Text: ")

end_sentence = [".", "!", "?"]

n_words = 0
n_letters = 0
n_sentences = 0

for i in sentence:
    if i == " ":
        n_words = n_words + 1
    elif i in end_sentence:
        n_sentences = n_sentences + 1
    else:
        if i.isalpha():
            n_letters = n_letters + 1
n_words = n_words + 1

print(grade_sentence(evaluate_grade(n_letters, n_words, n_sentences)))
