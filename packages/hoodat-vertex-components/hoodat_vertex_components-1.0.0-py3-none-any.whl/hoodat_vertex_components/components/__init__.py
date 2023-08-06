"""
Hoodat components
"""
import os

try:
    from kfp.v2.components import load_component_from_file
except ImportError:
    from kfp.components import load_component_from_file

__all__ = [
    "AddPyOp",
    "MakeCascadeFileOp",
    "VideoToFramesOp",
    "HaarFromFramesOp",
    "QueryDatabaseOutputDataOp",
    "QueryDatabaseOutputStringOp",
]

AddPyOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "add_py/component.yaml")
)

MakeCascadeFileOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "make_cascade_file/component.yaml")
)

VideoToFramesOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "video_to_frames/component.yaml")
)

HaarFromFramesOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "haar_from_frames/component.yaml")
)

QueryDatabaseOutputDataOp = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "query_database_output_data/component.yaml")
)

QueryDatabaseOutputStringOp = load_component_from_file(
    os.path.join(
        os.path.dirname(__file__), "query_database_output_string/component.yaml"
    )
)
