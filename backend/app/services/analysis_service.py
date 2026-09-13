from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.analysis import FullAnalysisResponse, AnalysisStatus, FaceAnalysisResult, HairAnalysisResult
from app.schemas.common import FaceShape, HairType, HairLength, HairDensity, HairVolume
from app.models.analysis import AnalysisSession, FaceAnalysis, HairProfile

# ML imports
from app.ml.face_analysis.image_validator import ImageValidator
from app.ml.face_analysis.detector import FaceDetector
from app.ml.face_analysis.landmarks import FaceLandmarkExtractor
from app.ml.face_analysis.face_shape import FaceShapeClassifier
from app.ml.hair_analysis.hair_classifier import HairTypeClassifier
from app.ml.hair_analysis.hair_attributes import HairAttributeEstimator
from app.ml.hair_analysis.hair_segmentation import HairSegmenter

import cv2
import traceback

class AnalysisService:
    def __init__(self, analysis_repo: AnalysisRepository):
        self.analysis_repo = analysis_repo
        
        # Initialize ML modules
        self.validator = ImageValidator()
        self.detector = FaceDetector()
        self.landmark_extractor = FaceLandmarkExtractor()
        self.shape_classifier = FaceShapeClassifier()
        self.hair_classifier = HairTypeClassifier()
        self.hair_segmenter = HairSegmenter()
        self.attr_estimator = HairAttributeEstimator()

    async def analyze_image(self, session_id: str) -> FullAnalysisResponse:
        session = await self.analysis_repo.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")
            
        session.status = AnalysisStatus.PROCESSING
        
        try:
            # 1. Load Image
            img = cv2.imread(session.original_image_path)
            if img is None:
                raise ValueError("Could not read image file.")

            # 2. Validate
            is_valid = self.validator.validate(img)
            if not is_valid:
                raise ValueError("Image validation failed.")

            # 3. Detect Face
            face_bbox, conf = self.detector.detect(img)
            if face_bbox is None:
                raise ValueError("No face detected.")

            # 4. Extract Landmarks
            landmarks = self.landmark_extractor.extract(img, face_bbox)

            # 5. Classify Face Shape
            shape_result = self.shape_classifier.classify(landmarks)

            # 6. Segment Hair
            hair_mask = self.hair_segmenter.segment(img)

            # 7. Classify Hair Type
            hair_type_result = self.hair_classifier.classify(img, hair_mask)

            # 8. Estimate Hair Attributes
            hair_attrs = self.attr_estimator.estimate(img, hair_mask)

            # Combine and map back to models
            face_analysis = FaceAnalysisResult(
                face_shape=shape_result.get("shape", FaceShape.OVAL),
                confidence=shape_result.get("confidence", 0.9),
                face_length=shape_result.get("face_length", 0.0),
                forehead_width=shape_result.get("forehead_width", 0.0),
                cheekbone_width=shape_result.get("cheekbone_width", 0.0),
                jaw_width=shape_result.get("jaw_width", 0.0),
                chin_width=shape_result.get("chin_width", 0.0),
                face_width=shape_result.get("face_width", 0.0),
                face_aspect_ratio=shape_result.get("face_aspect_ratio", 0.0),
                jaw_ratio=shape_result.get("jaw_ratio", 0.0),
                forehead_ratio=shape_result.get("forehead_ratio", 0.0),
                cheekbone_ratio=shape_result.get("cheekbone_ratio", 0.0),
                explanation=shape_result.get("explanation", "Analyzed successfully.")
            )

            hair_analysis = HairAnalysisResult(
                hair_type=hair_type_result.get("type", HairType.STRAIGHT),
                hair_type_confidence=hair_type_result.get("confidence", 0.9),
                hair_length=hair_attrs.get("length", HairLength.MEDIUM),
                hair_density=hair_attrs.get("density", HairDensity.MEDIUM),
                hair_volume=hair_attrs.get("volume", HairVolume.AVERAGE),
                raw_predictions={}
            )
            
            session.status = AnalysisStatus.COMPLETED
            
            return FullAnalysisResponse(
                session_id=session.id,
                status=AnalysisStatus.COMPLETED,
                original_image_url=session.original_image_path,
                face_analysis=face_analysis,
                hair_profile=hair_analysis
            )

        except Exception as e:
            session.status = AnalysisStatus.FAILED
            print("Analysis Error:", traceback.format_exc())
            raise ValueError(f"Analysis failed: {str(e)}")
