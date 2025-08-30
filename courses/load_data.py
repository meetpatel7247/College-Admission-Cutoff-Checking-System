import csv
from django.core.files import File
from courses.models import College, Course

def load_college_data():
    with open('courses/colleges.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            college, created = College.objects.get_or_create(
                name=row['Name'],
                website=row['Website']
            )
            Course.objects.get_or_create(
                college=college,
                name=row['Course'],
                stream=row['Stream'],
                min_percentage=row['Min_Percentage'],
                description=row['Description']
            )

if __name__ == "__main__":
    load_college_data()