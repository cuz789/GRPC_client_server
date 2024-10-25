# measure_delays.py

import time
import matplotlib.pyplot as plt
from client import create_stub, query_category_year_range, query_keyword, query_name

# Measure delays for 100 runs of each query
def run_queries_100_times():
    stub = create_stub()  # Only getting the stub as the create_stub no longer returns the channel

    # Lists to store delays for each query
    query1_delays = []
    query2_delays = []
    query3_delays = []

    # Run Query 1 (Laureates by category and year range) 100 times
    for _ in range(100):
        start_time = time.time()
        response = query_category_year_range(stub)
        end_time = time.time()
        query1_delays.append(end_time - start_time)

    if response:
        print(f"Query 1 completed 100 times with total laureates: {response.total}")

    # Run Query 2 (Laureates by keyword) 100 times
    for _ in range(100):
        start_time = time.time()
        response = query_keyword(stub)
        end_time = time.time()
        query2_delays.append(end_time - start_time)

    if response:
        print(f"Query 2 completed 100 times with total laureates: {response.total}")

    # Run Query 3 (Laureate by name) 100 times
    for _ in range(100):
        start_time = time.time()
        response = query_name(stub)
        end_time = time.time()
        query3_delays.append(end_time - start_time)

    print(f"Query 3 completed 100 times.")

    print(query1_delays, query2_delays, query3_delays)

    # Plot the box plots for each query's delays
    plot_delays(query1_delays, query2_delays, query3_delays)


# Plot the end-to-end delays
def plot_delays(query1_delays, query2_delays, query3_delays):
    plt.figure(figsize=(10, 6))
    plt.boxplot([query1_delays, query2_delays, query3_delays], labels=["Query 1", "Query 2", "Query 3"])
    plt.title("End-to-End Delay for Each Query (100 Runs)")
    plt.ylabel("Time (seconds)")
    plt.show()


if __name__ == "__main__":
    run_queries_100_times()
