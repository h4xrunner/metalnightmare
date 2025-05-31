# Metal Nightmare - Melee Survival

## Proje Özeti

Metal Nightmare, yukarıdan görünüşlü, yakın dövüş odaklı bir hayatta kalma oyunudur. Oyuncu, zombilerle dolu şehir sokaklarında kılıcıyla hayatta kalmaya çalışır. Fare imlecine göre saldırı yönünü otomatik belirler ve farklı saldırı animasyonları oynatır. Zombiler bağımsız hızlara ve yapay zekaya sahiptir, oyuncuyu kovalayıp saldırırlar. Zombiler hasar aldıklarında sersemleyip geri savrulur, öldüklerinde ölüm animasyonlarını oynatıp kaybolurlar.

## Özellikler

- Tam animasyonlu yürüyüş, idle ve saldırı sistemi
- Fareye göre otomatik saldırı yönü
- Her zombinin bağımsız hızı (takip algoritmalarıayne ve greddy follow eksen odaklı)
- Hasar alınca kan efekti (blood overlay) screen vincetting
- Ölüm animasyonu sistemi 10 frame -1. aldığım bir hatadan dolayı bir frame eksilttim
- Tam müzik ve ses kontrolü (menü ve oyun için ayrı müzikler)
- Ses kapatma ve açma sistemi (toggle)

## Kontroller

| Tuş | İşlev |
|-----|-------|
| W / A / S / D | Hareket |
| Space | Saldırı (yakın dövüş kılıç) |
| Fare | Saldırı yönünü belirler |
| Mouse Click | Menü ve Game Over ekranı butonları |

Gereksinimler:

- Python 3.x
- `pgzero` kütüphanesi yüklü olmalı

**Pgzero kurulumu:**

```bash
Debian tabanlı:
pip install pgzero()


Arch Tabanlı:
sudo pacman -S python-pipx
pipx install pgzero

venv önerilmez
