#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char rotate(char a, int number);
bool only_digits(string cla);

int main(int argc, string argv[])
{
    // Make sure program was run with just one command-line argument

    if (argc != 2) // ONLY ONE CLA
    {
        printf("Enter one digit CLA\n");
        return 1;
    }

    // Make sure every character in argv[1] is a digit

    if (!only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Convert argv[1] from a `string` to an `int`

    int key = atoi(argv[1]);
    if (key < 0)
    {
        printf("Enter non-negative numerical integer");
        return 1;
    }

    // Prompt user for plaintext

    string plaintext = get_string("Plaintext: ");
    int n = strlen(plaintext);
    char result[n + 1];
    char rotated;
    result[0] = '\0';

    // For each character in the plaintext:

    for (int a = 0; a < n; a++)
    {

        // Rotate the character if it's a letter:

        if (isalpha(plaintext[a]))
        {
            rotated = rotate(plaintext[a], key);
            strncat(result, &rotated, 1);
        }

        else
        {
            strncat(result, &plaintext[a], 1);
        }
    }

    printf("ciphertext: %s\n", result);
    return 0;
}

// Only_digits function

bool only_digits(string cla)
{
    int n = strlen(cla);
    for (int j = 0; j < n; j++)
    {
        if (!isdigit(cla[j]))
        {
            return false;
        }
    }
    return true;
}

// rotate function

char rotate(char a, int number)
{
    // A-Z is 65-90
    // a-z is 97-122
    int c;

    if (isupper(a))
    {
        c = (((int) a - 'A' + number) % 26) + 'A';  // se a = 'A' então (65-65+15)%26 + 65
    }
    else
    {
        c = (((int) a - 'a' + number) % 26) + 'a';
    }
    return (char) c;
}