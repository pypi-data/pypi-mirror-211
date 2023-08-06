cryptopp
========
cryptopp is a lightweight command line based cryptocurrency portfolio.
Built on Python 3 and ncurses with simplicity in mind, cryptop updates in realtime.

.. image:: img\cryptop.png

version 1.0.1

Changes
------------

This now requires a CryptoCompare.com and CoinMarketCap.com API key because of rate limits and extra data points.

See the Credits section on how to get an API key.

Added option for extra decimal places in .cryptop/config.ini based on currency.locale

Fixed + add coin user error to just add coin instead of error.

Added Market Cap from CoinMarketCap. API required.

Reads wallet every refresh and entry. Enables cryptop to be run on multiple computers from within a sharedrive.

Less url requests. Coin list is fetched every 10 days, instead of 
every coin addition. Speeds up processing of app.


TODO
------------

* Instead of using CC for 24h +/-, data already fetched from CMC in quote. Use CMC quote data for less requests.
* Add average price paid within wallet. Requires an addition "history" wallet.
* More historical portfolio changes.
* Coin Value +/- with mrkt conditions.
* History interface to interact with coin additions / subtractions.


Installation
------------

Via Pip

.. code:: bash

    pip3 install cryptopp

Or locally

cryptop requires Python 3 to run, and has only been tested in Python 3.6-3.10 so far.

First clone this repo

.. code:: bash

    git clone https://github.com/GordianSimpul/cryptopp

Then install cryptop through pip

.. code:: bash

    cd cryptopp
    pip3 install -e .


Make sure $HOME/.local/bin is in your environment PATH variable. 

Usage
-----

Start from a terminal.

.. code:: bash

    cryptopp [-k api_key] [-l api_key]

Follow the on screen instructions to add/remove or add/subtract values from your current wallet. The api_key options are only necessary if you didn't specify it in the .cryptop/config.ini file. An initial run is necessary to copy over config.ini to the .cryptop directory. 

.cryptop/config.ini

.. code:: bash

    key=CryptoComare API KEY
    key2=CoinMarketCap API KEY

Both of those need to edited o/w cryptop will not work.

Customisation
-------------

Cryptop creates two config files in a .cryptop folder in your home directory.

.cryptop/config.ini contains theme configuration (text/background colors) and
options to change the output currency (default USD), update frequency, number of decimal places to display and maximum width for float values.

.cryptop/wallet.json contains the coins and amounts you hold, you shouldn't need to edit it manually

Credits / API
-------------

Both are FREE.

Uses the `cryptocompare.com API
<http://www.cryptocompare.com/>`_.

Uses the `coinmarketcap.com API
<https://coinmarketcap.com/api>`_.

Tipjar
-------------

Help me reach my goal of contributing to the ongoing development of privacy coins

.. code:: bash

    XMR: 83az9t2fLjoC25d9UBUUiM1v6zemeKhjNf2Qw2Fnk1MFB3ecDx5oNVEG2tmdJJbxc97oAgjVbgCKHEgwTNFALh2c9jeWfdS

.. code:: bash

    DERO: dero1qyxctkgzee00jh3md4etc8kxkr8x4hh7cckezrhn7de39kj4xaf9xqqa6xeta

.. code:: bash

    BTC: bc1qfckkcnxxhxh5h0hnuc8gucymuvnxrw2a4traws

.. code:: bash
    
    ARRR: zs1gn457262c52z5xa666k77zafqmke0hd60qvc38dk48w9fx378h4zjs5rrwnl0x8qazj4q3x4svz



Disclaimer
----------

I am not liable for the accuracy of this program’s output nor actions
performed based upon it.
