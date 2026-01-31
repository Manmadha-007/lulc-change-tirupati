# Tirupati LULC Change Detection (2018-2023)

A web-based geospatial decision support system to analyze, visualize, and quantify Land Use Land Cover (LULC) changes in the Tirupati region.

---

## 2. Problem Statement

### Background
Tirupati is experiencing rapid urbanization and land-use shifts due to its growing significance as a pilgrimage and educational hub. Unplanned expansion often comes at the cost of agricultural land, water bodies, and green cover, threatening long-term environmental sustainability.

### The Gap
Existing monitoring approaches often rely on static reports or expensive commercial software. There is a lack of accessible, interactive tools that allow stakeholders (planners, researchers, citizens) to verify changes at a granular level and understand the "confidence" behind those detections.

### Our Solution
This project provides an automated, open-source pipeline and interactive dashboard to:
*   Map LULC classes for 2018 and 2023 using satellite imagery.
*   Detect and quantify transitions (e.g., Agriculture to Built-up).
*   Provide confidence metrics for every pixel to ensure reliability.

---

## 3. Project Objectives

*   **Automated Classification**: Develop a Machine Learning pipeline to classify LULC features from Landsat imagery.
*   **Change Quantification**: Calculate the exact area (sq. km) of visual transitions between 2018 and 2023.
*   **Confidence Estimation**: Provide a "Transition Probability" score to help users identify likely vs. uncertain changes.
*   **Interactive Visualization**: Build a responsive web dashboard for exploring maps, statistics, and pixel-level details.

---

## 4. Solution Overview

The system operates as an end-to-end pipeline:
1.  **Input**: Raw Landsat 8/9 satellite imagery (2018 & 2023).
2.  **Processing**: Python-based pipeline performs cloud masking, feature extraction (bands + indices), and Random Forest classification.
3.  **Analysis**: Post-processing scripts generate change maps and transition matrices.
4.  **Delivery**: A FastAPI backend serves tiles and stats to a React-based frontend, allowing users to explore the data interactively.

---

## 5. System Architecture

### 1. Data Ingestion
*   Raw GeoTIFFs from USGS Earth Explorer (Landsat).
*   District boundary shapefiles.

### 2. Preprocessing
*   Cloud masking using QA bands.
*   Mosaicking multiple scenes (Row/Path: 142/51 & 143/51).
*   Clipping to Tirupati Area of Interest (AOI).

### 3. AI/ML Layer
*   **Model**: Random Forest Classifier.
*   **Features**: Blue, Green, Red, NIR, NDVI.
*   **Training**: Ground truth points labeled for 5 classes (Water, Forest, Agriculture, Barren, Built-up).

### 4. Analytics
*   Pixel-wise change detection.
*   Area aggregation (sq. km).
*   Confidence/Probability calculation.

### 5. Visualization
*   **Frontend**: React + Leaflet for map rendering.
*   **Backend**: FastAPI for serving XYZ tiles and JSON statistics.

---

## 6. Technologies Used

### 6.1 Programming Languages
*   **Python 3.8+**: Core processing and backend.
*   **JavaScript (ES6+)**: Frontend application.

### 6.2 Remote Sensing & Geospatial Tools
*   **Rasterio**: Reading/writing GeoTIFFs, windowed reading for memory efficiency.
*   **Pyproj**: Coordinate Reference System (CRS) transformations.
*   **GDAL**: (Underlying dependency for Rasterio).

### 6.3 Machine Learning & Analytics
*   **Scikit-learn**: Random Forest implementation.
*   **NumPy**: High-performance array operations.
*   **Pandas**: Handling tabular data and transition matrices.

### 6.4 Visualization / Frontend
*   **React**: UI Framework.
*   **Vite**: Build tool.
*   **Leaflet (React-Leaflet)**: Interactive maps.
*   **Recharts**: Statistical charts.
*   **Tailwind CSS**: Styling.

---

## 7. Dataset Description

*   **Area of Interest (AOI)**: Tirupati Region (buffered district boundary).
*   **Source**: Landsat 8 OLI / Landsat 9 OLI-2.
*   **Time Periods**:
    *   **2018**: Pre-monsoon / Early season.
    *   **2023**: Comparable seasonal timestamp to minimize phenological errors.
*   **Resolution**: 30 meters per pixel.

---

## 8. Data Preprocessing

1.  **Cloud Masking**: Pixels flagged as cloud/shadow in the QA_PIXEL band are masked out to prevent misclassification.
2.  **Mosaicking**: Adjacent Landsat scenes are stitched together.
3.  **Clipping**: Using the vector boundary of Tirupati to reduce processing extent.
4.  **Resampling**: Ensuring 2018 and 2023 pixels align perfectly on the same grid.

