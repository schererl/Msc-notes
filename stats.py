#!/usr/bin/env python3
"""
This script computes the intersection of solved problems for a given set of experiment configurations
and aggregates statistics (averages) only over the common set of solved problems. A problem is considered
solved if the "solution_size" is greater than 0 and "expanded_nodes" is greater than 1. The output includes
aggregated metrics (as averages, formatted with two decimal places) for each domain and experiment, plus a
total row showing the aggregated results across all domains.

Usage:
    python compute_intersection.py --input results.csv --output intersection_results.csv --args lmcount-tdg Novelty-lmcount-tdg-f-t
Alternatively, you can pass the experiments as a single comma-separated list enclosed in brackets:
    python compute_intersection.py --input results.csv --output intersection_results.csv --args "[lmcount-tdg, Novelty-lmcount-tdg-f-t]"
"""

import pandas as pd
import argparse
import numpy as np
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute intersections and aggregate experiment statistics (averages) over solved problems."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the input CSV file")
    parser.add_argument("-o", "--output", required=True, help="Path to the output CSV file")
    parser.add_argument("-a", "--args", nargs="+", required=True, help="List of experiment names to compare")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Process the experiment names: allow a single argument in the form "[exp1, exp2,...]"
    experiments = args.args
    if len(experiments) == 1 and experiments[0].startswith('[') and experiments[0].endswith(']'):
        # Remove the surrounding brackets and split by comma
        experiments = experiments[0][1:-1].split(',')
        experiments = [exp.strip() for exp in experiments if exp.strip()]
    
    # Read the input CSV file into a pandas DataFrame.
    try:
        df = pd.read_csv(args.input)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)
    
    # Ensure that the 'experiment_name' column exists.
    if "experiment_name" not in df.columns:
        print("Error: The input CSV file does not contain the 'experiment_name' column.")
        sys.exit(1)
    
    # Check that each experiment specified exists in the input CSV.
    available_experiments = set(df["experiment_name"].unique())
    missing_experiments = [exp for exp in experiments if exp not in available_experiments]
    if missing_experiments:
        print("Error: The following experiment configuration(s) were not found in the input file:")
        for exp in missing_experiments:
            print(f"  - {exp}")
        print("\nAvailable experiment configurations in the input file:")
        for exp in sorted(available_experiments):
            print(f"  - {exp}")
        sys.exit(1)
    
    # Filter rows to include only the specified experiments.
    df = df[df["experiment_name"].isin(experiments)].copy()
    
    # Get the unique domains in the dataset.
    domains = df["domain_name"].unique()
    
    # List to store aggregated results for each domain and experiment.
    aggregated_rows = []
    
    # Define the list of numeric columns to average.
    avg_columns = [
        "search_elapsed_time", "solution_size", "expanded_nodes"
    ]
    
    # Process each domain separately.
    for domain in domains:
        df_domain = df[df["domain_name"] == domain].copy()
        
        # For each experiment, compute the set of solved problem names in this domain.
        # A problem is considered solved if solution_size > 0 and expanded_nodes > 1.
        problem_sets = []
        for exp in experiments:
            df_exp = df_domain[df_domain["experiment_name"] == exp].copy()
            # Convert relevant columns to numeric.
            df_exp["solution_size"] = pd.to_numeric(df_exp["solution_size"], errors="coerce")
            df_exp["expanded_nodes"] = pd.to_numeric(df_exp["expanded_nodes"], errors="coerce")
            solved_rows = df_exp[(df_exp["solution_size"] > 0) & (df_exp["expanded_nodes"] > 1)]
            problems = set(solved_rows["problem_name"].unique())
            print(f"{exp} {domain}")
            print(sorted(problems))
            problem_sets.append(problems)
        
        # Compute the intersection of solved problem names across all selected experiments.
        if problem_sets:
            common_problems = set.intersection(*problem_sets)
        else:
            common_problems = set()
        
        # Skip domain if there is no common solved problem.
        if not common_problems:
            continue
        
        # For each experiment, filter rows to include only those solved and with problem_name in the intersection.
        for exp in experiments:
            df_exp = df_domain[df_domain["experiment_name"] == exp].copy()
            df_exp["solution_size"] = pd.to_numeric(df_exp["solution_size"], errors="coerce")
            df_exp["expanded_nodes"] = pd.to_numeric(df_exp["expanded_nodes"], errors="coerce")
            solved_df = df_exp[(df_exp["solution_size"] > 0) & (df_exp["expanded_nodes"] > 1)]
            df_exp_final = solved_df[solved_df["problem_name"].isin(common_problems)]
            if df_exp_final.empty:
                continue
            
            aggregated_data = {}
            aggregated_data["domain_name"] = domain
            aggregated_data["experiment_name"] = exp
            # Set problem_count to the number of intersecting solved problems.
            aggregated_data["problem_count"] = len(common_problems)
            
            # Compute average for numeric columns.
            for col in avg_columns:
                if col in df_exp_final.columns:
                    aggregated_data[col] = df_exp_final[col].mean()
                else:
                    aggregated_data[col] = np.nan
            
            # For non-numeric fields like heuristic_name, join unique values.
            if "heuristic_name" in df_exp_final.columns:
                unique_names = df_exp_final["heuristic_name"].dropna().unique()
                aggregated_data["heuristic_name"] = ";".join(unique_names)
            else:
                aggregated_data["heuristic_name"] = ""
            
            aggregated_rows.append(aggregated_data)
    
    # Create an aggregated DataFrame.
    agg_df = pd.DataFrame(aggregated_rows)
    
    if agg_df.empty:
        print("No domains with common solved problems were found for the specified experiments.")
        sys.exit(0)
    
    # Compute overall totals across all domains.
    total_row = {"domain_name": "Total", "experiment_name": ""}
    total_row["problem_count"] = agg_df["problem_count"].sum() if "problem_count" in agg_df.columns else np.nan
    for col in avg_columns:
        total_row[col] = agg_df[col].mean() if col in agg_df.columns else np.nan
    total_row["heuristic_name"] = ""
    
    # Append the total row using pd.concat (since DataFrame.append is deprecated)
    total_df = pd.DataFrame([total_row])
    agg_df = pd.concat([agg_df, total_df], ignore_index=True)
    
    # Write the aggregated results to the output CSV, formatting floats to 2 decimal places.
    try:
        agg_df.to_csv(args.output, index=False, float_format="%.2f")
        print(f"Aggregated results written to {args.output}")
    except Exception as e:
        print(f"Error writing output file: {e}")
    
if __name__ == "__main__":
    main()
