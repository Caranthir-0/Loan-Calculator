import math
import argparse
import sys

parser = argparse.ArgumentParser(description="Loan calculator")
parser.add_argument("--type", help="Type of payment: annuity or diff")
parser.add_argument("--payment", type=float, help="Monthly payment")
parser.add_argument("--principal", type=float, help="Loan principal")
parser.add_argument("--periods", type=int, help="Number of months")
parser.add_argument("--interest", type=float, help="Annual interest rate (percent)")

args = parser.parse_args()

# --- Walidacja parametrów ---
if args.type not in ["annuity", "diff"] or args.interest is None:
    print("Incorrect parameters")
    sys.exit()

params = [args.type, args.payment, args.principal, args.periods, args.interest]
if len([p for p in params if p is not None]) < 4:
    print("Incorrect parameters")
    sys.exit()

if any((isinstance(p, (int, float)) and p < 0) for p in [args.payment, args.principal, args.periods, args.interest] if p is not None):
    print("Incorrect parameters")
    sys.exit()

i = args.interest / (12 * 100)  # miesięczna stopa procentowa

# --- Obsługa diff ---
if args.type == "diff":
    if args.payment is not None:
        print("Incorrect parameters")
        sys.exit()

    total_payment = 0
    P, n = args.principal, args.periods

    for m in range(1, n + 1):
        Dm = (P / n) + i * (P - (P * (m - 1) / n))
        Dm = math.ceil(Dm)
        total_payment += Dm
        print(f"Month {m}: payment is {Dm}")

    overpayment = int(total_payment - P)
    print(f"\nOverpayment = {overpayment}")

# --- Obsługa annuity ---
elif args.type == "annuity":
    P, A, n = args.principal, args.payment, args.periods

    if P and A and not n:
        # liczba miesięcy
        n = math.log(A / (A - i * P), 1 + i)
        n = math.ceil(n)

        years = n // 12
        months = n % 12
        time_str = []
        if years > 0:
            time_str.append(f"{years} year{'s' if years > 1 else ''}")
        if months > 0:
            time_str.append(f"{months} month{'s' if months > 1 else ''}")

        print(f"It will take {' and '.join(time_str)} to repay this loan!")
        overpayment = int(A * n - P)
        print(f"Overpayment = {overpayment}")

    elif P and n and not A:
        # wysokość raty
        A = P * (i * (1 + i) ** n) / ((1 + i) ** n - 1)
        A = math.ceil(A)
        print(f"Your annuity payment = {A}!")
        overpayment = int(A * n - P)
        print(f"Overpayment = {overpayment}")

    elif A and n and not P:
        # kwota kredytu
        P = A / ((i * (1 + i) ** n) / ((1 + i) ** n - 1))
        P = math.floor(P)
        print(f"Your loan principal = {P}!")
        overpayment = int(A * n - P)
        print(f"Overpayment = {overpayment}")

    else:
        print("Incorrect parameters")