import torch


def get_device(device_name: str):
    try:
        device = torch.device(device_name)
        return device
    except Exception as e:
        raise e
