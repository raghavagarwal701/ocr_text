import time
from image_reader import initilize_reader
import openai
import json
import boto3
from config import AWS_REGION
import json
import time
from trp import Document



def read_text_from_image(image):
    reader = initilize_reader()
    result = reader.readtext(image)
    return result

def call_openai_api(command):

    prompt = f"""Given a mobile app command, classify it into one of these action types: tap, text, validate, swipe, or other.
                        Further extract the details of the command and return it as a json object.
                        The json object should have the following fields:
                        - action_type: The action type of the command
                        - element: The UI element of the command, just UI element name or metadata, not the full description. Suct as icon or text field.\
                            eg: command: Tap on "Explore Used Car" icon. element: "Explore Used Car"
                        Command: "{command}". The output should be a json object:"""

    response = openai.chat.completions.create(
        model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                max_tokens=1000,
    )


    prediction = json.loads(response.choices[0].message.content.strip())
    return prediction


def match(action_object, image_text):
    action_object = action_object.upper()
    action_object = action_object.split(' ')
    matching_elements = []
    for item in image_text:
        bbox, text, confidence = item
        text = text.upper()
        text = text.split(' ')
        if confidence > 0.5:
            count = 0
            for word in action_object:
                if word in text:
                    count += 1
            if count > 0:
                formatted_bbox = [[int(point[0]), int(point[1])] for point in bbox]
                x_coords = [point[0] for point in bbox]
                y_coords = [point[1] for point in bbox]
                center = [
                    int(sum(x_coords) / len(x_coords)),  # Average x-coordinate
                    int(sum(y_coords) / len(y_coords))   # Average y-coordinate
                ]
                new = {
                    "matching_words": count,
                    "image_txt": text,
                    "bbox": formatted_bbox,
                    "confidence": confidence,
                    "center": center
                }
                matching_elements.append(new)
    matching_elements = sorted(matching_elements, key=lambda x: x["matching_words"], reverse=True)
    if len(matching_elements) == 1 and matching_elements[0]['matching_words'] == len(action_object):
        return True, matching_elements[0]['center'], matching_elements[0]['bbox']
    elif len(matching_elements) > 1 and matching_elements[0]['matchig_words'] == len(action_object) and matching_elements[1]['matching_words'] != matching_elements[0]['matching_words']:
        return True, matching_elements[0]['bbox']
    else:
        return False, None, None
    
    
def tap_ocr(action_object, image_before_action):
    start = time.time()
    image_text = read_text_from_image(image_before_action)
    does_match, center, bbox = match(action_object,image_text)
    end = time.time()
    if does_match:
        box = []
        box.append(bbox[1])
        box.append(bbox[3])
        return box, end-start
    return None, end-start


def tap_ocr_without_classifier(user_action, image_before_action):
    print("OCR starts here")
    print("calling llm to get the object form the command")
    start = time.time()
    action_object =  call_openai_api(user_action)
    end = time.time()
    print("time taken by llm for getting the object from the command", end-start)
    return tap_ocr(action_object['element'], image_before_action)

# read_text_from_image("/home/ec2-user/s_enricher_output/executionScreens/com.rapido.passenger/1_0_before_tap_OlBOY.png")
    



documentName = "1.png"

# Amazon Textract client
textract = boto3.client('textract',
                      region_name=AWS_REGION)



        
        
        
        
def match_aws(action_object, response):
    action_object = action_object.upper().replace(" ", "")
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
    
    for item in layout_text_dict:
        bbox, text = item['bbox'], item['text']
        text = text.replace(" ", "").upper()
        if action_object == text:
            box = [[bbox[0]['X'], bbox[0]['Y']], [bbox[2]['X'], bbox[2]['Y']]]
            return box
    for item in ocr_word_dict:
        bbox, text = item['bbox'], item['text']
        text = text.replace(" ", "").upper()
        if action_object == text:
            box = [[bbox[0]['X'], bbox[0]['Y']], [bbox[2]['X'], bbox[2]['Y']]]
            return box
        
    return None
    
    
            
            
def ocr_by_amazon(action_object, image_before_action):
    with open(image_before_action, "rb") as document:
        start = time.time()
        response = textract.analyze_document(
            Document={
                'Bytes': document.read(),
            },
            FeatureTypes=["LAYOUT"])
        end = time.time()
        print(f"Time taken By amazon ocr call: {end-start}")
    box = match_aws(action_object,response)
    end = time.time()
    return box, end-start


# print(ocr_by_amazon("vehicle search", "1.png"))
