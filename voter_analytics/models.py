from django.db import models

# Create your models here.
import csv
from datetime import datetime


import csv
from datetime import datetime


def load_data(file_path="newton_voters.csv"):
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Convert "TRUE"/"FALSE" strings to boolean values
                v20state = row["v20state"].strip().upper() == "TRUE"
                v21town = row["v21town"].strip().upper() == "TRUE"
                v21primary = row["v21primary"].strip().upper() == "TRUE"
                v22general = row["v22general"].strip().upper() == "TRUE"
                v23town = row["v23town"].strip().upper() == "TRUE"

                Voter.objects.create(
                    first_name=row["First Name"],
                    last_name=row["Last Name"],
                    street_number=row["Residential Address - Street Number"],
                    street_name=row["Residential Address - Street Name"],
                    apartment_number=row["Residential Address - Apartment Number"]
                    or None,
                    zip_code=row["Residential Address - Zip Code"],
                    date_of_birth=datetime.strptime(row["Date of Birth"], "%Y-%m-%d"),
                    date_of_registration=datetime.strptime(
                        row["Date of Registration"], "%Y-%m-%d"
                    ),
                    party_affiliation=row["Party Affiliation"].strip(),
                    precinct_number=row["Precinct Number"].strip(),
                    voter_score=int(row["voter_score"]),
                    v20state=v20state,
                    v21town=v21town,
                    v21primary=v21primary,
                    v22general=v22general,
                    v23town=v23town,
                )
            except Exception as e:
                print(f"Error processing row: {row}")
                print(f"Exception: {e}")


class Voter(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=10)  # Changed to CharField
    voter_score = models.IntegerField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.party_affiliation}"
