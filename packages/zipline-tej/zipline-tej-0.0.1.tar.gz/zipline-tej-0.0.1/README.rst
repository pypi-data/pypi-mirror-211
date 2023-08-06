Installation
============

Requirements
------------

-  Zipline-reloaded 2.2.0
-  Python 3.8 or above
-  Microsoft Windows OS
-  Python packages: Pandas, Numpy, Logbook, Exchange-calendars

How to install Zipline Reloaded modified by TEJ
-----------------------------------------------

-  We’re going to illustrate under anaconda environment, so we suggest
   using `Anaconda <https://www.anaconda.com/data-science-platform>`__
   as development environment.

-  Download dependency packages.
   `(zipline-tej.yml) </uploads/04b6deacb4850e807e28e9f0dcc82833/zipline-tej.yml>`__

-  Start an Anaconda (base) prompt, create an virtual environment and
   install the appropriate versions of packages:

::

   # create virtual env
   $ conda env create -f zipline-tej.yml

   # activate virtual env
   $ conda activate zipline-tej

   # install required packages
   $ pip install zipline-tej

Exchange Calendar Issues
------------------------

We’re now developing specfic on Taiwan securities backtesting strategy,
so we’re using the unique trading calendar created by ourselves.
`download <>`__

After downloaded the calendar file above, overwrite them into
exchange_calendars folder.

\* Navigate to the exchange_calendars folder within site packages. This
is typically located at C::raw-latex:`\Users`\\< your username
>:raw-latex:`\Anaconda3`:raw-latex:`\envs`:raw-latex:`\zipline`-tej:raw-latex:`\Lib`:raw-latex:`\site`-packages:raw-latex:`\exchange`\_calendars

Quick start
===========

CLI Interface
-------------

The following code implements a simple buy_and_hold trading algorithm.

.. code:: python

   from zipline.api import order, record, symbol

   def initialize(context):
       context.asset = symbol("2330")
       
   def handle_data(context, data):
       order(context.asset, 10)
       record(TSMC=data.current(context.asset, "price"))
       
   def analyze(context=None, results=None):
       import matplotlib.pyplot as plt

       # Plot the portfolio and asset data.
       ax1 = plt.subplot(211)
       results.portfolio_value.plot(ax=ax1)
       ax1.set_ylabel("Portfolio value (TWD)")
       ax2 = plt.subplot(212, sharex=ax1)
       results.TSMC.plot(ax=ax2)
       ax2.set_ylabel("TSMC price (TWD)")

       # Show the plot.
       plt.gcf().set_size_inches(18, 8)
       plt.show()

You can then run this algorithm using the Zipline CLI. But first, you
need to download some market data with historical prices and trading
volumes: \* Before ingesting data, you have to set some environment
variables as follow:

::

   # setting TEJAPI_KEY to get permissions loading data
   $ set TEJAPI_KEY=<your_key>

   # setting download ticker
   $ set ticker=2330 2317

   # setting backtest period
   $ set mdate=20200101 20220101

-  Ingest and run backtesting algorithm

::

   $ zipline ingest -b tquant
   $ zipline run -f buy_and_hold.py  --start 20200101 --end 20220101 -o bah.pickle --no-benchmark --trading-calendar TEJ_XTAI

Then, the resulting performance DataFrame is saved as bah.pickle, which
you can load and analyze from Python.

Jupyter Notebook
----------------

Set environment variables TEJAPI_KEY, ticker and mdate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

\* ticker would be your target ticker symbol, and it should be a string.
If there’re more than one ticker needed, use ” “,”,” or “;” to split
them apart.

\* mdate refers the begin date and end date, use ” “,”,” or “;” to split
them apart.

.. code:: python

   In[1]:
   import os    
   os.environ['TEJAPI_KEY'] = <your_key>    
   os.environ['ticker'] ='2330 2317'     
   os.environ['mdate'] ='20200101 20220101'  

Call ingest to download data to ~\.zipline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   In[2]:    
   !zipline ingest -b tquant
   [Out]: 
   Merging daily equity files:
   [YYYY-MM-DD HH:mm:ss.ssssss] INFO: zipline.data.bundles.core: Ingesting tquant.

