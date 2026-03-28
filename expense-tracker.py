import argparse, os, csv, datetime


def set_args():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    # action -> add, delete, list, summary
    subparsers = parser.add_subparsers(dest="action", required=True)

    # add subparser -> --amount, --description
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument(
        "--amount", help="the amount of the expense added", type=float, required=True
    )
    add_parser.add_argument(
        "--description",
        help="description of the expense added",
        default="undefined",
        type=str,
    )

    # delete -> --id
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument(
        "--id", help="id of the expense to delete", type=int, required=True
    )

    # list
    list_parser = subparsers.add_parser("list")

    # summary -> --month, --year
    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument(
        "--month",
        help="Summary the expense for one month or for all time",
        default="total",
    )

    # update --> --id, --description, --amount
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument(
        "--id", help="id of the expense to update", type=int, required=True
    )
    update_parser.add_argument(
        "--description", help="optional of you want to update the description", type=str
    )
    update_parser.add_argument(
        "--amount", help="optional if you want to update the amount", type=float
    )
    args = parser.parse_args()
    return args


def main(args):
    match args.action:
        case "add":
            add_expense(args.amount, args.description)
        case "delete":
            delete_expense(args.id)
        case "list":
            show_expense()
        case "summary":
            show_summary(args.month)
        case "update":
            update_expense(args.id, args.description, args.amount)


def add_expense(amount, description):
    date = datetime.date.today()
    with open("expense.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        expense_id = str(int(rows[-1]["ID"]) + 1) if rows else "1"
    with open("expense.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([expense_id, date, description, amount])
    print(f"Expense added successfully :{expense_id}")


def delete_expense(target_id):
    with open("expense.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        fieldnames = reader.fieldnames
    new_rows = [row for row in rows if int(row["ID"]) != target_id]
    if len(new_rows) == len(rows):
        return print(f"There is no expense for this ID : {target_id}")
    with open("expense.csv", "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_rows)
    print(f"{target_id} expense has been deleted successfully")


def show_expense():
    with open("expense.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        rows = list(reader)
    if len(rows) == 0:
        return print("No expense available")
    print("-" * 150)
    for filed in headers:
        print(f"{filed:30}", end="|")
    print()
    for row in rows:
        for value in row:
            if value == "Amount":
                row[value] = row[value] + "$"
            print(f"{row[value]:.<30}", end="|")
        print()
    print("-" * 150)


def show_summary(month):
    current_year = datetime.datetime.today().strftime("%Y")
    with open("expense.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        rows = list(reader)
    target_rows = []
    summary = 0
    if month == "total":
        summary = 0
        for row in rows:
            summary += float(row["Amount"])
        show_expense()
        return print(f"the summary is :${summary}")
    try:
        month = int(month)
        if not 0 > month > 13:
            return print(f"invalid month :{month}")
    except ValueError:
        return print("You should enter the number of the month (1, 2, 3, ...)")
    for row in rows:
        expense_month = (row["Date"].split("-"))[1]
        expense_year = (row["Date"].split("-"))[0]
        if int(expense_month) == month and int(expense_year) == int(current_year):
            summary += float(row["Amount"])
            target_rows.append(row)
    if len(target_rows) == 0:
        return print("No expense for this month :", month)
    print("-" * 150)
    for filed in headers:
        print(f"{filed:30}", end="|")
    print()
    for row in target_rows:
        for value in row:
            if value == "Amount":
                row[value] = row[value] + "$"
            print(f"{row[value]:.<30}", end="|")
        print()
    print("-" * 150)
    print(f"the total is $:{summary}")


def update_expense(id, description, amount):
    with open("expense.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        headers = reader.fieldnames
    founded = False
    for row in rows:
        if row["ID"] == str(id):
            founded = True
            if amount:
                row["Amount"] = amount
            if description:
                row["Description"] = description
    if not founded:
        return print("ID is not founded")
    with open("expense.csv", "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{id} expense updated successfully")


if __name__ == "__main__":
    if not os.path.exists("expense.csv"):
        with open("expense.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Description", "Amount"])

    main(set_args())
