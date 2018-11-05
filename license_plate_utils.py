import pandas as pd
from datetime import datetime, timedelta
import sql_script_utils as sqlscript

datetime_format = "%Y-%m-%d %H:%M:%S"
def set_usage_checked_out(df,sql_script) :
   # df_list = list(df.iterrows())
    for index in range(0, df.shape[0]) :
        
        first_checked_in_time = datetime.strptime(df.iloc[index, df.columns.get_loc('checked_in')],datetime_format)
        if pd.isna(df.iloc[index, df.columns.get_loc('checked_out')]) :
            if index + 1 >= df.shape[0] - 1 :
                checked_out_time = first_checked_in_time + timedelta(hours=6)
                df.iloc[index, df.columns.get_loc('checked_out')] = checked_out_time.strftime(datetime_format)
                
            else :
                second_checked_in_time = datetime.strptime(df.iloc[index + 1, df.columns.get_loc('checked_in')],datetime_format)
                if second_checked_in_time.hour - first_checked_in_time.hour < 2 :
                    checked_out_time = first_checked_in_time + timedelta(hours=0, minutes=30)
                    df.iloc[index, df.columns.get_loc('checked_out')] = checked_out_time.strftime(datetime_format)
                else : 
                    checked_out_time = second_checked_in_time - timedelta(hours=1, minutes=30)
                    df.iloc[index, df.columns.get_loc('checked_out')] = checked_out_time.strftime(datetime_format)
        
        set_total_time_spent(df,index, sql_script)
        sqlscript.create_sql_for_update_checked_out_and_time_spent(df.iloc[index],sql_script)

    #return


def set_total_time_spent(df, index ,sql_script) :
    checked_in = datetime.strptime(df.iloc[index, df.columns.get_loc('checked_in')],datetime_format)
    checked_out = datetime.strptime(df.iloc[index, df.columns.get_loc('checked_out')],datetime_format)
    df.iloc[index, df.columns.get_loc('total_time_spent')] = (checked_out - checked_in).total_seconds()
    #print(df_entry['total_time_spent'])

def check_duplicate_usages(df, sql_script) :
    for index in range(0, df.shape[0]) :
        if index + 1 < df.shape[0] :
            checked_in = datetime.strptime(df.iloc[index, df.columns.get_loc('checked_in')],datetime_format)
            checked_out = datetime.strptime(df.iloc[index + 1, df.columns.get_loc('checked_in')],datetime_format)
            if (checked_out - checked_in).total_seconds() < 10 :
                sqlscript.create_sql_for_delete_usage(df.iloc[index, df.columns.get_loc('id')], sql_script)

