import seaborn as sns
import matplotlib.pyplot as plt


class Plot:
    """ Code for making catplots and relplots """
    # Adding standard values for heigt, aspect and palette
    PALETTE = "plasma"
    HEIGHT = 4
    ASPECT = 3

    def __init__(self, df, xlim_low=None, xlim_high=None):
        self.data = df
        self._df = self.data
        self.xlim_low = xlim_low
        self.xlim_high = xlim_high
        sns.set_style('darkgrid')

    def cat(self, x, y, hue=None, kind='bar'):
        """
        A function to make a catplot, based on the dataframe used for Plot

        Parameters:
        --------------
        self :
            The given name of the class

        x : str
            Column name for x parameter

        y : str
            Column name for y parameter

        hue : str (default = None)
            A column name for differentiating per category

        kind : str (default = 'bar')
            The kind of plot you want to make, options are:
                strip, swarm, box, violin, boxen, point, bar and count

        Returns:
        --------------
        None :
            Instead it shows the plot for which the parameters are given
        """

        # try-except so it will show all columns if you use the wrong column
        try:
            # making the catplot using seaborn and defining certain attributes
            sns.catplot(data=self._df, x=x, y=y, palette=Plot.PALETTE,
                        hue=hue, kind=kind, height=Plot.HEIGHT,
                        aspect=Plot.ASPECT)
            plt.xlim(self.xlim_low, self.xlim_high)
            plt.title(label=f'{kind}plot with x: {x} and y: {y}')
            plt.show()
        except ValueError:
            raise ValueError(f"Make sure x, y and hue are \
                             a column name. Check {[*self._df.columns]}")

    def rel(self, x, y, hue=None, kind='scatter'):
        """
        A function to make a relplot, based on the dataframe used for Plot

        Parameters:
        --------------
        self :
            The given name of the class

        x : str
            Column name for x parameter

        y : str
            Column name for y parameter

        hue : str (default = None)
            A column name for differentiating per category

        kind : str (default = 'bar')
            The kind of plot you want to make, options are:
                strip, swarm, box, violin, boxen, point, bar and count

        Returns:
        --------------
        None :
            Instead it shows the plot for which the parameters are given
        """

        # try-except so it will show all columns if you use the wrong column
        try:
            # making the relplot using seaborn and defining certain attributes
            sns.relplot(data=self._df, x=x, y=y, palette=Plot.PALETTE,
                        hue=hue, kind=kind,
                        height=Plot.HEIGHT, aspect=Plot.ASPECT)
            plt.xlim(self.xlim_low, self.xlim_high)
            plt.title(label=f'{kind}plot with x: {x} and y: {y}')
            plt.show()
        except ValueError:
            raise ValueError(f"Make sure x, y and hue are \
                             a column name. Check {[*self._df.columns]}")


class MeltPlot(Plot):
    """ A child-class that uses a melted dataframe to make visualisations """
    def __init__(self, data, xlim_low=None, xlim_high=None):
        Plot.__init__(self, data, xlim_low, xlim_high)

    def cat(self, x, y, kind='bar'):
        """
        A function to make a catplot, based on the dataframe used for Plot

        Parameters:
        --------------
        self :
            The given name of the class

        x : str
            Column name for x parameter

        y : str
            Column name for y parameter

        kind : str (default = 'bar')
            The kind of plot you want to make, options are:
                strip, swarm, box, violin, boxen, point, bar and count

        Returns:
        --------------
        None :
            Instead it shows the plot for which the parameters are given
        """

        # try-except so it will show all columns if you use the wrong column
        try:
            # if-statement so that the function will work
            # as the normal Plot.cat as well
            if type(x) is str:
                Plot.cat(self, x, y, kind=kind)
            else:
                # making a melted df to use for Plot.cat
                self._df = self.data[x + [y]].melt(id_vars=y)
                hue = 'variable'
                x = 'value'
                Plot.cat(self, x, y, hue, kind)
        except KeyError:
            raise KeyError(f"Make sure x, y and hue are \
                           a column name. Check {[*self._df.columns]}")

    def rel(self, x, y, kind='scatter'):
        """
        A function to make a relplot, based on the dataframe used for Plot

        Parameters:
        --------------
        self :
            The given name of the class

        x : str
            Column name for x parameter

        y : str
            Column name for y parameter

        kind : str (default = 'scatter')
            The kind of plot you want to make, options are:
                strip, swarm, box, violin, boxen, point, bar and count

        Returns:
        --------------
        None :
            Instead it shows the plot for which the parameters are given
        """

        # try-except so it will show all columns if you use the wrong column
        try:
            # if-statement so that the function will work
            # as the normal Plot.rel as well
            if type(y) is str:
                Plot.rel(self, x, y, kind=kind)
            else:
                # making a melted df to use for Plot.rel
                self._df = self.data[[x] + y].melt(id_vars=x)
                hue = 'variable'
                x = 'value'
                Plot.rel(self, x, y, hue, kind)
        except KeyError:
            raise KeyError(f"Make sure x, y and hue are \
                           a column name. Check {[*self._df.columns]}")
