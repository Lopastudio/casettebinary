# My attempt with heavy use of AI to make an program that can convert files into sound, that can be recorded onto a audio casette

import math
import wave

# Parameters for the sine wave
frequency_0 = 440.0  # Hz (middle A)
frequency_1 = 880.0  # Hz (A an octave higher)
duration = 0.1  # seconds
volume = 8192  # 0-32767


# Function to encode a binary string as a sine wave and save to a wave file
def binary_to_wave(binary_string, filename):
  # Open a new wave file for writing
  with wave.open(filename, 'w') as wave_file:
    # Set the wave file parameters
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(44100)

    # Iterate over each bit in the binary string
    for bit in binary_string:
      # Determine the frequency and duration of the sine wave for this bit
      if bit == '0':
        frequency = frequency_0
      else:
        frequency = frequency_1

      # Generate the sine wave samples for this bit
      num_samples = int(duration * wave_file.getframerate())
      samples = []
      for i in range(num_samples):
        sample = int(
          volume *
          math.sin(2 * math.pi * frequency * i / wave_file.getframerate()))
        samples.append(sample)

      # Write the sine wave samples to the wave file
      wave_file.writeframes(b''.join(
        [wave.struct.pack('<h', sample) for sample in samples]))


# Function to decode a sine wave from a wave file and convert to a binary string
def wave_to_binary(filename):
  # Open the wave file for reading
  with wave.open(filename, 'r') as wave_file:
    # Iterate over each frame in the wave file
    binary_string = ''
    for i in range(wave_file.getnframes()):
      # Read the next frame and convert it to a sample value
      frame = wave_file.readframes(1)
      sample = wave.struct.unpack('<h', frame)[0]

      # Determine whether this sample represents a '0' or '1' bit
      if sample > 0:
        binary_string += '1'
      else:
        binary_string += '0'

    return binary_string


# Function to convert an ASCII string to binary
def ascii_to_binary(ascii_string):
  binary_string = ''
  for char in ascii_string:
    binary_string += bin(ord(char))[2:].zfill(
      8)  # Convert each character to binary and append to the binary string
  return binary_string


# Function to convert a binary string to an ASCII string
def binary_to_ascii(binary_string):
  ascii_string = ''
  for i in range(0, len(binary_string),
                 8):  # Convert each 8-bit chunk to an ASCII character
    ascii_string += chr(int(binary_string[i:i + 8], 2))
  return ascii_string


# Main function to encode or decode a wave file
def encode_decode_wave(input_string, filename=None):
  if filename is None:  # Encoding mode
    binary_string = ascii_to_binary(input_string)
    wave_filename = 'wave.wav'
    binary_to_wave(binary_string, wave_filename)
    print(f'Successfully encoded ASCII text as sine wave in {wave_filename}.')

  else:  # Decoding mode
    binary_string = wave_to_binary(filename)
    ascii_string = binary_to_ascii(binary_string)

    if filename.endswith('.txt'):
      with open(input_string, 'w') as file:
        file.write(ascii_string)
      print(
        f'Successfully decoded sine wave in {filename} and saved ASCII text to {input_string}.'
      )

    else:
      print(f'Successfully decoded sine wave in {filename}:')
      print(ascii_string)


# Sample input string
input_string = 'Hello, world!'

# Encode the input string as a sine wave and save to a wave file
encode_decode_wave(input_string)

# Decode the sine wave from the wave file and save as a text file
encode_decode_wave('decoded.txt', 'wave.wav')
