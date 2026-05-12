# AI Resume Analyzer & ATS Optimizer

A professional, Streamlit-based web application designed to analyze resumes, extract key technical skills, and evaluate ATS compatibility against job descriptions. This tool provides actionable feedback and personalized recommendations to help job seekers optimize their profiles.

## 🚀 Features

- **ATS Compatibility Scoring:** Uses TF-IDF and Cosine Similarity to calculate a match percentage between your resume and the job description.
- **Skill Gap Analysis:** Automatically identifies technical skills present in your resume and highlights missing ones required for the role.
- **AI-Powered Recommendations:** Generates personalized suggestions for improving your resume based on detected gaps.
- **Interactive Dashboard:** A modern, premium UI with real-time visualizations and a responsive layout.
- **PDF Extraction:** Seamlessly extracts text from PDF resumes for analysis.

## 📂 Project Structure

- `app.py`: The main entry point for the Streamlit dashboard and UI logic.
- `preprocessing.py`: Handles text cleaning, tokenization, and skill extraction.
- `similarity.py`: Contains the logic for vectorization and similarity calculations.
- `recommender.py`: Provides the recommendation engine for skill improvement.
- `resume_parser.py`: Utility for extracting text from PDF files.
- `requirements.txt`: List of Python dependencies.

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aasthaojha-ai/TalentSynapse_AI
   cd TalentSynapse_AI
   ```

2. **Set up a virtual environment (optional):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## 📊 Deployment on Streamlit Cloud

To deploy this app on Streamlit Cloud:
1. Push this code to a new GitHub repository.
2. Connect your GitHub account to [Streamlit Cloud](https://share.streamlit.io/).
3. Select your repository and the `app.py` file as the main entry point.
4. The app will automatically handle NLTK data downloads on the first run.

## 🛡️ License

This project is open-source and available under the [MIT License](LICENSE).
