import streamlit as st
import mysql.connector 
import pandas as pd

st.title("Expense Tracker")

def connect_to_database():
    conn = mysql.connector.connect(
        host="localhost",
    user="root",
    password="Tigerx@007",
    database="expense_tracker"
    )
    return conn

def run_query(query):
    conn = connect_to_database()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.sidebar.title("Navigation")
options = [
    "Total Spending by Category",
    "Total Spending by Payment Mode",
    "Total Cashback Received",
    "Top 5 Most Expensive Categories",
    "Transportation Spending by Payment Mode",
    "Transactions with Cashback",
    "Monthly Spending",
    "High Spending Months for Specific Categories",
    "Recurring Expenses",
    "Monthly Cashback",
    "Spending Trends Over Time",
    "Average Travel Costs",
    "Grocery Spending Patterns",
    "High and Low Priority Categories",
    "Category with Highest Percentage of Spending"
]
choice = st.sidebar.selectbox("Choose an analysis", options)

if choice == "Total Spending by Category":
    st.header("Total Spending by Category")
    query = """
    SELECT category, SUM(amount_paid) AS total_spent
    FROM expenses
    GROUP BY category;
    """
    df = run_query(query)
    st.bar_chart(df.set_index('category'))

elif choice == "Total Spending by Payment Mode":
    st.header("Total Spending by Payment Mode")
    query = """
    SELECT payment_mode, SUM(amount_paid) AS total_spent
    FROM expenses
    GROUP BY payment_mode;
    """
    df = run_query(query)
    st.bar_chart(df.set_index('payment_mode'))

elif choice == "Total Cashback Received":
    st.header("Total Cashback Received")
    query = """
    SELECT SUM(cashback) AS total_cashback
    FROM expenses;
    """
    df = run_query(query)
    st.write(f"Total Cashback Received: ${df.iloc[0, 0]:.2f}") 

elif choice == "Top 5 Most Expensive Categories":
    st.header("Top 5 Most Expensive Categories")
    query = """
    SELECT category, SUM(amount_paid) AS total_spent
    FROM expenses
    GROUP BY category
    ORDER BY total_spent DESC
    LIMIT 5;
    """
    df = run_query(query)
    st.write(df)  
    st.bar_chart(df.set_index('category'))

elif choice == "Transportation Spending by Payment Mode":
    st.header("Transportation Spending by Payment Mode")
    query = """
    SELECT payment_mode, SUM(amount_paid) AS total_spent
    FROM expenses
    WHERE category = 'Transportation'
    GROUP BY payment_mode;
    """
    df = run_query(query)
    st.bar_chart(df.set_index('payment_mode'))

elif choice == "Transactions with Cashback":
    st.header("Transactions with Cashback")
    query = """
    SELECT *
    FROM expenses
    WHERE cashback > 0;
    """
    df = run_query(query)
    st.write(df)  

elif choice == "Monthly Spending":
    st.header("Monthly Spending")
    query = """
    SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(amount_paid) AS total_spent
    FROM expenses
    GROUP BY month;
    """
    df = run_query(query)
    st.line_chart(df.set_index('month'))

elif choice == "High Spending Months for Specific Categories":
    st.header("High Spending Months for Specific Categories")
    query = """
    SELECT DATE_FORMAT(date, '%Y-%m') AS month, category, SUM(amount_paid) AS total_spent
    FROM expenses
    WHERE category IN ('Travel', 'Entertainment', 'Gifts')
    GROUP BY month, category
    ORDER BY total_spent DESC;
    """
    df = run_query(query)
    st.write(df)  

elif choice == "Recurring Expenses":
    st.header("Recurring Expenses")
    query = """
    SELECT category, DATE_FORMAT(date, '%Y-%m') AS month, SUM(amount_paid) AS total_spent
    FROM expenses
    WHERE category IN ('Insurance', 'Subscriptions', 'Bills')
    GROUP BY category, month;
    """
    df = run_query(query)
    st.write(df)  

elif choice == "Monthly Cashback":
    st.header("Monthly Cashback")
    query = """
    SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(cashback) AS total_cashback
    FROM expenses
    GROUP BY month;
    """
    df = run_query(query)
    st.line_chart(df.set_index('month'))

elif choice == "Spending Trends Over Time":
    st.header("Spending Trends Over Time")
    query = """
    SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(amount_paid) AS total_spent
    FROM expenses
    GROUP BY month
    ORDER BY month;
    """
    df = run_query(query)
    st.line_chart(df.set_index('month'))

elif choice == "Average Travel Costs":
    st.header("Average Travel Costs")
    query = """
    SELECT category, AVG(amount_paid) AS average_cost
    FROM expenses
    WHERE category IN ('Flights', 'Accommodation', 'Transportation')
    GROUP BY category;
    """
    df = run_query(query)
    st.write(df)  

elif choice == "Grocery Spending Patterns":
    st.header("Grocery Spending Patterns")
    query = """
    SELECT DATE_FORMAT(date, '%Y-%m') AS month, DAYOFWEEK(date) AS day_of_week, SUM(amount_paid) AS total_spent
    FROM expenses
    WHERE category = 'Groceries'
    GROUP BY month, day_of_week;
    """
    df = run_query(query)
    st.write(df)  

elif choice == "High and Low Priority Categories":
    st.header("High and Low Priority Categories")
    query = """
    SELECT category,
           CASE
               WHEN category IN ('Bills', 'Groceries', 'Transportation') THEN 'High Priority'
               ELSE 'Low Priority'
           END AS priority
    FROM expenses
    GROUP BY category;
    """
    df = run_query(query)
    st.write(df)  

elif choice == "Category with Highest Percentage of Spending":
    st.header("Category with Highest Percentage of Spending")
    query = """
    SELECT category,
           SUM(amount_paid) * 100.0 / (SELECT SUM(amount_paid) FROM expenses) AS percentage
    FROM expenses
    GROUP BY category
    ORDER BY percentage DESC
    LIMIT 1;
    """
    df = run_query(query)
    st.write(df)

st.sidebar.markdown("---")
st.sidebar.markdown("Created with using Streamlit")
