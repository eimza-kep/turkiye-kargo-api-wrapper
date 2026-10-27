# Türkiye Kargo API Entegrasyon Wrapper'ı & Desi Hesaplayıcı 🚚📦

[![Lisans: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Kargo Firmaları](https://img.shields.io/badge/Kargo-Yurti%C3%A7i%20%7C%20Aras%20%7C%20DHL%20%7C%20PTT-blue.svg)](https://kaargoo.com.tr)
[![Bağımlılık: Yok](https://img.shields.io/badge/Dependencies-Zero--Dependency-success.svg)](https://github.com)
[![Rehber](https://img.shields.io/badge/Rehber-Kargo%20Lojistik%20Rehberi-e11d48.svg)](https://kaargoo.com.tr)

Türkiye'de faaliyet gösteren ulusal ve küresel kargo taşımacılık devleri (**Yurtiçi Kargo, Aras Kargo, DHL eCommerce [eski MNG], PTT Kargo, Sürat Kargo**) için geliştirilmiş **Tek Çatı Kargo API İstemcisi, Desi/Faturalandırılabilir Ağırlık Hesaplayıcısı ve Sandbox Mock Test Kütüphanesi**.

Kargo fiyat karşılaştırmaları, kurumsal sözleşme pazarlıkları ve 38 firmanın yer aldığı kapsamlı dizin için [Kargo & Lojistik Rehberi (kaargoo.com.tr)](https://kaargoo.com.tr) portalını ziyaret edebilirsiniz.

---

## ✨ Temel Özellikler

* 📦 **Türkiye Standart Desi Hesaplama Motoru:**
  * Yurtiçi kargo standardı olan `(En x Boy x Yükseklik) / 3000` formülünü uygular.
  * Uluslararası IATA hava kargo için `5000` bölen desteği sunar.
  * Tartılan gerçek ağırlık ile hacimsel desi arasındaki `max()` değerini bularak kargo firmasının faturaya yansıtacağı esas ağırlığı (`billable_weight`) ve paket kategorisini belirler.
* 🔄 **Birleşik Kargo Takip Durumları (Unified Statuses):**
  * Tüm firmaların karmaşık durum kodlarını standart hale getirir:
    * `KAYIT_ACILDI (CREATED)`
    * `KURYE_TESLIM_ALDI (PICKED_UP)`
    * `YOLDA_AKTM_MERKEZINDE (IN_TRANSIT)`
    * `DAGITIMA_CIKTI (OUT_FOR_DELIVERY)`
    * `TESLIM_EDILDI (DELIVERED)`
    * `IADE_EDILDI (RETURNED)`
* 🧪 **Entegratör Sandbox Mock Desteği:**
  * Canlı kargo API şifresi beklemeden e-ticaret sitenizin kargo akışlarını (etiket üretimi, takip sorgulama) anında test etmenizi sağlar.
* 🪶 **Sıfır Dış Bağımlılık (Zero-Dependency):** C kütüphaneleri veya ağır paketler olmadan saf Python standart kütüphanesiyle çalışır.

---

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
git clone https://github.com/eimza-kep/turkey-cargo-api-wrapper.git
cd turkey-cargo-api-wrapper
```

### 2. Komut Satırı (CLI) Kullanımı

#### A. Koli Desi ve Faturalandırılacak Ağırlığı Hesaplayın:
```bash
python -m turkey_cargo desi --width 30 --length 40 --height 20 --weight 5.0
```
*Çıktı:*
```
📦 TÜRKİYE STANDART KARGO DESİ RAPORU
Ebatlar: 30.0 x 40.0 x 20.0 cm
Hesaplanan Hacimsel Desi: 8.0 Desi (Bölen: 3000)
Tartılan Gerçek Ağırlık: 5.0 kg
Faturalandırılacak Ağırlık: 8.0 (DESİ BAZLI)
Paket Kategorisi: 6-15 Desi / Orta Boy Koli
```

#### B. Kargo Takip Kodu Sorgulayın:
```bash
python -m turkey_cargo track --carrier aras --code ARAS123456789
```

#### C. Test Kargo Siparişi ve Barkod Verisi Üretin:
```bash
python -m turkey_cargo create --carrier yurtici --recipient "Ahmet Kaya" --city "İzmir" --desi 3.5
```

---

## 🐍 Python Kütüphanesi Olarak Kullanım

```python
from turkey_cargo import get_billable_weight, get_carrier_client

# 1. Desi Hesabı
desi_info = get_billable_weight(width_cm=35, length_cm=45, height_cm=25, actual_kg=4.2)
print(f"Faturalandırılacak: {desi_info.billable_weight} ({desi_info.charged_by})")

# 2. Kargo Gönderi Siparişi Oluşturma
client = get_carrier_client("yurtici")
shipment = client.create_shipment(
    order_number="SIP-2026-001",
    recipient_name="Mehmet Öz",
    recipient_phone="05551234567",
    city="İstanbul",
    district="Ataşehir",
    address="Barbaros Mah. No:15",
    desi=desi_info.desi
)

print(f"Takip Kodu: {shipment.tracking_number}")
print(f"Yazdırılacak Barkod: {shipment.barcode_data}")
```

---

## 📜 Lisans

Bu proje **MIT Lisansı** altında sunulmaktadır. Ticari ve kişisel e-ticaret projelerinizde serbestçe kullanabilirsiniz. Ayrıntılar için [LICENSE](LICENSE) dosyasına bakabilirsiniz.
