# ChartGPT

ChartGPT is a Python library that leverages the power of Langchain and Plotly to generate charts from a pandas dataframe with just a single command.

It provides an intuitive and easy-to-use interface for creating visually appealing and interactive charts, making data visualization a breeze.

## Installation

To install ChartGPT, you can use pip:

```bash
pip install chartgpt
```

## Usage

Once installed, you can start using ChartGPT in your Python projects. Here's an example of how to use it:

```Python
from chartgpt import ChartGPT

cg = ChartGPT()
cg.plot(df, title="My Chart", x_label="X", y_label="Y")
```

The above code snippet demonstrates the basic usage of ChartGPT. Let's break it down:

1. Import the `ChartGPT` class from the `cg` module.
2. Create an instance of `ChartGPT` using `cg = ChartGPT()`.
3. Call the `plot` method on the `cg` instance, passing in your pandas dataframe (`df`), and providing optional parameters such as `title`, `x_label`, and `y_label`.

The `plot` method will generate a chart based on the provided dataframe and display it. You can customize the chart further by using additional parameters or methods provided by the Plotly library.

## Examples

ChartGPT supports various types of charts, including bar charts, line charts, scatter plots, and more. Here are a few examples:

### Bar Chart

```Python
cg.plot(df, chart_type="bar", title="Bar Chart", x_label="Categories", y_label="Values")
```

### Line Chart

```Python
cg.plot(df, chart_type="line", title="Line Chart", x_label="Time", y_label="Values")
```

### Scatter Plot

```Python
cg.plot(df, chart_type="scatter", title="Scatter Plot", x_label="X", y_label="Y")
```

These are just a few examples of what you can achieve with ChartGPT. Feel free to explore the Plotly documentation to learn more about customizing your charts.

## Additional Resources

- [Langchain Documentation](https://python.langchain.com/en/latest/)
- [Plotly Documentation](https://plotly.com/python/)

For detailed usage instructions and advanced features, refer to the official documentation of ChartGPT.

---

ChartGPT is an open-source project maintained by the community. If you have any questions, feedback, or issues, please don't hesitate to reach out on the project's GitHub page. We appreciate your contribution and hope you find ChartGPT useful for your data visualization needs.