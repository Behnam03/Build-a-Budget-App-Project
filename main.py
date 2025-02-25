class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
        
    def deposit(self, amount, description=""):
        """Add a deposit to the ledger"""
        self.ledger.append({"amount": amount, "description": description})
    
    def withdraw(self, amount, description=""):
        """Attempt to withdraw from the ledger"""
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False
    
    def get_balance(self):
        """Get current balance"""
        return sum(item["amount"] for item in self.ledger)
    
    def transfer(self, amount, category):
        """Transfer amount to another category"""
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False
    
    def check_funds(self, amount):
        """Check if funds are available"""
        return amount <= self.get_balance()
    
    def get_withdrawals(self):
        """Get total withdrawals (used for spend chart)"""
        return sum(-item["amount"] for item in self.ledger if item["amount"] < 0)
    
    def __str__(self):
        """String representation of the category"""
        title = f"{self.name.center(30, '*')}\n"
        items = ""
        for item in self.ledger:
            description = item["description"][:23].ljust(23)
            amount = format(float(item["amount"]), ".2f").rjust(7)
            items += f"{description}{amount}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total

def create_spend_chart(categories):
    """Create a bar chart of spending percentages"""
    
    total_spent = sum(category.get_withdrawals() for category in categories)
    percentages = []
    for category in categories:
        spent = category.get_withdrawals()
        percentage = (spent / total_spent * 100) if total_spent > 0 else 0
        percentages.append(int(percentage // 10 * 10))  
    
    
    chart = "Percentage spent by category\n"
    
    
    for i in range(100, -10, -10):
        chart += str(i).rjust(3) + "| "
        for percentage in percentages:
            chart += "o  " if percentage >= i else "   "
        chart += "\n"
    
    
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"
    
    
    max_name_length = max(len(category.name) for category in categories)
    for i in range(max_name_length):
        chart += "     "
        for category in categories:
            if i < len(category.name):
                chart += category.name[i] + "  "
            else:
                chart += "   "
        if i != max_name_length - 1:
            chart += "\n"
    
    return chart