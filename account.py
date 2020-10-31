class Account:
	def __init__(self, balance=0, name=None):
		self.name = name
		self.remaining_balance = balance
		self.cashflows = {"Balance":[]}

	def update(self, current_period, balance):
		self.remaining_balance += balance
		self.cashflows["Balance"].append(self.remaining_balance)

	def increase_balance(self, balance):
		self.remaining_balance += balance

	def decrease_balance(self, balance):
		self.remaining_balance -= balance
