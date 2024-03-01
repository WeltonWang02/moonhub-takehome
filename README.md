## Deployment Instructions

### Backend

1. Install dependencies:
   ```sh
   pip install -r backend/requirements.txt
   ```
2. Set environment variables in a `.env` file:
   ```env
PORT=3000
HOST=0.0.0.0
DATABASE=db.sqlite
FRONTEND_URL=http://localhost:5173
   ```
3. Run the Flask application:
   ```sh
   python backend/app.py
   ```

### Frontend

1. Enter directory and install dependencies:
   ```sh
   cd frontend/moonhub
   npm install
   ```
2. Set the backend API endpoint in an `.env` file:
   ```env
   VITE_API_ENDPOINT=http://localhost:3000
   ```
3. Start the development server:
   ```sh
   npm run dev
   ```
4. For production, build and serve the static files:
   ```sh
   npm run build
   npm run preview
   ```
