# -*- coding: utf-8 -*-
"""
Kargo Desi ve Faturalandırılabilir Ağırlık Hesaplama Motoru
"""

from dataclasses import dataclass

@dataclass
class DesiResult:
    width_cm: float
    length_cm: float
    height_cm: float
    actual_kg: float
    desi: float
    billable_weight: float
    charged_by: str  # 'DESI' or 'WEIGHT'
    category: str

def calculate_desi(width_cm: float, length_cm: float, height_cm: float, divisor: int = 3000) -> float:
    """
    Kargo Desi (Hacimsel Ağırlık) Hesabı:
    Formül: (En * Boy * Yükseklik) / 3000 (Türkiye Yurtiçi Standartı)
    """
    if width_cm <= 0 or length_cm <= 0 or height_cm <= 0:
        return 0.0
    return round((width_cm * length_cm * height_cm) / float(divisor), 2)

def get_billable_weight(
    width_cm: float,
    length_cm: float,
    height_cm: float,
    actual_kg: float = 0.0,
    divisor: int = 3000
) -> DesiResult:
    """
    Kargo firmasının faturalandıracağı esas ağırlığı hesaplar: max(Gerçek KG, Desi)
    """
    desi_val = calculate_desi(width_cm, length_cm, height_cm, divisor)
    billable = max(actual_kg, desi_val)
    charged_by = "DESI" if desi_val >= actual_kg else "WEIGHT"

    if billable <= 0.5:
        category = "Dosya / Evrak"
    elif billable <= 2.0:
        category = "1-2 Desi / Küçük Paket"
    elif billable <= 5.0:
        category = "3-5 Desi / Standart Koli"
    elif billable <= 15.0:
        category = "6-15 Desi / Orta Boy Koli"
    elif billable <= 30.0:
        category = "16-30 Desi / Büyük Koli"
    else:
        category = "31+ Desi / Ağır Yük / Palet"

    return DesiResult(
        width_cm=width_cm,
        length_cm=length_cm,
        height_cm=height_cm,
        actual_kg=actual_kg,
        desi=desi_val,
        billable_weight=round(billable, 2),
        charged_by=charged_by,
        category=category
    )
