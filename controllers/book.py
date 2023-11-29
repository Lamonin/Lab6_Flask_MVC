from app import app


@app.route('/book', methods=['get'])
def book():
    return "Books pages"


@app.route('/statistics', methods=['get'])
def statistics():
    return "Statistics pages"