Design the backtesting strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   In[3]:
   from zipline.api import order, record, symbol

   def initialize(context):
       context.asset = symbol("2330")
       
   def handle_data(context, data):
       order(context.asset, 10)
       record(TSMC=data.current(context.asset, "price"))
       
   def analyze(context=None, results=None):
       import matplotlib.pyplot as plt

       # Plot the portfolio and asset data.
       ax1 = plt.subplot(211)
       results.portfolio_value.plot(ax=ax1)
       ax1.set_ylabel("Portfolio value (TWD)")
       ax2 = plt.subplot(212, sharex=ax1)
       results.TSMC.plot(ax=ax2)
       ax2.set_ylabel("TSMC price (TWD)")

       # Show the plot.
       plt.gcf().set_size_inches(18, 8)
       plt.show()

Run backtesting algorithm and plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   In[4]:
   from zipline import run_algorithm
   import pandas as pd
   from zipline.utils.calendar_utils import get_calendar
   trading_calendar = get_calendar('TEJ_XTAI')

   start = pd.Timestamp('20200103', tz ='utc' )
   end = pd.Timestamp('20211230', tz='utc')

   result = run_algorithm(start=start,
                     end=end,
                     initialize=initialize,
                     capital_base=1000000,
                     handle_data=handle_data,
                     bundle='tquant',
                     trading_calendar=trading_calendar,
                     analyze=analyze,
                     data_frequency='daily'
                     )
   [Out]:

.. figure:: /uploads/90b6240acf50bc0a6435edf09b86c3e8/output_3_0.png
   :alt: output_3_0

   output_3_0

Show trading process
~~~~~~~~~~~~~~~~~~~~

.. code:: python

   In[5]: 
   result
   [Out]:

