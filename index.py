import pandas as pd
import datetime as dt
import numpy as np
import license_plate_utils as lputils

original_usages_df = pd.read_csv('exported_usages.csv', na_values="")
usages_df = original_usages_df.copy(deep=True)
usages_df = usages_df[usages_df['parking_lot_id'] == 1]
usages_df['date_checked_in'] = usages_df['checked_in'].str[:11]

plate_col = ['license_plate_letter', 'license_plate_number', 'license_plate_province', 'date_checked_in']
plate_grouped_usages = usages_df.groupby(plate_col)

sql_script = []
delete_sql_script = []

for group, df in plate_grouped_usages :
    lputils.set_usage_checked_out(df, sql_script)
    lputils.check_duplicate_usages(df, delete_sql_script)
print(sql_script)
print("=================================================================================")
print(delete_sql_script)

with open("sql_script", "w") as file :
    script = "\n".join(sql_script)
    file.write(script)

with open("delete_sql_script", "w") as file :
    script = "\n".join(delete_sql_script)
    file.write(script)

