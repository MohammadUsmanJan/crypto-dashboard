# Create virtual enviroment
cd project
python3 -m venv venv
source venv/bin/activate   # (Mac/Linux)
venv\Scripts\activate      # (Windows)

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# For Fetching coins from api to our database
python manage.py fetch_coingecko

# Start Django server
python manage.py runserver
