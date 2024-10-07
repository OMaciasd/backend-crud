from src.app import app
from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    app.run(debug=True, port=50010)
