import json

file_path = "templates/executiveSummaryReference.json"

with open(file_path, "r") as fp:
    data = json.load(fp)

key_mapping = {
    "Alcohol": "habits-alcoholIntake",
    "Smoking": "habits-smoking",
    "Weight": "bodyMassIndex",
    "Blood Pressure": "systolicBloodPressure",
    "Diabetes": "glucose",
    "Lipids": "totalCholesterol"
}

template_info = [[k, " ".join(data[v]["recommendations"])] for k, v in key_mapping.items()]
