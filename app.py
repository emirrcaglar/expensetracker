import sys
import csv
import argparse
from datetime import datetime

DATA_CSV = "data.csv"

CSV_HEADER = 'ID,Date,Description,Amount'

def read_file(data_csv):
    with open(data_csv, mode='r') as f:
        csv_reader = csv.reader(f)
        rows = list(csv_reader)
    return rows

def write_file(data_csv, data):
     with open(data_csv, mode='w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(data)

def list_print(data_csv):
    with open(data_csv, mode='r') as f:
        csv_reader = csv.reader(f)
        rows = list(csv_reader)
        for row in rows:
            print("#", " ".join(row))

def print_list(data_csv):
    rows = read_file(data_csv)
    print('# ID\tDate\t\tDescription\tAmount')
    for row in rows:
        print('#',row[0],'\t',row[1],'\t',row[2],'\t\t',row[3])

def find_max_id(data_csv):
    data = read_file(data_csv)
    maxid = 0
    for d in data:
        if int(d[0]) > maxid:
            maxid = int(d[0])
    return maxid + 1

def add_data_to_file(data_csv, description, amount):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    id = find_max_id(data_csv)
    csv_data = read_file(data_csv)
    new_row = [id, date, description, amount]
    csv_data.append(new_row)
    write_file(data_csv, csv_data)     

def delete_expense(data_csv, id=None, desc=None):
    csv_data = read_file(data_csv)
    new_data = []
    deleted_id = False
    deleted_desc = False
    if id is not None:
        for d in csv_data:
            if id != int(d[0]):
                new_data.append(d)
            else:
                deleted_id = True
    elif desc is not None:
            for d in csv_data:
                if desc != d[2]:
                    new_data.append(d)
                elif deleted_desc == False:
                    x = input(f"all items named ({desc}) will be deleted. (Y/n)") 
                    if x.lower() == 'y':
                        deleted_desc = True
    write_file(data_csv, new_data)
    if deleted_id:
        print(f"deletion successful. id: {id}")
    elif deleted_desc:
        print(f"deletion successful. desc: {desc}")
    else:
        print(f"no item found to delete.")

def summary(data_csv):
    csv_data = read_file(data_csv)
    sum_amount = 0
    for d in csv_data:
        sum_amount += float(d[3])
    print("total expenses: $" + str(sum_amount))

def update_expense(data_csv, id, desc=None, amount=None):
    rows = read_file(data_csv)
    for row in rows:
        if int(row[0]) == id:
            if desc is not None:
                row[2] = desc
            if amount is not None:
                row[3] = amount
    write_file(data_csv, rows)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="a cli app to track your expenses")

    parser.add_argument('command', choices=['add', 'list', 'summary', 'delete', 'update'])
    parser.add_argument('-d', '--description', type=str, help="the expense")
    parser.add_argument('-a', '--amount', type=float, help="the amount of expense")
    parser.add_argument('-i', '--id', type=int, help="the id of expense")

    args = parser.parse_args()

    return args, parser

def main():
    args = parse_arguments()[0]
    parser = parse_arguments()[1]

    if args.command == 'list':   
        print_list(DATA_CSV)
        parser.print_help()
    if args.command == 'add': 
        add_data_to_file(DATA_CSV, args.description, args.amount)
    if args.command == 'delete':
        delete_expense(DATA_CSV, args.id, args.description)
    if args.command == 'summary':
        print()
        summary(DATA_CSV)
        print()
        parser.print_help()
    if args.command == 'update':
        update_expense(DATA_CSV, args.id, args.description, args.amount)


if __name__ == '__main__':
        main()