from dataclasses import dataclass
from bytez.tasks.visual_reasoning._models.allenai_visprog import AllenaiVisprogModel


@dataclass
class VisualReasoningModels:
    allenai_visprog = AllenaiVisprogModel().inference