import pandas 

DATA_SOURCE = "/home/tahir/Projects/Logistic/0_data/SCMS_Delivery_History_Dataset.csv"

data = pandas.read_csv(DATA_SOURCE)

print(data)