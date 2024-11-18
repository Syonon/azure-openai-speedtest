import matplotlib.pyplot as plot
import pandas


if __name__ == "__main__":
    df = pandas.read_csv("output.csv")

    plot.boxplot(x=df, tick_labels=df.columns, showmeans=True)
    plot.title("Response time")
    plot.show()