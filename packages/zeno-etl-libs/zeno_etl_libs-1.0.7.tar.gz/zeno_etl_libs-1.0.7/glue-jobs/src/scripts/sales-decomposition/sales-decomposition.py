"""
Author:jnanansu.bisoi@zeno.health
Purpose: Comparing sales change between any two time periods
"""
#importing libraries
from datetime import datetime
import numpy as np
import pandas as pd
from decimal import Decimal
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

pd.set_option('display.max_columns', None)
from warnings import filterwarnings
filterwarnings("ignore")
import argparse
import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper import helper

from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
from dateutil.tz import gettz


st_dt1 = (datetime.now()-timedelta(days = 2)).strftime("%Y-%m-%d")
ed_dt1 = (datetime.now()-timedelta(days = 1)).strftime("%Y-%m-%d")

st_dt2 = (datetime.now()-timedelta(days = 4)).strftime("%Y-%m-%d")
ed_dt2 = (datetime.now()-timedelta(days = 3)).strftime("%Y-%m-%d")


parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="jnanansu.bisoi@zeno.health", type=str, required=False)
parser.add_argument('-sd1', '--start_date1', default=None, type= str, required=False)
parser.add_argument('-ed1', '--end_date1', default=None, type= str, required=False)
parser.add_argument('-sd2', '--start_date2', default=None, type= str, required=False)
parser.add_argument('-ed2', '--end_date2', default='', type= str, required=False)
parser.add_argument('-p', '--param',default= "old_new", type= str, required=False)
parser.add_argument('-pl', '--param_limit',default= 10, type= int, required=False )
parser.add_argument('-ml', '--max_level',default= 5, type= int, required=False )
parser.add_argument('-fr', '--full_run',default= 'yes', type= str, required=False )
parser.add_argument('-dt', '--data',default= 'summary', type= str, required=False )
parser.add_argument('-fc', '--filter_cutoff',default= 0.05, type= float, required=False )

args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

# parameters
email_to = args.email_to
start_date1 = args.start_date1
end_date1 = args.end_date1
start_date2 = args.start_date2
end_date2 = args.end_date2
param = args.param
param_limit = args.param_limit
max_level = args.max_level
full_run = args.full_run
data = args.data
filter_cutoff = args.filter_cutoff

if start_date1 == None and end_date1 == None:
    start_date1 = st_dt1
    end_date1 = ed_dt1

if start_date2 == None and end_date2 == '':
    start_date2 = st_dt2
    end_date2 = ed_dt2

logger = get_logger()

logger.info(f"env: {env}")
logger.info(f"print the env again: {env}")


schema = 'prod2-generico'

rs_db = DB()
rs_db.open_connection()

s3 = S3()

read_schema = 'prod2-generico'


# Query to fetch sales data
query1 = f"""
select
s."bill-id" ,
s."patient-id" ,
s."store-id" ,
s."drug-id" ,
s."drug-name" ,
s."type" ,
s.category ,
s.composition ,
s.company ,
(case when s."bill-flag" = 'gross' then s.quantity
     when s."bill-flag" = 'return' then (-1*s.quantity)
     else 0
     end) as quantity,
date(s."created-at" ),
s.rate ,
s.ptr ,
s."substitution-status" ,
s."created-by" ,
s."bill-flag" ,
s."old-new" ,
s."payment-method" ,
s."promo-code" ,
s."pc-type" ,
s."pr-flag" ,
s."hd-flag" ,
s."ecom-flag" ,
s."store-name" ,
s."line-manager" ,
s.city ,
s.abo ,
s."franchisee-id" ,
s."franchisee-name" ,
s."cluster-id" ,
s."cluster-name" ,
s."drug-grade" ,
s."doctor-id" ,
(case when s."bill-flag" = 'gross' then (s.rate * s.quantity)
     when s."bill-flag" = 'return' then (-1*(s.rate * s.quantity))
     else 0
     end) as sales
from
"{read_schema}".sales s 
where date(s."created-at" ) between '{start_date1}' and '{end_date1}';
"""

# sales data for period 1
query = query1
mos1 = rs_db.get_df(query = query)
mos1.columns = [c.replace('-', '_') for c in mos1.columns]

