#include <iostream>
#include <ctime>
using namespace std;


const int ATM_PIN = 12345;


class display {
public:
    static void welcome();  
    static void showDateTime();
};


class ATM {
private:
    int accountBalance;
    int startingBalance;
public:
   
    ATM() {
        startingBalance = 60000;
        accountBalance = 20000;
    }

   
    void helpScreen() {
        cout << "\n--- Help Screen ---\n";
        cout << "1. Enter correct ATM PIN to access your account.\n";
        cout << "2. You can Deposit, Withdraw, or Check Balance.\n";
        cout << "3. Only one attempt is allowed to enter the PIN.\n";
        cout << "=============================================================\n";
    }

   
    void deposit() {
        int amount;
        cout << "\nEnter amount to deposit: ";
        cin >> amount;
        accountBalance += amount;

        cout << "\n--- Deposit Successful ---\n";
        cout << "Initial Starting Balance: Rs. " << startingBalance << endl;
        cout << "Present Account Balance: Rs. " << accountBalance << endl;
    }

 
    void withdraw() {
        int amount;
        cout << "\nEnter amount to withdraw: ";
        cin >> amount;

        if (amount > accountBalance) {
            cout << "\n--- Withdrawal Failed ---\n";
            cout << "Insufficient Balance! Try a lower amount.\n";
        } else {
            accountBalance -= amount;
            cout << "\n--- Withdrawal Successful ---\n";
            cout << "Remaining Balance: Rs. " << accountBalance << endl;
        }
    }

    
    void checkBalance() {
        cout << "\n--- Account Balance ---\n";
        cout << "Current Balance: Rs. " << accountBalance << endl;
    }
};


void display::showDateTime() {
    time_t now = time(0);
    char* dt = ctime(&now);
    cout << "Current Date and Time: " << dt << endl;
}

void display::welcome() {
    cout << "=============================\n";
    cout << "      Welcome to ATM\n";
    cout << "=============================\n";
    showDateTime();
}


int main() {
    ATM atm;  
    int choice;
    int enteredPin;

    display::welcome();  

    do {
        cout << "\n1. Enter ATM PIN\n2. Help\n3. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "\nEnter ATM PIN: ";
                cin >> enteredPin;
                if (enteredPin == ATM_PIN) {
                    int subChoice;
                    do {
                        cout << "\n--- ATM MENU ---\n";
                        cout << "1. Deposit\n2. Withdraw\n3. Check Balance\n4. Exit\n";
                        cout << "Enter your choice: ";
                        cin >> subChoice;

                        switch (subChoice) {
                            case 1: atm.deposit(); break;
                            case 2: atm.withdraw(); break;
                            case 3: atm.checkBalance(); break;
                            case 4: cout << "\nExiting... Thank you!\n"; break;
                            default: cout << "\nInvalid choice. Try again.\n";
                        }
                    } while (subChoice != 4);
                } else {
                    cout << "\nIncorrect PIN. Exiting...\n";
                }

                choice = 3;
                break;

            case 2:
                atm.helpScreen();
                break;

            case 3:
                cout << "\nThank you for using ATM. Goodbye!\n";
                break;

            default:
                cout << "\nInvalid choice. Please try again.\n";
        }

    } while (choice != 3);

    return 0;
}
