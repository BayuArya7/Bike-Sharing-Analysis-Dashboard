# Bike Sharing Analysis Dashboard 🚴‍♂️📊

## Overview

This project is an interactive dashboard built with **Streamlit** for analyzing bike sharing data. The dashboard provides insights into daily and hourly rental patterns, and explores the impact of weather conditions on bike rentals.

The dataset includes information such as total rentals, temperature, humidity, weather conditions, and user types (casual and registered). Users can interact with the dashboard by filtering data based on season and weather, as well as exploring trends at different hours of the day.

## Project Setup

### Option 1: Setup with Anaconda

1. Create a new environment:
   ```bash
   conda create --name bike-sharing python=3.12
   ```
2. Activate the environment:
   ```bash
   conda activate bike-sharing
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Setup with Pipenv (Terminal)

1. Create a project directory and navigate into it:
   ```bash
   mkdir proyek_analisis_data
   cd proyek_analisis_data
   ```
2. Install dependencies using Pipenv:
   ```bash
   pipenv install
   pipenv shell
   ```
3. Install additional dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Dashboard

To run the dashboard locally, make sure you're in your project directory and that all dependencies are installed. Then, use the following command:

```bash
streamlit run dashboard.py
```
