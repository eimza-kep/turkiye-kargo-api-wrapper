# -*- coding: utf-8 -*-
"""
Türkiye Kargo CLI Aracı
"""

import sys
import argparse
from .desi import get_billable_weight
from .carriers import get_carrier_client

def main():
    parser = argparse.ArgumentParser(
        description="Türkiye Kargo API Entegrasyon Wrapper'ı & Desi Hesaplayıcı"
    )
    subparsers = parser.add_subparsers(dest="command", help="Komutlar: desi, track, create")

    # Desi command
    desi_parser = subparsers.add_parser("desi", help="Kargo paketi için desi ve faturalandırılacak ağırlığı hesaplar")
    desi_parser.add_argument("--width", type=float, required=True, help="En (cm)")
    desi_parser.add_argument("--length", type=float, required=True, help="Boy (cm)")
    desi_parser.add_argument("--height", type=float, required=True, help="Yükseklik (cm)")
    desi_parser.add_argument("--weight", type=float, default=0.0, help="Gerçek Ağırlık (kg)")
    desi_parser.add_argument("--divisor", type=int, default=3000, help="Desi böleni (Yurtiçi standart 3000, IATA hava kargo 5000)")

    # Track command
    track_parser = subparsers.add_parser("track", help="Kargo takip kodu sorgular")
    track_parser.add_argument("--carrier", required=True, choices=["yurtici", "aras", "dhl", "mng", "ptt"])
    track_parser.add_argument("--code", required=True, help="Kargo Takip No")

    # Create command
    create_parser = subparsers.add_parser("create", help="Kargo gönderi siparişi ve barkod oluşturur")
    create_parser.add_argument("--carrier", required=True, choices=["yurtici", "aras", "dhl", "mng", "ptt"])
    create_parser.add_argument("--recipient", required=True, help="Alıcı Adı Soyadı")
    create_parser.add_argument("--phone", default="5551234567", help="Alıcı Telefon")
    create_parser.add_argument("--city", default="İstanbul", help="İl")
    create_parser.add_argument("--district", default="Kadıköy", help="İlçe")
    create_parser.add_argument("--desi", type=float, default=2.0, help="Desi")

    args = parser.parse_args()

    if args.command == "desi":
        res = get_billable_weight(args.width, args.length, args.height, args.weight, args.divisor)
        print("\n" + "=" * 50)
        print("📦 TÜRKİYE STANDART KARGO DESİ RAPORU")
        print("=" * 50)
        print(f"Ebatlar: {res.width_cm} x {res.length_cm} x {res.height_cm} cm")
        print(f"Hesaplanan Hacimsel Desi: {res.desi} Desi (Bölen: {args.divisor})")
        print(f"Tartılan Gerçek Ağırlık: {res.actual_kg} kg")
        print(f"Faturalandırılacak Ağırlık: {res.billable_weight} ({'DESİ BAZLI' if res.charged_by == 'DESI' else 'KG BAZLI'})")
        print(f"Paket Kategorisi: {res.category}")
        print("=" * 50)
        return

    if args.command == "track":
        client = get_carrier_client(args.carrier)
        shipment = client.query_tracking(args.code)
        print("\n" + "=" * 50)
        print(f"🚚 {shipment.carrier_name.upper()} KARGO TAKİP")
        print("=" * 50)
        print(f"Takip No: {shipment.tracking_number}")
        print(f"Güncel Durum: {shipment.status.value}")
        print(f"Varış Şehri: {shipment.city} / {shipment.district}")
        print("\nHareket Geçmişi:")
        for h in shipment.history:
            print(f"  • [{h.timestamp}] ({h.city}) {h.branch_name}: {h.description}")
        print("=" * 50)
        return

    if args.command == "create":
        client = get_carrier_client(args.carrier)
        shipment = client.create_shipment(
            order_number="SIP-100",
            recipient_name=args.recipient,
            recipient_phone=args.phone,
            city=args.city,
            district=args.district,
            address="Örnek Mah. Test Sok.",
            desi=args.desi
        )
        print("\n" + "=" * 50)
        print(f"✅ {shipment.carrier_name} GÖNDERİ KAYDI AÇILDI")
        print("=" * 50)
        print(f"Takip Numarası: {shipment.tracking_number}")
        print(f"Barkod Verisi: {shipment.barcode_data}")
        print(f"Alıcı: {shipment.recipient_name} ({shipment.city})")
        print(f"Desi: {shipment.desi}")
        print("=" * 50)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
