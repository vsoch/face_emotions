# Emotions in Library of Congress Images

The code in this repo will extract face/portrait images from the library of Congress pictures API, and then use the Microsoft Emotion API (rate is for preview is 30,000 transactions per month, 20 per minute), and save to a graphical relational database (or locally to a file.)

- Sign up for a Microsoft API key [here](https://www.microsoft.com/cognitive-services/en-us/emotion-api). You will need an account.
- Save this key in a file in the PWD called `.secret`. An example `.secret_dummy` is provided.
- If you want to update / produce your own data set (a json object of library of congress images) you can run [get_face_json.py](get_face_json.py). Otherwise, just use the script run.py.

**rest is currently under development!** :)
