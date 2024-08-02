import requests
from bs4 import BeautifulSoup

# URL of bohr page containing the course descriptions
url = "https://bohr.wlu.ca/courses/courseDescriptions.php#Computing"
output_file = "courses.txt"


# Fetch raw HTML
response = requests.get(url)
webpage_content = response.content

# Parse the HTML
soup = BeautifulSoup(webpage_content, "html.parser")

# Extract the course titles from h3 tags
course_titles = soup.find_all("h3")

# Count the number of unique courses
unique_courses = set([course.get_text() for course in course_titles])


def valid_cp_course(course) -> bool:
    """Just filters out Physics courses, Astronomy courses, and courses without a title"""
    return (
        ":" in course
        and course.split(":")[1].strip() != ""  # Check if the course has a title
        and not course.startswith("PC")  # Check if the course is a Physics course
        and not course.startswith("AS")  # Check if the course is an Astronomy course
    )


courses = []

for course in unique_courses:
    if valid_cp_course(course):
        courses.append(course)

print("Available Computer Science Courses:", len(courses))

with open(output_file, "w") as file:
    for course in courses:
        file.write(course + "\n")
