
class BankAccount:
    bank_name = "TBC Bank"
    __total_accounts = 0

    def __init__(self, owner, balance):
        self._owner = owner

        if BankAccount.validate_amount(balance):
            self.__balance = balance
        else:
            self.__balance = 0

        BankAccount.__total_accounts += 1
        self.__account_number = f"AN{BankAccount.__total_accounts:04d}"

    def deposit(self, amount):
        if BankAccount.validate_amount(amount):
            self.__balance += amount
            print(f"{amount} GEL deposited.")
        else:
            print("Invalid amount!")

    def withdraw(self, amount):
        if not BankAccount.validate_amount(amount):
            print("Invalid amount!")
            return

        if amount > self.__balance:
            print("Insufficient balance!")
        else:
            self.__balance -= amount
            print(f"{amount} GEL withdrawn.")

    def check_balance(self):
        return self.__balance

    def get_account_number(self):
        return self.__account_number

    def change_owner(self, new_owner):
        self._owner = new_owner

    @classmethod
    def get_total_accounts(cls):
        return cls.__total_accounts

    @staticmethod
    def validate_amount(amount):
        return amount > 0

    def __str__(self):
        return f"Account: {self.__account_number} | Owner: {self._owner}"



acc1 = BankAccount("Nino Beridze", 1000)
acc2 = BankAccount("Giorgi Meskhi", 500)

print(acc1)
print(acc2)

acc1.deposit(300)
acc1.withdraw(200)

print("Balance:", acc1.check_balance())
print("Account Number:", acc1.get_account_number())

acc2.change_owner("Luka Beridze")
print(acc2)

print("Total Accounts:", BankAccount.get_total_accounts())

