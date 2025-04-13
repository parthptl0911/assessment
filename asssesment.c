#include <stdio.h>

int main()
{
    int no, q, sum = 0;
    char ch;

    do
    {
        printf("\n-------------Menu-------------");
        printf("\n1. Pizza       Price = 180rs/pc");
        printf("\n2. Burger      Price = 100rs/pc");
        printf("\n3. Dosa        Price = 120rs/pc");
        printf("\n4. Idli        Price =  50rs/pc");

        printf("\n\nPlease enter your choice (1-4): ");
        scanf("%d", &no);

        switch (no)
        {
        case 1:
            printf("You have selected Pizza.\n");
            printf("Enter the quantity: ");
            scanf("%d", &q);
            sum += 180 * q;
            printf("Total amount is:%d", sum);
            break;

        case 2:
            printf("You have selected Burger.\n");
            printf("Enter the quantity: ");
            scanf("%d", &q);
            sum += 100 * q;
            printf("Total amount is:%d", sum);
            break;

        case 3:
            printf("You have selected Dosa.\n");
            printf("Enter the quantity: ");
            scanf("%d", &q);
            sum += 120 * q;
            printf("Total amount is:%d", sum);
            break;

        case 4:
            printf("You have selected Idli.\n");
            printf("Enter the quantity: ");
            scanf("%d", &q);
            sum += 50 * q;
            printf("Total amount is:%d", sum);
            break;

        default:
            printf("Invalid choice.\n");
        }

        printf("\nDo you want to order more? (y/n): ");
        scanf(" %c", &ch);

    } while (ch == 'y' || ch == 'Y');

    printf("\nTotal Bill Amount = Rs. %d\n", sum);
    printf("Thank you for your order!\n");

    return 0;
}
