import json
from os.path import join
from random import choices, randint
from typing import Any, Dict, List

from jsonschema import validate

from image_operations.process_request_schema import PROCESS_REQUEST_SCHEMA


# for tests & demos, provide a semi-random sampling of work coming from PDP
def mimic_pdp_mq_message(tempdir: str, seen_image_ids: List[int]) -> Dict[str, Any]:
    image_id = _get_image_id(seen_image_ids)
    img_path = join(tempdir, f"image_{image_id}_path.bin")
    with open(img_path, 'w') as f:
        json.dump([0, 0, 0, 0, 0], f)

    telem_path = join(tempdir, f"image_{image_id}_telemetry.json")
    with open(telem_path, 'w') as f:
        json.dump({}, f)

    # uncomment if we need the path instead of the object
    # model_path = join(tempdir, f"sc_{sc_id}_model.json")
    # with open(model_path, 'w') as f:
    #     json.dump({}, f)
    #
    # mission_plan = _spoof_mission_plan(image_id, seen_image_ids)
    # mp_path = join(tempdir, f"task_{mission_plan['task_id']}.json")
    # with open(mp_path, 'w') as f:
    #     json.dump(mission_plan, f)

    message = {
        'image_path': img_path,
        'telemetry_path': telem_path,
        'sat_model': {},
        'mission_plan': _spoof_mission_plan(image_id, seen_image_ids),
    }
    validate(message, schema=PROCESS_REQUEST_SCHEMA)
    return message


def _spoof_mission_plan(image_id: int, seen_image_ids: List[int]) -> Dict[str, Any]:
    random_task_id = randint(1, 100000)
    plan = {
        'request_id': 1,
        'task_id': random_task_id,
        'image_id': image_id,
        'priority': 13,
        'task': {}
    }
    if randint(1, 100) <= 20:  # make 80% of requests single_image
        plan['other_image_ids_in_image_plan'] = choices(seen_image_ids, k=2)
        multi_type = choices(['stereo', 'area', 'video'])[0]
        plan['task']['product_options'] = {
            'is_stereo_product': multi_type == 'stereo',
            'is_stitched_product': multi_type == 'area',
            'is_video_product': multi_type == 'video',
        }
    return plan


def _get_image_id(seen_image_ids: List[int]):
    random_image_id = 0
    while random_image_id in seen_image_ids:
        random_image_id = randint(1, 100000)
    seen_image_ids.append(random_image_id)
    return random_image_id
