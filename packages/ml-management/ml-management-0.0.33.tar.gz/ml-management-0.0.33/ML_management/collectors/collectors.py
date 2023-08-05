"""Collectors."""
from typing import Dict, Type

from ML_management.collectors.collector_pattern import CollectorPattern
from ML_management.collectors.dummy.dummy_collector import DummyCollector
from ML_management.collectors.s3.s3collector import S3Collector
from ML_management.collectors.topic_markers.topic_markers_collector import TopicMarkersCollector

DATA_COLLECTORS: Dict[str, Type[CollectorPattern]] = {
    "s3": S3Collector,
    "topic_marker": TopicMarkersCollector,
    "dummy": DummyCollector,
}
