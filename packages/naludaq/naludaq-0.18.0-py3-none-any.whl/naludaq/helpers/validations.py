"""Helper functions for validating inputs."""
import pathlib


def validate_dir_or_raise(output_dir, name="Directory"):
    if not isinstance(output_dir, (str, pathlib.Path)):
        raise TypeError(f"{name} must be a string.")
    if not pathlib.Path(output_dir).exists():
        raise FileNotFoundError(f"{name} must exist.")
    if output_dir is None or not pathlib.Path(output_dir).is_dir():
        raise NotADirectoryError(f"{name} must be specified.")


def validate_chip_list_or_raise(chips: list[int], params: dict):
    num_chips = len(params.get("chips", ["single"]))
    if not isinstance(chips, list):
        raise TypeError("Chips must be a list.")
    if len(chips) != len(set(chips)):
        raise ValueError("One or more chip numbers is repeated.")
    for chip in chips:
        if not isinstance(chip, int):
            raise TypeError("Chips must be a list of integers.")
        if not 0 <= chip < num_chips:
            raise ValueError("One or more chip numbers is out of range.")
