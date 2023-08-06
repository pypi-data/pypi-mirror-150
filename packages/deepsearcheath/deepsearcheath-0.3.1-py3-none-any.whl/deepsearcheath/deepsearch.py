import requests
from datetime import datetime
import time
import os
import asyncio
import aiohttp

import pandas as pd

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

from dateutil.relativedelta import relativedelta

load_dotenv(verbose=True)


class asyncDeepSearchAPI(object):
    _COMPUTE_API = "{}/v1/compute".format('https://api.deepsearch.com')
    _AUTH_ID = os.getenv('_AUTH_ID')
    _AUTH_PW = os.getenv('_AUTH_PW')
    _AUTH = HTTPBasicAuth(_AUTH_ID, _AUTH_PW)
    
    @classmethod
    async def compute(cls, query, locale='ko_KR'):
        params = {
            'input': query,
            'locale': locale
        } 

        async with aiohttp.ClientSession() as sess:
            async with sess.post( url=cls._COMPUTE_API, auth=aiohttp.BasicAuth(cls._AUTH_ID, cls._AUTH_PW), data=params, timeout=120 ) as co_resp:
                response_json = await co_resp.json()
                if (co_resp.status != 200) or (not response_json['success']):
                    print("Response code, Success status:", co_resp.status, response_json['success'])
                    print("Exception query log:", query)
                    print(response_json)
                    return None

                pods = response_json['data']['pods']  # pods[0]: input

                if pods[1]['class'] == 'Result:DataFrame':
                    data    =    pods[1]['content']['data']
                    index   =   pods[1]['content']['index']
                    dtypes  =  pods[1]['content']['dtypes']
                    columns = pods[1]['content']['columns']

                    results = []

                    no_obs = len(data[columns[0]])
                    for i in range(no_obs):
                        item = dict()
                        for col in columns:
                            item[col] = data[col][i]
                        results.append(item)

                    df_results = pd.DataFrame(results)

                    if df_results.empty:
                        return None

                    for col in dtypes.keys():  # pyarrow converting
                        df_results[col] = df_results[col].astype(dtypes[col])

                    df_results = df_results.set_index(index)  # 'symbol'
                    df_results = df_results.sort_index()

                    return df_results

                elif pods[1]['class'] == 'Result:DocumentTrendsResult':
                    data    =    pods[1]['content']['data']
                    trends  =   pods[1]['content']['data']['trends']
                    total_matches = trends[0]['total_matches']
                    buckets = trends[0]['buckets']

                    df_results = pd.DataFrame(buckets)
                    
                    return df_results

                else:
                    return pods[1]['content']


class DeepSearchAPI(object):
    _COMPUTE_API = "{}/v1/compute".format('https://api.deepsearch.com')
    _AUTH_ID = os.getenv('_AUTH_ID')
    _AUTH_PW = os.getenv('_AUTH_PW')
    _AUTH = HTTPBasicAuth(_AUTH_ID, _AUTH_PW)

    @classmethod
    def compute(cls, query, locale='ko_KR'):
        params = {
            'input': query,
            'locale': locale
        } 

        response = requests.post( url=cls._COMPUTE_API, auth=cls._AUTH, data=params, timeout=120 )

        if (response.status_code != 200) or (not response.json()['success']):
            print("Response code:", response.status_code)
            print("AUTH info:", cls._AUTH_ID, cls._AUTH_PW)
            print("Exception query log:", query)
            return None

        pods = response.json()['data']['pods']  # pods[0]: input

        if pods[1]['class'] == 'Result:DataFrame':
            data    =    pods[1]['content']['data']
            index   =   pods[1]['content']['index']
            dtypes  =  pods[1]['content']['dtypes']
            columns = pods[1]['content']['columns']

            results = []

            no_obs = len(data[columns[0]])
            for i in range(no_obs):
                item = dict()
                for col in columns:
                    item[col] = data[col][i]
                results.append(item)

            df_results = pd.DataFrame(results)

            if df_results.empty:
                return None

            for col in dtypes.keys():  # pyarrow converting
                df_results[col] = df_results[col].astype(dtypes[col])

            df_results = df_results.set_index(index)  # 'symbol'
            df_results = df_results.sort_index()

            return df_results

        elif pods[1]['class'] == 'Result:DocumentTrendsResult':
            data    =    pods[1]['content']['data']
            trends  =   pods[1]['content']['data']['trends']
            total_matches = trends[0]['total_matches']
            buckets = trends[0]['buckets']

            df_results = pd.DataFrame(buckets)
            
            return df_results

        else:
            return pods[1]['content']


