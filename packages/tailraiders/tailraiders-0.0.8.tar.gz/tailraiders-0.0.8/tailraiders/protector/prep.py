import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Outliers:
    """ A class to analyse and deal with potential outliers """
    def __init__(self, df):
        self.df = df

    def check_skew(self, column, th=0.5):
        """
        This function checks the skewness of a given
        column from the dataframe given to the class

        Parameters:
        --------------------
        self :
            The given name of the class

        column : str
            The column of the dataframe you want to check

        th : float (default = 0.5)
            The threshold of which a column is
            considered skewed or nearly symmetrical

        Returns:
        --------------------
        None :
            Instead returns two print statements and a graph
            detailing and showing the distribution of the column
        """

        # If-statement to check for int or float
        if isinstance(self.df[column], (int, float)):
            # Checking the skewness of the given column
            skewness = self.df[column].skew()

            # if-statement for the type of skewness
            if abs(skewness) <= th:
                skewness_type = "Symmetric"
            elif skewness > 0:
                skewness_type = "Right-skewed"
            else:
                skewness_type = "Left-skewed"

            # Printing the skewness type and value
            print(f"Skewness type: {skewness_type}")
            print(f"Skewness value: {skewness}")

            # Visualising the skewness
            plt.figure(figsize=(8, 6))
            sns.histplot(self.df[column], kde=True)
            plt.xlabel("Values")
            plt.ylabel("Frequency")
            plt.title(f"Distribution of {column}")
            plt.show()

        # raising an error when column isnt int or float
        else:
            raise ValueError(f'The column {column} is not \
                             interger or float, so skewness \
                             cannot be calculated')

    def check_outliers(self, column, th=1.5, remove=False):
        """
        This function checks a column for outliers if
        there is a normal distribution and possibly removes them.
        Checking the outliers is based on using the Inter Quartile Range.

        Parameters:
        --------------------
        self :
            The given name of the class

        column : str
            The name of the column you want to check

        th : float or int (default = 1.5)
            The threshold for the IQR, with th
            having the most common value of 1.5

        remove : bool (default = False)
            A boolean value that determines if
            the outliers will be removed or not

        Returns:
        --------------------
        None :
            Instead returns a print which shows the outliers
        """

        # Check if column is a string or a list
        if isinstance(column, str):
            # Process a single column
            columns = [column]
        elif isinstance(column, list) and \
                all(isinstance(col, str) for col in column):
            # Process each column in the list
            columns = column
        else:
            raise ValueError("The column parameter must be \
                             a string or a list of strings.")

        # Create a list to store outliers for each column
        skipped_columns = []

        for col in columns:
            # If-statement to check for int or float
            if isinstance(self.df[col], (int, float)):
                # Making the quartile ranges
                q1 = np.percentile(self.df[col], 25)
                q3 = np.percentile(self.df[col], 75)
                iqr = q3 - q1

                # Making the upper and lower bounds for the values
                # to see if they are considered an outlier
                lower_bound = q1 - th * iqr
                upper_bound = q3 + th * iqr

                # Making a DataFrame where only the
                # outliers are contained within
                outliers = self.df[col][(self.df[col] <= lower_bound)
                                        | (self.df[col] >= upper_bound)]

                # If-statement to print out the amount of outliers
                if len(outliers) == 0:
                    print(f"No outliers were found in {col}.")
                else:
                    print(f"The following outliers are found in {col}:")
                    print(outliers)

                # If-statement for checking if the outliers will be removed.
                if remove is True:
                    # Remove outliers from the DataFrame
                    self.df = self.df[(self.df[col] >= lower_bound)
                                      & (self.df[col] <= upper_bound)]

            # Append the col into the skipped_columns list
            else:
                skipped_columns.append(col)
                continue

        # If columns are skipped, print the columns that were skipped
        if len(skipped_columns) > 0:
            print(f"The following columns were skipped \
                    due to non-numeric values: {skipped_columns}")

        return self.df
