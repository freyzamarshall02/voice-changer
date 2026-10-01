import torch

from .model import ModelDimensions, Whisper


def load_model(path) -> Whisper:
    device = "cpu"
    checkpoint = torch.load(path, map_location=device, weights_only=False)
    dims = ModelDimensions(**checkpoint["dims"])
    model = Whisper(dims)
    model.load_state_dict(checkpoint["model_state_dict"])
    model = model.to(device)
    return model
