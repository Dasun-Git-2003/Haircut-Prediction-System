import os
from datasets import load_dataset
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_and_inspect():
    logger.info("Downloading Figaro1k dataset from HuggingFace...")
    try:
        ds = load_dataset("nobg/figaro1k")
        logger.info("Successfully downloaded dataset.")
        
        train_split = ds.get('train')
        test_split = ds.get('test')
        
        logger.info(f"Train samples: {len(train_split) if train_split else 0}")
        logger.info(f"Test samples: {len(test_split) if test_split else 0}")
        
        if train_split:
            # Inspect first sample
            sample = train_split[0]
            logger.info(f"Sample keys: {sample.keys()}")
            
            # Print class distribution
            classes = [s['hairstyle'] for s in train_split]
            from collections import Counter
            dist = Counter(classes)
            logger.info(f"Train class distribution (0-6): {dist}")
            
    except Exception as e:
        logger.error(f"Error downloading dataset: {e}")

if __name__ == "__main__":
    download_and_inspect()
