# 🦅 Talon Order Suite for EDMC

[![Elite Dangerous](https://img.shields.io/badge/Game-Elite%20Dangerous-orange.svg)](https://www.elitedangerous.com/)
[![EDMC Plugin](https://img.shields.io/badge/EDMC-Plugin-blue.svg)](https://github.1s/EDCD/EDMarketConnector)
[![Python](https://img.shields.io/badge/Python-3.13%2B-green.svg)](https://www.python.org/)

[Türkçe](#türkçe) | [English](#english)

---

## Türkçe

**Talon Order Suite**, Elite Dangerous oyuncuları, özellikle de PvP ve filo (squadron) operasyonları ile ilgilenenler için geliştirilmiş çok fonksiyonlu bir **EDMC (E:D Market Connector)** eklentisidir.

### ✨ Öne Çıkan Özellikler
* **Canlı Radar (Real-time Overlay):** Çatışmada hedef aldığınız düşman gemilerinin gövde (hull), kalkan ve alt sistem durumlarını anlık olarak filonuzdaki diğer üyelerle paylaşır ve ekranda yüzen şık bir overlay üzerinde gösterir.
* **KOS & Düşman Takibi:** Girdiğiniz sistemlerdeki oyuncuları otomatik olarak yerel veritabanı ve Firebase üzerinden tarar; KOS veya düşman pilotlarla karşılaşıldığında sesli alarm çalar ve Discord'a otomatik bildirim gönderir.
* **Post-Session PvP Raporu:** Geçmiş Journal loglarınızı tarayarak detaylı PvP leş (kill) raporları çıkarır, bunları HTML sayfasına dönüştürür veya Discord'a embed olarak raporlar.
* **Yedekleme Araçları (Backup Tools):** Format veya oyun çökmesi gibi durumlarda kaybolma riskine karşı Elite Dangerous log klasörünüzü ve tuş atamalarınızı (`Bindings`) tek tıkla `.zip` olarak yedeklemenizi ve geri yüklemenizi sağlar.
* **Çoklu Dil Desteği:** Arayüz üzerinden anlık olarak **Türkçe** veya **İngilizce** diline geçiş yapabilirsiniz.
* **Oto-Güncelleme (Auto-Update):** GitHub reposunu takip ederek yeni güncellemeleri otomatik algılar ve tek tıkla güncellemenize olanak tanır.

---

## English

**Talon Order Suite** is a feature-rich **EDMC (E:D Market Connector)** plugin built for Elite Dangerous pilots, specifically tailored for PvP and squadron operations.

### ✨ Key Features
* **Live Target Radar (Overlay):** Real-time tracking of targeted hostile ships' hull, shield, and subsystem health, synchronized with squadron members via a floating overlay panel.
* **KOS & Enemy Tracker:** Automatically cross-references pilots in your system with a synchronized database, triggering audio alerts and Discord webhooks upon encountering hostile commanders.
* **Post-Session PvP Report:** Scans your flight logs to generate comprehensive PvP kill statistics, outputting clean HTML reports or formatted Discord embeds.
* **Backup & Restore Tools:** Protect your hard-earned progress and custom configurations by backing up and restoring your ED Journal logs and control bindings (`Bindings`) into a `.zip` archive with a single click.
* **Multi-Language Support:** Fully switchable between **English** and **Turkish** interfaces dynamically.
* **Auto-Updater:** Automatically checks your GitHub repository for updates and prompts you to update seamlessly.

---

## 📥 Kurulum / Installation

1. EDMC uygulamasının kapalı olduğundan emin olun.
2. Bu repodaki dosyaları indirin ve EDMC'nin eklenti dizinine (`%LOCALAPPDATA%\EDMarketConnector\plugins\`) **"Kos Tracker"** adında bir klasör açarak içine atın.
3. EDMC'yi başlatın; eklenti otomatik olarak yüklenecek ve `kos_database.json` dosyasını oluşturacaktır.
4. Ayarlar menüsünden Firebase bağlantı adresinizi, şifrelerinizi ve Discord Webhook URL'lerinizi yapılandırın.

---
*Developed by Cmdr Yu-gen (Talon Order)*
