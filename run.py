from app import app, db


@app.route('/', methods=['GET'])
def home():
    return "<h1>Flask Product Cart API</h1>"

if __name__ == '__main__':
    app.run(debug=True)