# for period 2
query2 = f"""
select
s."bill-id" ,
s."patient-id" ,
s."store-id" ,
s."drug-id" ,
s."drug-name" ,
s."type" ,
s.category ,
s.composition ,
s.company ,
(case when s."bill-flag" = 'gross' then s.quantity
     when s."bill-flag" = 'return' then (-1*s.quantity)
     else 0
     end) as quantity,
date(s."created-at" ),
s.rate ,
s.ptr ,
s."substitution-status" ,
s."created-by" ,
s."bill-flag" ,
s."old-new" ,
s."payment-method" ,
s."promo-code" ,
s."pc-type" ,
s."pr-flag" ,
s."hd-flag" ,
s."ecom-flag" ,
s."store-name" ,
s."line-manager" ,
s.city ,
s.abo ,
s."franchisee-id" ,
s."franchisee-name" ,
s."cluster-id" ,
s."cluster-name" ,
s."drug-grade" ,
s."doctor-id" ,
(case when s."bill-flag" = 'gross' then (s.rate * s.quantity)
     when s."bill-flag" = 'return' then (-1*(s.rate * s.quantity))
     else 0
     end) as sales
from
"{read_schema}".sales s 
where date(s."created-at" ) between '{start_date2}' and '{end_date2}';
"""

# sales data for period 2
mos2 = rs_db.get_df(query=query2)
mos2.columns = [c.replace('-', '_') for c in mos2.columns]


# defining change fuction
def change(A, B):
    return float((B - A))


# Defining function to calculate percentage change
def per_change(A, B):
    if (A == 0):
        return float((B - A))
    elif (A == B):
        return float((B - A))
    else:
        return float(((B - A) / A) * 100)


# The function takes the bills-1 table and the period as 'period1' or 'period2'
def sale(table):
    return table['sales'].sum()


def break_sale(table, sale_type):
    if sale_type == 'gross':
        mos_gs_local = table[table['bill_flag'] == 'gross']
        return mos_gs_local
    if sale_type == 'return':
        mos_ret_local = table[table['bill_flag'] == 'return']
        mos_ret_local['sales'] = np.where(mos_ret_local['sales'] <= 0, -1 * mos_ret_local['sales'],
                                          mos_ret_local['sales'])
        mos_ret_local['quantity'] = np.where(mos_ret_local['quantity'] <= 0, -1 * mos_ret_local['quantity'],
                                             mos_ret_local['quantity'])
        return mos_ret_local


# Defining functions for all required metrics
def num_cust(table):
    num = table.patient_id.nunique()
    return num

def avg_gs_per_customer(table):
    gs = sale(table)
    num = num_cust(table)
    return (gs / num) if (num) != 0 else 0

def num_bills(table):
    num = table.bill_id.nunique()
    return num

def avg_gs_per_bill(table):
    gs = sale(table)
    num = num_bills(table)
    return (gs / num) if (num) != 0 else 0

def num_drugs(table):
    num = table.drug_id.nunique()
    return num

def avg_gs_per_drug(table):
    gs = sale(table)
    num = num_drugs(table)
    return (gs / num) if (num) != 0 else 0

def num_quantity(table):
    num = table['quantity'].sum()
    return num

def rate(table):
    gs = sale(table)
    num = num_quantity(table)
    return (gs / num) if (num) != 0 else 0

def num_bills_per_customer(table):
    num1 = num_bills(table)
    num2 = num_cust(table)
    return (num1 / num2) if (num2) != 0 else 0

def num_quantity_per_bill(table):
    num1 = num_quantity(table)
    num2 = num_bills(table)
    return (num1 / num2) if (num2) != 0 else 0

# taking num of unique drug-bill combination
def num_bills_drugs(table):
    num = len(table[['bill_id', 'drug_id']].drop_duplicates())
    return num

def num_drugs_per_bill(table):
    num1 = num_bills_drugs(table)
    num2 = num_bills(table)
    return (num1 / num2) if (num2) != 0 else 0

def num_quantity_per_drug(table):
    num1 = num_quantity(table)
    num2 = num_drugs(table)
    return (num1 / num2) if (num2) != 0 else 0

def avg_gs_per_drug_per_bill(table):
    gs = sale(table)
    num = num_bills_drugs(table)
    return (gs / num) if (num) != 0 else 0

def num_quantity_per_drug_per_bill(table):
    num1 = num_quantity(table)
    num2 = num_bills_drugs(table)
    return (num1 / num2) if (num2) != 0 else 0


