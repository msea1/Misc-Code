import json
from typing import Any, Dict, List

from attr import attrib, attrs

from blacksky_payload.payload import DioptraPayload
from image_processing.image.image_factory import Image


@attrs(slots=True)
class MockSensor(DioptraPayload):
    # stand-in for the sensor data which we don't yet have a serialization method
    # and also, we just want a simple, autospec-like, object skeleton to demo
    num_cameras = 1
    image: List[int] = attrib()
    sidecar: Dict[str, Any] = attrib()
    calibration_data: Dict[str, Any] = attrib()
    image_id: int = attrib()
    meta_layers: Dict[str, Any] = attrib()

    def __str__(self) -> str:
        return json.dumps({
            'image_id': self.image_id,
            'image_data': self.image,
            'sidecar_data': self.sidecar,
            'calibration_data': self.calibration_data,
            'meta_layers': self.meta_layers,
        })

    @property
    def serialization_name(self):
        return f"{self.image_id:010d}_scid_here"

    @classmethod
    def from_file(cls, read_path: str) -> "MockSensor":
        with open(read_path) as f:
            spec = json.load(f)
        return cls(
            image_id=spec.get('image_id', -1),
            image=spec.get('image_data', [0, 0, 0, 0, 0]),
            sidecar=spec.get('sidecar_data', {'sat_model': {}, 'pic_telem': {}}),
            calibration_data=spec.get('calibration_data', {}),
            meta_layers=spec.get('meta_layers', {})
        )

    def to_file(self, save_path: str) -> None:
        with open(save_path, 'w') as f:
            f.write(str(self))

    def serialize_payload(self, *args) -> None:
        pass

    def crop_to_area_of_interest(self) -> None:
        pass

    def get_pan_image(self) -> Image:
        pass

    def get_rgb_image(self) -> Image:
        pass
