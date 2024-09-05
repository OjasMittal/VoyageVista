import streamlit as st 
import google.generativeai as palm
from ics import Calendar, Event
from datetime import datetime, timedelta
import json
palm.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = palm.GenerativeModel("gemini-1.5-flash")
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
import io
import zipfile
from PIL import Image

img = Image.open('icon.png')
st.set_page_config(page_title="Voyage Vista",page_icon = img)

#Custom CSS
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://res.cloudinary.com/dgfehrdfq/image/upload/v1725541998/7489_uhmyfv.jpg");
    background-size: 100vw 100vh;
    background-position: center;
    background-repeat: no-repeat;
}

.glass-container {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 15px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 20px;
    margin: 20px 0;
}

.glass-text {
    color: #000;
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

hide_menu_style="""
<style>
header{visibility:hidden;}
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
</style>
"""
st.markdown(hide_menu_style,unsafe_allow_html=True)

# Font size
st.markdown(
    """
    <style>
        textarea {
            font-size: 3rem !important;
        }
        input {
            font-size: 1.5rem !important;
        }
        .css-qrbaxs {
            font-size: 1.5rem !important; /* Adjust label font size */
        }
        .css-1d391kg {
            font-size: 1.5rem !important; /* Adjust text input font size */
        }
        .css-1d91f3x {
            font-size: 1.5rem !important; /* Adjust date input font size */
        }
        .css-1xs5jwz {
            font-size: 1.5rem !important; /* Adjust date input font size */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

#Main UI & Backend
#Title
st.markdown("""
    <style>
        .center-title {
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
        }
    </style>
    <div class="center-title">Voyage Vista 🗺️</div>
""", unsafe_allow_html=True)
st.write("")
st.write("")

#User Inputs
place = st.text_input("Enter the place you want to visit:")
col1,col2 =  st.columns(2)
with col1:
  start_date = st.date_input("Select the start date for your trip:", value=datetime.today())
with col2:
  # Setting the maximum end date to 30 days after the start date
  max_end_date = start_date + timedelta(days=30)

  # User selects the end date of the trip
  end_date = st.date_input("Select the end date for your trip:",
                          value=start_date + timedelta(days=1),  # Default to the next day
                          min_value=start_date,
                          max_value=max_end_date)

# Calculate the number of days between start_date and end_date
days = (end_date - start_date).days

# User preferences multiselect
preferences = st.multiselect(
    "Choose your preferences:",
    options=["Art", "Museums", "Outdoor Activities", "Indoor Activities", "Good for Kids", "Good for Young People", "Spiritual", "Relaxing","City Life","Cultural","OFFBEAT Destinations","Tourist Attractions"],
    default=None,
    help="Select the types of activities you are interested in for your itinerary."
)

# Generate itinerary button
if st.button("Generate Itinerary"):
    with st.spinner("Generating Your Itinerary..."):
      # Create a prompt based on user input
      prompt = f"You are a travel expert. Give me an itinerary for {place}, for {days} days, assuming each day starts at 9am and ends at 8pm with a buffer of 30 minutes between each activity. I like to"

      # Add selected preferences to the prompt
      if "Art" in preferences:
          prompt += " explore art,"
      if "Museums" in preferences:
          prompt += " visit museums,"
      if "Outdoor Activities" in preferences:
          prompt += " engage in outdoor activities,"
      if "Indoor Activities" in preferences:
          prompt += " explore indoor activities,"
      if "Good for Kids" in preferences:
          prompt += " find places suitable for kids,"
      if "Good for Young People" in preferences:
          prompt += " discover places suitable for young people,"
      if "Spiritual" in preferences:
          prompt += " visit spiritual sites,"
      if "Relaxing" in preferences:
          prompt += " enjoy relaxing activities,"
      if "City Life" in preferences:
          prompt += " visit city life related places,"
      if "Cultural" in preferences:
          prompt += " discover cultural sites,"
      if "OFFBEAT Destinations" in preferences:
          prompt += " discover off beat destinations that reflect the true generosity of the place"
      if "Tourist Attractions" in preferences:
          prompt += "visit all the major Tourist ATtractions that the place is famous for."
      prompt += """ Limit the length of output JSON string to 1800 characters. Generate a structured JSON representation for the travel itinerary.

        {
    "days": [
      {
        "day": 1,
        "activities": [
          {
            "title": "Activity 1",
            "description": "Description of Activity 1",
            "link": "https://example.com/activity1",
            "start_time": "10:00 AM",
            "end_time": "12:00 PM",
            "location": "https://maps.google.com/?q=location1"
          },
          {
            "title": "Activity 2",
            "description": "Description of Activity 2",
            "link": "https://example.com/activity2",
            "start_time": "02:00 PM",
            "end_time": "04:00 PM",
            "location": "https://maps.google.com/?q=location2"
          },
          ....
        ]
      },
      {
        "day": 2,
        "activities": [
          {
            "title": "Another Activity 1",
            "description": "Description of Another Activity 1",
            "link": "https://example.com/activity1",
            "start_time": "09:30 AM",
            "end_time": "11:30 AM",
            "location": "https://maps.google.com/?q=location1"
          },
          {
            "title": "Another Activity 2",
            "description": "Description of Another Activity 2",
            "link": "https://example.com/activity2",
            "start_time": "01:00 PM",
            "end_time": "03:00 PM",
            "location": "https://maps.google.com/?q=location2"
          },
          ...
        ]
      }
    ]
  }

          Ensure that each day has a 'day' field and a list of 'activities' with 'title', 'description', 'start_time', 'end_time', 'location', 'link' fields. Keep descriptions concise also do not shortened locations URLs using Dynamic Links.
  """
      prompt += """
      Also, include a hotel recommendation for each day with a link to booking.com. Limit the length of output JSON string to 1800 characters. Generate a structured JSON representation for the travel itinerary.

      {
          "days": [
            {
              "day": 1,
              "hotel": {
                "name": "Hotel Name",
                "link": "https://booking.com/"
              },
              "activities": [
                {
                  "title": "Activity 1",
                  "description": "Description of Activity 1",
                  "link": "https://example.com/activity1",
                  "start_time": "10:00 AM",
                  "end_time": "12:00 PM",
                  "location": "https://maps.google.com/?q=location1"
                },
                ...
              ]
            },
            ...
          ]
      }
      Ensure that each day has a 'day' field, 'hotel' field with 'name' and 'link', and a list of 'activities' with 'title', 'description', 'start_time', 'end_time', 'location', 'link' fields. Keep descriptions concise and do not shorten location URLs using Dynamic Links.
      """
      # Generating itinerary using the gemini model
      completion = model.generate_content(prompt)
      itinerary = completion.text.strip()

      # Remove '''json from start and ''' from end
      itinerary = itinerary[7:-3]
      print(itinerary)
      try:
        itinerary_json = json.loads(itinerary)
        container = st.container()
        for day in itinerary_json["days"]:
          #adding glass effect in the containers
            with container:
                st.markdown(f"<div class='glass-container'><h3>Day {day['day']}</h3>", unsafe_allow_html=True)
                if "hotel" in day:
                  hotel_html = f"""
                      <div class='glass-container'>
                          <h4>Hotel:</h4>
                          <p><strong>{day['hotel']['name']}</strong></p>
                          <p><a href='{day['hotel']['link']}' target='_blank'>Book this hotel </a>🏨</p>
                      </div>
                  """
                  st.markdown(hotel_html, unsafe_allow_html=True)
                for activity in day["activities"]:
                    activity_html = f"""
                          <div class='glass-container'>
                              <h4>{activity['title']}</h4>
                              <p><strong>Description: {activity['description']}</strong></p>
                              <p><strong>Location:📍<a href='{activity['location']}'>{activity['location']}</a></strong> </p>
                              <p><strong>Time: {activity['start_time']} - {activity['end_time']}</strong></p>
                              <p><strong>Link:<a href='{activity['link']}'>{activity['link']}</a></strong> </p>
                          </div>
                      """
                    st.markdown(activity_html, unsafe_allow_html=True)

        # Function to generate a download link for the calendar
        def get_download_link(content, filename):
            """Generates a download link for the given content."""
            b64_content = content.encode().decode("utf-8")
            href = f'<a href="data:text/calendar;charset=utf-8,{b64_content}" download="{filename}">Download {filename}</a>'
            return href

        # Export itinerary to a calendar file
        cal = Calendar()
        
        for day, activities in enumerate(itinerary_json.get("days", []), start=1):
            for activity in activities.get("activities", []):
                event = Event()
                event.name = activity.get("title", "")
                event.description = activity.get("description", "")
                event.location = activity.get("location", "")

                # Convert start and end times from 12-hour format to 24-hour format
                start_time = datetime.strptime(activity.get("start_time", "00:00 AM"), "%I:%M %p").time()
                end_time = datetime.strptime(activity.get("end_time", "00:00 AM"), "%I:%M %p").time()

                # Calculate event start and end times based on the start_date
                event_begin_utc = datetime.combine(
                    start_date + timedelta(days=day - 1), start_time
                ) - timedelta(hours=5, minutes=30)  # Subtract 5 hours 30 minutes for UTC

                event_end_utc = datetime.combine(
                    start_date + timedelta(days=day - 1), end_time
                ) - timedelta(hours=5, minutes=30)  # Subtract 5 hours 30 minutes for UTC

                # Set the adjusted UTC times
                event.begin = event_begin_utc
                event.end = event_end_utc

                # Add the event to the calendar
                cal.events.add(event)

        # Create calendar content
        cal_content = str(cal)

        # Generate PDF
        def create_pdf(itinerary_json):
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            for day in itinerary_json["days"]:
                elements.append(Paragraph(f"Day {day['day']}", styles['Heading1']))
                if 'hotel' in day:
                  hotel_name = day['hotel'].get('name', 'No Hotel Information')
                  hotel_link = day['hotel'].get('link', '#')
                  hotel_link_html = f'<a href="{hotel_link}" color="blue">{hotel_name}</a>'
                  elements.append(Paragraph(f"Hotel: {hotel_link_html}", styles['Normal']))
                for activity in day["activities"]:
                  elements.append(Paragraph(activity["title"], styles['Heading2']))
                  elements.append(Paragraph(f"Description: {activity['description']}", styles['Normal']))

                  location_link = f'<a href="{activity["location"]}" color="blue">{activity["location"]}</a>'
                  elements.append(Paragraph(f"Location: {location_link}", styles['Normal']))

                  activity_link = f'<a href="{activity["link"]}" color="blue">{activity["link"]}</a>'
                  elements.append(Paragraph(f"Link: {activity_link}", styles['Normal']))

                  elements.append(Paragraph(f"Time: {activity['start_time']} - {activity['end_time']}", styles['Normal']))
                  elements.append(Paragraph("<br />", styles['Normal']))  # Adding space between activities
            doc.build(elements)
            pdf_buffer.seek(0)
            return pdf_buffer

        pdf_buffer = create_pdf(itinerary_json)

        # Creating a ZIP file containing both ICS and PDF files
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            # Adding ICS file to ZIP
            zip_file.writestr("Itinerary.ics", cal_content)
            # Adding PDF file to ZIP
            zip_file.writestr("Itinerary.pdf", pdf_buffer.getvalue())

        zip_buffer.seek(0)

        # A single download button for the ZIP file
        st.download_button(
            label="Download Itinerary (ZIP) ⬇️",
            data=zip_buffer,
            file_name="Itinerary.zip",
            mime="application/zip"
        )
      # An error might occur while converting to json format.
      except Exception as e:
        st.error("Oops, Something went wrong, please try again in a moment.")
        