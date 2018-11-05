
import numpy as np

def create_sql_for_update_checked_out_and_time_spent(df_entry, sql_script) :
    id_str = str(np.asscalar(df_entry['id']))
    sql_script.append("update parking_lot_usages" + " set checked_out=" + "\'" + df_entry['checked_out'] + "\'" + " ,total_time_spent=" + str(int(df_entry['total_time_spent'])) + " where id=" + id_str + ";")

def create_sql_for_delete_usage(id, sql_script) : 
    id_str = str(np.asscalar(id))
    sql_script.append("delete from parking_lot_usages" + " where id=" + id_str + ";")

