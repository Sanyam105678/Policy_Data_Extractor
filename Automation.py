import re
import os

# ---------------------------
# Helper function to extract fields using regex
# ---------------------------
def extract(pattern, text, group=1):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(group).strip() if match else None


# ---------------------------
# Function to read & parse a single text file
# ---------------------------
def parse_file(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    data = {}

    # Extracting all fields
    data["FileName"] = os.path.basename(file_path)
    data["PolicyNumber"] = extract(r"Policy Number:\s*([A-Z0-9 /-]+)", text)
    data["GSTIN"] = extract(r"GST Reg No\s*([A-Z0-9]+)", text)
    data["InsuredName"] = extract(r"Name:\s*([A-Z ]+)", text)
    data["PartnerName"] = extract(r"Partner Name:\s*([A-Z ]+)", text)
    data["MobileNumber"] = extract(r"Mobile Number:\s*([x0-9]+)", text)
    data["PartnerMobile"] = extract(r"Partner Mobile Number:\s*([0-9]+)", text)
    data["Email"] = extract(r"Email:\s*([\w.\-@x]+)", text)
    data["PartnerEmail"] = extract(r"Partner Email\s*:\s*([\w.\-@]+)", text)
    data["Address"] = extract(r"Address\s*(.+)", text)
    data["EngineNumber"] = extract(r"Engine No\.?\s*([A-Z0-9]+)", text)
    data["ChassisNumber"] = extract(r"Chassis No\.?\s*'?([A-Z0-9]+)", text)
    data["PrevPolicyNo"] = extract(r"Previous Policy No\.\s*([A-Z0-9]+)", text)

    return data


# ---------------------------
# MAIN LOGIC – LOOP THROUGH ALL TXT FILES
# ---------------------------

folder_path = "media\ocr_logs"   
all_results = []     # to store results of all files

# Iterate over all files in the folder
for file in os.listdir(folder_path):
    if file.endswith(".txt"):
        file_path = os.path.join(folder_path, file)

        print("\n==============================")
        print(f"Processing File: {file}")
        print("==============================")

        result = parse_file(file_path)
        all_results.append(result)

        # Printing field-wise output
        for key, value in result.items():
            print(f"{key}: {value}")

        print("----------------------------------")

# ---------------------------
# Print combined summary
# ---------------------------
print("\n\n===== SUMMARY OF ALL FILES =====")
for r in all_results:
    print("\n---------------------------")
    for k, v in r.items():
        print(f"{k}: {v}")