---

## 9. Feature Engineering

For every pixel, the following feature vector is constructed:
1.  **Blue Band**
2.  **Green Band**
3.  **Red Band**
4.  **NIR (Near Infrared) Band**
5.  **NDVI**: Normalized Difference Vegetation Index calculated as `(NIR - Red) / (NIR + Red)`.

---

## 10. LULC Classification Methodology

*   **Algorithm**: Supervised Random Forest Classifier.
*   **Classes**:
    1.  **Forest**
    2.  **Water**
    3.  **Agriculture**
    4.  **Barren Land**
    5.  **Built-up Area**
*   **Training**: The model is trained on labeled samples from 2018 and validated against a hold-out set.
*   **Inference**: The trained model predicts the class and confidence score for every pixel in both 2018 and 2023 images.

---

## 11. Change Detection Logic

*   **Pixel-Level Comparison**: The 2018 LULC map is compared to the 2023 LULC map pixel by pixel.
*   **Encoding**: Transitions are encoded as `Code = (Class_2018 * 10) + Class_2023`.
    *   *Example*: 35 indicates Agriculture (3) -> Built-up (5).
*   **No-Change Handling**: Pixels where `Class_2018 == Class_2023` are marked as stable.

---

## 12. Confidence & Probability Estimation

*   **Classification Confidence**: The Random Forest model outputs probability estimates for each class. The maximum probability is taken as the pixel's confidence.
    *   `Conf_2018 = max(P_class_i)`
    *   `Conf_2023 = max(P_class_j)`
*   **Transition Probability**: Reliability of the detected change.
    *   `P_Change = Conf_2018 * Conf_2023`
    *   Low values indicate that one or both classifications were uncertain, suggesting potential false positives.

---

## 13. Transition Analytics

*   **Matrix Construction**: A square matrix representing exact area transfers between classes.
*   **Key Indicators**:
    *   **Net Gain/Loss**: Total area change for each class.
    *   **Urban Expansion**: Specifically tracking non-built-up classes converting to Built-up.

---

## 14. Outputs & Results

### Raster Outputs (GeoTIFF)
*   `lulc_2018.tif` / `lulc_2023.tif`: Classified maps.
*   `change_map.tif`: Coded transitions.
*   `transition_probability.tif`: Confidence map for changes.

### JSON Stats
*   `summary_stats.json`: Class distribution stats.
*   `transition_matrix.json`: Detailed change flows.

---

## 15. Visualization & Dashboard

*   **Layer Controls**: Toggle between LULC 2018, LULC 2023, and Change Map.
*   **Opacity Filter**: Adjust layer transparency overlay.
*   **Pixel Inspector**: Click anywhere on the map to see the exact class, coordinates, and model confidence for both years.
*   **Charts**: Interactive pie charts and bar graphs updating based on the data.

---

## 16. Project Structure

```
├── backend/                # FastAPI application
│   ├── api/                # API Endpoints (tiles, stats, pixel)
│   ├── main.py             # App entry point
├── frontend/               # React application
│   ├── src/                # Components and pages
├── data/
│   ├── processed/          # Final TIFs and Stats
│   ├── raw/                # Original Landsat data
├── pipeline/               # Python processing scripts
│   ├── train_lulc_rf.py    # Model training
│   ├── infer_lulc.py       # Classification
│   ├── compute_*.py        # Change detection & stats
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

---

## 17. Local Setup Instructions

### 17.1 Prerequisites
*   **Python 3.8+**
*   **Node.js & npm**
*   **GDAL** (Recommended for Rasterio, though binary wheels often suffice).

### 17.2 Installation

1.  **Clone the Repository**:
    ```bash
    git clone <repo-url>
    cd lulc-change-tirupati
    ```

2.  **Backend Setup**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    
    pip install -r requirements.txt
    ```

3.  **Frontend Setup**:
    ```bash
    cd frontend
    npm install
    ```

### 17.3 Running the Pipeline (Optional)
If you want to re-process the data:
```bash
# Example: Train model
python pipeline/train_lulc_rf.py

# Example: Run Inference
python pipeline/infer_lulc.py
```

### 17.4 Running the Application
**Backend**:
```bash
# From root directory
uvicorn backend.main:app --reload
```
Runs at `http://127.0.0.1:8000`.

**Frontend**:
```bash
# From frontend directory
npm run dev
```
Runs at `http://localhost:5173`.
