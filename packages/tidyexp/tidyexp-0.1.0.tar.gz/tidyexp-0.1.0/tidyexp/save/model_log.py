import os


class ModelLog(object):

    """
    ModelLog is a logger used for models.
    """

    def __init__(self, experiment_id, experiment_dir, model_type):
        self.experiment_id = experiment_id
        self.experiment_dir = experiment_dir
        self.model_counter = 0

        # check before assigning
        assert model_type in ["torch", "sklearn"]
        self.model_type = model_type

        self.model_dir = os.path.join(self.experiment_dir, "models/")
        self.final_model_dir = os.path.join(
            self.model_dir, "final", "final_" + self.experiment_id
        )
        self.start_model_dir = os.path.join(
            self.model_dir, "start", "start_" + self.experiment_id
        )

        if self.model_type == "torch":
            self.model_ext = ".pt"
        elif self.model_type == "sklearn":
            self.model_ext = ".pkl"

        self.final_model_dir += self.model_ext

    def setup_model_dir(self):
        os.makedirs(self.model_dir, exist_ok=True)

    def save(self, model):
        self.model_counter += 1
        if self.model_counter == 1:
            os.makedirs(os.path.join(self.model_dir, "final"), exist_ok=True)
            self.setup_model_dir()

        self.save_final_model(model)

    def save_final_model(self, model):
        save_model(model, self.final_model_dir, self.model_type)


def save_model(model, model_fname, model_type):
    if model_type == "torch":
        save_torch_model(model_fname, model)

    if model_type == "sklearn":
        save_sklearn_model(model_fname, model)


def save_torch_model(path, model):
    try:
        import torch
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "torch is not installed. Please install `torch` to save a PyTorch model."
        )

    torch.save(model.state_dict(), path)


def save_sklearn_model(path, model):
    try:
        import sklearn
        import pickle
    except:
        raise ModuleNotFoundError(
            "sklearn and pickle is not installed. Please install `sklearn` and `pickle` to save a sklearn model."
        )

    with open(path, "wb") as file:
        pickle.dump(model, file)
