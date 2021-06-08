import os
from skincare_confessions import app

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)  # Change to false before final deployment, delete msg
