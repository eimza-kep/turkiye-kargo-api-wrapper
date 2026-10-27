# -*- coding: utf-8 -*-
"""
Türkiye Kargo API Entegrasyon Wrapper & Desi Hesaplayıcı
Yurtiçi, Aras, DHL eCommerce, PTT, Sürat Kargo
"""

__version__ = "1.0.0"
__author__ = "eimza-kep"

from .desi import calculate_desi, get_billable_weight, DesiResult
from .models import TrackingStatus, TrackingEvent, ShipmentOrder
from .carriers import YurticiCargoClient, ArasCargoClient, DHLeCommerceClient, PTTCargoClient, get_carrier_client

__all__ = [
    "calculate_desi",
    "get_billable_weight",
    "DesiResult",
    "TrackingStatus",
    "TrackingEvent",
    "ShipmentOrder",
    "YurticiCargoClient",
    "ArasCargoClient",
    "DHLeCommerceClient",
    "PTTCargoClient",
    "get_carrier_client"
]
