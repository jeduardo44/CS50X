#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text, int n);
int count_words(string text, int n);
int count_sentences(string text, int n);
void calculate_grade(int letters, int words, int sentences);

int main(void)
{
    string text = get_string("Text: ");
    int n = strlen(text);
    calculate_grade(count_letters(text, n), count_words(text, n), count_sentences(text, n));
}

int count_letters(string text, int n)
{
    int letters = 0;
    for (int i = 0; i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters = letters + 1;
        }
    }
    return letters;
}

int count_words(string text, int n)
{
    int words = 0;
    for (int i = 0; i < n; i++)
    {
        if (text[i] == ' ')
        {
            words = words + 1;
        }
    }
    words = words + 1;
    return words;
}

int count_sentences(string text, int n)
{
    int sentences = 0;
    for (int i = 0; i < n; i++)
    {
        if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            sentences = sentences + 1;
        }
    }
    return sentences;
}

void calculate_grade(int letters, int words, int sentences)
{
    float L = (letters / (float) words) * 100;
    float S = (sentences / (float) words) * 100;
    float index = (0.0588 * L - (0.296 * S) - 15.8);

    if (index >= 16)
    {
        printf("Grade 16+\n");
    }

    else if (index >= 1 && index < 16)
    {
        double grade = round(index);
        printf("Grade %i\n", (int) grade);
    }

    else
    {
        printf("Before Grade 1\n");
    }
}