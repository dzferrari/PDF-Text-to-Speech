# PDF-Text-to-Speech
A set of 2 python scripts. One to read PDF using pdfminer.six, and another one to generate audio using Google Cloud Text-to-Speech libraries.


## Credits

This project is inspired by [PDF_AUDIO_READER](https://github.com/nikhilkumarsingh/PDF_AUDIO_READER), a nikhilkumarsing repository. The code is based on [pdfminer.six](https://github.com/pdfminer/pdfminer.six) and on [Python-Doc-Samples](https://github.com/GoogleCloudPlatform/python-docs-samples), from GoogleCloudPlataform.


## How it works?

As PDF_AUDIO_READER, the task can be devided into 2 steps:

1. Extract text from PDF. Refer [pdf_to_text.py](https://github.com/dzferrari/PDF-Text-to-Speech/blob/main/pdf_to_txt.py). This script uses LAParams from pdfminer.six along with 3 other functions to remove lines or paragraphs started with specific elements. 

2. Convert text to speech. Refer [synthesize_file.py](https://github.com/dzferrari/PDF-Text-to-Speech/blob/main/synthesize_file.py). This script uses Google Cloud TTS API, but, since the maximum size of the text can only be 5kb per execution, it was necessary to work by chunks. So in order to convert long texts into speech, it creates multiple calls of 3kb and adds their result to the final audio output file.  


## Setup

1. Install pdfminer.six.
  ```
  pip install pdfminer.six
  ```
  
2. Obtain authentication credentials.

Create local credentials by running the following command and following the oauth2 flow (read more about the command [here](https://cloud.google.com/sdk/gcloud/reference/beta/auth/application-default/login)):
  ```
  gcloud auth application-default login
  ```
Read more about [Google Cloud Platform Authentication](https://cloud.google.com/docs/authentication#projects_and_resources).

