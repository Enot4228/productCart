from app import create_app

app, db = create_app()


@app.route('/', methods=['GET'])
def home():
    return "<h1>Flask Product Cart API</h1>"

if __name__ == '__main__':
    app.run(debug=True)