# Function to store metric values in dictionary
def metric(t1, t2):
    # defining dictionary to return
    d = {}
    # metric_name == 'num_cust':
    nc1 = num_cust(t1)
    nc2 = num_cust(t2)
    ch_nc = change(nc1, nc2)
    d['pc_nc'] = per_change(nc1, nc2)

    # metric_name == 'avg_gs_per_customer':
    agpc1 = avg_gs_per_customer(t1)
    agpc2 = avg_gs_per_customer(t2)
    ch_agpc = change(agpc1, agpc2)
    d['pc_agpc'] = per_change(agpc1, agpc2)

    # metric_name == 'num_bills':
    nb1 = num_bills(t1)
    nb2 = num_bills(t2)
    ch_nb = change(nb1, nb2)
    d['pc_nb'] = per_change(nb1, nb2)

    # metric_name == 'avg_gs_per_bill':
    agpb1 = avg_gs_per_bill(t1)
    agpb2 = avg_gs_per_bill(t2)
    ch_agpb = change(agpb1, agpb2)
    d['pc_agpb'] = per_change(agpb1, agpb2)

    # number of unique drugs
    nd1 = num_drugs(t1)
    nd2 = num_drugs(t2)
    ch_nd = change(nd1, nd2)
    d['pc_nd'] = per_change(nd1, nd2)

    # avg gs per drug
    agpd1 = avg_gs_per_drug(t1)
    agpd2 = avg_gs_per_drug(t2)
    ch_agpd = change(agpd1, agpd2)
    d['pc_agpd'] = per_change(agpd1, agpd2)

    # metric_name == 'num_quantity':
    nq1 = num_quantity(t1)
    nq2 = num_quantity(t2)
    ch_nq = change(nq1, nq2)
    d['pc_nq'] = per_change(nq1, nq2)

    # metric_name == 'avg_gs_per_quantity':
    agpq1 = rate(t1)
    agpq2 = rate(t2)
    ch_agpq = change(agpq1, agpq2)
    d['pc_agpq'] = per_change(agpq1, agpq2)

    # metric_name == 'num_bills_per_customer':
    nbpc1 = num_bills_per_customer(t1)
    nbpc2 = num_bills_per_customer(t2)
    ch_nbpc = change(nbpc1, nbpc2)
    d['pc_nbpc'] = per_change(nbpc1, nbpc2)

    # metric_name == 'num_quantity_per_bill':
    nqpb1 = num_quantity_per_bill(t1)
    nqpb2 = num_quantity_per_bill(t2)
    ch_nqpb = change(nqpb1, nqpb2)
    d['pc_nqpb'] = per_change(nqpb1, nqpb2)

    # num of drugs per bill
    ndpb1 = num_drugs_per_bill(t1)
    ndpb2 = num_drugs_per_bill(t2)
    ch_ndpb = change(ndpb1, ndpb2)
    d['pc_ndpb'] = per_change(ndpb1, ndpb2)

    # num of quantities per drug
    nqpd1 = num_quantity_per_drug(t1)
    nqpd2 = num_quantity_per_drug(t2)
    ch_nqpd = change(nqpd1, nqpd2)
    d['pc_nqpd'] = per_change(nqpd1, nqpd2)

    # avg gs per drug per bill
    agpdpb1 = avg_gs_per_drug_per_bill(t1)
    agpdpb2 = avg_gs_per_drug_per_bill(t2)
    ch_agpdpb = change(agpdpb1, agpdpb2)
    d['pc_agpdpb'] = per_change(agpdpb1, agpdpb2)

    # number of quantities per drug per bill
    nqpdpb1 = num_quantity_per_drug_per_bill(t1)
    nqpdpb2 = num_quantity_per_drug_per_bill(t2)
    ch_nqpdpb = change(nqpdpb1, nqpdpb2)
    d['pc_nqpdpb'] = per_change(nqpdpb1, nqpdpb2)

    # returing the dictionary containing all metric values
    return d

