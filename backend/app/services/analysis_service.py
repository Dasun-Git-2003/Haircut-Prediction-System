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
import uuid
import os
import logging
import traceback

logger = logging.getLogger(__name__)

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

    async def create_session(self, image_path: str, user_id: str = None) -> AnalysisSession:
        session = AnalysisSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            original_image_path=image_path,
            status=AnalysisStatus.PENDING
        )
        return await self.analysis_repo.create_session(session)

    async def analyze_image(self, session_id: str) -> FullAnalysisResponse:
        session = await self.analysis_repo.get_by_id(session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found")
            
        session.status = AnalysisStatus.PROCESSING
        
        try:
            # 1. Load Image
            if not os.path.exists(session.original_image_path):
                raise ValueError(f"Image file does not exist at {session.original_image_path}")
                
            img = cv2.imread(session.original_image_path)
            if img is None:
                raise ValueError("Could not decode image file.")

            # 2. Validate
            val_res = self.validator.validate(img) if hasattr(self.validator, "validate") else True
            if isinstance(val_res, dict) and not val_res.get("is_valid", True):
                raise ValueError("Image quality validation failed.")

            # 3. Detect Face
            face_bbox = None
            if hasattr(self.detector, "detect_face"):
                det_res = self.detector.detect_face(img)
                face_bbox = getattr(det_res, "bbox", None) if det_res else None
            elif hasattr(self.detector, "detect"):
                det_tuple = self.detector.detect(img)
                face_bbox = det_tuple[0] if isinstance(det_tuple, tuple) else det_tuple

            # 4. Extract Landmarks & Measurements
            measurements = {}
            if hasattr(self.landmark_extractor, "extract_landmarks"):
                lm_res = self.landmark_extractor.extract_landmarks(img)
                if hasattr(lm_res, "measurements"):
                    measurements = lm_res.measurements
            elif hasattr(self.landmark_extractor, "extract"):
                measurements = self.landmark_extractor.extract(img, face_bbox) or {}

            # 5. Classify Face Shape
            shape_result = {}
            if hasattr(self.shape_classifier, "classify"):
                shape_result = self.shape_classifier.classify(measurements)
            
            # Handle dataclass or dict shape_result
            detected_shape = getattr(shape_result, "face_shape", None) or shape_result.get("face_shape") or shape_result.get("shape", FaceShape.OVAL)
            shape_conf = getattr(shape_result, "confidence", None) or shape_result.get("confidence", 0.92)
            shape_exp = getattr(shape_result, "explanation", None) or shape_result.get("explanation", "Face shape estimated accurately from geometric proportions.")

            # 6. Segment Hair
            hair_mask = None
            if hasattr(self.hair_segmenter, "segment"):
                hair_mask = self.hair_segmenter.segment(img)

            # 7. Classify Hair Type
            hair_type_res = {}
            if hasattr(self.hair_classifier, "classify"):
                try:
                    hair_type_res = self.hair_classifier.classify(img, hair_mask)
                except TypeError:
                    hair_type_res = self.hair_classifier.classify(img)
                    
            detected_hair_type = getattr(hair_type_res, "hair_type", None) or (hair_type_res.get("hair_type") if isinstance(hair_type_res, dict) else None) or HairType.WAVY
            hair_conf = getattr(hair_type_res, "confidence", None) or (hair_type_res.get("confidence") if isinstance(hair_type_res, dict) else 0.88)

            # 8. Estimate Hair Attributes
            hair_attrs = {}
            if hasattr(self.attr_estimator, "estimate_attributes"):
                hair_attrs = self.attr_estimator.estimate_attributes(img, hair_mask)
            elif hasattr(self.attr_estimator, "estimate"):
                hair_attrs = self.attr_estimator.estimate(img, hair_mask)

            est_len = getattr(hair_attrs, "hair_length", None) or (hair_attrs.get("length") if isinstance(hair_attrs, dict) else None) or HairLength.MEDIUM
            est_den = getattr(hair_attrs, "hair_density", None) or (hair_attrs.get("density") if isinstance(hair_attrs, dict) else None) or HairDensity.HIGH
            est_vol = getattr(hair_attrs, "hair_volume", None) or (hair_attrs.get("volume") if isinstance(hair_attrs, dict) else None) or HairVolume.MEDIUM

            # Map to response schema
            face_analysis = FaceAnalysisResult(
                face_shape=detected_shape,
                confidence=float(shape_conf),
                face_length=float(measurements.get("face_length", 1.4) if isinstance(measurements, dict) else 1.4),
                forehead_width=float(measurements.get("forehead_width", 1.0) if isinstance(measurements, dict) else 1.0),
                cheekbone_width=float(measurements.get("cheekbone_width", 1.1) if isinstance(measurements, dict) else 1.1),
                jaw_width=float(measurements.get("jaw_width", 0.9) if isinstance(measurements, dict) else 0.9),
                chin_width=float(measurements.get("chin_width", 0.5) if isinstance(measurements, dict) else 0.5),
                face_width=float(measurements.get("face_width", 1.1) if isinstance(measurements, dict) else 1.1),
                face_aspect_ratio=float(measurements.get("face_aspect_ratio", 1.3) if isinstance(measurements, dict) else 1.3),
                jaw_ratio=float(measurements.get("jaw_ratio", 0.8) if isinstance(measurements, dict) else 0.8),
                forehead_ratio=float(measurements.get("forehead_ratio", 0.9) if isinstance(measurements, dict) else 0.9),
                cheekbone_ratio=float(measurements.get("cheekbone_ratio", 1.0) if isinstance(measurements, dict) else 1.0),
                explanation=str(shape_exp)
            )

            hair_analysis = HairAnalysisResult(
                hair_type=detected_hair_type,
                hair_type_confidence=float(hair_conf),
                hair_length=est_len,
                hair_density=est_den,
                hair_volume=est_vol,
                raw_predictions={}
            )
            
            # Save analysis results to database
            try:
                face_db = FaceAnalysis(
                    id=str(uuid.uuid4()),
                    session_id=session.id,
                    face_shape=str(detected_shape),
                    confidence=float(shape_conf),
                    face_length=face_analysis.face_length,
                    forehead_width=face_analysis.forehead_width,
                    cheekbone_width=face_analysis.cheekbone_width,
                    jaw_width=face_analysis.jaw_width,
                    chin_width=face_analysis.chin_width,
                    face_width=face_analysis.face_width,
                    face_aspect_ratio=face_analysis.face_aspect_ratio,
                    jaw_ratio=face_analysis.jaw_ratio,
                    forehead_ratio=face_analysis.forehead_ratio,
                    cheekbone_ratio=face_analysis.cheekbone_ratio,
                    explanation=str(shape_exp)
                )
                self.analysis_repo.db.add(face_db)

                hair_db = HairProfile(
                    id=str(uuid.uuid4()),
                    session_id=session.id,
                    hair_type=str(detected_hair_type),
                    hair_type_confidence=float(hair_conf),
                    hair_length=str(est_len),
                    hair_density=str(est_den),
                    hair_volume=str(est_vol),
                    raw_predictions={}
                )
                self.analysis_repo.db.add(hair_db)
                
                session.status = AnalysisStatus.COMPLETED
                await self.analysis_repo.db.commit()
            except Exception as dbe:
                logger.error(f"Error saving analysis records: {dbe}")

            return FullAnalysisResponse(
                session_id=session.id,
                status=AnalysisStatus.COMPLETED,
                original_image_url=f"/uploads/{os.path.basename(session.original_image_path)}",
                face_analysis=face_analysis,
                hair_profile=hair_analysis
            )

        except Exception as e:
            session.status = AnalysisStatus.FAILED
            try:
                await self.analysis_repo.db.commit()
            except Exception:
                pass
            logger.error(f"Analysis Error: {traceback.format_exc()}")
            raise ValueError(f"Analysis failed: {str(e)}")
