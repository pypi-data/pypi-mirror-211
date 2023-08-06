import numpy as np
import torch


class OffsetPredictor:
    def __init__(self, model_path, device="cpu"):
        self.model = torch.load(model_path, map_location=device)
        self.model.eval()

        self.input_dim = next(self.model.parameters()).shape[1]
        self.device = device

    @torch.no_grad()
    def __call__(self, x):
        """runs the input through the neural network. performs some basic tests to ensure compatability.

        Args:
            x (np.ndarray): numpy array of dimensions (batch_size, n_attributes) or (n_attributes, ) containing the data. The columns need to be ordered as follows:
            'xA_before_0_x', 'xA_before_0_y', 'xA_before_0_z',
            'xA_before_1_x', 'xA_before_1_y', 'xA_before_1_z',
            'xA_before_2_x', 'xA_before_2_y', 'xA_before_2_z',
            'xA_before_3_x', 'xA_before_3_y', 'xA_before_3_z',
            'xA_before_4_x', 'xA_before_4_y', 'xA_before_4_z',
            'roll_calculated', 'pitch_calculated', 'yaw_calculated',
            'xC_x', 'xC_y', 'xC_z',
            'leg_to_move_0', 'leg_to_move_1', 'leg_to_move_2', 'leg_to_move_3', 'leg_to_move_4'

            The Leg_to_move_{0-4} attributes are one-hot encoded depending on the number of the leg that is about to be moved.

        Returns:
            offsets: the predicted difference between the commanded positions and the desired ones.
            Returns an array of shape (3, ) or (batch_size, 3) depending on the input.
            Values are in the following order: x, y, z
        """

        was_single_dim = False
        if len(x.shape) == 1:
            was_single_dim = True
            x = x.reshape(1, -1)

        # test the input size
        assert (
            x.shape[1] == self.input_dim
        ), f"Wrong size of the input. {x.shape[1]} != {self.input_dim}."

        # test whether leg_to_move is one-hot encoded
        assert (
            len(np.unique(x[:, -5:])) == 2
        ), f"'leg_to_move' attribute is not one-hot encoded. Values: {x[:, -5:]}."
        assert np.all(
            np.sum(x[:, -5:], axis=1) == 1
        ), f"'leg_to_move' attribute is not one-hot encoded. Values: {x[:, -5:]}."

        x = torch.tensor(x, device=self.device)

        offset = self.model(x)
        offset = offset.detach().cpu().numpy()
        if was_single_dim:
            offset = offset.reshape(-1)
        return offset
