from .ovutils import fibonacci
from openviatica_rust import fibonacci as rust_fibonacci

__all__ = [
    'fibonacci', 
    'rust_fibonacci'
    ]