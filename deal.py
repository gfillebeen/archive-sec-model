from dateutil.relativedelta import relativedelta
from account import Account

class Deal:
	def __init__(self, fist_period_date, total_periods, interest_rates, name=None):
		self.name = name
		self.current_period_date = fist_period_date
		self.total_periods = total_periods
		self.interest_rates = interest_rates
		self.accounts = {"Interest_Collections": Account(), "Principal_Collections": Account()}
		self.assets = {}
		self.tranches = {}
		self.waterfall_steps = {}

	def run(self):
		for current_period in range(1, self.total_periods + 1):
			self.update(current_period)
			for name, waterfall_step in self.waterfall_steps.items():
				if current_period == 1:
					waterfall_step.parse_script(self.accounts, self.tranches)
				waterfall_step.run(current_period)
			self.current_period_date += relativedelta(months=1)
		return self.export_simple_cashflows()

	def update(self, current_period):
		self.update_assets(current_period)
		total_interest, total_principal = 0, 0
		for name, asset in self.assets.items():
			total_interest += asset.get_interest(current_period)
			total_principal += asset.get_principal(current_period)
		self.update_accounts(current_period, total_interest, total_principal)
		self.update_tranches(current_period)

	def update_accounts(self, current_period, interest, principal):
		for name, account in self.accounts.items():
			if name == "Interest":
				self.accounts["Interest"].update(current_period, interest)
			elif name == "Principal":
				self.accounts["Principal"].update(current_period, principal)
			else:
				account.update(current_period, 0)

	def update_assets(self, current_period):
		for name, asset in self.assets.items():
			asset.update(current_period)

	def update_tranches(self, current_period):
		for name, tranche in self.tranches.items():
			tranche.update(current_period)

	def export_simple_cashflows(self):
		cashflows = {}
		for name, asset in self.assets.items():
			cashflows[name] = asset.cashflows
		for name, tranche in self.tranches.items():
			cashflows[name] = tranche.cashflows
		return cashflows
