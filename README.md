# Emotions in Library of Congress Images

The code in this repo will extract face/portrait images from the library of Congress pictures API, and then use the Microsoft Emotion API (rate is for preview is 30,000 transactions per month, 20 per minute), and save to a graphical relational database (or locally to a file). Images will first be assessed for having / not having a face using the OpenCV library (python extension).

- Sign up for a Microsoft API key [here](https://www.microsoft.com/cognitive-services/en-us/emotion-api). You will need an account.
- Save this key in a file in the PWD called `.secret`. An example `.secret_dummy` is provided.
- The [loc_images.json](loc_images.json) provided is a small sample of data, to account for the fact that Github file size limit is 50MB. If you want to update / produce your own data set (a json object of library of congress images) you can run [get_face_json.py](get_face_json.py). Otherwise, just use the sample with the script [run.py](run.py).

**rest is currently under development!** :)

#### Acknowledgements
- Thanks for shantnu for [FaceDetect](https://github.com/shantnu/FaceDetect/)
