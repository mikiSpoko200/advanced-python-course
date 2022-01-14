# -*- encoding: utf-8 -*-

"""
DISCLAIMER:
    I used the weather data that was shared and approved to use in our solutions.
    Data retrieval is not a part of a program as I encountered difficulties with the csv file encodings.

** Result discussion **

Running the script should create two .jpg files named:
    1. ex1-Depta Covid-19 active cases during the first wave.jpg
    2. ex1-Depta Covid-19 active cases during warm period.jpg

The first one displays comparison of infection rates during the first wave.
That is the period when the number of active cases became especially large.
In the plot we can clearly see that the more temperature drops the higher the
number of active cases gets.

On the other hand, when it comes to the warmer period depicted on the second plot,
the number of active cases is substantially lower.
The discrepancy in values is so large in fact that if we were to plot the warmer period data
on the same axes as the values from the first wave period, the minor fluctuations visible on the plot
would be completely dwarfed by the numbers of active cases during the first wave.

I purposely omitted the first two months of the records due to the fact that
I don't think they are very representative.


** Conclusion **

As one could expect, the covid-19 active cases, as with most of flue-like diseases,
skyrocketed during the cold period of the year.
"""


import logging
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dts
from datetime import date
from typing import Iterable


LOGGING_LEVEL = logging.FATAL

INFECTIONS_FILENAME = "infections.csv"
INFECTIONS_PATH = "ex1Deptadata/%s" % INFECTIONS_FILENAME

TEMPERATURE_FILENAME = "temperatures.csv"
TEMPERATURE_PATH = "ex1Deptadata/%s" % TEMPERATURE_FILENAME


logging.basicConfig(level=LOGGING_LEVEL)


def plot(
        dates: Iterable[date],
        average_temperatures: Iterable[float],
        infection_data: Iterable[int],
        title: str) -> None:
    """Displays plots comparing active Covid-19 cases with the changes in temperature."""
    ax1_color = r"#1A1166"
    ax2_color = r"#C61115"

    # axis creation / figure configuration.
    fig, ax1 = plt.subplots(1, 1)
    ax2 = ax1.twinx()
    fig.set_figheight(7)
    fig.set_figwidth(10)

    # ax1 data series.
    ax1.plot(dates, average_temperatures, label="avg. temperatures", color=ax1_color)

    # ax2 data series.
    ax2.plot(dates, infection_data, label="active cases", color=ax2_color)

    # ax1 specific formatting.
    ax1.set_xlabel("date")
    ax1.set_ylabel("temperature, C°")
    ax1.grid(True, axis="y", linestyle="--")
    ax1.xaxis.set_major_formatter(dts.DateFormatter("%Y-%m-%d"))
    ax1.xaxis.set_major_locator(dts.MonthLocator())
    ax1.legend()

    # ax1 specific formatting.
    ax2.set_ylabel("Active cases")
    ax2.legend()
    ax2.set_ylim(0)

    # plot configuration
    fig.autofmt_xdate()
    plt.title(title)
    plt.savefig("ex1-Depta " + title + ".jpg", dpi=300)


def main():
    # download_infection_csv()
    # read data
    infections = pd.read_csv(INFECTIONS_PATH, sep=";")
    temperatures = pd.read_csv(TEMPERATURE_PATH, encoding="ISO-8859-1", sep=";")

    # process the data
    dates = [date.fromisoformat(_) for _ in temperatures["Date"]]
    average_temperatures = temperatures["Daily average temperature"]
    infection_data = infections["Active cases"]

    _ = list(dates).index(date.fromisoformat("2020-10-01"))
    dates_wave = dates[_:]
    infections_wave = infection_data[_:]
    temperatures_wave = average_temperatures[_:]
    infections_warm_period = infection_data[60:_]
    dates_warm_period = dates[60:_]
    temperatures_warm_period = average_temperatures[60:_]

    plot(
        dates_wave,
        temperatures_wave,
        infections_wave,
        "Covid-19 active cases during the first wave"
    )

    plot(
        dates_warm_period,
        temperatures_warm_period,
        infections_warm_period,
        "Covid-19 active cases during warm period"
    )


if __name__ == '__main__':
    main()
