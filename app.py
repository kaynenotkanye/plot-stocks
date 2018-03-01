# pylint: disable=E1101, C0103
"""A dash application for plotting up-to-date stock prices."""
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dash
from plot_stocks.data import StockPrices
from plot_stocks import ui

app = dash.Dash()
stock = StockPrices()
symbols = stock.get_symbols()
periods = ui.get_periods()

app.layout = ui.layout(symbols)

@app.callback(
    dash.dependencies.Output('plot-stock', 'figure'),
    [
        dash.dependencies.Input('ticker-selector-dropdown', 'value'),
        dash.dependencies.Input('period-selector-radio', 'value')
    ])
def update_figure(selected_symbols, selected_period):
    """Update figure with inputs."""
    if not selected_symbols:
        return None
    if isinstance(selected_symbols, str):
        selected_symbols = [selected_symbols]
    print('Tickers selected: ', selected_symbols)
    names = list(stock.get_metadata(selected_symbols)['name'])

    if selected_period > 1:
        data = stock.get_history(selected_symbols)
    else:
        data = stock.get_recent(selected_symbols)

    selected_data = data.loc[selected_symbols]

    start = (datetime.today() - relativedelta(hour=10)).replace(
        hour=16, minute=0, second=0, microsecond=0)\
        - periods[selected_period]

    return ui.plot_history(
        selected_data[
            selected_data.index.get_level_values(1) > start],
        names
    )

app.css.append_css(
    {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
# Loading screen CSS
app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

if __name__ == '__main__':
    app.run_server(debug=True)
