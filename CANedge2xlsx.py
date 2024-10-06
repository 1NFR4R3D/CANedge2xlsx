#!/usr/bin/python

import can_decoder
import mdf_iter
from datetime import datetime
import argparse
# 
import pandas as pd
# pd.options.mode.chained_assignment = None  # default='warn'

# Parse command line args
parser = argparse.ArgumentParser(description="Convert MF4 files from datalogger to Excel spreadsheets")
############## TODO - Update Default ##############
parser.add_argument("mdf_filename",
                    help="MF4 file to be converted to XLSX. Default: data.mf4",
                    nargs="?",
                    type=str,
                    default="example_data/test.MF4")
parser.add_argument("xlsx_filename",
                    help="XLSX file to be generated. Will be appended by date and time of conversion. Default: test",
                    nargs="?",
                    type=str,
                    default="example_data/test.xlsx")
parser.add_argument("dbc_filename",
                    help="CAN database file. Default: test.dbc",
                    nargs="?",
                    type=str,
                    default="example_data/test.dbc")
args = parser.parse_args()

# Parse dbc file to decode data
print("Using DBC file -", args.dbc_filename)
db = can_decoder.load_dbc(args.dbc_filename)
df_decoder = can_decoder.DataFrameDecoder(db)

print("Decoding MDF file -", args.mdf_filename)
# Convert data to dataframe
with open(args.mdf_filename, "rb") as mdf_file_handle:
    mdf_file = mdf_iter.MdfFile(mdf_file_handle)
    can_data_raw = mdf_file.get_data_frame()
# Decode data to get physical values. Get rid of raw values and numerical ID.
dropCols = ["Raw Value",
            "CAN ID"]
can_data_physical = df_decoder.decode_frame(can_data_raw,
                                            columns_to_drop=dropCols)

# Convert timestamps to datetime and calculate time from the beginning, 
# getting rid of timezone data because Excel can't handle it
can_data_physical.reset_index(inplace=True)
can_data_physical["TimeStamp"] = can_data_physical["TimeStamp"].dt.tz_localize(None)
can_data_physical["Timedelta"] = (((can_data_physical["TimeStamp"]
                                  - can_data_physical["TimeStamp"].iloc[0]).astype("str"))#'timedelta64[us]'))
                                  ) # Multiply or divide to correct for floating point error 
# Final formatting
can_export_df = can_data_physical.pivot(index="Timedelta", 
                                        columns="Signal", 
                                        values="Physical Value")

now = datetime.now()
dt_string = now.strftime(".D%d%m%Y.T%H%M")
outFileName = args.xlsx_filename + dt_string + ".xlsx"
print("Exporting XLSX file -", outFileName)
writer = pd.ExcelWriter(outFileName, datetime_format="hh:mm:ss")
can_export_df.to_excel(outFileName)
