import cv2
import tempfile
import numpy as np
from edgeDetection import sobel_edge_detection_color
from gammacorrection import gamma_correction
from adjust_saturation import saturation_adjust_color
from gaussian_blur import gaussian_blur_color
import base64

def processing_video(video_data, algo_id):
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
        print("Writing video data to temporary file...")
        temp_video_file.write(video_data)
        temp_video_file.flush()  # Ensure all data is written
        print("Temporary file created.")

        # Open the video from the temporary file using OpenCV
        print("Opening video file...")
        cap = cv2.VideoCapture(temp_video_file.name)
        if not cap.isOpened():
            raise Exception("Could not open video data.")
        print("Video file opened successfully.")

        # Get the original video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for output video
        frame_size = (frame_width, frame_height)  # Use original frame size
        print(f"Video properties: FPS={fps}, Frame Size={frame_size}, Total Frames={total_frames}")

        output_frames = []  # Collect frames for final encoding
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                print("No more frames to process. Exiting loop.")
                break  # Exit loop when no more frames are available

            frame_count += 1
            print(f"Processing frame {frame_count} of {total_frames}...")

            # Apply the selected algorithm to the frame
            if algo_id == 3:
                processed_frame = sobel_edge_detection_color(frame)
                print(f"Applied Sobel Edge Detection on frame {frame_count}.")
            elif algo_id == 4:
                processed_frame = gamma_correction(frame, 1.5)
                print(f"Applied Gamma Correction on frame {frame_count}.")
            elif algo_id == 1:
                processed_frame = gaussian_blur_color(frame)
                print(f"Applied Gaussian Blur on frame {frame_count}.")
            elif algo_id == 2:
                processed_frame = saturation_adjust_color(frame)
                print(f"Applied Saturation Adjustment on frame {frame_count}.")
            else:
                raise ValueError(f"Invalid algorithm ID: {algo_id}")

            output_frames.append(processed_frame)

        cap.release()
        print(f"Finished processing {frame_count} frames.")

        # Encode the processed video to a memory buffer
        print("Encoding processed video...")
        output_video_bytes = encode_video(output_frames, fps, fourcc, frame_size)
        print("Video encoding complete.")

    print("Returning Base64-encoded processed video.")
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
    print("Starting video encoding process...")
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_output_file:
        out = cv2.VideoWriter(temp_output_file.name, fourcc, fps, frame_size)
        for i, frame in enumerate(frames):
            print(f"Writing frame {i + 1} to video...")
            out.write(frame)
        out.release()
        print("Video writing complete.")

        temp_output_file.seek(0)
        return temp_output_file.read()
