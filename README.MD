# GREEN STEP BIDS: MY FINAL START2IMPACT BLOCKCHAIN DEVELOPMENT PROJECT! 👟
Hello and welcome to my final Start2Impact Blockchain Development Project. I enjoyed this Master and wow.. what a journey has been! From not knowing even what VSCode was to build such a complex project. I'm proud of myself!

## OVERVIEW 🌎
Welcome to GreenStepBids, a Django project for an online auction application, allowing users to participate in auctions and place bids on eco-friendly and sustainable sneakers.
At the conclusion of each auction, an automated process generates a JSON file containing comprehensive auction details, including the winning bidder's information. This JSON data is then hashed and securely transmitted to the Sepolia blockchain through a transaction.

Functionalities are explained in detail in the presentation attached to this repository.

![Homepage](screenshots/auctions.png)

## TECHNOLOGIES USED ⛓️
- Django
- CSS/Bootstrap
- Redis
- Celery
- Web3.py
- Javascript
- Git

## FEATURES 🧑🏻‍💻
- SIGN UP / LOGIN PAGE (W/ RESET PASSWORD FUNCIONALITIES) 
- DJANGO MESSAGES & OTHER GRAPHICS ELEMENTS (LOADING SPINNERS, ETC.)
- AUCTIONS PAGE
- AUCTION DETAILS PAGE
![AuctionDetails](screenshots/auctiondetail.png)
- MY AUCTIONS PAGE
![MyAuctions](screenshots/myauctions.png)

## WHAT HAPPENS WHEN AN AUCTION ENDS? 
When an auction expires, three Celery workers come into play. These workers are scheduled to listen to events every minute, such as the end of an auction. 

The first worker is responsible for fetching the highest bid and the winner from the Redis cache for that particular auction and then saving them in the database.
The second worker handles auctions that have concluded but have not yet been broadcasted to the Sepolia blockchain. 
It creates a JSON containing the auction data, hashes it, writes the transaction to the Sepolia blockchain and saves the tx hash to the database
The third worker activates when it detects a new Ethereum transaction has been broadcasted. In this case, to manage memory efficiently, it proceeds to clear the Redis cache (remember, Auctions are stored in the SQLite DB and Bids are stored in Redis!)  for the corresponding auction, preventing unnecessary memory consumption.

## LOCAL INSTALLATION
1. Clone the repository: git clone <https://github.com/diegoddie/VotingDapp-Start2ImpactProject>
2. Navigate to the project directory
3. Create a virtual environment: ```python -m venv venv```
4. Activate the virtual environment: 
    - On Windows: ```venv\Scripts\activate```
    - On macOS and Linux: ```source venv/bin/activate```
5. Install dependencies: ```pip install -r requirements.txt```
6. Configure environment variables:
- SECRET_KEY=your-secret-key
- DEBUG=True
- REDIS_URL=redis://localhost:6379/0
- EMAIL_HOST_USER=your-email@gmail.com
- EMAIL_HOST_PASSWORD=your-email-password
- ETHEREUM_URL=your-infura-ethereum-url
- PRIVATE_KEY=your-private-key
7. Apply migrations: ```python manage.py makemigrations``` and ```python manage.py migrate```
8. Create a superuser: ```python manage.py createsuperuser```
9. python manage.py runserver

## USAGE
- Access the admin interface at http://127.0.0.1:8000/admin/ using the superuser credentials created earlier.
- Create shoes and auctions of eco-friendly sneakers, place bids, and monitor auctions in the user interface at http://127.0.0.1:8000/auctions

## CONTACTS
Email: diego.boost@gmail.com
Github: github.com/diegoddie
Personal Website: https://diegolauricella.netlify.app/
Fiverr: fiverr.com/diegoddie
Upwork: upwork.com/freelancers/~01021369935709b658
