# TODO:
# update data (csv) daily
# - sparklend
#   - market data
# - sdai
#   - sdai holders
#   - dsr rate

import pandas as pd

# sparklend
df_market_ethereum = get_data('spark_v1ethereummarket')
df_market_gnosis = get_data('spark_v1gnosismarket')
df_market_ethereum['network'] = 'ethereum'
df_market_gnosis['network'] = 'gnosis'
db_markets = pd.concat([df_market_ethereum, df_market_gnosis], ignore_index=True)

emode_categories = get_data('spark_v1ethereumemodecategoryaddedevent')
db_markets_merged = pd.merge(db_markets, emode_categories[['category', 'name', 'ltv', 'liquidation_threshold', 'liquidation_bonus']], 
                             left_on='emode_category', 
                             right_on='category', 
                             how='left',
                             suffixes=(None,'_emode')
                            )
db_markets.to_csv('assets.csv',index=False)

# sdai
sdai_wallets = get_data('spark_v1ethereumsdaimarket')
sdai_wallets.to_csv('sdai_wallets.csv',index=False)

pot_dsr = get_data('spark_v1potdsr')
pot_dsr.to_csv('pot_dsr.csv',index=False)


# get user data, create param file
df_market_state = get_data('spark_v1ethereumcurrentmarketstate')
# TODO: add cleaning, including emode categories
column_names = df_market_state.columns.tolist()
with open('params.py', 'w') as f:
    for column in column_names:
        f.write(f"{column} = '{column}'\n")