# Function to store the metric in a dataFrame
def store_table(df, gs_factor, ret_factor, gs_mult_factor, ret_mult_factor, param_mult_fact, d_gs, d_ret):
    # gross sale
    # level 1
    df['Gross sale'] = gs_factor * param_mult_fact
    # level 2
    df['No. of customers'] = d_gs['pc_nc'] * gs_mult_factor * param_mult_fact
    df['ACV'] = d_gs['pc_agpc'] * gs_mult_factor * param_mult_fact
    # Level 3
    df['No. of bills per customer'] = d_gs['pc_nbpc'] * gs_mult_factor * param_mult_fact
    df['ABV'] = d_gs['pc_agpb'] * gs_mult_factor * param_mult_fact
    # Level 4
    df['No. of drugs per bill'] = d_gs['pc_ndpb'] * gs_mult_factor * param_mult_fact
    df['Avg. spend per drug per bill'] = d_gs['pc_agpdpb'] * gs_mult_factor * param_mult_fact
    # Level 5
    df['No. of quantities per drug per bill'] = d_gs['pc_nqpdpb'] * gs_mult_factor * param_mult_fact
    df['Avg. rate per quantity'] = d_gs['pc_agpq'] * gs_mult_factor * param_mult_fact

    # return
    # level1
    df['Return'] = ret_factor * param_mult_fact
    # level2
    df['No. of customers for return'] = d_ret['pc_nc'] * ret_mult_factor * param_mult_fact
    df['Avg. return per customer'] = d_ret['pc_agpc'] * ret_mult_factor * param_mult_fact
    # Level 3
    df['No. of bills per customer for return'] = d_ret['pc_nbpc'] * ret_mult_factor * param_mult_fact
    df['Avg. return per bill'] = d_ret['pc_agpb'] * ret_mult_factor * param_mult_fact
    # Level 4
    df['No. of returned drugs per bill'] = d_ret['pc_ndpb'] * ret_mult_factor * param_mult_fact
    df['Avg. return per drug per bill'] = d_ret['pc_agpdpb'] * ret_mult_factor * param_mult_fact
    # Level 5
    df['No. of returned quantities per drug per bill'] = d_ret['pc_nqpdpb'] * ret_mult_factor * param_mult_fact
    df['Avg. rate per returned quantity'] = d_ret['pc_agpq'] * ret_mult_factor * param_mult_fact
    return df

#Function to calculate change factor of any parameter
def factor_param(d1, d2, ch_ns, pc_ns):
    ns1_param = sale(d1)
    ns2_param = sale(d2)
    ch_ns_param = change(ns1_param, ns2_param)
    pc_ns_param = per_change(ns1_param, ns2_param)
    ns_factor_param = (ch_ns_param / ch_ns) * pc_ns
    return float(pc_ns_param), float(ns_factor_param)

# Function to control level of output columns i.e level of decomposition
def level(table, max_level, local_list):
    if max_level == 1:
        df = table.loc[:, local_list[0:3]]
        return df
    if max_level == 2:
        df = table.loc[:, local_list[0:7]]
        return df
    if max_level == 3:
        df = table.loc[:, local_list[0:11]]
        return df
    if max_level == 4:
        df = table.loc[:, local_list[0:15]]
        return df
    if max_level == 5:
        df = table.loc[:, local_list[0:19]]
        return df

#Function which returns the final table containing the metric contributions of total change of net sale
def decomposition(table1, table2, df, param_mult_fact=1):
    # period1 net sale
    ns1_local = sale(table1)
    # period2 net sale
    ns2_local = sale(table2)
    # Total change in net sale from period1 to period2
    ch_ns_local = change(ns1_local, ns2_local)
    # percent change in net sale from p1 to p2
    pc_ns_local = float(per_change(ns1_local, ns2_local))

    # defining gross sale metrics
    mos1_gs_local = break_sale(table1, 'gross')
    mos2_gs_local = break_sale(table2, 'gross')
    gs1_local = sale(mos1_gs_local)
    gs2_local = sale(mos2_gs_local)
    ch_gs_local = change(gs1_local, gs2_local)
    pc_gs_local = float(per_change(gs1_local, gs2_local))

    # defining return metrics
    mos1_ret_local = break_sale(table1, 'return')
    mos2_ret_local = break_sale(table2, 'return')
    ret1_local = sale(mos1_ret_local)
    ret2_local = sale(mos2_ret_local)
    ch_ret_local = change(ret1_local, ret2_local)
    pc_ret_local = float(per_change(ret1_local, ret2_local))

    # change in gs and return in % of change in net sale
    # so gs factor
    gs_factor = float((ch_gs_local / ch_ns_local) * pc_ns_local)
    # return factor
    ret_factor = float((ch_ret_local / ch_ns_local) * pc_ns_local)

    # calling metrics for gross sale
    d_gs = metric(mos1_gs_local, mos2_gs_local)
    # calling metrics for return
    d_ret = metric(mos1_ret_local, mos2_ret_local)

    # Defining the factors to be multiplied with the metric values to find their contribution
    gs_mult_factor = float(np.divide(gs_factor, pc_gs_local))
    ret_mult_factor = float(np.divide(ret_factor,pc_ret_local))

    # final data frame
    df_final = store_table(df, gs_factor, ret_factor, gs_mult_factor, ret_mult_factor, param_mult_fact, d_gs, d_ret)
    return df_final

