"""Main module."""
import requests
import pandas as pd
from datetime import datetime
import logging

# create logger
logger = logging.getLogger(__name__)

class Status(object):
    '''
    Simple wrapper object for the EPSS status
    '''
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(self.__dict__)

class EPSS():

    def __init__(self, api_url='https://api.first.org/data/v1/'):
        self.api_url = api_url
        self.raw_url = "https://epss.cyentia.com/"
        self.logger = logging.getLogger('epss.EPSS')

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    def get_all(self, date: str = None) -> pd.DataFrame:
        if date is None:
            day_url = self.raw_url + 'epss_scores-current.csv.gz'
            date = datetime.today().strftime('%Y-%m-%d')
        elif type(date) is str:
            self.validate_date(date)
            day_url = self.raw_url + 'epss_scores-{date}.csv.gz'
        else:
            raise Exception(f'Date {date} is invalid')

        epss_df = pd.read_csv(day_url, compression='gzip', sep=',')
        if len(epss_df) > 0:
            header = epss_df.iloc[0]
            if len(header) == 2:
                version = header.index[0].split(':')[1]
                score_date = ''.join(header.index[1].split(':')[1:])
                epss_df.columns = epss_df.iloc[0]
                num_df = epss_df.iloc[1:].copy()
                del epss_df
                num_df['epss'] = num_df['epss'].astype('float')
                num_df['percentile'] = num_df['percentile'].astype('float')
                num_df['date'] = date
                status = Status(version=version, score_date=score_date)
                return num_df, status
            else:
                raise Exception(f'EPSS header {header} is malformed')

    def get(self, cve=None, envelope: bool = True, pretty: bool = False, offset: int = None, limit: int = None,
            order: bool = True, sort_fields: list = None,
            date: str = None, scope: str = 'public', epss_gt: float = None, epss_lt: float = None, fields: list = None,
            percentile_gt: float = None, percentile_lt: float = None, q: str = None) -> pd.DataFrame:

        '''
        Refer to parameters here: https://api.first.org/#Global-parameters
        '''
        url = self.api_url + 'epss'

        params = {}
        if type(cve) is list:
            params['cve'] = ','.join(cve)
        if type(cve) is str:
            params['cve'] = cve
        if type(sort_fields) is list:
            params['sort'] = ','.join(sort_fields)
        if type(fields) is list:
            params['fields'] = ','.join(fields)
        if type(date) is str:
            self.validate_date(date)
            params['date'] = date

        params['envelope'] = envelope
        params['pretty'] = pretty
        params['offset'] = offset
        params['limit'] = limit
        params['scope'] = scope
        params['epss-gt'] = epss_gt
        params['epss-lt'] = epss_lt
        params['percentile-gt'] = percentile_gt
        params['percentile-lt'] = percentile_lt
        params['q'] = q

        if order == False: params['order'] = '!epss'

        r = requests.get(url, params)

        if r.status_code == 200:
            data_status = r.json()

            if params['scope'] == 'public':
                df = pd.json_normalize(data_status, 'data')
                df.set_index('cve', inplace=True)
            elif params['scope'] == 'time-series':
                # iterate through each vulnerability
                df = pd.json_normalize(data_status, 'data')
                tmp = []
                for idx, ts in df.iterrows():
                    tmp_df = pd.DataFrame(ts['time-series'])
                    tmp_df['cve'] = ts['cve']
                    tmp_df = tmp_df.append(ts.drop(labels=['time-series']), ignore_index=True)
                    # tmp_df = pd.concat([tmp_df,ts.drop(labels=['time-series'])])
                    tmp.append(tmp_df)
                df = pd.concat(tmp)
                df.set_index('cve', inplace=True)
            else:
                raise Exception(f'Scope {scope} not supported')

            del data_status['data']
            if envelope is True:
                status = Status(**data_status)
            else:
                status = None
            return df, status
        else:
            raise Exception(f'HTTP errror {r.status_code}')
