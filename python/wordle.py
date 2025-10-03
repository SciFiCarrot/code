import pandas as pd

valid_words = (
    pd.read_csv(
        "wordle-words-main/valid-words.csv", header=None, names=["word"], dtype="string"
    )
    .set_index("word")  # ★ rows now labelled by each word
    .assign(value=0)  # add the column
)

win_words = pd.read_csv(
    "wordle-words-main/word-bank.csv", header=None, names=["word"], dtype="string"
)


def evaluate(check_word, goal_word):
    if len(check_word) < 5:
        return

    greens = 0
    for i in range(5):
        if check_word[i] == goal_word[i]:
            greens += 1

    yellows = 0
    for i in range(5):
        if check_word[i] in goal_word and check_word[i] != goal_word[i]:
            yellows += 1

    grays = 5 - (greens + yellows)

    green_value = 0
    yellow_value = (5 - yellows - greens) / (5 + yellows + greens) * yellows
    gray_value = (26 - grays - yellows - greens) * grays
    word_value = green_value + yellow_value + gray_value

    return word_value


for check_word in valid_words.index:
    for goal_word in win_words["word"]:
        current_value = evaluate(check_word, goal_word)
        valid_words.at[check_word, "value"] += current_value

    # print(check_word, goal_word, current_value)

valid_words = valid_words.sort_values("value", ascending=True)
print(valid_words)
