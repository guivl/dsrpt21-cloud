from flask import Flask, render_template, request, Response
import sqlalchemy


app = Flask(__name__)


def init_connection_engine():
    db_config = {
    "pool_size":5,
    "max_overflow":2,
    "pool_timeout":30,
    "pool_recycle":1800
    }


    db_user = 'username'
    db_pass = 'password'
    db_name = 'db-name'
    db_host = 'db-host'

    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])

    pool = sqlalchemy.create_engine(

        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_hostname,
            port=db_port,
            database=db_name,
        ),
        **db_config
    )

    return pool


@app.route('/')
def hello():
    return 'Hello World!'


@app.route("/list", methods=["GET"])
def list():
    db = init_connection_engine()
    with db.connect() as conn:
        result = conn.execute(
            "SELECT * FROM container;"
        ).fetchall()
    return str(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
