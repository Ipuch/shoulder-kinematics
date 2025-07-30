"""
Script to export d1 correction matrices for scapula local coordinates systems.

This script extracts scapula landmark information from a dataset CSV file,
calculates d1 correction rotation matrices for each landmark, and exports them to text files.
Each matrix is identified by a specific name (S-LCS-X), related to the spartacus classification.
"""

import pandas as pd
from spartacus.src.frame_reader import Frame
from spartacus.enums import DatasetCSV
from spartacus import Segment, BiomechCoordinateSystem

df = pd.read_csv(DatasetCSV.DATASETS.value)

mapping_dataset_to_scapula_lcs = {
    "#14": "S-LCS-1",
    "#2": "S-LCS-2",
    "#1": "S-LCS-3",
    "#11": "S-LCS-4",
    # "#6c": "S-LCS-5",
    "#7": "S-LCS-6",
    "#19": "S-LCS-7",
    "#8": "S-LCS-8",
    "#4": "S-LCS-9",
    "#15": "S-LCS-10",
    "#17": "S-LCS-11",
}

# Export d1 correction matrices for scapula frames
for key, value in mapping_dataset_to_scapula_lcs.items():

    # get row from dataframe
    row = df[df["dataset_id"] == key].iloc[0]

    scapula_frame = Frame.from_xyz_string(
        origin=row.scapula_origin,
        x_axis=row.scapula_x_direction,
        y_axis=row.scapula_y_direction,
        z_axis=row.scapula_z_direction,
        segment=Segment.SCAPULA,
        side="right" if row.side_as_right else "left",
    )
    biomech_coordinate_system = BiomechCoordinateSystem.from_frame(scapula_frame)
    correction_matrix = biomech_coordinate_system.get_rotation_matrix()
    # export in a txt file with float format
    filename = f"scapula_d1_correction_matrix_{value}.txt"
    with open(filename, "w") as f:
        for row in correction_matrix:
            f.write(" ".join(f"{value:.6f}" for value in row) + "\n")
