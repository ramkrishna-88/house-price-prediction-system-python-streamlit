### 🎤 House Price Prediction System

A Machine Learning-based web application that predicts house prices using property features like 

- area
- number of bathrooms
- balconies
 
The project uses a Random Forest Regressor model and provides an interactive dashboard built with Streamlit.


---
## Table of Contents
- <a href="#Project Overview">Project Overview</a>
- <a href="#Features">Features</a>
- <a href="#Technologies Used">Technologies Used</a>
- <a href="#Machine Learning Model">Machine Learning Model</a>
- <a href="#Project Structure">Project Structure</a>
- <a href="#WorkFlow">WorkFlow</a>
- <a href="#How to Run">How to Run</a>
- <a href="#Future Improvements">Future Improvements</a>
- <a href="#Author">Author</a>

---
<h2><a class="anchor" id="Project Overview"></a>Project Overview</h2>

This project aims to estimate real estate prices based on user inputs and provide additional insights such as:

- Price trends
- AI-based property advice
- Future price predictions
-  Auto-generated floor plans
- Location & amenities analysis

---
<h2><a class="anchor" id="Features"></a>Features</h2>

- Price Prediction
  - Predicts house price in Lakhs 
  - Calculates price per square foot

- Price Analysis
  - Graph showing price vs area
  - Low, predicted, and high estimates

- AI Property Advisor
  - Gives smart buying suggestions
  - Provides negotiation tips
  - Suggests ideal buyers

- Floor Plan Generator
  - Generates a schematic layout based on inputs

- Future Price Prediction
  - Predicts price growth over 10 years
  - Adjustable growth rate

- Location Intelligence
  - City-based price adjustment
  - Nearby amenities:
    - Schools
    - Hospitals
    - Metro
    - Malls
    - Parks
  
---
<h2><a class="anchor" id="Technologies Used"></a>Technologies Used</h2>

- Python
- Pandas & NumPy
- Scikit-learn (Random Forest Regressor)
- Streamlit (Web App Framework)
- Plotly (Data Visualization)
- Pickle (Model Serialization)

---
<h2><a class="anchor" id="Machine Learning Model"></a>Machine Learning Model</h2>

- Algorithm: Random Forest Regressor
- Features Used:
  - Area (sq ft)
  - Number of Bathrooms
  - Number of Balconies
- Target:
  -  House Price (in Lakhs)  

--- 
<h2><a class="anchor" id="Project Structure"></a>Project Structure</h2>

📁 House-Price-Predictor
│── train.py              
│── model.pkl             
│── app.py                
│── README.md 

--- 
<h2><a class="anchor" id="WorkFlow"></a>WorkFlow</h2>

- Data Preparation
  - Sample housing data is created manually
  - Converted into a Pandas DataFrame

- Model Training
  - Features (X): area, bath, balcony
  - Target (y): price
  - Model: Random Forest Regressor trained on dataset

- Model Saving
  - Model is saved using Pickle

- Web Application
  - Streamlit loads the trained model
  - User inputs property details
  - Model predicts price instantly

---

--- 
<h2><a class="anchor" id="How to Run"></a>How to Run</h2>

- Install Dependencies
   pip install pandas numpy scikit-learn streamlit plotly

- Train the Model
   python train.py

- Run the App
   streamlit run app.py


--- 
<h2><a class="anchor" id="Future Improvements"></a>Future Improvements</h2>

- Add real-world dataset
- Include more features (location, BHK, age of property)
- Use advanced models (XGBoost, Neural Networks)
- Deploy on cloud (AWS / Render / Hugging Face)

----
## Author

Ram Krishna
- Email: ramkrishna000888@gmail.com
- Linkeddin: https://www.linkedin.com/in/ramkrishna000/

