# HemoScan

A machine learning-based application for anemia detection and blood hemoglobin analysis.

## Project Overview

HemoScan is a Python-based project that uses machine learning to detect anemia and analyze hemoglobin levels from medical data. The project includes model training, data preprocessing, visualization, and PDF report generation capabilities.

## Features

- **Machine Learning Model**: Pre-trained anemia detection model using scikit-learn
- **Data Preprocessing**: Comprehensive data cleaning and preparation pipeline
- **Data Scaling**: Standardized data scaling with pre-fitted scaler
- **Visualization**: Data visualization and analysis tools
- **PDF Reports**: Automatic generation of analysis reports
- **Unit Conversion**: Support for different measurement units

## Project Structure

```
HemoScan/
├── index.py                    # Main application entry point
├── train_model.py             # Model training script
├── preprocessing_dataset.py   # Data preprocessing pipeline
├── scale_data.py              # Data scaling utilities
├── unit_converter.py          # Unit conversion utilities
├── visuals.py                 # Visualization tools
├── pdf_genarator.py           # PDF report generation
├── anemia_model.pkl           # Pre-trained anemia detection model
├── scaler.pkl                 # Pre-fitted data scaler
├── requirements.txt           # Project dependencies
├── dataset/                   # Dataset directory
└── reports/                   # Generated reports directory
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Abdul-Nasif/HemoScan.git
cd HemoScan
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main application:
```bash
python index.py
```

## Files Description

- **index.py**: Main application interface and user interaction
- **train_model.py**: Trains the anemia detection model
- **preprocessing_dataset.py**: Handles data cleaning and preprocessing
- **scale_data.py**: Scales and normalizes input data
- **unit_converter.py**: Converts between different measurement units
- **visuals.py**: Creates visualizations and charts
- **pdf_genarator.py**: Generates PDF reports with analysis results
- **anemia_model.pkl**: Serialized trained machine learning model
- **scaler.pkl**: Serialized fitted scaler for data normalization

## Requirements

See `requirements.txt` for all dependencies.

## License

This project is open source and available on GitHub.

## Author

Abdul-Nasif