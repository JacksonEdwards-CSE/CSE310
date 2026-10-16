# Sleep Data Analysis

A Python data-analysis application that examines a sleep dataset and presents the results in both the terminal and a Tkinter graphical interface. The project explores how total sleep varies by danger index and provides interactive filters for minimum sleep and danger level.

## Features

- Load and clean `dataset_2191_sleep.csv` with Pandas.
- Convert selected dataset columns to numeric values and treat `?` as missing data.
- Print the number of records, median total sleep, records above the median, and the records with the most sleep.
- Calculate average total sleep for each danger index.
- Save an average-sleep-by-danger bar chart as `sleep_by_danger.png`.
- Display two chart tabs in a Tkinter GUI:
  - Average total sleep by danger index
  - Total sleep by individual record, sorted from highest to lowest
- Filter charts by minimum total sleep and danger index.
- Validate filter input and report invalid or empty filter results.

## Instructions for Build and Use

### Prerequisites

- Python 3.11 or a compatible Python 3 release
- Pandas
- Matplotlib
- Tkinter (usually included with Python on Windows)

Install the libraries if they are not already available:

```text
python -m pip install pandas matplotlib
```

### Run the terminal analysis

From the `data_analysis` directory, run:

```text
python SleepData.py --no-gui
```

This prints the analysis results and saves the average-sleep chart to `sleep_by_danger.png`.

### Run the graphical application

```text
python SleepData.py
```

The application opens a window with two chart tabs. Enter a minimum total-sleep value, choose a danger index, and select **Apply filter** to update both charts. Select **Clear** to restore all records.

## Development Environment

The project was developed with:

- Python 3.11
- Pandas for loading, cleaning, grouping, and analyzing the data
- Matplotlib for chart creation
- Tkinter for the desktop GUI
- The `dataset_2191_sleep.csv` dataset

## Project Structure

```text
data_analysis/
├── SleepData.py              # Analysis functions and Tkinter application
├── dataset_2191_sleep.csv    # Source sleep dataset
├── sleep_by_danger.png       # Generated average-sleep chart
├── readme.md                 # Project documentation
└── sprint_time_log.md        # Development time log
```

## Analysis Questions

The program addresses these questions:

1. Which records have the most total sleep?
2. What is the average total sleep for each danger index?
3. How do the results change when records are filtered by sleep amount or danger index?

## Useful Websites to Learn More

- [Python documentation](https://docs.python.org/3/)
- [Pandas documentation](https://pandas.pydata.org/docs/)
- [Matplotlib documentation](https://matplotlib.org/stable/)
- [Tkinter documentation](https://docs.python.org/3/library/tkinter.html)

## Future Work

- [ ] Add automated tests for data loading, grouping, filtering, and chart creation.
- [ ] Add a table view showing the filtered records and calculated statistics.
- [ ] Add additional chart types for sleep exposure, predation, or body weight.
- [ ] Allow users to export filtered results to a CSV file.
- [ ] Improve chart labels and layout for datasets with many records.
