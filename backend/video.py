import cv2
import tempfile
import numpy as np
from io import BytesIO
from fourier import fourier_transform_super_resolution
from bicubic import bicubic_interpolation
from bilinear import bilinear_interpolation
from iteractivebackprojection import iterative_back_projection
from lanczos import lanczos_resample
from non_local import non_local_means_super_resolution
from wavelet import wavelet_super_resolution_color
from totalvariation import upscale_with_tv
from nearest_neighbour_interpolation import nearest_neighbour_interpolation
import base64

def process_video(video_data, algo_id):
    """
    Process a video using the selected algorithm and return the output as Base64.

    Args:
        video_data (bytes): Raw video data as bytes.
        algo_id (int): The ID of the algorithm to apply.

    Returns:
        str: Base64-encoded processed video.
    """
    # Write video data to a temporary file
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_video_file:
        temp_video_file.write(video_data)
        temp_video_file.flush()  # Ensure all data is written

        # Open the video from the temporary file using OpenCV
        cap = cv2.VideoCapture(temp_video_file.name)
        if not cap.isOpened():
            raise Exception("Could not open video data.")

        # Get the original video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for output video
        frame_size = (1000, 600)  # Use the desired dimensions here
        output_frames = []  # Collect frames for final encoding

        while True:
            ret, frame = cap.read()
            if not ret:
                break  # Exit loop when no more frames are available

            # Apply the selected algorithm to the frame
            if algo_id == 1:
                processed_frame = bicubic_interpolation(frame, 1000, 600)
            elif algo_id == 2:
                processed_frame = bilinear_interpolation(frame, 1000, 600)
            elif algo_id == 3:
                processed_frame = fourier_transform_super_resolution(frame, 1000, 600)
            elif algo_id == 4:
                processed_frame = iterative_back_projection(frame, 1000, 600)
            elif algo_id == 5:
                processed_frame = lanczos_resample(frame, 1000, 600)
            elif algo_id == 6:
                processed_frame = nearest_neighbour_interpolation(frame, 1000, 600)
            elif algo_id == 7:
                processed_frame = non_local_means_super_resolution(frame, 1000, 600)
            elif algo_id == 8:
                processed_frame = upscale_with_tv(frame, 1000, 600)
            elif algo_id == 9:
                processed_frame = wavelet_super_resolution_color(frame, 1000, 600)
            else:
                raise ValueError(f"Invalid algorithm ID: {algo_id}")

            output_frames.append(processed_frame)

        cap.release()

        # Encode the processed video to a memory buffer
        output_video_bytes = encode_video(output_frames, fps, fourcc, frame_size)

    return base64.b64encode(output_video_bytes).decode("utf-8")


def encode_video(frames, fps, fourcc, frame_size):
    """
    Encodes a list of frames into a video.

    Args:
        frames (list): List of processed frames (as NumPy arrays).
        fps (float): Frames per second of the video.
        fourcc (int): Codec identifier.
        frame_size (tuple): Frame dimensions (width, height).

    Returns:
        bytes: Encoded video data as bytes.
    """
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_output_file:
        out = cv2.VideoWriter(temp_output_file.name, fourcc, fps, frame_size)
        for frame in frames:
            out.write(frame)
        out.release()

        temp_output_file.seek(0)
        return temp_output_file.read()
