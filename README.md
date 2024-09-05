# **Voyage Vista - Travel Itinerary Generator**

![voyageVista](https://github.com/user-attachments/assets/f4a80a23-5f90-411a-9248-aababb8da4f8)

**Voyage Vista** is a Streamlit-based web application that allows users to generate personalized travel itineraries based on their preferences. This application leverages Google's Generative AI model to create detailed, day-by-day itineraries for a selected destination, including activities, locations, and hotel recommendations. Users can also download the itinerary in both calendar (ICS) and PDF formats.

## **Features**

- **User Input for Customization**: 
  - Enter a destination, trip duration, and select preferences for tailored itineraries.
  - Options include various activity types like outdoor, indoor, cultural, and more.
  
- **Generative AI Integration**:
  - Uses the `google.generativeai` API to create a detailed itinerary with activity descriptions, links, and locations.
  
- **Glassmorphism UI Design**: 
  - A sleek, modern interface using CSS for glass effect containers to enhance user experience.
  
- **Downloadable Itinerary**:
  - Exports the itinerary as both a PDF and ICS (calendar) file.
  - Both files can be downloaded as a single ZIP file.

## **Tech Stack**

- **Front-end**: [Streamlit](https://streamlit.io/)
- **Back-end**: 
  - **Google Generative AI API** (`palm`)
  - **Calendar export**: [ICS](https://pypi.org/project/ics/)
  - **PDF export**: [ReportLab](https://www.reportlab.com/)
- **UI Enhancements**: Custom CSS

## **Dependencies**

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

Here is a list of key packages used:

- `streamlit`: Front-end UI
- `google-generativeai`: Interface with Google's Generative AI for itinerary generation
- `ics`: To create and export calendar (ICS) files
- `reportlab`: To generate a downloadable PDF
- `Pillow`: For image processing and displaying icons
- `io` and `zipfile`: For creating ZIP files

## **Getting Started**

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/voyage-vista.git
cd voyage-vista
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Set up Google Generative AI API**:

   Obtain an API key from the [Google Cloud Console](https://console.cloud.google.com/) and add it to your `streamlit` secrets:

   In your `secrets.toml` file:

   ```toml
   GOOGLE_API_KEY = "your-google-api-key"
   ```

4. **Run the app**:

```bash
streamlit run app.py
```

5. **Access the web application**:

   Open the application in your browser at `http://localhost:8501`.

## **Usage**

1. **Enter Destination and Trip Dates**: 
   Input your destination and select the trip duration.

2. **Select Preferences**: 
   Choose from multiple categories of activities like museums, outdoor activities, and cultural sites.

3. **Generate Itinerary**: 
   Click the "Generate Itinerary" button, and a day-by-day itinerary will be created based on your inputs.

4. **Download Itinerary**: 
   The generated itinerary can be downloaded as a ZIP file containing both the ICS and PDF files.

## **Customizing UI**

The application's look and feel can be customized by modifying the CSS in the `background_image` and `glass-container` sections in the `app.py` file.

```python
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("your-image-url");
    background-size: cover;
    background-position: center;
}
</style>
"""
```

## **Contributing**

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m 'Add your feature'`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request.

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## **Deployed Website**

`https://voyagevista.streamlit.app/`