class WaveletAPI(object):
    _COMPUTE_API_INDEX = 'https://api.ddi.deepsearch.com/wavelet/v1/indices' 
    _COMPUTE_API = 'https://api.ddi.deepsearch.com/wavelet/v1/prices'
    _AUTH_ID = os.getenv('_AUTH_ID')
    _AUTH_PW = os.getenv('_AUTH_PW')
    _AUTH = HTTPBasicAuth(_AUTH_ID, _AUTH_PW)

    @classmethod
    def compute(cls, symbol, date_from, date_to, interval=None):
        assert type(symbol) == list
        num_of_pdf = len(symbol)
        symbol_str = ','.join(symbol)
        return_dict = dict()
        
        if symbol in [['KOSPI'], ['KOSDAQ']]:
            query = f'{cls._COMPUTE_API_INDEX}/{symbol_str}?from={date_from}&to={date_to}'
        else:
            query = f'{cls._COMPUTE_API}/{symbol_str}?from={date_from}&to={date_to}'

        response = requests.get(query, auth=cls._AUTH)
        
        if (response.status_code != 200):
            print("Response code:", response.status_code)
            print("AUTH info:", cls._AUTH_ID, cls._AUTH_PW)
            print("Exception query log:", query)
            return None
            
        # print(query)

        if symbol in [['KOSPI'], ['KOSDAQ']]:
            data = response.json()['data'][0]
            points = data['points']

            df = pd.DataFrame.from_dict(points)
            df = df.set_index(['timestamp'])
            df.index = pd.to_datetime(df.index)

            return_dict[symbol[0]] = df  #! 인덱스 리턴은 하나밖에 못한다가 됨
            return return_dict

        else:
            for i in range(num_of_pdf):
                try:
                    data = response.json()['data'][i]
                    points = data['points']

                    df = pd.DataFrame.from_dict(points)
                    df = df.set_index(['timestamp'])
                    df.index = pd.to_datetime(df.index)

                    if num_of_pdf == 1:
                        return_dict[data['exchange'] + ':' + data['symbol']] = df
                        return return_dict
                
                    return_dict[data['exchange'] + ':' + data['symbol']] = df
                except:
                    print("Response code:", response.status_code)
                    print("Exception query log:", query)
                    break

            return return_dict


class asyncWaveletAPI(object):
    _COMPUTE_API_INDEX = 'https://api.ddi.deepsearch.com/wavelet/v1/indices' 
    _COMPUTE_API = 'https://api.ddi.deepsearch.com/wavelet/v1/prices'
    _AUTH_ID = os.getenv('_AUTH_ID')
    _AUTH_PW = os.getenv('_AUTH_PW')
    _AUTH = HTTPBasicAuth(_AUTH_ID, _AUTH_PW)

    @classmethod
    def compute():
        return


class HaystackAPI(object):
    """
    api.ddi.deepsearch.com/haystack/v1/news/_search?query=삼성전자&count=1
        - https://help.deepsearch.com/ddi/haystack/search

    @domain: 
        - news
            politics, economy, society, culture, world, tech, entertainment, opinion
        - research
            market, strategy, company, industry, economy, bond   
        - company
            ir, disclosure
        - patent
            patent
    """
    _COMPUTE_API = "{}/v1".format('https://api.ddi.deepsearch.com/haystack')
    _AUTH_ID = os.getenv('_AUTH_ID')
    _AUTH_PW = os.getenv('_AUTH_PW')
    _AUTH = HTTPBasicAuth(_AUTH_ID, _AUTH_PW)

    @classmethod
    def compute(cls, category, section, params, module='_search?', locale='ko_KR'):
        assert type(params) is dict
        url = os.path.join(cls._COMPUTE_API, category, section, module, '_search?')

        response = requests.get( url=url, auth=cls._AUTH, params=params, timeout=30 )

        if (response.status_code != 200) or (not response.json()['found']):
            print("Response code, Found status:", response.status_code, response.json()['found'])
            print("Exception query log:", response.url)
            return None

        return response.json()['data']


class asyncHaystackAPI(object):
    """
    api.ddi.deepsearch.com/haystack/v1/news/_search?query=삼성전자&count=1
        - https://help.deepsearch.com/ddi/haystack/search

    @category - section: 
        - news
            politics, economy, society, culture, world, tech, entertainment, opinion
        - research
            market, strategy, company, industry, economy, bond   
        - company
            ir, disclosure
        - patent
            patent
    """
    _COMPUTE_API = "{}/v1".format('https://api.ddi.deepsearch.com/haystack')
    _AUTH_ID = os.getenv('_AUTH_ID')
    _AUTH_PW = os.getenv('_AUTH_PW')
    _AUTH = HTTPBasicAuth(_AUTH_ID, _AUTH_PW)

    @classmethod
    async def compute(cls, category, section, params, locale='ko_KR'):
        assert type(params) is dict
        url = os.path.join(cls._COMPUTE_API, category, section, '_search?')
        async with aiohttp.ClientSession() as sess:
            async with sess.get( url=url, auth=aiohttp.BasicAuth(cls._AUTH_ID, cls._AUTH_PW), params=params, timeout=60 ) as co_resp:
                response_json = await co_resp.json()
                if (co_resp.status != 200):# or (not response_json['found']):
                    print("Response code, Success status:", co_resp.status)#, response_json['found'])
                    print("Exception query log:", co_resp.url)
                    print(response_json)
                    return None
        return response_json['data']



