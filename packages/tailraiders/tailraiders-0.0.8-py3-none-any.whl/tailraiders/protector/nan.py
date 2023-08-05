import pandas as pd


class Nan:
    """ Checks for NaN values and manipulate them """
    def __init__(self, df):
        self.df = df
        self.missing = df.isna().sum().to_frame()
        self.values = df.count().to_frame()
        self.rows = self.missing + self.values
        self.perc = round(self.missing / self.rows * 100, 2)
        self.dfnan = pd.concat([self.missing, self.values,
                                self.rows, self.perc], axis=1)
        self.dfnan.columns = ['total rows', 'rows with nan',
                              'rows without nan', 'perc nan']

    def drop_cols(self, th=20):
        """
        Drops columns based on a given threshold

        Parameters:
        ---------------
        self :
            The given name of the class

        th : int (default = 20)
            The percentage threshold of when
            columns should be dropped

        Returns:
        ----------------
        None :
            It makes it so that self.df is now edited
            to no longer has the dropped columns
        """

        # making a temp df to see what columns go over the threshold
        self.nan_df = self.dfnan[self.dfnan['perc nan'] > th]

        # making a list from the index to use for drop
        dropcols = list(self.nan_df.index)
        print(f'The columns {dropcols} are being dropped')

        # dropping the columns in the list
        self.df = self.df.drop(dropcols, axis=1)
        self.__init__(self.df)

    def fill_na(self, col, group, stat='mean'):
        """
        Fills dataframe columns based on
        a given group and method

        Parameters:
        --------------
        self :
            The given name of the class

        col : str
            The column name that will be filled

        group : str
            Column name that will be used to group by

        stat : str (default = 'mean')
            The stat on how people will be grouped

        Returns:
        ----------------
        None :
            It makes it so that self.df is now edited
            to no longer have the dropped columns
        """

        # using fillna to fill the given column with
        # given groupby column using the given method
        self.df[col] = self.df[col].fillna(self.df
                                           .groupby(group)[col]
                                           .transform(stat))
        self.__init__(self.df)

    def drop_na(self, axis=0):
        """
        Drops columns based on the given axis

        Parameters:
        ---------------
        self :
            The given name of the class

        axis : int (default = 0)
            Bool value, either 0 or 1. 0 is
            for rows and 1 is for columns

        Returns:
        ----------------
        None :
            It makes it so that self.df is now edited
            to no longer have the dropped rows or columns
        """

        # dropna to drop rows or columns, based on given axis
        self.df = self.df.dropna(axis=axis)
        self.__init__(self.df)

    @classmethod
    def use_file(cls, file_path):
        """
        A function to immediately convert files to be used for Nan

        Parameters
        --------------------
        cls :
            The class it is in (will not be filled in when using the function)

        file_path : str
            The file_path to the file containing the data you want to use

        returns:
        --------------------
        cls(df) : pandas.Dataframe
            A pandas dataframe that is immediately used for Nan.__init__
        """

        df = pd.read_csv(file_path)
        return cls(df)
