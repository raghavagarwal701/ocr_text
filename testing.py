import boto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, BUCKET_NAME
import json
import time
from trp import Document

# Document
documentName = "1.png"

# Amazon Textract client
textract = boto3.client('textract',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_REGION)

# Call Amazon Textract
with open(documentName, "rb") as document:
    start = time.time()
    response = textract.analyze_document(
        Document={
            'Bytes': document.read(),
        },
        FeatureTypes=["LAYOUT"])
    end = time.time()
    print("Time taken: ", end-start)

#print(response)

doc = Document(response)
with open("output.json", "w") as file:
    file.write(json.dumps(response, indent=4))
    
blocks = response.get("Blocks", [])

# Initialize dictionaries
layout_text_dict = []
ocr_word_dict = []
word_dict = {}

for block in blocks:
    if block["BlockType"] == "LINE" and block["Confidence"] > 50:
        word_text = block["Text"]
        bbox = block["Geometry"]["Polygon"]
        id = block["Id"]
        ocr_word_dict.append({"text": word_text, "bbox": bbox})
        word_dict[id] = word_text

for block in blocks:
    if block["BlockType"] == "LAYOUT_TEXT" and block["Confidence"] > 50:
        bbox = block["Geometry"]["Polygon"]
        word_text = ""
        for relation in block["Relationships"]:
            if relation["Type"] == "CHILD":
                for child_id in relation["Ids"]:
                    if child_id in word_dict:
                        word_text += word_dict[child_id]
        layout_text_dict.append({"text": word_text, "bbox": bbox})
        
        
# # Output results

# #save these in a file name dict.json
# with open("dict.json", "w") as file:
#     file.write(json.dumps({"layout_text_dict": layout_text_dict, "ocr_word_dict": ocr_word_dict}, indent=4))
# # print("Layout Text Dictionary:")
# # print(json.dumps(layout_text_dict, indent=4))
# # print("\nWord Dictionary:")
# # print(json.dumps(ocr_word_dict, indent=4))

