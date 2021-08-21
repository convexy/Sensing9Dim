import json
import sqlite3
from sqlite3.dbapi2 import connect
from bottle import Bottle, static_file, request

app = Bottle()

def getT_9DIM():
    ret = []
    conn = sqlite3.connect("./db/main.sqlite3")
    cur = conn.cursor()
    for row in cur.execute("select * from T_9DIM order by MDATETIME desc limit 20"):
        ret.append(row)
    cur.close()
    conn.close()
    return ret

@app.get("/")
@app.get("/<path:path>")
def callback(path="index.html"):
    if path.split("/")[0] == "data":
        return json.dumps(getT_9DIM())
    return static_file(path, root="./htdocs")


app.run(host='0.0.0.0', port=8080, debug=True)
