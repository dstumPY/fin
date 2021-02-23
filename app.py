# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from fin.io.run_app import app

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8050)