.. container::

   .. raw:: html

      <table border="1" class="dataframe">

   .. raw:: html

      <thead>

   .. raw:: html

      <tr style="text-align: right;">

   .. raw:: html

      <th>

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   period_open

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   period_close

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   starting_value

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   ending_value

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   starting_cash

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   ending_cash

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   portfolio_value

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   longs_count

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   shorts_count

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   long_value

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   …

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   treasury_period_return

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   trading_days

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   period_label

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   algo_volatility

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   benchmark_period_return

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   benchmark_volatility

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   algorithm_period_return

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   alpha

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   beta

   .. raw:: html

      </th>

   .. raw:: html

      <th>

   sharpe

   .. raw:: html

      </th>

   .. raw:: html

      </tr>

   .. raw:: html

      </thead>

   .. raw:: html

      <tbody>

   .. raw:: html

      <tr>

   .. raw:: html

      <th>

   2020-01-03 05:30:00+00:00

   .. raw:: html

      </th>

   .. raw:: html

      <td>

   2020-01-03 01:01:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2020-01-03 05:30:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.000000e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.000000e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.000000e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2020-01

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   NaN

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   NaN

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.000000

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   NaN

   .. raw:: html

      </td>

   .. raw:: html

      </tr>

   .. raw:: html

      <tr>

   .. raw:: html

      <th>

   2020-01-06 05:30:00+00:00

   .. raw:: html

      </th>

   .. raw:: html

      <td>

   2020-01-06 01:01:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2020-01-06 05:30:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   3320.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.000000e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   9.966783e+05

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   9.999983e+05

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   3320.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2020-01

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.000019

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -0.000002

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -11.224972

   .. raw:: html

      </td>

   .. raw:: html

      </tr>

   .. raw:: html

      <tr>

   .. raw:: html

      <th>

   2020-01-07 05:30:00+00:00

   .. raw:: html

      </th>

   .. raw:: html

      <td>

   2020-01-07 01:01:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2020-01-07 05:30:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   3320.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   6590.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   9.966783e+05

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   9.933817e+05

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   9.999717e+05

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   6590.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   3

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2020-01

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.000237

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -0.000028

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -10.038514

   .. raw:: html

      </td>

   .. raw:: html

      </tr>

   .. raw:: html

      <tr>

   .. raw:: html

      <th>

   2020-01-08 05:30:00+00:00

   .. raw:: html

      </th>

   .. raw:: html

      <td>

   2020-01-08 01:01:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2020-01-08 05:30:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   6590.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   9885.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   9.933817e+05

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   9.900850e+05

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   9.999700e+05

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   9885.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   4

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2020-01

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.000203

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -0.000030

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -9.298128

   .. raw:: html

      </td>

   .. raw:: html

      </tr>

   .. raw:: html

      <tr>

   .. raw:: html

      <th>

   2020-01-09 05:30:00+00:00

   .. raw:: html

      </th>

   .. raw:: html

      <td>

   2020-01-09 01:01:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2020-01-09 05:30:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   9885.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   13500.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   9.900850e+05

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   9.867083e+05

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.000208e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   13500.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   5

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2020-01

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.001754

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.000208

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   5.986418

   .. raw:: html

      </td>

   .. raw:: html

      </tr>

   .. raw:: html

      <tr>

   .. raw:: html

      <th>

   …

   .. raw:: html

      </th>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      </tr>

   .. raw:: html

      <tr>

   .. raw:: html

      <th>

   2021-12-24 05:30:00+00:00

   .. raw:: html

      </th>

   .. raw:: html

      <td>

   2021-12-24 01:01:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2021-12-24 05:30:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2920920.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2917320.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -1.308854e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -1.314897e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.602423e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2917320.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   484

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2021-12

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.232791

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.602423

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.170743

   .. raw:: html

      </td>

   .. raw:: html

      </tr>

   .. raw:: html

      <tr>

   .. raw:: html

      <th>

   2021-12-27 05:30:00+00:00

   .. raw:: html

      </th>

   .. raw:: html

      <td>

   2021-12-27 01:01:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2021-12-27 05:30:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2917320.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2933040.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -1.314897e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -1.320960e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.612080e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2933040.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   485

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2021-12

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.232577

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.612080

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.182864

   .. raw:: html

      </td>

   .. raw:: html

      </tr>

   .. raw:: html

      <tr>

   .. raw:: html

      <th>

   2021-12-28 05:30:00+00:00

   .. raw:: html

      </th>

   .. raw:: html

      <td>

   2021-12-28 01:01:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2021-12-28 05:30:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2933040.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2982750.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -1.320960e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -1.327113e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.655637e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2982750.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   486

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2021-12

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.233086

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.655637

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.237958

   .. raw:: html

      </td>

   .. raw:: html

      </tr>

   .. raw:: html

      <tr>

   .. raw:: html

      <th>

   2021-12-29 05:30:00+00:00

   .. raw:: html

      </th>

   .. raw:: html

      <td>

   2021-12-29 01:01:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2021-12-29 05:30:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2982750.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2993760.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -1.327113e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -1.333276e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.660484e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2993760.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   487

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2021-12

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.232850

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.660484

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.243176

   .. raw:: html

      </td>

   .. raw:: html

      </tr>

   .. raw:: html

      <tr>

   .. raw:: html

      <th>

   2021-12-30 05:30:00+00:00

   .. raw:: html

      </th>

   .. raw:: html

      <td>

   2021-12-30 01:01:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2021-12-30 05:30:00+00:00

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2993760.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2995050.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -1.333276e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   -1.339430e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.655620e+06

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2995050.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   …

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   488

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   2021-12

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.232629

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.0

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   0.655620

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   None

   .. raw:: html

      </td>

   .. raw:: html

      <td>

   1.235305

   .. raw:: html

      </td>

   .. raw:: html

      </tr>

   .. raw:: html

      </tbody>

   .. raw:: html

      </table>

   .. raw:: html

      <p>

   488 rows × 38 columns

   .. raw:: html

      </p>

Common errors
-------------

-  NotSessionError : The date of algorithm start date or end date is not
   available in trading algorithm.

   -  Solution : Adjust start date or end date to align trading
      calendar.

-  DateOutOfBounds : The trading calendar would update every day, but it
   would be fixed on the **FIRST TIME** executed date in Jupyter
   Notebook.

   -  Solution : Restart Jupyter Notebook kernel.

More Zipline Tutorials
======================

-  For more `tutorials <>`__

Suggestions
===========

-  Any `suggestions <>`__
-  To get TEJAPI_KEY `(link) <https://api.tej.com.tw/trial.html>`__
-  `TEJ Official Website <https://www.tej.com.tw/>`__
