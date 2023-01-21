#!/usr/bin/env python
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# All Rights Reserved.

"""Google Cloud Text-To-Speech API application based on the sample by GoogleCloudPlataform/python-doc-samples.

Example usage:
    python synthesize_file.py --text resources/hello.txt
"""

import argparse
import os
import datetime

# [START tts_synthesize_text_file]
def synthesize_text_file(text_file):
    """Synthesizes speech from the input file of text."""
    from google.cloud import texttospeech

    # Defining time format
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    
    client = texttospeech.TextToSpeechClient()
    
    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-I",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    # Encode to MP3 and set the speaking speed rate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.9
    )
       
    # Select or create the output folder
    output_folder = "/path/to/folder"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    # Generate a unique file name 
    output_file = os.path.join(output_folder, f"output-{current_time}.mp3")

    with open(text_file, "r") as f:
        chunks = iter(lambda: f.read(3000), '')
        for chunk in chunks:
            input_text = texttospeech.SynthesisInput(text=chunk)
            response = client.synthesize_speech(
                request={"input": input_text, "voice": voice, "audio_config": audio_config}
            )

            # The response's audio_content is binary.
            with open(output_file, "ab") as out:
                out.write(response.audio_content)
                print(f'Audio content written to file "{output_file}"')


# [END tts_synthesize_text_file]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="The text file from which to synthesize speech.")

    args = parser.parse_args()

    if args.text:
        synthesize_text_file(args.text)
    else:
        synthesize_ssml_file(args.ssml)