# Its like the final main function to call the decomposition function with given parameter and limit
def my_func(param, param_limit, max_level):
    # period1 net sale
    ns1 = sale(mos1)
    # period2 net sale
    ns2 = sale(mos2)
    # Total change in net sale from period1 to period2
    ch_ns = change(ns1, ns2)
    # percent change in net sale from p1 to p2
    pc_ns = float(per_change(ns1, ns2))

    # simply passing the base tables if no parameter is set
    if param == 'none':
        # creating dataframe
        index = [param]
        df_op = pd.DataFrame(index=index)
        df_op['Net sale'] = np.round(pc_ns)
        return decomposition(mos1, mos2, df_op, 1)

    # If parameters are set
    if param != 'none':

        # sorting the parameter values in descending order of change of net sale from period1 to period2
        df1_sort = mos1.groupby(param)['sales'].sum().reset_index().sort_values(param, ascending=False)
        df2_sort = mos2.groupby(param)['sales'].sum().reset_index().sort_values(param, ascending=False)
        df_sort = pd.merge(df1_sort, df2_sort, on=param, how='outer')
        df_sort.fillna(0, inplace=True)
        df_sort['s_diff'] = df_sort['sales_y'] - df_sort['sales_x']
        # sorting from +ve to -ve if change is +ve
        if pc_ns > 0:
            df_sort = df_sort.sort_values('s_diff', ascending=False)

        # sorting from -ve to +ve if change is -ve
        if pc_ns < 0:
            df_sort = df_sort.sort_values('s_diff', ascending=True)

        sort_list = list(df_sort[param])

        # choosing the parameter values from set limit
        if len(sort_list) <= param_limit:
            param_list = sort_list
        else:
            param_list = sort_list[0:param_limit]

        # creating dataframe with rows as parameter values
        df_temp = pd.DataFrame()

        # Iterating through each parameter value
        for c in param_list:
            # Filtering base table based on set parameter
            p1 = mos1[mos1[param] == c]
            p2 = mos2[mos2[param] == c]

            # calculating contribution factor by calling the factor_param function
            pc_ns_param, ns_factor_param = factor_param(p1, p2, ch_ns, pc_ns)

            # printing the contribution of parameters in total change of net sale
            df_op = pd.DataFrame(index=[c])
            df_op['Net sale'] = ns_factor_param

            # To calculate the multiplication factor to be multipled with the final metric value to find the contribution
            param_mult_factor = float(ns_factor_param / pc_ns_param)

            # Calling the decomposition funtion for set parameters and level
            df2 = decomposition(p1, p2, df_op, param_mult_factor)
            df_final = pd.concat([df_temp, df2])
            df_temp = df_final

        # adding 1st row for net sale change
        index = ['Total_change']
        col = list(df_final.columns)
        df1 = pd.DataFrame(index=index, columns=col)
        df1['Net sale'] = np.round(pc_ns,2)
        df_final = pd.concat([df1, df_final])
        df_final.fillna('-', inplace=True)

        # adding level column
        index = ['Split level']
        col = list(df_final.columns)
        col_value = ['Lvl_0', 'Lvl_1_1(0)', 'Lvl_2_1(1_1)', 'Lvl_2_2(1_1)',
                     'Lvl_3_1(2_2)', 'Lvl_3_2(2_2)', 'Lvl_4_1(3_2)', 'Lvl_4_2(3_2)',
                     'Lvl_5_1(4_2)', 'Lvl_5_2(4_2)', 'Lvl_1_2(0)', 'Lvl_2_3(1_2)', 'Lvl_2_4(1_2)',
                     'Lvl_3_3(2_4)', 'Lvl_3_4(2_4)', 'Lvl_4_3(3_4)', 'Lvl_4_4(3_4)', 'Lvl_5_3(4_4)', 'Lvl_5_4(4_4)']
        df1 = pd.DataFrame(index=index, columns=col)
        df1.loc['Split level'] = col_value
        df_final = pd.concat([df1, df_final])

        # Arranging column names in a relevant way
        local_list = ['Net sale', 'Gross sale', 'Return',
                      'No. of customers', 'ACV',
                      'No. of customers for return', 'Avg. return per customer',
                      'No. of bills per customer', 'ABV',
                      'No. of bills per customer for return', 'Avg. return per bill',
                      'No. of drugs per bill', 'Avg. spend per drug per bill',
                      'No. of returned drugs per bill', 'Avg. return per drug per bill',
                      'No. of quantities per drug per bill', 'Avg. rate per quantity',
                      'No. of returned quantities per drug per bill', 'Avg. rate per returned quantity']

        # return final df
        return level(df_final, max_level, local_list)

