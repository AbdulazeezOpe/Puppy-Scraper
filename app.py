import streamlit as st
from puppy_scraper_app import run_scraper
import os

st.set_page_config(page_title="Puppies.com Scraper", page_icon="🐶")
st.title("🐾 Puppies.com Breeder Contact Scraper")

st.markdown("""
Enter a **U.S. city** below to fetch breeder phone numbers, city, age, and puppy breed details.

This tool logs in, applies filters (puppies aged 4–8 weeks within 100 miles), and extracts listing info.
""")

city = st.text_input("Enter City Name (e.g., Charlotte, NC)", value="Charlotte, NC")

# These can be hidden or set as env vars in production
email = st.text_input("Login Email", value="paul.kintgen@edu.escp.eu", type="password")
password = st.text_input("Login Password", value="upwork2024", type="password")

if st.button("Start Scraping"):
    if not city.strip():
        st.warning("Please enter a valid city name.")
    else:
        with st.spinner("🔍 Gathering listing links... please wait..."):
            try:
                output_file = run_scraper(city, email, password, report_to=st)
                st.success("🎉 Done scraping!")
                st.download_button(
                    label="📥 Download CSV",
                    data=open(output_file, "rb"),
                    file_name=os.path.basename(output_file),
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Something went wrong: {e}")
