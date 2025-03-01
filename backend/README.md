Stock Tracker Backend

📌 Backend Project Overview

This project provides a backend for tracking stock market trends, screening for breakout stocks, and organizing industry group analysis. It follows Stan Weinstein’s Top-Down Technical Analysis, allowing users to analyze sectors, industry groups, and individual stocks to identify strong investment opportunities.

🚀 Features

Stock Market Data Collection: Fetches stock price history, moving averages, RSI, volume spikes, and relative strength to the S&P 500.

Industry & Sector Analysis: Ranks industry groups based on relative strength and moving average trends.

Stock Screening: Identifies breakout stocks using a combination of price action, volume spikes, and momentum indicators.

GraphQL API: Allows querying for stock trends, sector strength, and potential breakout stocks.

User Features (Upcoming): Users will be able to create watchlists, save their own analysis, and track historical performance.

Automated Updates: Weekly automated stock data updates (can be enabled/disabled).

📍 Development Roadmap

✅ Phase 1: Data Collection & Storage

1️⃣ Fetch & Store Stock Market Data



2️⃣ Organize Sector & Industry Group Data

3️⃣ Populate the Database with Real Stocks & Sectors


✅ Phase 2: Data Processing & Analysis



4️⃣ Rank Sectors & Industry Groups



5️⃣ Screen for Breakout Stocks (Top-Down Analysis)



6️⃣ Automated Stock Data Updates





🔄 Phase 3: User & Sharing Features


7️⃣ Allow Users to Track Stocks & Save Analysis



8️⃣ Add GraphQL API for Insights & Reports



📖 Installation & Setup


Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Start the development server:

python manage.py runserver

