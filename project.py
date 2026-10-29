import pandas as pd
import matplotlib.pyplot as plt


def load_and_clean_data(file_path):
    """
    Reads the CSV file, validates rows, cleans invalid data,
    and computes the revenue for each valid row.
    """
    valid_rows = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None

    if not lines:
        return pd.DataFrame(columns=['Order_ID', 'Product', 'Category', 'Quantity', 'Price', 'Revenue'])

    header = [h.strip() for h in lines[0].split(',')]
    if len(header) < 5:
        print("Error: CSV header is invalid.")
        return pd.DataFrame(columns=['Order_ID', 'Product', 'Category', 'Quantity', 'Price', 'Revenue'])

    for idx, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue

        parts = [p.strip() for p in line.strip().split(',')]
        if len(parts) < 5:
            print(f"Row {idx} skipped: incomplete data")
            continue

        order_id, product, category, qty_str, price_str = parts[:5]

        try:
            quantity = int(qty_str)
            if quantity <= 0:
                print(f"Row {idx} skipped: invalid Quantity '{qty_str}'")
                continue
        except ValueError:
            print(f"Row {idx} skipped: invalid Quantity '{qty_str}'")
            continue

        try:
            price = float(price_str)
            if price <= 0:
                print(f"Row {idx} skipped: Price must be positive")
                continue
        except ValueError:
            print(f"Row {idx} skipped: Price must be positive")
            continue

        revenue = quantity * price
        valid_rows.append({
            'Order_ID': order_id,
            'Product': product,
            'Category': category,
            'Quantity': quantity,
            'Price': price,
            'Revenue': revenue
        })

    if not valid_rows:
        return pd.DataFrame(columns=['Order_ID', 'Product', 'Category', 'Quantity', 'Price', 'Revenue'])

    return pd.DataFrame(valid_rows)


def display_summary(df):
    """Option 1: Summary (Total Revenue, Orders, Units Sold, Top Product)"""
    if df.empty:
        print("\n--- Summary ---")
        print("Total Revenue: 0 | Orders: 0")
        print("Units sold: 0 | No products available")
        return

    total_revenue = df['Revenue'].sum()
    total_orders = df['Order_ID'].nunique()
    total_units = df['Quantity'].sum()

    product_revenue = df.groupby('Product')['Revenue'].sum()
    top_product = product_revenue.idxmax()
    top_product_rev = product_revenue.max()

    print("\n--- Summary ---")
    print(f"Total Revenue: {int(total_revenue) if total_revenue.is_integer() else total_revenue} | Orders: {total_orders}")
    print(f"Units sold: {total_units} | Top product: {top_product} ({int(top_product_rev)})")


def display_category_revenue(df):
    """Option 2: Category-wise revenue with percentage and visualization"""
    if df.empty:
        print("\n--- Category-wise Revenue ---")
        print("No data available.")
        return

    cat_revenue = df.groupby('Category')['Revenue'].sum()
    total_revenue = cat_revenue.sum()

    print("\n--- Category-wise Revenue ---")
    for category, rev in cat_revenue.items():
        percentage = (rev / total_revenue) * 100 if total_revenue > 0 else 0
        print(f"{category}: {int(rev) if rev.is_integer() else rev} ({percentage:.2f}%)")

    plt.figure(figsize=(6, 6))
    plt.pie(cat_revenue, labels=cat_revenue.index, autopct='%1.2f%%', startangle=140)
    plt.title('Category-wise Revenue')
    plt.show()


def show_top_products_chart(df):
    """Plot top selling products using a bar chart"""
    if df.empty:
        return

    product_revenue = df.groupby('Product')['Revenue'].sum().nlargest(5)

    plt.figure(figsize=(8, 5))
    product_revenue.plot(kind='bar', color='skyblue')
    plt.title('Top Selling Products by Revenue')
    plt.xlabel('Product')
    plt.ylabel('Revenue')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    file_path = 'orders.csv'
    df = load_and_clean_data(file_path)
    if df is None:
        return

    while True:
        print("\n=== E-Commerce Sales Analyzer Menu ===")
        print("1. Summary")
        print("2. Category-wise revenue")
        print("3. Show Top Products Bar Chart")
        print("4. Exit")

        choice = input("Enter menu option (Summary / Category-wise revenue or 1-4): ").strip().lower()

        if choice in ['1', 'summary', 'menu option 1 (summary)']:
            display_summary(df)
        elif choice in ['2', 'category-wise revenue', 'menu option 2 (category-wise revenue)']:
            display_category_revenue(df)
        elif choice in ['3', 'show top products bar chart']:
            show_top_products_chart(df)
        elif choice in ['4', 'exit']:
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == '__main__':
    main()