# Machine Learning & AI Pipeline Documentation

StyleAI separates **Recommendation** (deterministic geometric ML & classification) from **Visualization** (Generative AI).

---

## 1. Pipeline Overview

```text
User Image 
   │
   ▼
[1] Image Quality Validation (Laplacian Blur Detection + Resolution Check)
   │
   ▼
[2] Face Detection (MediaPipe Face Detection)
   │
   ▼
[3] Landmark Extraction (MediaPipe Face Mesh: 468 3D Landmarks)
   │
   ▼
[4] Scale-Invariant Geometric Measurement Calculation
   │
   ▼
[5] Face Shape Classification (Random Forest / Geometric Ratio Engine)
   │
   ▼
[6] Hair Segmentation & Mask Generation (DeepLabV3 / U-Net / MediaPipe)
   │
   ▼
[7] Hair Attribute Classification (MobileNetV3 on Figaro1k: Texture, Length, Density, Volume)
   │
   ▼
[8] Hybrid Recommendation Engine (Multi-Factor Scoring + Preference Weighting)
   │
   ▼
[9] Explainability Engine (Rule-based Natural Language Reasoning Generation)
   │
   ▼
[10] Generative AI Virtual Try-On (Identity-Preserving Hair Synthesis)
```

---

## 2. Geometric Face Feature Extraction

MediaPipe provides 468 landmark coordinates $(x_i, y_i, z_i)$ normalized to $[0, 1]$. To make calculations scale-invariant, distances are normalized relative to maximum facial width.

### Key Anatomical Measurements:
- **Face Length ($L$)**: Euclidean distance between landmark 10 (top of forehead/trichion) and landmark 152 (menton/chin tip).
- **Forehead Width ($W_f$)**: Distance between temple landmarks 70 and 300.
- **Cheekbone Width ($W_c$)**: Distance between zygomatic landmarks 234 and 454.
- **Jaw Width ($W_j$)**: Distance between gonial angles 172 and 397.
- **Chin Width ($W_{ch}$)**: Distance across landmark points 202 and 422.

### Geometric Ratios:
1. $\text{Aspect Ratio} = L / \max(W_f, W_c, W_j)$
2. $\text{Jaw Ratio} = W_j / \max(W_f, W_c)$
3. $\text{Forehead Ratio} = W_f / \max(W_c, W_j)$
4. $\text{Cheekbone Ratio} = W_c / \max(W_f, W_j)$

### Face Shape Decision Boundaries:
- **Oval**: Aspect ratio $\in [1.25, 1.45]$, Forehead width $\approx$ Cheekbone width $>$ Jaw width, rounded jawline.
- **Round**: Aspect ratio $< 1.2$, Cheekbone width is prominent, soft circular chin.
- **Square**: Aspect ratio $< 1.25$, Forehead width $\approx$ Cheekbone width $\approx$ Jaw width, angular jawline.
- **Oblong**: Aspect ratio $> 1.45$, straight vertical side profile.
- **Heart**: Forehead width significantly wider than jawline, sharp tapered chin.
- **Diamond**: Cheekbone width significantly wider than forehead and jaw.

---

## 3. Figaro1k Dataset & Hair Classification

Dataset Source: [nobg/figaro1k on HuggingFace](https://huggingface.co/datasets/nobg/figaro1k)

### Characteristics:
- **1,050 unconstrained photographs** (840 train / 210 test).
- Pixel-level binary hair segmentation masks (`0` = background/face, `255` = hair).
- **7 Hairstyle Classes**:
  1. `straight`
  2. `wavy`
  3. `curly`
  4. `kinky` (mapped to Coily)
  5. `braids`
  6. `dreadlocks`
  7. `short-men` (short fades / crops)

### Training Scripts in `ml/training/`:
- `download_figaro1k.py`: Downloads and validates the HuggingFace dataset.
- `hair_type_trainer.py`: Fine-tunes MobileNetV3-Small on the 7 Figaro1k classes with data augmentation (random flips, rotations $\pm 15^\circ$, color jitter).
- `hair_segmentation_trainer.py`: Trains DeepLabV3 / U-Net with binary cross-entropy + Dice loss for hair region segmentation masks.
- `face_shape_trainer.py`: Fits and evaluates a Random Forest classifier with hyperparameter tuning on facial geometric vectors.

---

## 4. Hybrid Recommendation Engine

The recommendation engine scores every candidate hairstyle $h$ against the user's analyzed profile and optional preferences:

$$\text{Total Score}(h) = \sum_{k} w_k \cdot S_k(h)$$

| Factor | Weight | Evaluation Criteria |
| :--- | :--- | :--- |
| **Face Shape Match** | **35%** | $1.0$ for primary supported shapes, $0.7$ for compatible shapes, $0.3$ for neutral |
| **Hair Type Match** | **25%** | $1.0$ for exact texture match, $0.5$ for adjacent texture (e.g. wavy with straight) |
| **Hair Length Compatibility**| **10%** | $1.0$ for equal length, $0.8$ if user hair is longer (haircut feasible), $0.2-0.5$ if growth needed |
| **Hair Density Compatibility**| **10%** | Compatibility between style volume requirements and user hair density |
| **User Style Preferences** | **15%** | Tag matching against user's preferred style, lifestyle, and haircut category |
| **Maintenance Level** | **5%** | Matches user's willingness for daily styling routine |

---

## 5. Virtual Try-On Prompt Engineering

To generate naturalistic hairstyle visualizations while strictly preserving identity, prompts are constructed dynamically:

```text
Edit the provided photograph while strictly preserving the person's identity,
facial structure, skin tone, eyes, nose, mouth, facial proportions, clothing,
and background.

Change only the hairstyle.

Apply the hairstyle: {HAIRCUT_NAME}
Hair characteristics: {HAIR_TYPE}, {HAIR_LENGTH}
Description: {HAIRCUT_DESCRIPTION}

The haircut should look physically realistic and naturally integrated with the
person's existing head shape, hairline, lighting, shadows, and hair texture.
Do not modify the person's facial features, age, skin tone, or background.
```
