import csv
import pymysql
pymysql.install_as_MySQLdb()

# Database connection settings
mydb = pymysql.connect(
    host="localhost", user="tahir", password="Password123#@!", database="logistic"
)

# To access column names in csv file
import pandas as pd
d = pd.read_csv("0_data/SCMS_Delivery_History_Dataset.csv")
print(d.columns)


# Read the data row by row
with open("0_data/SCMS_Delivery_History_Dataset.csv") as csv_file:
    csvfile = csv.reader(csv_file, delimiter=",")
    # to skip columns when reading file row by row
    next(csvfile)
    each_row_values = []
    for row in csvfile:
        value = (
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
            row[8],
            row[9],
            row[10],
            row[11],
            row[12],
            row[13],
            row[14],
            row[15],
            row[16],
            row[17],
            row[18],
            row[19],
            row[20],
            row[21],
            row[22],
            row[23],
            row[24],
            row[25],
            row[26],
            row[27],
            row[28],
            row[29],
            row[30],
            row[31],
            row[32],
        )
        each_row_values.append(value)


# Create table into database
create_table = """
    CREATE TABLE IF NOT EXISTS `Delivery_History` (
        ID VARCHAR(100),
        Project_Code VARCHAR( 100),
        PQ VARCHAR(100),
        PO_SO VARCHAR(100),
        ASN_DN VARCHAR(100),
        Country VARCHAR(100),
        Managed_By VARCHAR(100),
        Fulfill_Via VARCHAR(100),
        Vendor_INCO_Term VARCHAR(100),
        Shipment_Mode VARCHAR(100),
        PQ_First_Sent_to_Client_Date VARCHAR(100),
        PO_Sent_to_Vendor_Date VARCHAR(100),
        Scheduled_Delivery_Date VARCHAR(100),
        Delivered_to_Client_Date VARCHAR(100),
        Delivery_Recorded_Date VARCHAR(100),
        Product_Group VARCHAR(100),
        Sub_Classification VARCHAR(100),
        Vendor VARCHAR(100),
        Item_Description VARCHAR(500),
        Molecule_Test_Type VARCHAR(100),
        Brand VARCHAR(100),
        Dosage VARCHAR(100),
        Dosage_Form VARCHAR(100),
        Unit_of_Measure_Per_Pack VARCHAR(100),
        Line_Item_Quantity VARCHAR(100),
        Line_Item_Value VARCHAR(100),
        Pack_Price VARCHAR(100),
        Unit_Price VARCHAR(100),
        Manufacturing_Site VARCHAR(100),
        First_Line_Designation VARCHAR(100),
        Weight_Kilograms VARCHAR(100),
        Freight_Cost_USD VARCHAR(100),
        Line_Item_Insurance_USD VARCHAR(100)
    );
"""

# Insert values into created table
query = """
    INSERT INTO `Delivery_History`(
        ID, 
        Project_Code, 
        PQ, 
        PO_SO,
        ASN_DN, 
        Country,
        Managed_By, 
        Fulfill_Via,
        Vendor_INCO_Term,
        Shipment_Mode,
        PQ_First_Sent_to_Client_Date,
        PO_Sent_to_Vendor_Date,
        Scheduled_Delivery_Date, 
        Delivered_to_Client_Date,
        Delivery_Recorded_Date,
        Product_Group,
        Sub_Classification,
        Vendor,
        Item_Description, 
        Molecule_Test_Type,
        Brand,
        Dosage,
        Dosage_Form,
        Unit_of_Measure_Per_Pack,
        Line_Item_Quantity,
        Line_Item_Value,
        Pack_Price,
        Unit_Price, 
        Manufacturing_Site,
        First_Line_Designation,
        Weight_Kilograms, 
        Freight_Cost_USD,
        Line_Item_Insurance_USD   
    ) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

# Execute the query
mycursor = mydb.cursor()
mycursor.execute(create_table)
mycursor.executemany(query, each_row_values)
mydb.commit()
