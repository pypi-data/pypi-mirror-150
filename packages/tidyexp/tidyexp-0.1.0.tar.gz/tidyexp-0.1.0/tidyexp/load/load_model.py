def load_model(path, model_type, model=None):

    """
    Loads model from path.

    :param path: Model path
    :param model_type: Model type
    :param model: Model
    """

    # TODO: add sklearn model loading
    if model_type == "torch":
        try:
            import torch
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "torch is not installed. Please install `torch` to load a PyTorch model."
            )

        checkpoint = torch.load(path, map_location="cpu")
        if model is not None:
            model.load_state_dict(checkpoint)
            return model
        else:
            return checkpoint
