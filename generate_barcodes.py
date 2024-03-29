#!/usr/bin/env python

import pandas as pd
import fire

def generate_files(input_csv, read1_enzyme, read2_enzyme, reverse_read1=False, 
        reverse_read2=False, id_last=False, id_cols="sample_id"):
    """
    Read 1 corresponds with i5 end of read, and rows on plate
    Read 2 corresponds with i7 end of read, and columns on plate
    
    Read 1 enzyme options: 
      Adapter names corresond to enzyme which cuts adapter dimer
      "nhei" if xbai was used for cutting, 
      "clai" if mspi was used for cutting

    Read 2 enzyme options: 
      "ecori", "bamhi", "hindiii"  

    Generates 1 output file containing all data.
    Generates a barcodes file for each plate.

    Use the reverse_read1 and reverse_read2 options if you loaded the adapters 
        on to a plate backwards

    Change id_last to False if you want the id in the first column of the barcodes file.

    Change id_cols if you want to use a different column as the sample id in the
        barcodes file. The default is "sample_id". Argument accepts multiple
        column name separated by spaces all enclosed in a single set of quotes.
        The columns will be concatenated.
    """ 
    # Check inputs
    if read1_enzyme not in ["nhei", "clai"]:
        quit("Error: {} not a valid option for read1_enzyme. Choose one of: nhei, clai")

    if read2_enzyme not in ["ecori", "bamhi", "hindiii"]:
        quit("Error: {} not a valid option for read1_enzyme. Choose one of: ecori, bamhi, hindiii")

    df = pd.read_csv(input_csv)

    # Get barcodes sequences for different enzymes
    barcodes_df = pd.read_csv("data/barcodes.csv")

    # Separate barcodes into read1 and read2 barcode data frames
    read1_df = barcodes_df[barcodes_df["read"] == "read1"].drop(
            columns=["read"])
    read2_df = barcodes_df[barcodes_df["read"] == "read2"].drop(
            columns=["read"])

    # Select subset of barcodes for input enzymes
    read1_df = read1_df[read1_df["enzyme"] == read1_enzyme]
    read2_df = read2_df[read2_df["enzyme"] == read2_enzyme]

    # Reverse barcode order
    if reverse_read1:
        read1_df["position"] = read1_df["position"].values[::-1]
    if reverse_read2:
        read2_df["position"] = read2_df["position"].values[::-1]
    
    # Change type of position column for read2_barcode_df
    read2_df["position"] = read2_df["position"].apply(pd.to_numeric)

    # Rename "barcode_sequence" columns
    read1_df = read1_df.rename(columns={
        "barcode_sequence": "read1_barcode_sequence",
        "enzyme": "read1_enzyme",
        "barcode_id": "read1_barcode_id",
        "position": "row"})
    read2_df = read2_df.rename(columns={
        "barcode_sequence": "read2_barcode_sequence",
        "enzyme": "read2_enzyme",
        "barcode_id": "read2_barcode_id",
        "position": "column"})

    # Merge selected barcodes with input data frame 
    df = df.merge(read1_df, on="row")
    df = df.merge(read2_df, on="column")

    # Sort data by plate id and plate index 
    df = df.sort_values(by=["plate_id", "plate_index"])

    # Output complete data frame
    df.to_csv("out.csv", index=False)
    
    # Output barcodes files for stacks/ipyrad 
    id_cols = id_cols.split() 
    df["sample_id"] = df[id_cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

    if id_last:
        cols = ["read1_barcode_sequence", "read2_barcode_sequence", "sample_id"]
    else:
        cols = ["sample_id", "read1_barcode_sequence", "read2_barcode_sequence"]

    for group, data in df.groupby("plate_id"):
        group_df = data[cols]
        filename = "tags-indiv-{}.tsv".format(group)
        group_df.to_csv(filename, sep="\t", index=False, header=None)

if __name__ == "__main__":
    fire.Fire(generate_files)


