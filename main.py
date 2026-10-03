class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        total = 0
        for item in self.ledger:
            total += item["amount"]
        return total

    def transfer(self, amount, category_instance):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category_instance.name}")
            category_instance.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        for item in self.ledger:
            desc = item["description"][:23]
            amt = f"{item['amount']:.2f}"[:7]
            items += f"{desc:<23}{amt:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    title = "Percentage spent by category\n"
    
    # Calculate spending per category and total spending (withdrawals only)
    spendings = []
    total_spend = 0
    for cat in categories:
        cat_spend = 0
        for item in cat.ledger:
            if item["amount"] < 0:
                cat_spend += abs(item["amount"])
        spendings.append(cat_spend)
        total_spend += cat_spend

    # Calculate percentages rounded down to nearest 10
    percentages = []
    for spend in spendings:
        if total_spend > 0:
            pct = int((spend / total_spend) * 100 // 10) * 10
        else:
            pct = 0
        percentages.append(pct)

    # Build the chart lines from 100 down to 0
    chart = ""
    for r in range(100, -1, -1):
        if r % 10 == 0:
            chart += f"{r:>3}|"
            for pct in percentages:
                if pct >= r:
                    chart += " o "
                else:
                    chart += "   "
            chart += " \n"

    # Add the horizontal separation line
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # Find the maximum name length to properly structure vertical alignment
    max_len = max(len(cat.name) for cat in categories)
    
    # Write names vertically below the graph line
    for i in range(max_len):
        chart += "    "
        for cat in categories:
            if i < len(cat.name):
                chart += f" {cat.name[i]} "
            else:
                chart += "   "
        chart += " "
        if i < max_len - 1:
            chart += "\n"

    return title + chart
