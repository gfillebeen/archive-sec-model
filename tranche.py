class Tranche:
	def __init__(self, balance, rate_type, interest_rate, pay_frequency, name=None):
		self.name = name
		self.rate_type = rate_type
		self.interest_rate = interest_rate
		self.pay_frequency = pay_frequency
		self.remaining_interest = 0
		self.remaining_balance = balance
		self.cashflows =  {a: [] for a in ["Balance", "Interest", "Interest Paid", "Interest Missed", "Principal Paid"]}
		self.cashflows["Balance"].append(balance)

	def update(self, current_period):
		if current_period > 1:
			self.cashflows["Interest Paid"].append(self.cashflows["Interest"][current_period - 2] - self.remaining_interest)
			self.cashflows["Principal Paid"].append(self.cashflows["Balance"][current_period - 2] - self.remaining_balance)
			self.cashflows["Interest Missed"].append(self.remaining_interest)
			self.cashflows["Balance"].append(self.remaining_balance)
		self.cashflows["Interest"].append(self.cashflows["Balance"][current_period - 1] * (self.interest_rate / self.pay_frequency))
		self.reset(current_period)

	def reset(self, current_period):
		self.remaining_interest = self.cashflows["Interest"][current_period - 1]
		self.remaining_balance = self.cashflows["Balance"][current_period - 1]

	def pay_interest(self, account, amount=None):
		amount = self.remaining_interest if amount is None else amount
		temp = min(account.remaining_balance, amount, self.remaining_interest)
		self.remaining_interest -= temp
		account.decrease_balance(temp)

	def pay_principal(self, account, amount=None):
		amount = self.remaining_balance if amount is None else amount
		temp = min(account.remaining_balance, amount, self.remaining_balance)
		self.remaining_balance -= temp
		account.decrease_balance(temp)
