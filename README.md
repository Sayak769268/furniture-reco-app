# 🪑 Furniture Recommendation Web App

A **full-stack, ML-powered web application** that helps users discover furniture products through **semantic search**, **intelligent recommendations**, and **interactive analytics**.  
Built with **FastAPI**, **React**, and **Hugging Face**, this project demonstrates end-to-end integration of NLP, embeddings, and responsive UI design.

---

## 🚀 Features

### 🔍 Semantic Search
- Natural-language queries matched to product embeddings  
- Fast, accurate retrieval using **Pinecone vector database**  
- Metadata-enhanced filtering for higher relevance  

### 🧠 ML Recommendations
- **Cosine similarity-based** product suggestions  
- **Color-coded match scores** with intuitive indicators  
- AI-generated product descriptions powered by `flan-t5-small`  

### 💬 Chat Interface
- Real-time AI chat with typing indicators  
- Contextual memory for seamless conversation  
- Reset and clear chat functionality  

### 🖼️ Product Cards
- High-quality product visuals  
- **Match score colors:**
  - 🟢 70%+ (High Match)
  - 🟡 40–69% (Moderate Match)
  - 🔴 <40% (Low Match)
- Hover animations and responsive grid layout  
- Brand, price, material, and category metadata  

### 📊 Analytics Dashboard
- Key product metrics and insights  
- Interactive visualizations using **Matplotlib + Pandas**  
- Raw data transparency and summaries  
- Clean, professional UI  

### 📱 Responsive Design
- **Desktop:** Multi-column grid  
- **Tablet:** Adaptive sizing and spacing  
- **Mobile:** Touch-friendly stacked layout  
- Cross-browser compatible with modern CSS fallbacks  

---

## 🧰 Tech Stack

### Frontend
- React + Vite  
- TailwindCSS  
- Axios  

### Backend
- FastAPI  
- LangChain + Hugging Face Transformers  
- Pinecone (Vector Database)  
- Pandas + Matplotlib  

### ML / NLP
- Sentence Transformers (`all-MiniLM-L6-v2`)  
- Text Generation with `flan-t5-small`  

---

## 📁 Folder Structure

```bash
FURNITURE-RECO-APP/
├── .venv/
├── backend/
│   ├── app/
│   │   ├── __pycache__/
│   │   ├── data/
│   │   ├── .env
│   │   ├── analytics.py
│   │   ├── data_preview.py
│   │   ├── embed_and_index.py
│   │   ├── furniture-reco-app.lnk
│   │   ├── generate_description.py
│   │   ├── main.py
│   │   ├── recommend.py
│   │   └── search.py
│   └── requirements.txt
├── furniture-frontend/
│   ├── .vite/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── config.js
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   └── vite.config.js
├── .gitignore
├── .python-version
├── Data_Analytics.ipynb
├── package-lock.json
├── Procfile
└── README.md


```
## 🐍 Backend Setup

**🔧 Step 1: Create a virtual environment**
```bash
python -m venv .venv
```

**💡 Activate the environment**
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

**📦 Step 2: Install dependencies**
```bash
pip install -r backend/requirements.txt
```

**🚀 Step 3: Run the FastAPI server**
```bash
python -m uvicorn app.main:app --reload --port 8000
```

**📜 Step 4: Open the API documentation**
```
http://localhost:8000/docs
```

## 💻 Frontend Setup

**Step 1: Navigate to the frontend folder**
```bash
cd furniture-frontend
```

**Step 2: Install dependencies**
```bash
npm install
```

**Step 3: Start the development server**
```bash
npm run dev
```

**Step 4: Open the app in your browser**
```
http://localhost:5173
```

---

## 📡 API Endpoints

| Method | Endpoint                 | Description                             |
|--------|--------------------------|-----------------------------------------|
| POST   | `/search/query`          | Perform semantic search for products    |
| POST   | `/recommend/chat`        | Get ML-powered product recommendations  |
| GET    | `/analytics/overview`    | Retrieve product analytics summary      |
| POST   | `/generate/description`  | Generate AI-based product descriptions  |

---

## 📊 Example Analytics

- Top product categories and brand insights  
- Price distribution and material analysis  
- Embedding similarity heatmaps  
- Explore more in `Data_Analytics.ipynb`

---

## 🧠 Future Enhancements

- Add user authentication & personalized recommendations  
- Integrate real-time product inventory APIs  
- Improve recommendation feedback loops  
- Containerized deployment (Docker + CI/CD pipeline)

---

## 🪪 License

This project is open-source under the **MIT License**.

---

## 🌟 Made with ❤️ by Sayak Mukherjee


