import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt

def load_performances(file_name):
    return json.load(open(file_name))

def save_as_json(file_name, o):
    with open(file_name, 'w') as output_file:
        json.dump(o, output_file)

def plot_results_by_date(dates, marks):
    # print("Dates: ", dates)
    print("Marks: ", marks)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())

    plt.plot(dates, marks)
    plt.gcf().autofmt_xdate()
    plt.show()

def create_time_series(first, last, event):
    print("Creating time series for {} {} in the {}".format(first, last, event))

    ind_perfs = filter(lambda perf: "LAST NAME" in perf and
        perf["FIRST NAME"] == first and perf["LAST NAME"] == last, performances)
    event_perfs = filter(lambda perf: perf["EVENT"] == event, ind_perfs)

    dates = []
    marks = []
    for perf in event_perfs:
        date_string = perf["DATE"]
        dates.append(dt.strptime(date_string, '%m/%d/%Y').date())
        mark = None
        if "TIME" in perf:
            try:
                mark = dt.strptime(perf["TIME"], '%M:%S.%f')
            except ValueError:
                mark = dt.strptime(perf["TIME"], '%M:%S')
        elif "MARK" in perf:
            mark = float(perf["MARK"][:-1])
        elif "POINTS" in perf:
            mark = int(perf["POINTS"])
        else:
            print("WARNING: No mark found in performance")
        marks.append(mark)
    if len(dates) > 0:
        zipped = list(zip(dates, marks))
        zipped.sort()
        dates, marks = zip(*zipped)
        return (dates, marks)
    else:
        return ([], [])

def plot_athlete_progress(first, last, event):
    dates, marks = create_time_series(first, last, event)
    plot_results_by_date(dates, marks)

if __name__ == "__main__":

    performances = load_performances("tutf-performances.json")

    plot_athlete_progress("Chris", "Gregory", "800m")
