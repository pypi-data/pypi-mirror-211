import datetime
import logging
import re
import sqlite3
from typing import Dict, List, Optional, Type, Union

import pandas as pd
import polars as pl
from pydantic import BaseModel, StrictStr, ValidationError

from . import repository_path as rp
from .pandastic import cast_with_model, validate_dataframe

logger = logging.getLogger(__name__)

TABLE_STATEMENTS = "statements"
DATA_TYPE_TEXT = "TEXT"
DATA_TYPE_REAL = "REAL"
DATA_DIFINITION = [
    ("DisclosedDate", DATA_TYPE_TEXT),
    ("DisclosedTime", DATA_TYPE_TEXT),
    ("LocalCode", DATA_TYPE_TEXT),
    ("DisclosureNumber", DATA_TYPE_TEXT),
    ("TypeOfDocument", DATA_TYPE_TEXT),
    ("TypeOfCurrentPeriod", DATA_TYPE_TEXT),
    ("CurrentPeriodStartDate", DATA_TYPE_TEXT),
    ("CurrentPeriodEndDate", DATA_TYPE_TEXT),
    ("CurrentFiscalYearEndDate", DATA_TYPE_TEXT),
    ("CurrentFiscalYearStartDate", DATA_TYPE_TEXT),
    ("NextFiscalYearStartDate", DATA_TYPE_TEXT),
    ("NextFiscalYearEndDate", DATA_TYPE_TEXT),
    ("NetSales", DATA_TYPE_REAL),
    ("OperatingProfit", DATA_TYPE_REAL),
    ("OrdinaryProfit", DATA_TYPE_REAL),
    ("Profit", DATA_TYPE_REAL),
    ("EarningsPerShare", DATA_TYPE_REAL),
    ("DilutedEarningsPerShare", DATA_TYPE_REAL),
    ("TotalAssets", DATA_TYPE_REAL),
    ("Equity", DATA_TYPE_REAL),
    ("EquityToAssetRatio", DATA_TYPE_REAL),
    ("BookValuePerShare", DATA_TYPE_REAL),
    ("CashFlowsFromOperatingActivities", DATA_TYPE_REAL),
    ("CashFlowsFromInvestingActivities", DATA_TYPE_REAL),
    ("CashFlowsFromFinancingActivities", DATA_TYPE_REAL),
    ("CashAndEquivalents", DATA_TYPE_REAL),
    ("ResultDividendPerShare1stQuarter", DATA_TYPE_REAL),
    ("ResultDividendPerShare2ndQuarter", DATA_TYPE_REAL),
    ("ResultDividendPerShare3rdQuarter", DATA_TYPE_REAL),
    ("ResultDividendPerShareFiscalYearEnd", DATA_TYPE_REAL),
    ("ResultDividendPerShareAnnual", DATA_TYPE_REAL),
    ("DistributionsPerUnitREIT", DATA_TYPE_REAL),
    ("ResultTotalDividendPaidAnnual", DATA_TYPE_REAL),
    ("ResultPayoutRatioAnnual", DATA_TYPE_REAL),
    ("ForecastDividendPerShare1stQuarter", DATA_TYPE_REAL),
    ("ForecastDividendPerShare2ndQuarter", DATA_TYPE_REAL),
    ("ForecastDividendPerShare3rdQuarter", DATA_TYPE_REAL),
    ("ForecastDividendPerShareFiscalYearEnd", DATA_TYPE_REAL),
    ("ForecastDividendPerShareAnnual", DATA_TYPE_REAL),
    ("ForecastDistributionsPerUnitREIT", DATA_TYPE_REAL),
    ("ForecastTotalDividendPaidAnnual", DATA_TYPE_REAL),
    ("ForecastPayoutRatioAnnual", DATA_TYPE_REAL),
    ("NextYearForecastDividendPerShare1stQuarter", DATA_TYPE_REAL),
    ("NextYearForecastDividendPerShare2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastDividendPerShare3rdQuarter", DATA_TYPE_REAL),
    ("NextYearForecastDividendPerShareFiscalYearEnd", DATA_TYPE_REAL),
    ("NextYearForecastDividendPerShareAnnual", DATA_TYPE_REAL),
    ("NextYearForecastDistributionsPerUnitREIT", DATA_TYPE_REAL),
    ("NextYearForecastPayoutRatioAnnual", DATA_TYPE_REAL),
    ("ForecastNetSales2ndQuarter", DATA_TYPE_REAL),
    ("ForecastOperatingProfit2ndQuarter", DATA_TYPE_REAL),
    ("ForecastOrdinaryProfit2ndQuarter", DATA_TYPE_REAL),
    ("ForecastProfit2ndQuarter", DATA_TYPE_REAL),
    ("ForecastEarningsPerShare2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastNetSales2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastOperatingProfit2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastOrdinaryProfit2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastProfit2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastEarningsPerShare2ndQuarter", DATA_TYPE_REAL),
    ("ForecastNetSales", DATA_TYPE_REAL),
    ("ForecastOperatingProfit", DATA_TYPE_REAL),
    ("ForecastOrdinaryProfit", DATA_TYPE_REAL),
    ("ForecastProfit", DATA_TYPE_REAL),
    ("ForecastEarningsPerShare", DATA_TYPE_REAL),
    ("NextYearForecastNetSales", DATA_TYPE_REAL),
    ("NextYearForecastOperatingProfit", DATA_TYPE_REAL),
    ("NextYearForecastOrdinaryProfit", DATA_TYPE_REAL),
    ("NextYearForecastProfit", DATA_TYPE_REAL),
    ("NextYearForecastEarningsPerShare", DATA_TYPE_REAL),
    ("MaterialChangesInSubsidiaries", DATA_TYPE_REAL),
    ("ChangesBasedOnRevisionsOfAccountingStandard", DATA_TYPE_REAL),
    ("ChangesOtherThanOnesBasedOnRevisionsOfAccountingStandard", DATA_TYPE_REAL),
    ("ChangesInAccountingEstimates", DATA_TYPE_REAL),
    ("RetrospectiveRestatement", DATA_TYPE_REAL),
    ("NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock", DATA_TYPE_REAL),
    ("NumberOfTreasuryStockAtTheEndOfFiscalYear", DATA_TYPE_REAL),
    ("AverageNumberOfShares", DATA_TYPE_REAL),
    ("NonConsolidatedNetSales", DATA_TYPE_REAL),
    ("NonConsolidatedOperatingProfit", DATA_TYPE_REAL),
    ("NonConsolidatedOrdinaryProfit", DATA_TYPE_REAL),
    ("NonConsolidatedProfit", DATA_TYPE_REAL),
    ("NonConsolidatedEarningsPerShare", DATA_TYPE_REAL),
    ("NonConsolidatedTotalAssets", DATA_TYPE_REAL),
    ("NonConsolidatedEquity", DATA_TYPE_REAL),
    ("NonConsolidatedEquityToAssetRatio", DATA_TYPE_REAL),
    ("NonConsolidatedBookValuePerShare", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedNetSales2ndQuarter", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedOperatingProfit2ndQuarter", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedOrdinaryProfit2ndQuarter", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedProfit2ndQuarter", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedEarningsPerShare2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedNetSales2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedOperatingProfit2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedOrdinaryProfit2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedProfit2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedEarningsPerShare2ndQuarter", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedNetSales", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedOperatingProfit", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedOrdinaryProfit", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedProfit", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedEarningsPerShare", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedNetSales", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedOperatingProfit", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedOrdinaryProfit", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedProfit", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedEarningsPerShare", DATA_TYPE_REAL),
]


class StatementsModel(BaseModel):

    DisclosedDate: StrictStr
    DisclosedTime: StrictStr
    LocalCode: StrictStr
    DisclosureNumber: StrictStr
    TypeOfDocument: StrictStr
    TypeOfCurrentPeriod: StrictStr
    CurrentPeriodStartDate: StrictStr
    CurrentPeriodEndDate: StrictStr
    CurrentFiscalYearEndDate: StrictStr
    CurrentFiscalYearStartDate: StrictStr
    NextFiscalYearStartDate: Optional[StrictStr]
    NextFiscalYearEndDate: Optional[StrictStr]
    NetSales: Optional[float]
    OperatingProfit: Optional[float]
    OrdinaryProfit: Optional[float]
    Profit: Optional[float]
    EarningsPerShare: Optional[float]
    DilutedEarningsPerShare: Optional[float]
    TotalAssets: Optional[float]
    Equity: Optional[float]
    EquityToAssetRatio: Optional[float]
    BookValuePerShare: Optional[float]
    CashFlowsFromOperatingActivities: Optional[float]
    CashFlowsFromInvestingActivities: Optional[float]
    CashFlowsFromFinancingActivities: Optional[float]
    CashAndEquivalents: Optional[float]
    ResultDividendPerShare1stQuarter: Optional[float]
    ResultDividendPerShare2ndQuarter: Optional[float]
    ResultDividendPerShare3rdQuarter: Optional[float]
    ResultDividendPerShareFiscalYearEnd: Optional[float]
    ResultDividendPerShareAnnual: Optional[float]
    DistributionsPerUnitREIT: Optional[float]
    ResultTotalDividendPaidAnnual: Optional[float]
    ResultPayoutRatioAnnual: Optional[float]
    ForecastDividendPerShare1stQuarter: Optional[float]
    ForecastDividendPerShare2ndQuarter: Optional[float]
    ForecastDividendPerShare3rdQuarter: Optional[float]
    ForecastDividendPerShareFiscalYearEnd: Optional[float]
    ForecastDividendPerShareAnnual: Optional[float]
    ForecastDistributionsPerUnitREIT: Optional[float]
    ForecastTotalDividendPaidAnnual: Optional[float]
    ForecastPayoutRatioAnnual: Optional[float]
    NextYearForecastDividendPerShare1stQuarter: Optional[float]
    NextYearForecastDividendPerShare2ndQuarter: Optional[float]
    NextYearForecastDividendPerShare3rdQuarter: Optional[float]
    NextYearForecastDividendPerShareFiscalYearEnd: Optional[float]
    NextYearForecastDividendPerShareAnnual: Optional[float]
    NextYearForecastDistributionsPerUnitREIT: Optional[float]
    NextYearForecastPayoutRatioAnnual: Optional[float]
    ForecastNetSales2ndQuarter: Optional[float]
    ForecastOperatingProfit2ndQuarter: Optional[float]
    ForecastOrdinaryProfit2ndQuarter: Optional[float]
    ForecastProfit2ndQuarter: Optional[float]
    ForecastEarningsPerShare2ndQuarter: Optional[float]
    NextYearForecastNetSales2ndQuarter: Optional[float]
    NextYearForecastOperatingProfit2ndQuarter: Optional[float]
    NextYearForecastOrdinaryProfit2ndQuarter: Optional[float]
    NextYearForecastProfit2ndQuarter: Optional[float]
    NextYearForecastEarningsPerShare2ndQuarter: Optional[float]
    ForecastNetSales: Optional[float]
    ForecastOperatingProfit: Optional[float]
    ForecastOrdinaryProfit: Optional[float]
    ForecastProfit: Optional[float]
    ForecastEarningsPerShare: Optional[float]
    NextYearForecastNetSales: Optional[float]
    NextYearForecastOperatingProfit: Optional[float]
    NextYearForecastOrdinaryProfit: Optional[float]
    NextYearForecastProfit: Optional[float]
    NextYearForecastEarningsPerShare: Optional[float]
    MaterialChangesInSubsidiaries: Optional[bool]
    ChangesBasedOnRevisionsOfAccountingStandard: Optional[bool]
    ChangesOtherThanOnesBasedOnRevisionsOfAccountingStandard: Optional[bool]
    ChangesInAccountingEstimates: Optional[bool]
    RetrospectiveRestatement: Optional[bool]
    NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock: Optional[float]
    NumberOfTreasuryStockAtTheEndOfFiscalYear: Optional[float]
    AverageNumberOfShares: Optional[float]
    NonConsolidatedNetSales: Optional[float]
    NonConsolidatedOperatingProfit: Optional[float]
    NonConsolidatedOrdinaryProfit: Optional[float]
    NonConsolidatedProfit: Optional[float]
    NonConsolidatedEarningsPerShare: Optional[float]
    NonConsolidatedTotalAssets: Optional[float]
    NonConsolidatedEquity: Optional[float]
    NonConsolidatedEquityToAssetRatio: Optional[float]
    NonConsolidatedBookValuePerShare: Optional[float]
    ForecastNonConsolidatedNetSales2ndQuarter: Optional[float]
    ForecastNonConsolidatedOperatingProfit2ndQuarter: Optional[float]
    ForecastNonConsolidatedOrdinaryProfit2ndQuarter: Optional[float]
    ForecastNonConsolidatedProfit2ndQuarter: Optional[float]
    ForecastNonConsolidatedEarningsPerShare2ndQuarter: Optional[float]
    NextYearForecastNonConsolidatedNetSales2ndQuarter: Optional[float]
    NextYearForecastNonConsolidatedOperatingProfit2ndQuarter: Optional[float]
    NextYearForecastNonConsolidatedOrdinaryProfit2ndQuarter: Optional[float]
    NextYearForecastNonConsolidatedProfit2ndQuarter: Optional[float]
    NextYearForecastNonConsolidatedEarningsPerShare2ndQuarter: Optional[float]
    ForecastNonConsolidatedNetSales: Optional[float]
    ForecastNonConsolidatedOperatingProfit: Optional[float]
    ForecastNonConsolidatedOrdinaryProfit: Optional[float]
    ForecastNonConsolidatedProfit: Optional[float]
    ForecastNonConsolidatedEarningsPerShare: Optional[float]
    NextYearForecastNonConsolidatedNetSales: Optional[float]
    NextYearForecastNonConsolidatedOperatingProfit: Optional[float]
    NextYearForecastNonConsolidatedOrdinaryProfit: Optional[float]
    NextYearForecastNonConsolidatedProfit: Optional[float]
    NextYearForecastNonConsolidatedEarningsPerShare: Optional[float]


class RawStatementsRepository:

    """ダウンロードした生の決算情報をデータベースに挿入するためのレポジトリ"""

    def __init__(self, repository_path: rp.AbstractRepositoryPath) -> None:
        self.repository_path = repository_path

    def insert_statements_df(self, df: pl.DataFrame) -> None:
        """データベースに対象日のレコードを挿入する"""

        # 入力のチェック
        if len(df) == 0:
            raise ValueError("DataFrame is empty.")

        if len(df["DisclosedDate"].unique()) != 1:
            raise ValueError("DataFrame contains two or more different disclosed date.")

        keys = [key for key, _ in DATA_DIFINITION]
        if len(df.columns) != len(keys):
            logger.warning("Fields size is different frop expectd size. Check JQuants sepcification updated.")

        # 既にレコードが存在していたら一度削除する
        conn = self.__get_connection()
        try:
            date = df["DisclosedDate"][0]
            if self.has_records(date):
                date_str = date.strftime("%Y-%m-%d")
                conn.execute(f"DELETE FROM stock WHERE DisclosedDateDate='{date_str}'")

            # 挿入処理
            df = preprocess_before_insert(df)

            if not validate_dataframe(df, StatementsModel):
                logger.error(f"Validation error on {date}")
                raise RuntimeError("Validation Failed.")

            df.write_database(TABLE_STATEMENTS, self.repository_path.connection_str, if_exists="append")
        finally:
            conn.close()

    def drop_index(self) -> None:
        """Indexを落とす"""
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("DROP INDEX IF EXISTS statements_index;")
        conn.commit()
        conn.close()

    def set_index(self) -> None:
        """CodeにIndexを貼る"""
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("CREATE INDEX IF NOT EXISTS statements_index ON statements (LocalCode);")
        conn.commit()
        conn.close()

    def create_table(self) -> None:
        """新しくstockテーブルを生成する"""
        conn = self.__get_connection()
        cur = conn.cursor()

        fields_str = ",".join([f"`{k}` {v}" for k, v in DATA_DIFINITION])
        query = f"""
            CREATE TABLE statements(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {fields_str}
        );"""
        cur.execute(query)

        conn.commit()
        conn.close()

    def table_exists(self) -> bool:
        """priceテーブルが存在するか判定する"""
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND name='statements';")
        size = res.fetchone()
        is_exist: bool = size[0] > 0
        conn.commit()
        conn.close()
        return is_exist

    def has_records(self, date: datetime.date) -> bool:
        """対象日のデータが存在するか確認する"""
        if not isinstance(date, datetime.date):
            raise TypeError("date must be 'datetiem.date'")
        date_str = date.strftime("%Y-%m-%d")
        conn = self.__get_connection()
        res = conn.execute(f"SELECT COUNT(*) FROM statements WHERE DisclosedDate='{date_str}';")
        size = res.fetchone()
        is_exist: bool = size[0] > 0
        conn.close()
        return is_exist

    def existing_date(self) -> List[datetime.date]:
        """DB上に存在している日付を列挙する"""
        conn = self.__get_connection()
        res = conn.execute("SELECT DISTINCT(DisclosedDate) FROM statements;")
        raw_date_list = [r[0] for r in res.fetchall()]
        date_list = [datetime.datetime.strptime(s, "%Y-%m-%d").date() for s in raw_date_list]
        conn.close()
        return date_list

    def records_size(self) -> int:
        """データ総数を取得"""
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM statements;")
        size: int = res.fetchone()[0]
        conn.commit()
        conn.close()
        return size

    def __get_connection(self) -> sqlite3.Connection:
        db_path = self.repository_path.sqlite_path
        conn = sqlite3.connect(db_path)
        return conn


def preprocess_before_insert(df: pl.DataFrame) -> pd.DataFrame:
    """Unicode型をSqliteが扱えないので予め処理する"""
    for col in df.columns:
        if df[col].dtype != pl.Utf8:
            continue
        df = df.with_columns(pl.when(pl.col(col) == "－").then(None).otherwise(pl.col(col)).alias(col))
        df = df.with_columns(pl.when(pl.col(col) == "").then(None).otherwise(pl.col(col)).alias(col))

    reit_pattern = re.compile(r"\(REIT\)")
    rename = {col: reit_pattern.sub("REIT", col) for col in df.columns}
    df = df.rename(rename)

    df = df.with_columns(pl.col("DisclosedDate").dt.strftime("%Y-%m-%d"))
    df = cast_with_model(df, StatementsModel, strict=False)
    validate_dataframe(df, StatementsModel)
    return df
