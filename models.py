from datetime import datetime


class Participant:
    def __init__(self, name):
        self.name = name
        self.total_paid = 0
        self.total_share = 0

    def __repr__(self):
        return f"{self.name}: Paid={self.total_paid}, Share={self.total_share}"


class Expense:
    def __init__(self, amount, payer, beneficiaries, description="", timestamp=None):
        self.amount = amount
        self.payer = payer
        self.beneficiaries = beneficiaries
        self.description = description
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return (
            f"{self.timestamp} | {self.description} | Amount: {self.amount}, "
            f"Payer: {self.payer}, Beneficiaries: {', '.join(self.beneficiaries)}"
        )


class Trip:
    def __init__(self, name):
        self.name = name
        self.participants = {}
        self.expenses = []

    def add_participant(self, name):
        if name not in self.participants:
            self.participants[name] = Participant(name)

    def edit_participant(self, old_name, new_name):
        if old_name in self.participants:
            participant = self.participants.pop(old_name)
            participant.name = new_name
            self.participants[new_name] = participant

            # Update payer/beneficiary names in expenses
            for expense in self.expenses:
                if expense.payer == old_name:
                    expense.payer = new_name
                expense.beneficiaries = [
                    new_name if name == old_name else name for name in expense.beneficiaries
                ]
        else:
            raise ValueError(f"Participant '{old_name}' does not exist.")

    def remove_participant(self, name):
        if name in self.participants:
            del self.participants[name]
            self.expenses = [
                expense for expense in self.expenses if name not in expense.beneficiaries and expense.payer != name
            ]
        else:
            raise ValueError(f"Participant '{name}' does not exist.")

    def add_expense(self, amount, payer, beneficiaries, description=""):
        if payer not in self.participants:
            raise ValueError(f"Payer '{payer}' is not a participant.")
        for person in beneficiaries:
            if person not in self.participants:
                raise ValueError(f"Beneficiary '{person}' is not a participant.")

        # Create the expense
        expense = Expense(amount, payer, beneficiaries, description)
        self.expenses.append(expense)

        # Update total_paid for the payer
        self.participants[payer].total_paid += amount

        # Calculate the share of each beneficiary
        share_per_person = amount / len(beneficiaries)
        for person in beneficiaries:
            self.participants[person].total_share += share_per_person

    def edit_expense(self, index, amount, payer, beneficiaries, description):
        if 0 <= index < len(self.expenses):
            # Revert the previous expense data
            expense = self.expenses[index]
            self.participants[expense.payer].total_paid -= expense.amount
            share_per_person = expense.amount / len(expense.beneficiaries)
            for person in expense.beneficiaries:
                self.participants[person].total_share -= share_per_person

            # Update with new expense data
            expense.amount = amount
            expense.payer = payer
            expense.beneficiaries = beneficiaries
            expense.description = description

            # Apply the new expense
            self.participants[payer].total_paid += amount
            share_per_person = amount / len(beneficiaries)
            for person in beneficiaries:
                self.participants[person].total_share += share_per_person
        else:
            raise IndexError("Invalid expense index.")

    def remove_expense(self, index):
        if 0 <= index < len(self.expenses):
            # Revert the expense from balances
            expense = self.expenses.pop(index)
            self.participants[expense.payer].total_paid -= expense.amount
            share_per_person = expense.amount / len(expense.beneficiaries)
            for person in expense.beneficiaries:
                self.participants[person].total_share -= share_per_person
        else:
            raise IndexError("Invalid expense index.")

    def calculate_balances(self):
        balances = {}
        for name, participant in self.participants.items():
            balances[name] = participant.total_paid - participant.total_share
        return balances

    def optimize_settlements(self):
        balances = self.calculate_balances()
        positive = {k: v for k, v in balances.items() if v > 0}
        negative = {k: -v for k, v in balances.items() if v < 0}

        settlements = []
        while positive and negative:
            creditor = max(positive, key=positive.get)
            debtor = max(negative, key=negative.get)

            amount = min(positive[creditor], negative[debtor])
            settlements.append((debtor, creditor, round(amount, 2)))

            positive[creditor] -= amount
            negative[debtor] -= amount

            if positive[creditor] == 0:
                del positive[creditor]
            if negative[debtor] == 0:
                del negative[debtor]

        return settlements
