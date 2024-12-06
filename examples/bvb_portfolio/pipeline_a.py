
import json

from etl import Pipe
from dotenv import load_dotenv
import pipeline_a_config as cfg


load_dotenv()


base_ds = Pipe.inject_extracted_dataset(cfg.base_s3_extr()) \
        .add_transformer(cfg.base_rename()) \
        .add_transformer(cfg.base_keep()) \
        .add_transformer(cfg.base_filter()) \
    .run()

index_ds = Pipe.inject_extracted_dataset(cfg.index_html_extr()) \
        .add_transformer(cfg.index_rename()) \
    .run()

ds = Pipe.inject_blended_dataset([base_ds, index_ds], cfg.blend1()) \
    .run()

symbols = ds.table['symbol'].to_pylist()

lp_ds = Pipe.inject_extracted_dataset(cfg.lastprice_tv_extr(symbols)) \
        .add_transformer(cfg.lastprice_rename()) \
        .add_transformer(cfg.lastprice_keep()) \
    .run()

portof_ds = Pipe.inject_blended_dataset([ds, lp_ds], cfg.blend2()) \
        .add_transformer(cfg.portf_fillna()) \
        .add_transformer(cfg.portf_tr()) \
        .add_transformer(cfg.portf_keep()) \
    .set_loader(cfg.google_sheet_loader()) \
    .run()

