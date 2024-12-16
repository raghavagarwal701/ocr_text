import time
from .image_reader import initilize_reader


def read_text_from_image(image):
    reader = initilize_reader()
    result = reader.readtext(image)
    print(result)
    return result


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
                new = {
                    "matching_words": count,
                    "image_txt": text,
                    "bbox": bbox,
                    "confidence": confidence
                }
                matching_elements.append(new)
    matching_elements = sorted(matching_elements, key=lambda x: x["matching_words"], reverse=True)
    if len(matching_elements) == 1 and matching_elements[0]['matching_words'] == len(action_object):
        return True, matching_elements[0]['bbox']
    elif len(matching_elements) > 1 and matching_elements[0]['matchig_words'] == len(action_object) and matching_elements[1]['matching_words'] != matching_elements[0]['matching_words']:
        return True, matching_elements[0]['bbox']
    else:
        return False, None
    
    
def tap_ocr(action_object, image_before_action):
    start = time.time()
    image_text = read_text_from_image(image_before_action)
    does_match, bbox = match(action_object,image_text)
    end = time.time()
    return does_match, bbox, end-start
    

