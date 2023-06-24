from flask import Flask, jsonify, render_template, send_from_directory
import mysql.connector
import datetime

app = Flask(__name__)

# Configure the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="nitesh",
    password="root@123",
    database="market"
)

# Define a Flask route to retrieve the data for a stock
@app.route('/<string:stock_name>')
def get_stock_data(stock_name):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {stock_name}")
    data = []
    for row in cursor.fetchall():
        date = row[1]
        date_string = date.strftime('%Y-%m-%d')
        date_object = datetime.datetime.strptime(date_string, '%Y-%m-%d')
        data.append({'date': date_string,'open': row[2], 'high': row[3], 'low': row[4], 'close': row[5],'volume': row[6], 'rsi': row[7], 'sma': row[8]})

    cursor.close()
    return jsonify(data)


# Define a Flask route to render the HTML page
#@app.route('/')
#def chart():
#    return render_template('chart.html')
    
@app.route('/')
def chart():
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")  # Assuming you have a table named 'stocks' with a column 'stock_name'
    stocks = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return render_template('chart.html', stocks=stocks)    

# Define a route to handle the favicon.ico request
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
