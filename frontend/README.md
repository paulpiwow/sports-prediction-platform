
---

# 🎨 Frontend README (`frontend/README.md`)

```md
# Sports Match Predictor Frontend

A React-based frontend application that allows users to interactively predict **Soccer** and **NBA** match outcomes using a machine learning API.

---

## ✨ Features

- Clean, modern UI
- Sport selection landing page
- Separate prediction pages for:
  - ⚽ Soccer
  - 🏀 NBA
- Dynamic team selection
- Real-time predictions via REST API
- Responsive design
- Visual card-based navigation

---

## 🧭 User Flow

1. User lands on **Home Page**
2. Selects a sport (Soccer or NBA)
3. Navigates to sport-specific page
4. Selects Home & Away teams
5. Clicks **Predict Match**
6. Views probabilities and predicted winner


---

## 🖼 UI Design

- Card-based landing page
- Sport-specific background images
- Hover animations
- Clear separation of concerns per sport

---

## 🔌 API Integration

The frontend communicates with the backend via:

http://localhost:8000/teams
http://localhost:8000/predict


CORS is enabled on the backend for local development.

---

## ▶️ Running the Frontend

### 1. Install Dependencies
```bash

npm install
npm start
http://localhost:3000

```

## Technologies Used

* React
* React Router
* Fetch API
* CSS Flexbox & Grid
* REST APIs
