# -*- coding: utf-8 -*-
import unittest
from turkiye_kargo.desi import calculate_desi, get_billable_weight
from turkiye_kargo.carriers import get_carrier_client
from turkiye_kargo.models import TrackingStatus

class TestTurkiyeKargo(unittest.TestCase):
    def test_calculate_desi(self):
        # 30 * 40 * 20 / 3000 = 8.0
        desi = calculate_desi(30, 40, 20)
        self.assertEqual(desi, 8.0)

    def test_billable_weight_desi_wins(self):
        # 8.0 desi vs 5.0 kg -> 8.0 billable (DESI)
        res = get_billable_weight(30, 40, 20, actual_kg=5.0)
        self.assertEqual(res.billable_weight, 8.0)
        self.assertEqual(res.charged_by, "DESI")

    def test_billable_weight_weight_wins(self):
        # 8.0 desi vs 12.0 kg -> 12.0 billable (WEIGHT)
        res = get_billable_weight(30, 40, 20, actual_kg=12.0)
        self.assertEqual(res.billable_weight, 12.0)
        self.assertEqual(res.charged_by, "WEIGHT")

    def test_carrier_shipment_creation(self):
        for carrier_code in ["yurtici", "aras", "dhl", "ptt"]:
            client = get_carrier_client(carrier_code)
            shipment = client.create_shipment(
                order_number="ORDER-1",
                recipient_name="Test Alıcı",
                recipient_phone="5550001122",
                city="Ankara",
                district="Çankaya",
                address="Adres Detayı",
                desi=3.5
            )
            self.assertTrue(len(shipment.tracking_number) > 5)
            self.assertEqual(shipment.status, TrackingStatus.CREATED)

    def test_carrier_tracking_query(self):
        client = get_carrier_client("aras")
        shipment = client.query_tracking("ARAS123456789")
        self.assertEqual(shipment.status, TrackingStatus.DELIVERED)
        self.assertTrue(len(shipment.history) > 0)

if __name__ == "__main__":
    unittest.main()
