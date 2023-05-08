from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)  # enable CORS

# PostgreSQL database connection
conn = psycopg2.connect(database="banking_db", user="postgres", password="12345", host="127.0.0.1", port="5432")
print("DB CONNECTION - SUCCESS!!")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/query', methods=['POST'])
def run_query():
    try:
        query = request.form['query']
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # Build an HTML table to display the results
        table = '<table class="table table-striped">'
        for col in cursor.description:
            table += '<th>' + col[0] + '</th>'
        table += '</tr>'
        for row in results:
            table += '<tr>'
            for col in row:
                table += '<td>' + str(col) + '</td>'
            table += '</tr>'
        table += '</table>'
        
        return render_template('results.html', table=table)
    except (psycopg2.Error, KeyError) as e:
        error = "An error occurred: " + str(e)
        return render_template('error.html', error=error)

if __name__ == '__main__':
    app.run()
