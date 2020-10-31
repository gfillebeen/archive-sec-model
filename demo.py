import numpy as np
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
from deal import Deal
from tranche import Tranche
from asset import Asset
from waterfall_step import Waterfall_Step

first_period_date = date(2018, 1, 1)
total_periods = 100
periods_per_year = 4
maturity_date = first_period_date + relativedelta(months=((12/periods_per_year*total_periods)-1))
interest_rates = np.random.rand(total_periods) + 1

my_deal = Deal(first_period_date, total_periods, interest_rates)

collateral_assumptions = {"Default Rates": np.full(total_periods, .05).astype(float),
                          "Recovery Rates": np.full(total_periods, .30),
                          "Recovery Lags": np.zeros(total_periods),
                          "Prepayment Rates": np.full(total_periods, .10)}

my_deal.assets["Loan_A"] = Asset(300e6, "Fixed", .05, periods_per_year, maturity_date, collateral_assumptions)

my_deal.tranches["Tranche_A"] = Tranche(250e6, "Fixed", .02, periods_per_year)

my_deal.waterfall_steps["Step_1"] = Waterfall_Step("PAY Tranche_A Interest FROM Interest_Collections")
my_deal.waterfall_steps["Step_2"] = Waterfall_Step("PAY Tranche_A Principal FROM Principal_Collections")

cashflows = my_deal.run()

print(cashflows)

# df = pd.DataFrame.from_dict(cashflows)
# df.to_csv("cashflows.csv")
