from flask import Flask, render_template
from gevent.pywsgi import WSGIServer
from models import get_analysis, get_ticker_data, get_chart_analysis
from statistics import mean
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.errorhandler(403)
def forbidden(error):
    return render_template("errors/403.html", title="Forbidden"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html", title="Page Not Found"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html", title="Server Error"), 500


@app.route('/', methods=['GET'])
def index():
    data = get_analysis()
    chart = get_chart_analysis()
    return render_template('front_page.html', data=data, legend=chart['legend'], the_date=chart['the_date'],
                           tickers=chart['tickers'], nested_dictionaries=chart['nested_dictionaries'])


@app.route('/stock/<string:ticker>', methods=['GET'])
def stock_data(ticker: str):
    ticker = ticker.upper()
    data = get_ticker_data(ticker)
    week_avg = mean(data.social_values)
    last_2_days_avg = (data.social_values[-1] + data.social_values[-2]) / 2
    return render_template('secondpage.html', data=data, data_social_dates=data.social_dates, data_social_values=data.social_values, week_avg=week_avg, last_2_days_avg=last_2_days_avg)


if __name__ == '__main__':
    app.run(debug=True)
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()
