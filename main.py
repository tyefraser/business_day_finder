# main.py
# 
# from business_days import generate_business_days
# import argparse
# 
# def parse_arguments():
#     # ... (same as before)
# 
#if __name__ == "__main__":
#    args = parse_arguments()
#
#    try:
#        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
#        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
#    except ValueError:
#        print("Invalid date format. Please use YYYY-MM-DD.")
#        exit(1)
#
#    business_days_list = generate_business_days(start_date, end_date)
#
#    print("Business days between {} and {}: {}".format(start_date, end_date, business_days_list))