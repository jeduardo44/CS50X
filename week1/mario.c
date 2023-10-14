#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Initialize needed variables

    int height;
    int i, p;

    // force user to insert a variable between 1 and 8

    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // printf("Stored: %i\n", height);

    for (i = 1; i <= height; i++) // the number of lines to print
    {
        for (p = height - i; p > 0; p--) // in the first line we should print height-1 spaces and then start to decrease
        {
            printf(" ");
        }

        for (int j = 0; j < i; j++) // in the first line we should print 1 # and then start to increase
        {
            printf("#");
        }

        printf("\n");
    }
}