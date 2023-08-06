import pandas as pd

class BackToTheFeature(pd.DataFrame):
    """
    BackToTheFeature

    A Python package that provides functionality for data processing and analysis using the "BackToTheFeature" class, which is derived from pandas DataFrame. This class offers convenient methods to add, filter, and group time-related features.

    Usage:
    ------

    Import the package with:
        import BackToTheFeature

    Example:
    --------
        import pandas as pd
        from BackToTheFeature import BackToTheFeature

        # Create an instance of the "BackToTheFeature" class
        data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
        df = pd.DataFrame(data)
        project = BackToTheFeature(df)

        # Add time-related features
        project.add_time_features('year', 'month', 'day')

        # Filter based on specific time-related features
        filtered_data = project.filter_time_features(year=2022, month='January')

        # Group by time-related feature and compute statistics
        grouped_data = project.group_time_feature('year')

    Features:
    ---------
    - BackToTheFeature: A class derived from the pandas DataFrame that provides convenient methods for managing and manipulating time-related features.
        - add_time_features: Adds time-related features to the dataset.
        - filter_time_features: Filters the dataset based on specific time-related features.
        - group_time_feature: Groups the dataset by a time-related feature and computes statistics.

    Dependencies:
    -------------
    - Python 3.6 or higher
    - pandas

    """      
    _metadata = ['_holiday_dates', '_time_features']
    
    @property
    def _constructor(self):
        return BackToTheFeature

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._time_features = {'year' : lambda x : x.index.year,
                               'month' : lambda x : x.index.month_name(),
                               'month_number' : lambda x : x.index.month,
                               'week_number' : lambda x : x.index.isocalendar().week.values.astype(int),
                               'weekday' : lambda x : x.index.day_name(),
                               'weekday_number' : lambda x : x.index.weekday,
                               'is_weekend': lambda x : x.index.weekday.map(lambda day : 1 if day >= 5 else 0),
                               'hour' : lambda x : x.index.hour,
                               'minute' : lambda x : x.index.minute,
                               'quarter' : lambda x : x.index.quarter,
                               'season_type': lambda x : x.index.month.map(lambda month : 'Winter' if month < 3 or month == 12 else ('Spring' if month < 6 else ('Summer' if month < 9 else 'Autumn'))),
                               'day_number' : lambda x : x.index.dayofyear 
                              }

    def add_time_features(self, *args, inplace=False, all_features=False):
        df = self if inplace else self.copy()
        if all_features: 
            return self.add_time_features(*self._time_features.keys())
        
        for feature in args:
            if feature in self._time_features:
                df[feature] = self._time_features[feature](df)
        if not inplace:
            return df

    def filter_time_features(self, inplace=False, **kwargs):
        df = self if inplace else self.copy()
        for key, value in kwargs.items():
            if key in self._time_features:
                df[key] = self._time_features[key](df)
                if value == 'all':
                    continue
                elif isinstance(value, list):
                    df = df[df[key].isin(value)]
                else:
                    df = df[df[key] == value]
        if not inplace:
            return df

    def group_time_feature(self, time_feature, inplace=False):
        df = self if inplace else self.copy()
        df[time_feature] = self._time_features[time_feature](df)
        df = df.select_dtypes(include='number')
        df = df.groupby(time_feature).agg(['mean', 'std'])
        if not inplace:
            return df