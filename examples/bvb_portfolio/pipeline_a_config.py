import os


def base_s3_extr():
    return {
        'extractor_name': 'SingleS3Extractor',
        'data_source_label': 'S3-mbro',
        'aws_credentials': {k: os.environ.get(k)
                            for k in [
                                'aws_access_key_id', 
                                'aws_secret_access_key'
                                ]
                            },
        'bucket': 'mbro-dev01-bucket-source',
        'file_key': 'portfolio/portof.csv',
        'delimiter': '\t',
        'skiprows': 1
    }

def base_rename():
    return {
        'transformer_name': 'RenameTransformer',
        'columns': {
            'simbol': 'symbol', 
            'sold': 'shares',
            'nume': 'portfolio_name'
        }
    }

def base_keep():
    return {
        'transformer_name': 'KeepTransformer',
        'columns_to_keep': ['symbol', 'shares', 'portfolio_name']
    }

def base_filter():
    return {
        'transformer_name': 'StringFilterTransformer',
        'column': 'symbol',
        'operation': 'notin',
        'args': ['RON']
    }


def index_html_extr():
    return {
        'extractor_name': 'HtmlExtractor',
        'url': 'https://bvb.ro/FinancialInstruments/Indices/IndicesProfiles.aspx?i=BET-TR',
        'table_id': 3,
        'data_source_label': 'from BVB oficial site'
    }

def index_rename():
    return {
        'transformer_name': 'RenameTransformer',
        'columns': {
            'Simbol': 'symbol', 
            'Pondere (%)': 'bet_weight',
            'Societate': 'bet_name'
        }
    }

def blend1():
    return {
        'blender_name': 'MergeBlender',
        'blend_method': 'OuterJoin',
        'on_column': 'symbol'
    }


def lastprice_tv_extr(symbols):
    return {
        'extractor_name': 'LastPriceTradingviewExtractor',
        'exchange': 'BVB',
        'symbols': symbols,
        'interval': '1D',
        'data_source_label': 'Tradingview BVB'
    }

def lastprice_rename():
    return {
        'transformer_name': 'RenameTransformer',
        'columns': {
            'symbol': 'symbol', 
            'close': 'price'
        }
    }

def lastprice_keep():
    return {
        'transformer_name': 'KeepTransformer',
        'columns_to_keep': ['symbol', 'price']
    }



def blend2():
    return {
        'blender_name': 'MergeBlender',
        'blend_method': 'LeftJoin',
        'on_column': 'symbol'
    }


def portf_fillna():
    return {
        'transformer_name': 'FillnaTransformer',
        'columns': {
            'bet_weight': 0, 
            'shares': 0
        }
    }

def portf_tr():
    return {
        'transformer_name': 'PortfolioTransformer'
    }

def portf_keep():
    return {
        'transformer_name': 'KeepTransformer',
        'columns_to_keep': [     
            'symbol', 
            'name', 
            'price', 
            'shares', 
            'bet_weight', 
            'portfolio_weight',     
        ], 
        'descending_by': 'bet_weight'
    }

def google_sheet_loader():
    return {
        'loader_name': 'GoogleSheetsLoader',
        'workbook_id': '1efTPW4gLjmFpqRpm9LULzjI_PKe8QMbjNtfdheM_YPI',
        'sheet_name': 'loading_zone',
        'replace': True,
    }