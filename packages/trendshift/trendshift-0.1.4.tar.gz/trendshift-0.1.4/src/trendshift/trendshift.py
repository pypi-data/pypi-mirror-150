import numpy as np
from pandas import DataFrame, Series

from .cache.pandascache import pd_cache


class TrendShift:
    """
    TrendShift is implemented following the builder pattern. It is instantiated
    with an input pandas DataFrame and the name of the target column in this
    DataFrame that watches on.

    The modification of the input dataframe in place is an option of the
    constructor as well.

    Most of the member functions are decorated with a result cache to avoid the
    same operation onto the same data twice.
    """

    # The precision decimals to take in account when comparing float numbers.
    PRECISION_DECIMALS = 10

    def __init__(self, df: DataFrame, target_column: str, in_place=False):
        self.__df = df if in_place else df.copy()
        self.__target_diff = df[target_column].diff()
        self.__sum = False
        self.__numbered_steps = False
        self.__sma = False
        self.__diff_by_trend = False
        self.__steps_by_trend = False

    def with_numbered_steps(self):
        """
        Building option to append a column for numbered steps into the product.

        The column name is "step_number".
        """
        self.__numbered_steps = True
        return self

    def with_sum(self):
        """
        Building option to append a column for the cumulative sum of every
        step in a shift. The first difference is added to the second step
        difference, the third to the second, and so on.

        The column name is "trends_sum".
        """
        self.__sum = True
        return self

    def with_simple_moving_avg(self):
        """
        Building option to append a column for the simple moving average into 
        the product.

        The column name is "simple_moving_avg".
        """
        self.__sma = True
        return self

    def with_difference_by_trend(self):
        """
        Building option to append a column with a value only in the first step
        of every trend. This value is the total difference of the trend, from
        the first step to the last. Only the first step in a trend has a value,
        the other steps are NaN.

        The column name is "trend_difference".
        """
        self.__diff_by_trend = True
        return self

    def with_steps_by_trend(self):
        """
        Building option to append the column with a value only in the first step
        of every trend. This value is the total number of steps of the trend.
        Only the first step in a trend has a value the other steps are NaN.

        The column name is "trend_steps".
        """
        self.__steps_by_trend = True
        return self

    def build(self):
        """
        Building method to create the dataframe according all building options
        described above.
        """
        if self.__sum:
            self.__df["trends_sum"] = self.__sum_steps_from(self.__target_diff)
        if self.__numbered_steps:
            self.__df["step_number"] = \
                self.__number_steps_from(self.__target_diff)
        if self.__sma:
            self.__df["simple_moving_avg"] = \
                self.__calculate_sma_from(self.__target_diff)
        if self.__diff_by_trend:
            self.__df["trend_difference"] = \
                self.total_trend_diff_from(self.__target_diff)
        if self.__steps_by_trend:
            self.__df["trend_steps"] = \
                self.count_trend_steps_from(self.__target_diff)
        return self.__df

    @classmethod
    def count_trend_steps_from(cls, a_series: Series):
        return cls.__create_total_column(a_series, cls.__count_reversed_from)

    @classmethod
    def total_trend_diff_from(cls, a_series: Series):
        return cls.__create_total_column(a_series, cls.__sum_reversed_from)

    @classmethod
    def __sum_reversed_from(cls, a_series: Series):
        return cls.__sum_steps_from(
            a_series.sort_index(ascending=False)
        ).sort_index(ascending=True)

    @classmethod
    def __count_reversed_from(cls, a_series: Series):
        return cls.__number_steps_from(
            a_series.sort_index(ascending=False)
        ).sort_index(ascending=True)

    @classmethod
    @pd_cache
    def __create_total_column(cls, a_series: Series, callback: callable):
        sandbox = DataFrame(index=a_series.index)
        sandbox["count"] = cls.__number_steps_from(a_series)
        sandbox["reversed"] = callback(a_series)
        sandbox["reversed"].loc[sandbox["count"] != 1] = np.nan
        return sandbox["reversed"]

    @classmethod
    @pd_cache
    def __calculate_sma_from(cls, a_series: Series):
        column_clone = a_series.copy()
        up_sma = cls.__sma_from(
            cls.__sum_ascending_from(column_clone),
            cls.__number_ascending_from(column_clone))
        down_sma = cls.__sma_from(
            cls.__sum_descending_from(column_clone),
            cls.__number_descending_from(column_clone))
        column_clone.replace([np.nan, np.any], 0, inplace=True)
        column_clone.update(up_sma)
        column_clone.update(down_sma)
        return column_clone

    @classmethod
    @pd_cache
    def __number_steps_from(cls, a_series: Series):
        column_clone = a_series.copy()
        column_clone.update(cls.__number_ascending_from(a_series))
        column_clone.update(cls.__number_descending_from(a_series))
        return column_clone

    @classmethod
    @pd_cache
    def __sum_steps_from(cls, a_series: Series):
        column_clone = a_series.copy()
        up_sum = cls.__sum_ascending_from(a_series)
        down_sum = cls.__sum_descending_from(a_series)
        column_clone.update(up_sum)
        column_clone.update(down_sum)
        return column_clone

    @classmethod
    @pd_cache
    def __set_not_null_to_1_from(cls, a_series: Series):
        """
        It sets any not null value to 1 and everything else to null
        """
        return a_series.notna().astype(int).replace(0, np.nan)

    @classmethod
    @pd_cache
    def __set_ascending_to_1_from(cls, a_series: Series):
        return cls.__set_not_null_to_1_from(
            cls.__ascending_trends_from(a_series))

    @classmethod
    @pd_cache
    def __set_descending_to_1_from(cls, a_series: Series):
        return cls.__set_not_null_to_1_from(
            cls.__descending_trends_from(a_series))

    @classmethod
    @pd_cache
    def __number_ascending_from(cls, a_series: Series):
        return cls.__sum_consecutive_from(
            cls.__set_ascending_to_1_from(a_series))

    @classmethod
    @pd_cache
    def __number_descending_from(cls, a_series: Series):
        return cls.__sum_consecutive_from(
            cls.__set_descending_to_1_from(a_series))

    @classmethod
    @pd_cache
    def __sum_ascending_from(cls, a_series: Series):
        return cls.__sum_consecutive_from(
            cls.__ascending_trends_from(a_series))

    @classmethod
    @pd_cache
    def __sum_descending_from(cls, a_series: Series):
        return cls.__sum_consecutive_from(
            cls.__descending_trends_from(a_series))

    @classmethod
    @pd_cache
    def __sum_consecutive_from(cls, a_series):
        cumulative_sum = a_series.cumsum().fillna(method='pad')
        reset = -cumulative_sum[a_series.isnull()].diff().fillna(cumulative_sum)
        result = a_series.where(a_series.notnull(), reset).cumsum()
        return result[0 != result.round(decimals=cls.PRECISION_DECIMALS)]

    @classmethod
    @pd_cache
    def __ascending_trends_from(cls, a_series: Series):
        return a_series.mask(a_series <= 0)

    @classmethod
    @pd_cache
    def __descending_trends_from(cls, a_series: Series):
        return a_series.mask(a_series >= 0)

    @classmethod
    @pd_cache
    def __sma_from(cls, distance, steps_count):
        return distance / steps_count