#Function to store output for all param in the list
def all_param(param_list,param_limit, max_level ):
    df_param_dict = {}
    for param in param_list:
        df_local = my_func(param , param_limit, max_level)
        df_local['params'] = param
        df_param_dict[param] = df_local
    return df_param_dict

#Sorting param on the basis of contribution to change
def sort_param(df_param_dict):
    params = []
    cont_value = []
    for key in df_param_dict:
        params.append(key)
        cont_value.append(abs(df_param_dict[key].iloc[2:, 0:]['Net sale'].sum()))
    df_local = pd.DataFrame(data = {'param' :params , 'contribution':cont_value} )
    df_sorted = df_local.sort_values('contribution', ascending = False)
    sorted_param_list = list(df_sorted['param'])
    return sorted_param_list

#Concating all stores dataframe in descending order of contribution
def concat(sorted_param_list, df_param_dict):
    p = 0
    df_final = pd.DataFrame()
    for param in sorted_param_list:
        if p == 0:
            df_temp = df_param_dict[param]
            df_final = pd.concat([df_final, df_temp])
        else:
            df_temp = df_param_dict[param].iloc[2:, 0:]
            df_final = pd.concat([df_final, df_temp])
        p = p + 1

    index = list(df_final.index)
    df_final.set_index(['params', index], inplace=True)
    return df_final

#Function to filter data based on larger contribution
def filtered(df , upper_value = 0.95, lower_value= 0.05):
    df1 = df.iloc[:2, 0:]
    df2 = df.iloc[2:, 0:]
    uv = np.quantile(df2, upper_value)
    lv = np.quantile(df2, lower_value)
    df2 = df2.applymap(lambda x: np.nan if x <= uv and x>= lv else x)
    df2 = df2.applymap(lambda x: np.round(x,2))
    df_new = pd.concat([df1,df2])
    df_new = df_new.dropna(axis = 0, how ='all')
    df_new = df_new.dropna(axis = 1, how ='all')
    return df_new

# Final run function
def run(param='old_new', param_limit=10, max_level=5, full_run='yes', data='summary',filter_cutoff = 0.05):
    if full_run == 'no':
        param = param
        param_limit = param_limit
        max_level = max_level
        df_local = my_func(param, param_limit, max_level)
        if data == 'full':
            df_local.reset_index(inplace=True)
            return df
        elif data == 'summary':
            df_local = filtered(df_local, (1-filter_cutoff), filter_cutoff)
            df_local.reset_index(inplace=True)
            df_local.iloc[0, 0] = np.nan
            df_local.iloc[1, 0] = np.nan
            return df_local

    if full_run == 'yes':
        param_limit = 5
        max_level = 5
        param_list = ['drug_name', 'type', 'category', 'composition', 'company', 'created_by', 'old_new',
                      'payment_method', 'promo_code', 'pr_flag', 'hd_flag', 'ecom_flag', 'store_name', 'line_manager',
                      'city', 'abo', 'franchisee_name', 'cluster_name', 'drug_grade']
        df_param_dict = all_param(param_list, param_limit, max_level)
        sorted_param_list = sort_param(df_param_dict)
        df_required = concat(sorted_param_list, df_param_dict)
        df_pr = df_required.copy()
        if data == 'full':
            df_pr.reset_index(inplace=True)
            df_pr.iloc[0, 0] = np.nan
            df_pr.iloc[1, 0] = np.nan
            return df_pr

        elif data == 'summary':
            df_pr = df_pr.applymap(lambda x: np.nan if x == '-' else x)
            df = filtered(df_pr, (1-filter_cutoff), filter_cutoff)
            df.reset_index(inplace=True)
            df.iloc[0, 0] = np.nan
            df.iloc[1, 0] = np.nan
            return df


# Running final function to get output
df_final = run(param = 'old_new',param_limit = 10, max_level = 5, full_run = 'yes', data = 'summary',filter_cutoff = 0.05)

#saving csv to s3
s3.save_df_to_s3(df=df_final, file_name='Stores-projects/76/sales-decomposition.csv', index=False)

# closing the connection
rs_db.close_connection()