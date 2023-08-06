import json
from typing import BinaryIO
from bytez.model import Model


class AllenaiVisprogModel(Model):
    def inference(self, method: str, question: str = None, instruction: str = None, image: BinaryIO = None, left_image: BinaryIO = None, right_image: BinaryIO = None) -> bytes:
        """
        Runs different visual programming tasks on input data.

        Args:
        - method (str): The method to run, one of 'gqa', 'image_editing', 'nlvr', 'ok_det'.
        - question (str, optional): A question to ask about an input image. Required if `method` is 'gqa'. Defaults to None.
        - instruction (str, optional): A textual instruction to apply to an input image. Required if `method` is 'image_editing', 'ok_det'. Defaults to None.
        - image (BinaryIO, optional): An image file to process. Required if `method` is 'gqa', 'image_editing', or 'ok_det'. Defaults to None.
        - left_image (BinaryIO, optional): The left image for an NLVR task. Required if `method` is 'nlvr'. Defaults to None.
        - right_image (BinaryIO, optional): The right image for an NLVR task. Required if `method` is 'nlvr'. Defaults to None.

        Returns:
        - dict[str, Union[str, Any]]: A dictionary with the following keys:
        - 'html_str' (str): The HTML string containing the output of the visual programming task.
        - 'result' (bytes or str): The output of the visual programming task.
        - 'prog_state' (dict): The current program state as a dictionary.
        """

        request_params = {
            "method": method,
            "question": question,
            "instruction": instruction,
            "image": image,
            "left_image": left_image,
            "right_image": right_image
        }

        url = 'http://35.239.71.169/'

        return json.loads(self._Model__inference(url=url, request_params=request_params))