import csv
import requests


def main():
    # Read NYTimes Covid Database
    download = requests.get(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    )
    decoded_content = download.content.decode("utf-8")
    file = decoded_content.splitlines()
    reader = csv.DictReader(file)

    # Construct 14 day lists of new cases for each states
    new_cases = calculate(reader)

    # Create a list to store selected states
    states = []
    print("Choose one or more states to view average COVID cases.")
    print("Press enter when done.\n")

    while True:
        state = input("State: ")
        if state in new_cases:
            states.append(state)
        if len(state) == 0:
            break

    print(f"\nSeven-Day Averages")

    # Print out 7-day averages for this week vs last week
    comparative_averages(new_cases, states)


# Create a dictionary to store 14 most recent days of new cases by state
def calculate(reader):
    cases = {}
    for line in reader:
        state = line["state"]
        if state not in cases:
            cases[state] = state
            cases[state] = []

        cases[state].append(line["cases"])
        if len(cases[state]) > 14:
            cases[state].pop(0)

    return cases


# Calculate and print out seven day average for given state


# Harvard preferred way
def comparative_averages(new_cases, states):
    for state in states:
        # Convert new cases into numbers
        for i in range(len(new_cases[state])):
            new_cases[state][i] = int(new_cases[state][i])

        # Separate last week from fourteen to seven week
        last_week = new_cases[state][7:]
        fourteen_to_seven_week = new_cases[state][:7]
        # Initialize counting variables
        last_week_average, fourteen_to_seven_week_average = 0, 0

        # Iterate through both week lists, count cases and average
        for i in range(len(last_week)):
            if i == 0:
                continue
            else:
                last_week_average += last_week[i] - last_week[i - 1]
        last_week_average = round(last_week_average / 7)

        for i in range(len(fourteen_to_seven_week)):
            if i == 0:
                continue
            else:
                fourteen_to_seven_week_average += (
                    fourteen_to_seven_week[i] - fourteen_to_seven_week[i - 1]
                )
        fourteen_to_seven_week_average = round(fourteen_to_seven_week_average / 7)

        # Calculate increase or decrease %
        try:
            average = round(
                (last_week_average - fourteen_to_seven_week_average)
                / last_week_average
                * 100
            )
        except:
            average = 0

        # Print result
        if average >= 0:
            print(
                f"{state} had a 7-day average of {last_week_average} and an increase of {average}%."
            )
        else:
            print(
                f"{state} had a 7-day average of {last_week_average} and a decrease of {abs(average)}%."
            )


# 2nd way (better and faster) to do this
"""
def comparative_averages(new_cases, states):
    for state in states:
        last_week_average = round((int(new_cases[state][13]) - int(new_cases[state][7])) / 7)
        fourteen_to_seven_week_average = round((int(new_cases[state][6]) - int(new_cases[state][0])) / 7)

        try:
            average = round((last_week_average - fourteen_to_seven_week_average) / last_week_average * 100)
            print("average is not 0", average)
        except:
            average = 0
            print("average is 0")

        if average >= 0:
            print(f'{state} had a 7-day average of {last_week_average} and an increase of {average}%.')
        else:
            print(f'{state} had a 7-day average of {last_week_average} and a decrease of {abs(average)}%.')

"""


main()
