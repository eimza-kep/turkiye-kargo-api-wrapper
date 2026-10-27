# -*- coding: utf-8 -*-
"""
Ortak Kargo Veri Modelleri ve Durum Kodları
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional

class TrackingStatus(str, Enum):
    CREATED = "KAYIT_ACILDI"
    PICKED_UP = "KURYE_TESLIM_ALDI"
    IN_TRANSIT = "YOLDA_AKTM_MERKEZINDE"
    OUT_FOR_DELIVERY = "DAGITIMA_CIKTI"
    DELIVERED = "TESLIM_EDILDI"
    UNDELIVERED = "TESLIM_EDILEMEDI"
    RETURNED = "IADE_EDILDI"
    EXCEPTION = "HASAR_VEYA_SORUN"

@dataclass
class TrackingEvent:
    status: TrackingStatus
    timestamp: str
    city: str
    branch_name: str
    description: str

@dataclass
class ShipmentOrder:
    tracking_number: str
    carrier_name: str
    recipient_name: str
    recipient_phone: str
    city: str
    district: str
    desi: float
    status: TrackingStatus
    barcode_data: str
    history: List[TrackingEvent] = field(default_factory=list)
