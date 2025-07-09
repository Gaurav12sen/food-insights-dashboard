# 🍽️ OpenFoodFacts India Dashboard

A comprehensive Streamlit dashboard that analyzes food products data from India using the OpenFoodFacts API. The dashboard provides insights into nutritional content, brands, categories, and additives across the Indian food market.

## 🌐 Live Demo

Check out the live dashboard: [Food Insights Dashboard](https://food-insider.streamlit.app/)

## 🌟 Features

- **Live Data**: Fetches real-time data from OpenFoodFacts API
- **Comprehensive Analysis**: Nutrient profiles, brand analysis, category insights
- **Interactive Visualizations**: Dynamic charts and filters
- **Data Quality Metrics**: Track completeness and reliability
- **Export Capability**: Download filtered data as CSV

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/food-insights-dashboard.git
cd food-insights-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the dashboard:
```bash
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

## 📊 Dashboard Sections

1. **Summary Metrics**
   - Total products
   - Unique brands
   - Average nutrient score
   - Data completeness

2. **Brand Analysis**
   - Top brands by product count
   - Brand distribution

3. **Nutrient Analysis**
   - Distribution of key nutrients
   - Category-wise nutrient profiles
   - Nutrient score analysis

4. **Category Insights**
   - Product distribution across categories
   - Category-level nutrient analysis

5. **Additives & Quality**
   - Common additives analysis
   - Data quality metrics
   - Missing value analysis

## 🔄 Data Refresh

- Data is automatically refreshed daily
- Manual refresh available through the UI
- Cached data used when available

## 🛠️ Project Structure

```
food-insights-dashboard/
├── data/                    # Data storage
├── src/                    # Source code
│   ├── config.py          # Configuration settings
│   ├── data_fetch.py      # API interaction
│   ├── etl.py            # Data processing
│   ├── analysis.py       # Data analysis
│   └── visuals.py        # Visualization functions
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
└── README.md             # Documentation
```

## 🚀 Deployment

The dashboard is deployed using [Streamlit Cloud](https://streamlit.io/cloud). You can:
- Access the live demo at [https://food-insider.streamlit.app/](https://food-insider.streamlit.app/)
- Deploy your own instance by following [Streamlit's deployment guide](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)

## 📝 Notes

- The OpenFoodFacts API is free and requires no authentication
- Data quality may vary as it's community-contributed
- Some products may have missing information

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenFoodFacts](https://world.openfoodfacts.org/) for providing the API
- [Streamlit](https://streamlit.io/) for the amazing dashboard framework
- [Plotly](https://plotly.com/) for interactive visualizations 