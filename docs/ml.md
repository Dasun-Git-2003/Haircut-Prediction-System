# Machine Learning Pipeline

## Overview
The ML pipeline consists of two main components: Face Analysis and Hair Analysis.

## Face Analysis
1. **Validation**: Checks for image blurriness, resolution, and format.
2. **Detection**: Detects bounding boxes for faces in the image.
3. **Landmarks**: Extracts 68 facial landmarks.
4. **Classification**: Uses geometric ratios to classify into 6 face shapes (Oval, Round, Square, Heart, Diamond, Oblong).

## Hair Analysis
- Uses models trained on datasets like **Figaro1k**.
- Extracts hair segments.
- Classifies hair type (Straight, Wavy, Curly, Coily) and estimates attributes (Length, Density, Volume).

## Training
To train custom models, refer to the `backend/app/ml/training/` scripts (if available) and place dataset images in `data/raw/`.
