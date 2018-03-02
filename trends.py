import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

def load_performances(file_name):
    return json.load(open(file_name))

def save_as_json(file_name, o):
    with open(file_name, 'w') as output_file:
        json.dump(o, output_file)

def plot_results_by_date(dates, times):
    print("Dates: ", dates)
    print("Times: ", times)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.plot(dates, times)
    plt.gcf().autofmt_xdate()
    plt.show()

def create_time_series(first, last, event):
    print("Creating time series for {} {} in the {}".format(first, last, event))
    dates = []
    times = []
    for perf in performances:
        if "LAST NAME" in perf:
            if perf["FIRST NAME"] == first and perf["LAST NAME"] == last and perf["EVENT"] == event:
                date_string = perf["DATE"]
                dates.append(dt.datetime.strptime(date_string, '%m/%d/%Y').date())
                times.append(perf["TIME"])
    if len(dates) > 0:
        zipped = list(zip(dates, times))
        zipped.sort()
        dates, times = zip(*zipped)
        return (dates, times)
    else:
        return ([], [])

def plot_athlete_progress(first, last, event):
    dates, times = create_time_series(first, last, event)
    plot_results_by_date(dates, times)

if __name__ == "__main__":

    performances = load_performances("tutf-performances.json")

    plot_athlete_progress("Christian", "Swenson", "1500m")
