# from bungee_gum import app
from bungee_gum import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
