# Hear the Words: Basic Model Code (Corrected)
# Stage 1: Vocal Isolation
# This version uses the correct 'torchaudio' library.

# --- Installation Instructions ---
# You need to install the correct libraries.
# Open your terminal or command prompt and run:
# pip install -U demucs torch torchaudio

import os
import torch
import torchaudio
from demucs.apply import apply_model
from demucs.pretrained import get_model

def isolate_vocals(input_song_path, output_directory="separated_vocals"):
    """
    Loads a song and separates it into its components, saving the vocal track.

    Args:
        input_song_path (str): Path to the song file (e.g., "my_song.mp3").
        output_directory (str): Folder to save the output files.
    """
    if not os.path.exists(input_song_path):
        print(f"Error: Input file not found: {input_song_path}")
        return

    print("Loading pre-trained Hybrid Demucs model...")
    model = get_model(name='htdemucs')
    model.eval()

    print(f"Loading audio file: {input_song_path}...")
    try:
        # CORRECTED LINE: Use torchaudio.load()
        wav, sr = torchaudio.load(input_song_path)
    except Exception as e:
        print(f"Could not load audio file. Error: {e}")
        return

    # The model expects audio in a specific format (stereo, correct sample rate)
    # We'll handle basic mono to stereo conversion
    if wav.shape[0] == 1: # If mono, duplicate the channel to make it stereo
        wav = torch.cat([wav, wav], dim=0)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    wav = wav.to(device)
    model.to(device)

    print("Applying the model to separate the vocals... (This may take a moment)")
    # The model works on batches, so we add a batch dimension with unsqueeze(0)
    with torch.no_grad():
        separated_sources = apply_model(model, wav.unsqueeze(0), split=True, overlap=0.5)[0]

    # The model separates the audio into drums, bass, other, and vocals.
    # We need to find the index for 'vocals'.
    try:
        vocal_index = model.sources.index('vocals')
        vocals = separated_sources[vocal_index]
    except ValueError:
        print("Error: 'vocals' stem not found in the model output.")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Save the isolated vocal track
    output_vocal_path = os.path.join(output_directory, f"{os.path.basename(input_song_path).split('.')[0]}_vocals.wav")
    print(f"Saving isolated vocals to: {output_vocal_path}")

    # CORRECTED LINE: Use torchaudio.save()
    torchaudio.save(output_vocal_path, vocals.cpu(), model.samplerate)

    print("\n--- Vocal isolation complete! ---")
    print(f"The clean vocal track is ready for Stage 2 analysis at: {output_vocal_path}")


# --- Main part of the script to run ---
if __name__ == '__main__':
    # --- IMPORTANT ---
    # Change this to the path of your song file
    song_to_process = "Believer.mp3"

    # Run the vocal isolation function
    isolate_vocals(input_song_path=song_to_process)