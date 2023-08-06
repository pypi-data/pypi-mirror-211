import re


def get_text_between_entities(sentence, entity_1, entity_2):
    try:
        x1 = re.search(f'{entity_1}\s', sentence)
        x2 = re.search(f'{entity_2}\s', sentence)
    except:
        return None
    with_entities = sentence[x1.start():x2.end()].strip() if x1.start() < x2.start() \
        else sentence[x2.start():x1.end()].strip()
    without_entities = sentence[x1.end():x2.start() - 1].strip() if x1.start() < x2.start() \
        else sentence[x2.end():x1.start() - 1].strip()
    return with_entities, without_entities
