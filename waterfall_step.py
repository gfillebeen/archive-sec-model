from account import Account
from tranche import Tranche

class Waterfall_Step:
	def __init__(self, script):
		self.script = script
		# self.cashflows = {}

	def parse_script(self, accounts, tranches):
		temp = str.split(self.script)
		self.payee = tranches[temp[1]]
		self.pay_type = temp[2]
		self.payer = accounts[temp[4]]

	def run(self, current_period):
		if self.pay_type == "Interest":
			self.payee.pay_interest(self.payer)
		elif self.pay_type == "Principal":
			self.payee.pay_principal(self.payer)

