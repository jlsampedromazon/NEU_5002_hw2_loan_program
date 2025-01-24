def find_payable_interest_rate(loan_amt: float, down_payment: float, loan_term: int, min_rate: float, max_rate: float) -> tuple[bool, float]:
    '''
    This function accepts a loan amount, annual down-payment amount and a long term amount, as well as a the minimum and maximum possible interest rates charged.
    This function then calculates the amount outstanding at the end of the loan term based on interest rate values within the range specified, starting at the maximum possible rate and for every 25bps down to the minimum possible rate.
    Finally, the function returns a tuple containing a boolean value indicating whether the loan can be paid of by the end of its term, and the highest interest rate computed at which the loan can be paid off within the term.
    '''
    # Initialize variable to keep track of the last interest rate value that resulted in a positive amount outstanding (initially max_rate)
    # When the algorithm finds an interest rate for which the loan is paid off, use variable to provide an approximate range for the rate that pays off the loan exactly by the end of the term
    watermark = max_rate

    # Tracking interest rate value being tested during 'goal-seeking' updated on each iteration. Start at highest possible value to be decremented
    interest_rate = max_rate

    # Set out loan terms and rate range for user clarity
    print(f"""\nTerms:
- Original Loan Amount: ${loan_amt:.2f}
- Annual Down-Payments: ${down_payment:.2f}
- Loan Term: {loan_term} years
- Minimum Rate: {min_rate:.2f}%
- Maximum Rate: {max_rate:.2f}%
    """)

    # Iterate through possible interest rate values seeking the value that makes the outstanding balance on the loan less than or equal to zero at the end of the term
    while interest_rate >= min_rate:
            
            # Calculate outstanding amount for each interest rate value (formula adapted from loan problem in 5001_hw2)
            outstanding_amt = loan_amt * ((1 + 0.01 * interest_rate)**loan_term - (down_payment / loan_amt) * ((1 + 0.01 * interest_rate)**loan_term - 1) / (0.01 * interest_rate))
            
            # Log the calculations performed in each iteration
            print(f"At an interest rate of {interest_rate:.2f}%, the amount outstanding at Year {loan_term} is ${outstanding_amt:.2f}\n")

            # Check whether the loan is more than paid off 
            if outstanding_amt < 0:
                # Where the loan can be paid off even at the highest possible interest rate, return
                if interest_rate == max_rate:
                    print(f"\nThe loan can be paid off in 20 years at the maximum interest rate specified of {max_rate:.2f}. The total amount outstanding at Year {loan_term} would be {outstanding_amt}.\n")
                    return (True, max_rate)
                # Where the loan can be paid off but not at the maximum possible rate, provide aprox. range for rate that pays down the loan exactly to the user fyi
                else:
                    print(f"\nThe loan can be paid off in 20 years at an interest rate of {interest_rate:.2f}% (and at slightly higher interest rates below {watermark:.2f}%).\n")
                    # Return the interest rate that pays the loan off even if not exact
                    return (True, interest_rate)
            # Keep iterating and do not return for interest rates that will leave an amount outstanding at the end of the term
            elif outstanding_amt > 0:
                  # Update watermark to form ranges where an interest rate allows paying down the loan is found
                  watermark = interest_rate
                  # Update interest rate decrementing from max_rate to continue goal-seeking (hardwired, could be optional parameter instead)
                  interest_rate -= 0.25
                  continue
            # Where the interest rate tested allows paying down the loan to exactly zero at the end of the term, return with exact message to user
            elif outstanding_amt == 0:
                  print(f"\nAt an interest rate of {interest_rate:.2f}%, the ${loan_amt:.2f} loan will be paid down in exactly {loan_term} years.\n")
                  return (True, interest_rate)
            # Raise an error if no other if condition is met (conditions designed to be explicitly MECE, so this code *should* never run) 
            else:
                 raise Exception("\nERROR: Something that should have never happened, happened.")
    
    # No prior returns mean interest rate that allows paying off the loan is not within the range of possible values
    # Inform the user and return
    print("\nThere is no interest rate within the specified range at which the loan could be paid off within its term.")
    print(f"Outstanding Amount at Year {loan_term}: {outstanding_amt}\n")
    return (False, None)


# Set-up for clean imports from other programs in future
def main():
    find_payable_interest_rate(100000, 10000, 20, 5, 10)

if __name__ == '__main__':
    main()