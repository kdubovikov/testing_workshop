
from typing import Optional
from testing_workshop.model import Metric, Session


def insert_metrics(metrics: list[Metric]):
    """Inserts a list of metrics into the database"""
    session = Session()
    for metric in metrics:
        session.add(metric)
    session.commit()

def find_metric_by_name(name: str) -> Optional[Metric]:
    """Returns a metric with the given name, or None if not found"""
    session = Session()
    return session.query(Metric).filter(Metric.name == name).first()

def insert_metric_normalized_name(metric: Metric):
    """Inserts a metric into the database, with the name normalized to lowercase"""
    session = Session()
    metric.name = metric.name.lower()
    session.add(metric)
    session.commit()

def find_and_square_metric(name: str) -> Optional[Metric]:
    """Finds a metric with the given name, squares its value, and returns it."""
    metric = find_metric_by_name(name)

    if metric:
        metric.value = metric.value ** 2 # side effect!!!

    insert_metric_normalized_name(metric)

    return metric