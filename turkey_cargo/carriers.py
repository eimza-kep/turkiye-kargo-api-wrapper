# -*- coding: utf-8 -*-
"""
Kargo Firmaları API İstemcileri (Mock & Canlı Uyumlu)
"""

import time
import random
from typing import Dict, Any, Optional
from .models import TrackingStatus, TrackingEvent, ShipmentOrder

class BaseCargoClient:
    carrier_id: str = "base"
    carrier_name: str = "Base Cargo"

    def __init__(self, api_key: str = "sandbox_key", api_secret: str = "sandbox_secret", test_mode: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.test_mode = test_mode

    def create_shipment(
        self,
        order_number: str,
        recipient_name: str,
        recipient_phone: str,
        city: str,
        district: str,
        address: str,
        desi: float,
        is_cod: bool = False,
        cod_amount: float = 0.0
    ) -> ShipmentOrder:
        raise NotImplementedError

    def query_tracking(self, tracking_number: str) -> ShipmentOrder:
        raise NotImplementedError


class YurticiCargoClient(BaseCargoClient):
    carrier_id = "yurtici"
    carrier_name = "Yurtiçi Kargo"

    def create_shipment(
        self,
        order_number: str,
        recipient_name: str,
        recipient_phone: str,
        city: str,
        district: str,
        address: str,
        desi: float,
        is_cod: bool = False,
        cod_amount: float = 0.0
    ) -> ShipmentOrder:
        tracking_no = f"YK{random.randint(100000000000, 999999999999)}"
        order = ShipmentOrder(
            tracking_number=tracking_no,
            carrier_name=self.carrier_name,
            recipient_name=recipient_name,
            recipient_phone=recipient_phone,
            city=city,
            district=district,
            desi=desi,
            status=TrackingStatus.CREATED,
            barcode_data=f"{tracking_no}-{int(desi)}D",
            history=[
                TrackingEvent(
                    status=TrackingStatus.CREATED,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                    city=city,
                    branch_name=f"{city} Merkez Şube",
                    description="Kargo sevk kaydı oluşturuldu, kurye alımı bekleniyor."
                )
            ]
        )
        return order

    def query_tracking(self, tracking_number: str) -> ShipmentOrder:
        # Mock realistic movement
        return ShipmentOrder(
            tracking_number=tracking_number,
            carrier_name=self.carrier_name,
            recipient_name="Alıcı Adı Gizli",
            recipient_phone="555***1234",
            city="İstanbul",
            district="Kadıköy",
            desi=2.5,
            status=TrackingStatus.OUT_FOR_DELIVERY,
            barcode_data=f"{tracking_number}-2D",
            history=[
                TrackingEvent(
                    status=TrackingStatus.CREATED,
                    timestamp="2026-10-26 14:00:00",
                    city="Ankara",
                    branch_name="Çankaya Şube",
                    description="Kargo gönderisi kabul edildi."
                ),
                TrackingEvent(
                    status=TrackingStatus.IN_TRANSIT,
                    timestamp="2026-10-26 23:30:00",
                    city="Kocaeli",
                    branch_name="Gebze Aktarma Merkezi",
                    description="Aktarma merkezinden çıkış yaptı."
                ),
                TrackingEvent(
                    status=TrackingStatus.OUT_FOR_DELIVERY,
                    timestamp="2026-10-27 09:15:00",
                    city="İstanbul",
                    branch_name="Kadıköy Dağıtım Şube",
                    description="Kurye dağıtıma çıktı, bugün teslim edilecek."
                )
            ]
        )


class ArasCargoClient(BaseCargoClient):
    carrier_id = "aras"
    carrier_name = "Aras Kargo"

    def create_shipment(
        self,
        order_number: str,
        recipient_name: str,
        recipient_phone: str,
        city: str,
        district: str,
        address: str,
        desi: float,
        is_cod: bool = False,
        cod_amount: float = 0.0
    ) -> ShipmentOrder:
        tracking_no = f"ARAS{random.randint(10000000000, 99999999999)}"
        return ShipmentOrder(
            tracking_number=tracking_no,
            carrier_name=self.carrier_name,
            recipient_name=recipient_name,
            recipient_phone=recipient_phone,
            city=city,
            district=district,
            desi=desi,
            status=TrackingStatus.CREATED,
            barcode_data=f"{tracking_no}-{int(desi)}",
            history=[
                TrackingEvent(
                    status=TrackingStatus.CREATED,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                    city=city,
                    branch_name="Aras Entegrasyon Servisi",
                    description="Entegrasyon üzerinden sipariş kaydı alındı."
                )
            ]
        )

    def query_tracking(self, tracking_number: str) -> ShipmentOrder:
        return ShipmentOrder(
            tracking_number=tracking_number,
            carrier_name=self.carrier_name,
            recipient_name="Alıcı Gizli",
            recipient_phone="542***9988",
            city="İzmir",
            district="Bornova",
            desi=3.0,
            status=TrackingStatus.DELIVERED,
            barcode_data=f"{tracking_number}-3",
            history=[
                TrackingEvent(
                    status=TrackingStatus.DELIVERED,
                    timestamp="2026-10-27 15:40:00",
                    city="İzmir",
                    branch_name="Bornova Şube",
                    description="Kargo alıcıya bizzat teslim edilmiştir."
                )
            ]
        )


class DHLeCommerceClient(BaseCargoClient):
    carrier_id = "dhl"
    carrier_name = "DHL eCommerce (Eski MNG Kargo)"

    def create_shipment(
        self,
        order_number: str,
        recipient_name: str,
        recipient_phone: str,
        city: str,
        district: str,
        address: str,
        desi: float,
        is_cod: bool = False,
        cod_amount: float = 0.0
    ) -> ShipmentOrder:
        tracking_no = f"DHL{random.randint(1000000000, 9999999999)}"
        return ShipmentOrder(
            tracking_number=tracking_no,
            carrier_name=self.carrier_name,
            recipient_name=recipient_name,
            recipient_phone=recipient_phone,
            city=city,
            district=district,
            desi=desi,
            status=TrackingStatus.CREATED,
            barcode_data=f"JJD01{tracking_no}",
            history=[
                TrackingEvent(
                    status=TrackingStatus.CREATED,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                    city=city,
                    branch_name="DHL eCommerce Hub",
                    description="Gönderi etiketi üretildi."
                )
            ]
        )

    def query_tracking(self, tracking_number: str) -> ShipmentOrder:
        return ShipmentOrder(
            tracking_number=tracking_number,
            carrier_name=self.carrier_name,
            recipient_name="Alıcı Gizli",
            recipient_phone="533***7711",
            city="Bursa",
            district="Nilüfer",
            desi=1.5,
            status=TrackingStatus.IN_TRANSIT,
            barcode_data=f"JJD01{tracking_number}",
            history=[
                TrackingEvent(
                    status=TrackingStatus.IN_TRANSIT,
                    timestamp="2026-10-27 18:20:00",
                    city="Bursa",
                    branch_name="Bursa Bölge Dağıtım Merkezi",
                    description="Kargo varış merkezine ulaştı."
                )
            ]
        )


class PTTCargoClient(BaseCargoClient):
    carrier_id = "ptt"
    carrier_name = "PTT Kargo"

    def create_shipment(
        self,
        order_number: str,
        recipient_name: str,
        recipient_phone: str,
        city: str,
        district: str,
        address: str,
        desi: float,
        is_cod: bool = False,
        cod_amount: float = 0.0
    ) -> ShipmentOrder:
        tracking_no = f"KP{random.randint(10000000000, 99999999999)}"
        return ShipmentOrder(
            tracking_number=tracking_no,
            carrier_name=self.carrier_name,
            recipient_name=recipient_name,
            recipient_phone=recipient_phone,
            city=city,
            district=district,
            desi=desi,
            status=TrackingStatus.CREATED,
            barcode_data=tracking_no,
            history=[
                TrackingEvent(
                    status=TrackingStatus.CREATED,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                    city=city,
                    branch_name="PTT Kargo Otomasyonu",
                    description="Gönderi kabul kaydı açıldı."
                )
            ]
        )

    def query_tracking(self, tracking_number: str) -> ShipmentOrder:
        return ShipmentOrder(
            tracking_number=tracking_number,
            carrier_name=self.carrier_name,
            recipient_name="Alıcı Gizli",
            recipient_phone="505***3322",
            city="Antalya",
            district="Muratpaşa",
            desi=5.0,
            status=TrackingStatus.DELIVERED,
            barcode_data=tracking_number,
            history=[
                TrackingEvent(
                    status=TrackingStatus.DELIVERED,
                    timestamp="2026-10-27 12:10:00",
                    city="Antalya",
                    branch_name="Muratpaşa Posta Dağıtım",
                    description="Gönderi teslim edilmiştir."
                )
            ]
        )


def get_carrier_client(carrier_code: str) -> BaseCargoClient:
    carriers = {
        "yurtici": YurticiCargoClient,
        "aras": ArasCargoClient,
        "dhl": DHLeCommerceClient,
        "mng": DHLeCommerceClient,  # MNG merged into DHL eCommerce
        "ptt": PTTCargoClient
    }
    cls = carriers.get(carrier_code.lower())
    if not cls:
        raise ValueError(f"Desteklenmeyen kargo firması: '{carrier_code}'. İzin verilenler: {', '.join(carriers.keys())}")
    return cls()
