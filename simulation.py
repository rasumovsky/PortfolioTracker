import numpy as np


class simulated_parameter:

    def __init__(self, parameter_name, parameter_mean, parameter_stddev, start_year, end_year):
        self._parameter_name = parameter_name
        self._parameter_mean = parameter_mean
        self._parameter_stddev = parameter_stddev
        self._start_year = start_year
        self._end_year = end_year

    def get_simulated_value(self):
        return np.random.normal(
            loc=self._parameter_mean,
            scale=self._parameter_stddev,
            size=1)[0]

    def get_param_name(self):
        return self._parameter_name


class recurring_payment:
    """
    Represents a recurring payment (income for positive sums and expenses for negative sums).
    Args:
      name: the name of the payment
      annual_sum: the annual total sum of the payment.
      annual_change: the annual change in the annual sum.
      payment_stdev: the standard deviation in the annual sum.
      start_year: the year in which the payment starts.
      end_year: the year in which the payment ends.
    """
    def __init__(self, name, annual_sum, annual_change, payment_stdev, start_year, end_year):
        self._name = name
        self._annual_sum = annual_sum
        self._initial_sum = annual_sum
        self._annual_change = annual_change
        self._payment_stdev = payment_stdev
        self._start_year = start_year
        self._end_year = end_year

    def update_payment(self):
        self._annual_sum = self._annual_sum * self._annual_change
    
    def simulate_payment(self, year):
        if year < self._start_year or year >= self._end_year:
            return 0.0
        sim = simulated_parameter(
            parameter_name=self._name, 
            parameter_mean=self._annual_sum, 
            parameter_stddev=abs(self._annual_sum * self._payment_stdev), 
            start_year=self._start_year, 
            end_year=self._end_year)
        return sim.get_simulated_value()

    def reset(self):
        self._annual_sum = self._initial_sum


def simulate_portfolio(initial_value,
                       annual_rate_of_return,
                       annual_payments,
                       start_year,
                       end_year,
                       num_simulations):
    # Store the values and incomes for each simulation and each year.
    values = []
    net_incomes = []

    # Loop over the number of simulations.
    for _ in range(num_simulations):

        curr_payments = annual_payments
        for p in curr_payments:
            p.reset()

        # Store the values and incomes for all years in this simulation.
        curr_values = [initial_value]
        curr_net_incomes = []

        # Loop over years.
        for year in range(start_year, end_year, 1):
            
            # Calculate current values.
            new_income = 0
            for p in curr_payments:
                new_income += p.simulate_payment(year)
                # Update payment value.
                p.update_payment()
            
            # Update value of assets.
            ror = annual_rate_of_return.get_simulated_value()
            if curr_values[-1] > 0:
                new_value = (curr_values[-1] * ror) + new_income
            else:
                new_value = curr_values[-1] + new_income

            # Update the incomes and values for one year in one simulation.
            if len(curr_net_incomes) == 0:
                curr_net_incomes.append(new_income)
            curr_net_incomes.append(new_income)
            curr_values.append(new_value)

        # Update the set of all incomes and values.
        net_incomes.append(curr_net_incomes)
        values.append(curr_values)
            
    return values, net_incomes