class backtest(object):
    _aum = 100_000_000_000.0
    deepsearch = DeepSearchAPI()
    async_deepsearch = asyncDeepSearchAPI()
    wavelet = WaveletAPI()

    def _split_phases(cls, deepsearch_df):
        return_dict = dict()
        phases = deepsearch_df.index.unique()
        for p in phases:
            pdf = deepsearch_df.loc[p]
            return_dict[p] = pdf
        return return_dict

    def _is_business_day(date):
        return bool(len(pd.bdate_range(date, date)))

    @classmethod
    async def _async_main(cls, symbol_list, date_from, date_to):
        query = ' '.join(symbol_list) + f' {date_from}-{date_to} 주가'  #! 주가수익률은 해당말일을 기준으로 한 점만 보여준다
        task = [cls.async_deepsearch.compute(query)]
        result = await asyncio.gather(*task)
        return result

    @classmethod
    def compute(cls, deepsearch_df, df_to_upload_bool=False):
        df = cls._split_phases(cls, deepsearch_df)
        rebalancing_dates = list(df.keys())
        
        loop = asyncio.get_event_loop()
        _async_batch_size = 10


        total_return = pd.DataFrame()
        for idx, date in enumerate(rebalancing_dates):  # idx starts from 0
            async_result = pd.DataFrame()

            ratio = df[date].reset_index().set_index(['symbol'])['weight'].astype(float)  # 단축코드, 비중(비중의합은1)
            pdf = list(df[date]['symbol'])  # 0 은 iter item (timestamp)

            delisted_firm_dict = dict()
            delisted_firm = df[date][df[date]['symbol'] != df[date]['symbol_listed']]
            for _, row in delisted_firm.iterrows():
                delisted_firm_dict[row['symbol_listed']] = row['symbol']

            date = datetime.strptime(date, "%m/%d/%Y")

            b_days = 0
            while True:
                if not cls._is_business_day(date): date, b_days = date +relativedelta(days=1), b_days +1
                else: break


            if idx+1 != len(rebalancing_dates):  #* if not the last phase
                _date_from = datetime.strftime(date -relativedelta(days=1), "%Y-%m-%d")
                _date_to = datetime.strftime(datetime.strptime(rebalancing_dates[idx+1], "%m/%d/%Y") -relativedelta(days=1), "%Y-%m-%d")

                # if wavelet_bool == True:
                #     #! 왜 다른가?
                #     try: pdf_wavelet = cls.wavelet.compute(cls, pdf, _date_from, _date_to )  #! 우분투에서 되고
                #     except: pdf_wavelet = cls.wavelet.compute(pdf, _date_from, _date_to )  #! 우분투에서 안된다
                # else:
                for i in range(len(pdf)//_async_batch_size +1):
                    chunk_start, chunk_end = i*_async_batch_size, (i+1)*_async_batch_size
                    chunk = pdf[chunk_start:chunk_end]
                    if len(chunk) == 0: break
                    #! 왜 다른가?
                    try: async_data = loop.run_until_complete( cls._async_main( cls, [i for i in chunk], _date_from, _date_to ) )
                    except: async_data = loop.run_until_complete( cls._async_main( [i for i in chunk], _date_from, _date_to ) )
                    for data in async_data: 
                        data.columns = ['entity_name', 'close']
                        async_result = pd.concat([async_result, data], axis=0)
            else:  #* if the last phase
                _date_from = datetime.strftime(date -relativedelta(days=1), "%Y-%m-%d")
                _date_to = datetime.strftime(datetime.today().date(), "%Y-%m-%d")

                # if wavelet_bool == True:
                #     #! 왜 다른가?
                #     try: pdf_wavelet = cls.wavelet.compute( cls, pdf, _date_from, _date_to )  # dict 반환
                #     except: pdf_wavelet = cls.wavelet.compute( pdf, _date_from, _date_to )  # dict 반환
                # else:
                for i in range(len(pdf)//_async_batch_size +1):
                    chunk_start, chunk_end = i*_async_batch_size, (i+1)*_async_batch_size
                    chunk = pdf[chunk_start:chunk_end]
                    if len(chunk) == 0: break
                    #! 왜 다른가?
                    try: async_data = loop.run_until_complete( cls._async_main( cls, [i for i in chunk], _date_from, _date_to) )  # datetime.strftime(datetime.today(), "%Y-%m-%d")
                    except: async_data = loop.run_until_complete( cls._async_main( [i for i in chunk], _date_from, _date_to) )  # datetime.strftime(datetime.today(), "%Y-%m-%d")
                    for data in async_data:
                        data.columns = ['entity_name', 'close']
                        async_result = pd.concat([async_result, data], axis=0)

            # print(_date_from, _date_to)

            # if wavelet_bool == True:
            #     pdf_returns_wavelet = pd.DataFrame(index=pdf_wavelet[pdf[0]].index)
            #     for symbol in pdf:
            #         wavelet_pct_change = (pdf_wavelet[symbol]['change_rate'] /100 +1).cumprod().rename(symbol)
            #         pdf_returns_wavelet = pd.concat([pdf_returns_wavelet, wavelet_pct_change], axis=1)
            #     pdf_returns_wavelet.index = pdf_returns_wavelet.index.date 
            # else:
            async_result_reset = async_result.reset_index()
            pdf_returns_ds = async_result_reset.drop_duplicates(subset=['date', 'symbol'], keep='first').pivot(index='date', columns='symbol', values='close')
            pdf_returns_async = (pdf_returns_ds.pct_change().fillna(0) +1).cumprod()  #! NICE가 없다
            # pdf_returns_ds.iloc[0, :] = 0  #* 주가수익률로 계산했을 시기의 코드 
            # pdf_returns_async = (pdf_returns_ds +1).cumprod()  #* 주가수익률로 계산했을 시기의 코드 
            pdf_returns_async.columns = [ delisted_firm_dict[i] if i in delisted_firm_dict.keys() else i for i in pdf_returns_async.columns ]

            bucket = ratio * cls._aum  # 시작분배금  #! NICE가 있다
            # if wavelet_bool == True:
            #     #* 시작일은 base_point를 남기고 그 이후부터는 첫날의 리밸런싱 무수익을 떨군다
            #     if idx > 0: _aum_change_wavelet = pdf_returns_wavelet[datetime.strptime(_date_from, "%Y-%m-%d").date() +relativedelta(days=1):] *bucket
            #     else: _aum_change_wavelet = pdf_returns_wavelet *bucket
            #     cls._aum = _aum_change_wavelet.sum(axis=1)[-1]  # 전기 기말값은 당기 기초값으로
            #     total_return = pd.concat([total_return, _aum_change_wavelet])
            # else: 
            #* 시작일은 base_point를 남기고 그 이후부터는 첫날의 리밸런싱 무수익을 떨군다
            if idx > 0: _aum_change_async = pdf_returns_async[datetime.strptime(_date_from, "%Y-%m-%d").date() +relativedelta(days=1):] *bucket
            else: _aum_change_async = pdf_returns_async *bucket
            cls._aum = _aum_change_async.sum(axis=1)[-1]
            total_return = pd.concat([total_return, _aum_change_async])
            print(cls._aum)

        total_return = total_return.groupby(total_return.index).first()

        cls._aum = 100_000_000_000.0  #! 변수 초기화

        if df_to_upload_bool:
            total_return = total_return.groupby(total_return.index).first()
            base_point = 1000
            daily_aum = total_return.sum(axis=1)
            daily_aum.index = pd.to_datetime(daily_aum.index)
            daily_idx = daily_aum / daily_aum[datetime.strftime(datetime.strptime(rebalancing_dates[0], "%m/%d/%Y"), "%Y-%m-%d")] *base_point
            daily_idx = daily_idx[datetime.strftime(datetime.strptime(rebalancing_dates[0], "%m/%d/%Y"), "%Y-%m-%d"):]
            kospi = cls.deepsearch.compute(f"코스피 지수 {datetime.strftime(datetime.strptime(rebalancing_dates[0], '%m/%d/%Y'), '%Y-%m-%d')}-{datetime.strftime(datetime.today().date(), '%Y-%m-%d')}").reset_index().set_index('date')
            kospi.columns = ['symbol', 'entity_name', 'close']
            kospi.index = pd.to_datetime(kospi.index).date
            kospi_ret = kospi['close'].loc[daily_idx.index].pct_change()  # 당일의 종가수익률이 아니라 판다스에서 추가적으로 계산된 값이므로 첫날의 수익률은 누락 #! 그런데 첫날이 월요일이면 -1day때문에 길이가 안맞는다
            daily_kospi = (kospi_ret+1).cumprod().fillna(1) *base_point
            #업로드용 파일 가공
            _excel_date_format = "%d/%m/%Y"
            df_to_upload = pd.concat([daily_idx, daily_kospi], axis=1)
            df_to_upload.index = pd.to_datetime(df_to_upload.index, format="%Y-%m-%d")
            df_to_upload.columns = ["index", 'KOSPI']
            df_to_upload.index = df_to_upload.index.strftime(_excel_date_format)
            df_to_upload = df_to_upload.T.reset_index()
            return df_to_upload
        return total_return
