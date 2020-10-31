class Asset:
	def __init__(self, balance, rate_type, interest_rate, pay_frequency, maturity_date, assumptions, name=None):
		self.name = name
		self.rate_type = rate_type
		self.interest_rate = interest_rate
		self.pay_frequency = pay_frequency
		self.maturity_date = maturity_date
		self.assumptions = assumptions
		self.cashflows = {a: [] for a in ["Balance", "Interest", "Principal", "Prepayments", "Defaults", "Recoveries"]}
		self.cashflows["Balance"].append(balance)

	def update(self, current_period):
		self.cashflows["Defaults"].append(self.cashflows["Balance"][current_period - 1] * (self.assumptions["Default Rates"][current_period - 1] / self.pay_frequency))
		self.cashflows["Recoveries"].append(self.cashflows["Defaults"][current_period - 1] * (self.assumptions["Recovery Rates"][current_period - 1] / self.pay_frequency))
		self.cashflows["Balance"].append(self.cashflows["Balance"][current_period - 1] - self.cashflows["Defaults"][current_period - 1])
		self.cashflows["Prepayments"].append(self.cashflows["Balance"][current_period] * (self.assumptions["Prepayment Rates"][current_period - 1] / self.pay_frequency))
		self.cashflows["Balance"][current_period] -= self.cashflows["Prepayments"][current_period - 1]
		self.cashflows["Interest"].append(self.cashflows["Balance"][current_period - 1] * (self.interest_rate / self.pay_frequency))
		self.cashflows["Principal"].append(self.cashflows["Recoveries"][current_period - 1] + self.cashflows["Prepayments"][current_period - 1])

	def get_interest(self, current_period):
		return self.cashflows["Interest"][current_period - 1]

	def get_principal(self, current_period):
		return self.cashflows["Principal"][current_period - 1]
