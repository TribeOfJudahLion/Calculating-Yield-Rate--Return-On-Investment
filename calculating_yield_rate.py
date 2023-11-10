import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count
import time

# TVM Calculation Function
def tvm_calculation(row):
    principal = row['principal']
    rate = row['rate']
    period = row['period']

    # Example TVM formula (compound interest)
    amount = principal * (1 + rate) ** period
    yield_rate = (amount - principal) / principal
    return yield_rate

# Function to process a chunk of data
def process_chunk(chunk):
    return chunk.apply(tvm_calculation, axis=1)

# Function to read CSV and process data using multiprocessing
def process_data(file_path):
    start_time = time.time()  # Start time for reading and processing data

    data = pd.read_csv(file_path)
    read_time = time.time() - start_time  # Time taken to read CSV

    # Splitting data into chunks for multiprocessing
    num_processes = cpu_count()
    chunk_size = int(np.ceil(len(data) / num_processes))
    chunks = [data.iloc[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Using a pool of processes to process each chunk
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_chunk, chunks)

    # Concatenating results into a single DataFrame
    final_result = pd.concat(results)
    total_time = time.time() - start_time  # Total time for reading and processing

    return final_result, read_time, total_time

# Function to save results to a text file
def save_results_to_file(result, read_time, total_time, end_time, file_name):
    with open(file_name, 'w') as file:
        # Writing header
        file.write("Time Value of Money Calculation Results\n")
        file.write("=======================================\n\n")

        # Writing results
        file.write("Yield Rates:\n")
        for index, yield_rate in result.items():  # Corrected to use .items() for Series
            file.write(f"Index {index}: Yield Rate = {yield_rate:.6f}\n")

        # Writing time metrics
        file.write("\nTime Metrics:\n")
        file.write(f"CSV Read Time: {read_time:.2f} seconds\n")
        file.write(f"Data Processing Time: {total_time:.2f} seconds\n")
        file.write(f"Total Execution Time: {end_time:.2f} seconds\n")

# Main execution block
if __name__ == '__main__':
    file_path = 'TVM_large_sample_data.csv'  # Replace with your CSV file path
    output_file_name = 'TVM_results.txt'     # Name of the output text file

    start_time = time.time()  # Start time for the entire operation
    result, read_time, process_time = process_data(file_path)
    end_time = time.time() - start_time  # Total time for the entire operation

    # Save results to file
    save_results_to_file(result, read_time, process_time, end_time, output_file_name)

    print(f"Results and Time Metrics saved to {output_file_name}")
