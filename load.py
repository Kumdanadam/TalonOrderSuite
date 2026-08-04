import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import winsound
import requests
import threading
import logging
import time
import urllib.parse
import webbrowser
import shutil
import zipfile
import re
import traceback
from datetime import datetime, timedelta
from collections import Counter

# ==========================================
# EKLENTİ BİLGİLERİ VE GITHUB GÜNCELLEYİCİ
# ==========================================
VERSION = "1.0.1"
GITHUB_USER = "Kumdanadam"
GITHUB_REPO = "TalonOrderSuite"

PLUGIN_NAME = "Talon Order Suite"
DB_FILE = ""
PLUGIN_DIR = ""
LOG_PATH = os.path.join(os.path.expanduser("~"), "Saved Games", "Frontier Developments", "Elite Dangerous")
BINDS_PATH = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser("~")), "Frontier Developments", "Elite Dangerous", "Options", "Bindings")

# ==========================================
# ÇEVİRİ VE DİL SÖZLÜĞÜ (TRANSLATIONS)
# ==========================================
TRANSLATIONS = {
    "TR": {
        "status_waiting": "Durum: Bekleniyor...",
        "btn_discord": "Discord'a Gönder",
        "btn_update_data": "Data Güncelle",
        "btn_logbook": "Logbook",
        "btn_settings": "Ayarlar",
        "btn_pvp_report": "PvP Raporu",
        "btn_radar_on": "🟢 Canlı Radarı Aç",
        "btn_radar_off": "🔴 Canlı Radarı Kapat",
        "sync_waiting": "Son Senk: Bekleniyor...",
        "sync_last": "Son Senk: ",
        "err_read_pass": "Hata: Okuma Şifresi veya URL Girilmedi!",
        "err_read_pass_wrong": "Hata: Okuma Şifresi Yanlış!",
        "status_updated": "Durum: Veriler Güncellendi!",
        "status_db_empty": "Durum: Veritabanı boş.",
        "err_conn": "Hata: Bağlantı sorunu!",
        "msg_sent_discord": "Discord'a Gönderildi!",
        "radar_waiting": "Filo hedefleri bekleniyor...",
        "radar_drag": "(Paneli taşımak için farenin sol tuşuyla sürükleyin)",
        
        "set_kos_cmdr": "KOS Cmdr",
        "set_enemy_cmdr": "Düşman Cmdr",
        "set_enemy_squad": "Düşman Filo",
        "set_settings": "Ayarlar",
        "cmdr_name": "CMDR Adı:",
        "threat": "Tehdit:",
        "btn_add": "Ekle",
        "btn_del_selected": "Seçili Olanı Sil",
        "squad_id": "Düşman Squadron ID:",
        "btn_del_squad": "Seçili Filoyu Sil",
        "lbl_fb_url": "Firebase Sunucu URL:",
        "discord_webhook": "Discord Radar Webhook URL",
        "read_pass": "Firebase Okuma Şifresi (Tüm Üyeler İçin):",
        "admin_pass": "Firebase Admin Şifresi (Sadece Yetkililer):",
        "discord_mode": "Discord Gönderim Modu:",
        "mode_auto": "Otomatik",
        "mode_manual": "Manuel",
        "sound_alert": "Bilgisayarda Sesli Alarm Çal",
        "cooldown_text": "Uyarı bekleme süresi:",
        "cooldown_min": "dakika",
        "language": "Uygulama Dili / Language:",
        "btn_save_settings": "Ayarları Kaydet",
        "msg_saved_admin": "Ayarlar kaydedildi ve Firebase güncellendi!",
        "msg_saved_local": "Lokal ayarlar kaydedildi. (Veri yazmak için Admin Şifresi girmelisiniz)",
        
        "lb_title": "Talon Order Suite - Logbook",
        "lb_date": "Tarih / Saat",
        "lb_interaction": "Etkileşim",
        "lb_target": "Hedef [Filo]",
        "lb_status": "Durum (DB)",
        "lb_threat": "Threat",
        "lb_system": "Sistem",
        "btn_lb_send": "Seçilen Kaydı Discord'a Gönder",
        
        "pvp_title": "Talon Order Suite - PvP Raporu",
        "lbl_url": "PvP Raporu Webhook URL:",
        "lbl_avt": "Avatar URL (Opsiyonel):",
        "lbl_exc": "Hariç Tutulan Filolar (Virgülle Ayır):",
        "btn_all": "Discord (Tümü)",
        "btn_day": "Discord (Son 12s)",
        "btn_last": "Discord (SON LEŞ)",
        "btn_web_all": "Web (Tümü)",
        "btn_web_day": "Web (Son 12s)",
        "status_ready": "Sistem Hazır.",
        "log_start": "Analiz başlatıldı...",
        "log_scan": "Taranıyor:",
        "log_none": "Kriterlere uygun veri bulunamadı.",
        "log_sent": "İşleniyor...",
        "msg_ok": "Başarılı",
        "msg_sent": "İşlem tamamlandı!",
        "d_title_day": "SON 12 SAAT RAPORU",
        "d_title_all": "GENEL PVP RAPORU",
        "d_title_last": "HEDEF YOK EDİLDİ",
        "d_desc": "CMDR {0} operasyon kayıtları.",
        "d_sum": "Özet",
        "d_kill": "Toplam Leş: {0}",
        "d_top_p": "En Çok Öldürülenler",
        "d_top_s": "En Çok Vurulan Filolar",
        "d_last": "Son Leşler",
        "d_list_full": "Tam Leş Listesi",
        "d_no_data": "-",
        "d_sq_kill": "üye",
        "lbl_tools": "--- Yedekleme Araçları ---",
        "btn_backup_logs": "Logları Yedekle",
        "btn_restore_logs": "Logları Yükle",
        "btn_backup_binds": "Binds Yedekle",
        "btn_restore_binds": "Binds Yükle",
        "msg_backup_done": "Yedekleme başarıyla oluşturuldu:\n{0}",
        "msg_restore_done": "Geri yükleme işlemi başarıyla tamamlandı!",
        "err_folder_not_found": "Klasör bulunamadı:\n{0}",
        "update_found": "🚀 v{0} Güncellemesi Hazır! (Tıkla)",
        "update_success": "Başarıyla güncellendi! Lütfen EDMC'yi tamamen kapatıp yeniden açın.",
        "update_error": "Güncelleme başarısız:"
    },
    "EN": {
        "status_waiting": "Status: Waiting...",
        "btn_discord": "Send to Discord",
        "btn_update_data": "Update Data",
        "btn_logbook": "Logbook",
        "btn_settings": "Settings",
        "btn_pvp_report": "PvP Report",
        "btn_radar_on": "🟢 Turn On Live Radar",
        "btn_radar_off": "🔴 Turn Off Live Radar",
        "sync_waiting": "Last Sync: Waiting...",
        "sync_last": "Last Sync: ",
        "err_read_pass": "Error: URL or Read Pass Missing!",
        "err_read_pass_wrong": "Error: Wrong Read Password!",
        "status_updated": "Status: Data Updated!",
        "status_db_empty": "Status: Database is empty.",
        "err_conn": "Error: Connection issue!",
        "msg_sent_discord": "Sent to Discord!",
        "radar_waiting": "Waiting for squad targets...",
        "radar_drag": "(Drag with left mouse button to move)",
        
        "set_kos_cmdr": "KOS Cmdr",
        "set_enemy_cmdr": "Enemy Cmdr",
        "set_enemy_squad": "Enemy Squad",
        "set_settings": "Settings",
        "cmdr_name": "CMDR Name:",
        "threat": "Threat:",
        "btn_add": "Add",
        "btn_del_selected": "Delete Selected",
        "squad_id": "Enemy Squadron ID:",
        "btn_del_squad": "Delete Selected Squad",
        "lbl_fb_url": "Firebase Database URL:",
        "discord_webhook": "Discord Radar Webhook URL",
        "read_pass": "Firebase Read Password (For All Members):",
        "admin_pass": "Firebase Admin Password (Officers Only):",
        "discord_mode": "Discord Posting Mode:",
        "mode_auto": "Auto",
        "mode_manual": "Manual",
        "sound_alert": "Play Sound Alert on PC",
        "cooldown_text": "Alert Cooldown:",
        "cooldown_min": "minutes",
        "language": "Uygulama Dili / Language:",
        "btn_save_settings": "Save Settings",
        "msg_saved_admin": "Settings saved and Firebase updated!",
        "msg_saved_local": "Local settings saved. (Enter Admin Pass to push data)",
        
        "lb_title": "Talon Order Suite - Logbook",
        "lb_date": "Date / Time",
        "lb_interaction": "Interaction",
        "lb_target": "Target [Squad]",
        "lb_status": "Status (DB)",
        "lb_threat": "Threat",
        "lb_system": "System",
        "btn_lb_send": "Send Selected Entry to Discord",
        
        "pvp_title": "Talon Order Suite - PvP Report",
        "lbl_url": "PvP Report Webhook URL:",
        "lbl_avt": "Avatar URL (Optional):",
        "lbl_exc": "Excluded Squadrons (Comma separated):",
        "btn_all": "Discord (All)",
        "btn_day": "Discord (Last 12h)",
        "btn_last": "Discord (LAST KILL)",
        "btn_web_all": "Web (All)",
        "btn_web_day": "Web (Last 12h)",
        "status_ready": "System Ready.",
        "log_start": "Analysis started...",
        "log_scan": "Scanning:",
        "log_none": "No data found matching criteria.",
        "log_sent": "Processing...",
        "msg_ok": "Success",
        "msg_sent": "Operation completed!",
        "d_title_day": "LAST 12 HOURS REPORT",
        "d_title_all": "OVERALL PVP REPORT",
        "d_title_last": "TARGET DESTROYED",
        "d_desc": "CMDR {0} operational logs.",
        "d_sum": "Summary",
        "d_kill": "Total Kills: {0}",
        "d_top_p": "Top Victims",
        "d_top_s": "Top Hit Squadrons",
        "d_last": "Recent Kills",
        "d_list_full": "Full Kill List",
        "d_no_data": "-",
        "d_sq_kill": "members",
        "lbl_tools": "--- Backup Tools ---",
        "btn_backup_logs": "Backup Logs",
        "btn_restore_logs": "Restore Logs",
        "btn_backup_binds": "Backup Binds",
        "btn_restore_binds": "Restore Binds",
        "msg_backup_done": "Backup successfully created at:\n{0}",
        "msg_restore_done": "Restore operation completed successfully!",
        "err_folder_not_found": "Folder not found:\n{0}",
        "update_found": "🚀 Update Ready: v{0} (Click Here)",
        "update_success": "Successfully updated! Please completely close and restart EDMC.",
        "update_error": "Update failed:"
    }
}

kos_data = {
    "enemy_cmdrs": {},   
    "kos_cmdrs": {},     
    "enemy_squads": [],  
    "firebase_url": "",
    "webhook_url": "",          
    "pvp_webhook_url": "",      
    "sound_enabled": True,
    "cooldown_minutes": 5,
    "post_mode": "Oto",
    "read_password": "",
    "admin_password": "",
    "pvp_avatar": "",
    "pvp_exclude": "",
    "language": "TR" 
}

def t(key):
    lang = kos_data.get("language", "TR")
    return TRANSLATIONS.get(lang, TRANSLATIONS["TR"]).get(key, key)

# ==========================================
# GÜNCEL EDMC & GLOBAL DEĞİŞKENLER
# ==========================================
last_alert_times = {}
last_log_times = {}
interaction_log = []
last_detected_msg = ""
edmc_status_label = None
edmc_post_button = None
edmc_sync_label = None
edmc_app_frame = None
radar_btn = None
b1, b2, b3, b4 = None, None, None, None
logbook_window = None
ui_window = None
pvp_tracker_window = None
logo_image = None
is_radar_active = False
active_overlay = None
my_cmdr_name = ""

# ==========================================
# OTO-GÜNCELLEME SİSTEMİ (AUTO-UPDATE)
# ==========================================
def check_for_updates():
    if not GITHUB_USER or GITHUB_USER == "SeninKullaniciAdinBuraya": return
    
    while edmc_app_frame is None:
        time.sleep(1)
        
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/load.py?t={int(time.time())}"
    
    try:
        resp = requests.get(url, timeout=5)
        
        if resp.status_code == 404:
            url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/master/load.py?t={int(time.time())}"
            resp = requests.get(url, timeout=5)
            
        if resp.status_code == 200:
            remote_code = resp.text
            match = re.search(r'VERSION\s*=\s*"([^"]+)"', remote_code)
            if match:
                remote_version = match.group(1)
                if remote_version != VERSION:
                    show_update_button(remote_version, remote_code)
    except Exception as e:
        logging.error(f"Talon Order Update Check Error: {e}")

def show_update_button(new_ver, code):
    def apply_update():
        try:
            with open(__file__, 'w', encoding='utf-8') as f:
                f.write(code)
            messagebox.showinfo("Talon Order Suite", t("update_success"))
        except Exception as e:
            logging.error(f"Talon Order Apply Update Error: {traceback.format_exc()}")
            messagebox.showerror("Error", f"{t('update_error')} {e}")
            
    if edmc_app_frame:
        edmc_app_frame.after(0, lambda: _create_update_btn(new_ver, apply_update))

def _create_update_btn(new_ver, cmd):
    btn = tk.Button(edmc_app_frame, text=t("update_found").format(new_ver), bg="#4CAF50", fg="white", font=("Arial", 9, "bold"), command=cmd, width=34)
    btn.pack(side=tk.TOP, pady=2)


# ==========================================
# EDMC & FIREBASE FONKSİYONLARI
# ==========================================
def plugin_start3(plugin_dir):
    global DB_FILE, kos_data, PLUGIN_DIR
    PLUGIN_DIR = plugin_dir
    DB_FILE = os.path.join(plugin_dir, "kos_database.json")
    
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
            kos_data.update(loaded_data)
    else:
        save_db_local()
        
    threading.Thread(target=sync_from_firebase_loop, daemon=True).start()
    threading.Thread(target=live_target_listener, daemon=True).start()
    threading.Thread(target=check_for_updates, daemon=True).start()
    
    return PLUGIN_NAME

def plugin_stop():
    base_url = kos_data.get("firebase_url", "").strip().rstrip('/')
    rp = kos_data.get("read_password", "").strip()
    if base_url and rp and my_cmdr_name:
        safe_cmdr = my_cmdr_name.upper().replace(".", "_").replace("#", "_").replace("$", "_").replace("[", "_").replace("]", "_")
        url = f"{base_url}/{rp}/live_targets/CMDR_{safe_cmdr}.json"
        try: requests.delete(url, timeout=2)
        except: pass

def save_db_local():
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(kos_data, f, indent=4)

def update_status_label(text, color):
    if edmc_status_label:
        edmc_status_label.after(0, lambda: edmc_status_label.config(text=text, fg=color))

def update_sync_label():
    if edmc_sync_label:
        current_time_str = time.strftime("%d.%m.%Y %H:%M:%S")
        edmc_sync_label.after(0, lambda: edmc_sync_label.config(text=f"{t('sync_last')}{current_time_str}"))

def refresh_main_ui_texts():
    if edmc_status_label: edmc_status_label.config(text=t("status_waiting"))
    if edmc_post_button: edmc_post_button.config(text=t("btn_discord"))
    if edmc_sync_label: edmc_sync_label.config(text=t("sync_waiting"))
    if b1: b1.config(text=t("btn_update_data"))
    if b2: b2.config(text=t("btn_logbook"))
    if b3: b3.config(text=t("btn_settings"))
    if b4: b4.config(text=t("btn_pvp_report"))
    if radar_btn: radar_btn.config(text=t("btn_radar_off") if is_radar_active else t("btn_radar_on"))

def get_firebase_url():
    base_url = kos_data.get("firebase_url", "").strip().rstrip('/')
    rp = kos_data.get("read_password", "").strip()
    if not base_url or not rp: return None
    return f"{base_url}/{rp}.json"

def sync_from_firebase_loop():
    while True:
        url = get_firebase_url()
        if url:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200 and response.json() is not None:
                    cloud_data = response.json()
                    kos_data["enemy_cmdrs"] = cloud_data.get("enemy_cmdrs", {})
                    kos_data["kos_cmdrs"] = cloud_data.get("kos_cmdrs", {})
                    kos_data["enemy_squads"] = cloud_data.get("enemy_squads", [])
                    kos_data["webhook_url"] = cloud_data.get("webhook_url", kos_data.get("webhook_url", ""))
                    save_db_local()
                    update_sync_label()
            except Exception as e: 
                logging.error(f"Sync Loop Error: {e}")
        time.sleep(600)

def manual_sync_action():
    url = get_firebase_url()
    if not url:
        update_status_label(t("err_read_pass"), "red")
        return

    try:
        response = requests.get(url, timeout=10)
        if response.status_code in [401, 403]:
            update_status_label(t("err_read_pass_wrong"), "red")
            return
        elif response.status_code == 200 and response.json() is not None:
            cloud_data = response.json()
            kos_data["enemy_cmdrs"] = cloud_data.get("enemy_cmdrs", {})
            kos_data["kos_cmdrs"] = cloud_data.get("kos_cmdrs", {})
            kos_data["enemy_squads"] = cloud_data.get("enemy_squads", [])
            kos_data["webhook_url"] = cloud_data.get("webhook_url", kos_data.get("webhook_url", ""))
            
            save_db_local()
            update_status_label(t("status_updated"), "green")
            update_sync_label()
        else:
            update_status_label(t("status_db_empty"), "orange")
    except Exception as e:
        logging.error(f"Manual Sync Error: {e}")
        update_status_label(t("err_conn"), "red")

def push_to_firebase_action():
    url = get_firebase_url()
    if not url: return False, t("err_read_pass")
    admin_pass = kos_data.get("admin_password", "")
    
    data_to_push = {
        "enemy_cmdrs": kos_data["enemy_cmdrs"],
        "kos_cmdrs": kos_data["kos_cmdrs"],
        "enemy_squads": kos_data["enemy_squads"],
        "webhook_url": kos_data["webhook_url"],
        "admin_key": admin_pass 
    }
    
    try:
        response = requests.put(url, json=data_to_push, timeout=10)
        if response.status_code in [401, 403]:
            return False, "Yazma İzni Reddedildi / Write Permission Denied"
        elif response.status_code != 200:
            return False, f"Error: {response.status_code}"
        
        update_sync_label()
        return True, "OK"
    except Exception as e:
        logging.error(f"Push to Firebase Error: {e}")
        return False, f"{t('err_conn')} {e}"

def send_webhook_thread(payload):
    webhook = kos_data.get("webhook_url", "")
    if not webhook: return
    
    def _send():
        try: requests.post(webhook, json=payload)
        except Exception as e: logging.error(f"Webhook Error: {e}")
            
    threading.Thread(target=_send).start()

def manual_post_action():
    global last_detected_msg
    if last_detected_msg:
        send_webhook_thread(last_detected_msg)
        update_status_label(t("msg_sent_discord"), "green")
        if edmc_post_button:
            edmc_post_button.config(state=tk.DISABLED)
        last_detected_msg = ""


# ==========================================
# CANLI RADAR (OVERLAY) SINIFI
# ==========================================
class TargetOverlay:
    def __init__(self, parent):
        self.root = tk.Toplevel(parent.winfo_toplevel())
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 0.85)
        self.root.configure(bg='#121212')
        
        self.x = 0
        self.y = 0
        
        window_width = 450
        window_height = 80
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int(screen_height / 8)
        self.root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        
        self.frame = tk.Frame(self.root, bg='#121212', highlightbackground="#ff9d00", highlightthickness=2)
        self.frame.pack(expand=True, fill='both')
        
        self.text_widget = tk.Text(self.frame, bg='#121212', fg='white', font=("Arial", 10, "bold"), bd=0, highlightthickness=0)
        self.text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.text_widget.tag_config('default', foreground='gray')
        self.text_widget.tag_config('cmdr', foreground='#00ff00') 
        self.text_widget.tag_config('target', foreground='#ff4444') 
        self.text_widget.tag_config('ship', foreground='yellow')
        self.text_widget.tag_config('hull', foreground='orange')
        self.text_widget.tag_config('shield', foreground='#33b5e5') 
        self.text_widget.tag_config('subtarget', foreground='#00ff00') 
        self.text_widget.config(state=tk.DISABLED)
        
        for widget in (self.root, self.frame, self.text_widget):
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<ButtonRelease-1>", self.stop_move)
            widget.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        if self.x is not None and self.y is not None:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{x}+{y}")
        
    def update_info(self, targets_data):
        def task():
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.delete('1.0', tk.END)
            
            if not targets_data:
                self.text_widget.insert(tk.END, f"{t('radar_waiting')}\n", 'default')
                self.text_widget.insert(tk.END, f"{t('radar_drag')}", 'default')
                new_height = 80
            else:
                for item in targets_data:
                    self.text_widget.insert(tk.END, f"[{item['cmdr'].upper()}] -> ", 'cmdr')
                    self.text_widget.insert(tk.END, f"{item['target'].upper()}\n", 'target')
                    
                    self.text_widget.insert(tk.END, f"{item['ship']} ", 'ship')
                    if item.get('hull') is not None:
                        self.text_widget.insert(tk.END, f"| Hull: %{int(item['hull'])} ", 'hull')
                    if item.get('shield') is not None:
                        self.text_widget.insert(tk.END, f"| Shld: %{int(item['shield'])} ", 'shield')
                    if item.get('subsys') and item.get('sub_health') is not None:
                        self.text_widget.insert(tk.END, f"| {item['subsys']}: %{int(item['sub_health'])}", 'subtarget')
                        
                    self.text_widget.insert(tk.END, "\n\n")
                
                new_height = len(targets_data) * 55 + 20 

            current_geom = self.root.geometry()
            if '+' in current_geom:
                parts = current_geom.split('+')
                if len(parts) >= 3:
                    x = parts[1]
                    y = parts[2]
                    self.root.geometry(f"450x{new_height}+{x}+{y}")
                    
            self.text_widget.config(state=tk.DISABLED)
        self.root.after(0, task)
        
    def destroy(self):
        self.root.destroy()

def push_live_target(target_name=None, ship_type="", hull=None, shield=None, subsys="", sub_health=None):
    base_url = kos_data.get("firebase_url", "").strip().rstrip('/')
    rp = kos_data.get("read_password", "").strip()
    if not base_url or not rp or not my_cmdr_name: return
    
    safe_cmdr = my_cmdr_name.upper().replace(".", "_").replace("#", "_").replace("$", "_").replace("[", "_").replace("]", "_")
    url = f"{base_url}/{rp}/live_targets/CMDR_{safe_cmdr}.json"
    
    def _send_data():
        if target_name:
            data = {"target": target_name, "ship": ship_type, "hull": hull, "shield": shield, "subsys": subsys, "sub_health": sub_health, "timestamp": time.time()}
            try: requests.put(url, json=data, timeout=3)
            except Exception as e: logging.error(f"Live Target Push Error: {e}")
        else:
            try: requests.delete(url, timeout=3)
            except Exception as e: logging.error(f"Live Target Delete Error: {e}")

    threading.Thread(target=_send_data, daemon=True).start()

def live_target_listener():
    global is_radar_active, active_overlay
    while True:
        if is_radar_active and active_overlay:
            base_url = kos_data.get("firebase_url", "").strip().rstrip('/')
            rp = kos_data.get("read_password", "").strip()
            if base_url and rp:
                url = f"{base_url}/{rp}/live_targets.json"
                try:
                    resp = requests.get(url, timeout=3)
                    if resp.status_code == 200:
                        data = resp.json()
                        active_data = []
                        if isinstance(data, dict):
                            for cmdr_key, t_data in data.items():
                                if isinstance(t_data, dict) and cmdr_key.startswith("CMDR_"):
                                    if time.time() - t_data.get("timestamp", 0) < 300:
                                        t_data_copy = t_data.copy()
                                        t_data_copy['cmdr'] = cmdr_key.replace("CMDR_", "")
                                        active_data.append(t_data_copy)
                        if active_overlay: active_overlay.update_info(active_data)
                except Exception as e: 
                    logging.error(f"Live Listener Polling Error: {e}")
        time.sleep(1.5)

def trigger_alert(name, status_str, max_threat, system, interaction_type):
    global last_detected_msg
    if kos_data.get("sound_enabled", True): winsound.Beep(1000, 400); winsound.Beep(1500, 400)
    
    embed_color = 16711680 
    if "KOS" in status_str: embed_color = 0 
    elif "Temiz" in status_str or "Clean" in status_str: embed_color = 65280 
        
    embed_payload = {
        "title": "🚨 TALON ORDER ALERT 🚨",
        "color": embed_color,
        "fields": [
            {"name": "🎯 Target", "value": f"**{name}**", "inline": True},
            {"name": "📍 System", "value": system, "inline": True},
            {"name": "⚔️ Interaction", "value": interaction_type, "inline": True},
            {"name": "📋 Status", "value": status_str, "inline": True}
        ],
        "footer": {"text": "Talon Order Enemy Tracker"}
    }
    
    if max_threat > 0: embed_payload["fields"].append({"name": "💀 Threat Lvl", "value": str(max_threat), "inline": True})
        
    last_detected_msg = {"embeds": [embed_payload]}
    hud_threat_info = f"[Lvl {max_threat}]" if max_threat > 0 else ""
    short_status = status_str.replace(" CMDR", "").replace(" Filosu", "").replace(" Squad", "")
    hud_text = f"{name} | {short_status} {hud_threat_info}"
    
    if kos_data.get("post_mode", "Oto") == "Manuel":
        update_status_label(f"Target: {hud_text}", "orange")
        if edmc_post_button: edmc_post_button.after(0, lambda: edmc_post_button.config(state=tk.NORMAL))
    else:
        update_status_label(f"Auto Post: {hud_text}", "green")
        send_webhook_thread(last_detected_msg)

def journal_entry(cmdr, is_beta, system, station, entry, state):
    global my_cmdr_name
    my_cmdr_name = cmdr
    event = entry.get("event")
    
    if event == "ShipTargeted" and is_radar_active:
        pilot_raw = entry.get("PilotName", "")
        if entry.get("TargetLocked") and pilot_raw.startswith("$cmdr_decorate"):
            ship_type = entry.get("Ship_Localised", entry.get("Ship", "Unknown Ship"))
            shield = entry.get("ShieldHealth")
            hull = entry.get("HullHealth")
            subsys = entry.get("Subsystem_Localised", entry.get("Subsystem"))
            sub_health = entry.get("SubsystemHealth")
            clean_name = pilot_raw.replace("$cmdr_decorate:#name=", "").replace(";", "")
            push_live_target(clean_name, ship_type, hull, shield, subsys, sub_health)
        else:
            push_live_target(None)
            
    pilot_raw = ""
    squad_raw = ""
    interaction_type = ""
    
    if event == "ShipTargeted" and entry.get("TargetLocked"):
        pilot_raw = entry.get("PilotName", "")
        squad_raw = entry.get("SquadronID", "")
        interaction_type = "Targeting"
    elif event == "Interdicted" and entry.get("IsPlayer"):
        pilot_raw = entry.get("Interdictor", "")
        interaction_type = "Interdicted You"
    elif event == "Interdiction" and entry.get("IsPlayer"):
        pilot_raw = entry.get("Interdicted", "")
        interaction_type = "You Interdicted"

    if not pilot_raw or pilot_raw.startswith("$ShipName"): return

    if pilot_raw.startswith("$cmdr_decorate:#name="): pilot = pilot_raw.replace("$cmdr_decorate:#name=", "").replace(";", "").strip().lower()
    else: pilot = pilot_raw.strip().lower()
        
    squad = squad_raw.strip().lower() if squad_raw else ""
    sys_name = system if system else "Deep Space"

    status_list = []
    max_threat = 0
    
    if pilot in kos_data["kos_cmdrs"]:
        status_list.append("KOS")
        max_threat = max(max_threat, kos_data["kos_cmdrs"][pilot])
        
    if pilot in kos_data["enemy_cmdrs"]:
        status_list.append("Enemy")
        max_threat = max(max_threat, kos_data["enemy_cmdrs"][pilot])
        
    if squad:
        saved_squads = [s.lower().strip() for s in kos_data.get("enemy_squads", [])]
        if squad in saved_squads:
            status_list.append(f"Squad ({squad.upper()})")

    status_str = " + ".join(status_list) if status_list else "Clean"
    display_name = f"{pilot.upper()} [{squad.upper()}]" if squad else pilot.upper()
    current_time = time.time()
    
    log_key = f"{pilot}_{interaction_type}"
    if log_key not in last_log_times or (current_time - last_log_times[log_key] > 10):
        log_item = {
            "time": time.strftime("%d.%m.%Y %H:%M:%S"),
            "type": interaction_type,
            "cmdr": display_name,
            "status": status_str,
            "threat": max_threat,
            "system": sys_name
        }
        interaction_log.insert(0, log_item)
        if len(interaction_log) > 100: interaction_log.pop()
        last_log_times[log_key] = current_time

    if not status_list: return 
        
    target_key = pilot if pilot else f"SQUAD_{squad}"
    cooldown_seconds = int(kos_data.get("cooldown_minutes", 5)) * 60

    if target_key in last_alert_times:
        if current_time - last_alert_times[target_key] < cooldown_seconds: return

    last_alert_times[target_key] = current_time
    trigger_alert(display_name, status_str, max_threat, sys_name, interaction_type)


# ==========================================
# POST-SESSION PVP TRACKER & BACKUP
# ==========================================
COLOR_BG = "#2b2b2b"
COLOR_FG = "#e0e0e0"
COLOR_ENTRY_BG = "#404040"
COLOR_ENTRY_FG = "#ffffff"
COLOR_BTN_DISC = "#5865F2"
COLOR_BTN_WEB = "#D35400"
COLOR_BTN_ALERT = "#C0392B"
COLOR_ACCENT = "#4fc3f7"
COLOR_CREDIT = "#808080" 
DEF_AVATAR = "https://i.imgur.com/Y2e1l1e.png"

POWER_COLORS = {
    "Jerome Archer": "#FF00FF", "Nakato Kaine": "#CCFF00", "Zemina Torval": "#0077FF",
    "Yuri Grom": "#FF8800", "Pranav Antal": "#FFCC00", "Li Yong-Rui": "#00FF88",
    "Felicia Winters": "#A5682A", "Edmund Mahon": "#008800", "Denton Patreus": "#00FFFF",
    "Archon Delaine": "#FF0000", "Aisling Duval": "#00CCFF", "Arissa Lavigny-Duval": "#9900FF",
    "A. Lavigny-Duval": "#9900FF", "Zachary Hudson": "#B20000"
}
POWER_SHORT = {
    "A. Lavigny-Duval": "ALD", "Arissa Lavigny-Duval": "ALD", "Zachary Hudson": "Hudson",
    "Felicia Winters": "Winters", "Aisling Duval": "Aisling", "Li Yong-Rui": "LYR",
    "Denton Patreus": "Patreus", "Zemina Torval": "Torval", "Pranav Antal": "Antal",
    "Archon Delaine": "Delaine", "Yuri Grom": "Grom", "Edmund Mahon": "Mahon",
    "Nakato Kaine": "Kaine", "Jerome Archer": "Archer"
}
RANKS = {0:"Harmless",1:"Mostly Harmless",2:"Novice",3:"Competent",4:"Expert",5:"Master",6:"Dangerous",7:"Deadly",8:"Elite",9:"Elite I",10:"Elite II",11:"Elite III",12:"Elite IV",13:"Elite V"}

class PvPTrackerUI:
    def __init__(self, root):
        self.root = root
        self.root.title(t("pvp_title"))
        self.root.geometry("460x760") 
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)
        self.root.attributes('-topmost', True)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.cmdr_name = my_cmdr_name if my_cmdr_name else "Unknown"

        input_frame = tk.Frame(root, bg=COLOR_BG)
        input_frame.pack(padx=15, pady=15, fill="x")

        self.lbl_url = tk.Label(input_frame, text=t("lbl_url"), anchor="w", bg=COLOR_BG, fg=COLOR_FG)
        self.lbl_url.pack(fill="x")
        self.ent_url = tk.Entry(input_frame, bg=COLOR_ENTRY_BG, fg=COLOR_ENTRY_FG, insertbackground="white", relief="flat")
        self.ent_url.pack(fill="x", pady=(2, 10), ipady=3)

        self.lbl_avt = tk.Label(input_frame, text=t("lbl_avt"), anchor="w", bg=COLOR_BG, fg=COLOR_FG)
        self.lbl_avt.pack(fill="x")
        self.ent_avatar = tk.Entry(input_frame, bg=COLOR_ENTRY_BG, fg=COLOR_ENTRY_FG, insertbackground="white", relief="flat")
        self.ent_avatar.pack(fill="x", pady=(2, 10), ipady=3)

        self.lbl_exc = tk.Label(input_frame, text=t("lbl_exc"), anchor="w", bg=COLOR_BG, fg=COLOR_FG)
        self.lbl_exc.pack(fill="x")
        self.ent_exclude = tk.Entry(input_frame, bg=COLOR_ENTRY_BG, fg=COLOR_ENTRY_FG, insertbackground="white", relief="flat")
        self.ent_exclude.pack(fill="x", pady=(2, 5), ipady=3)

        self.load_config()
        
        self.lbl_cmdr = tk.Label(root, text=f"👤 CMDR: {self.cmdr_name}", fg=COLOR_ACCENT, bg=COLOR_BG, font=("Segoe UI", 11, "bold"))
        self.lbl_cmdr.pack(pady=5)

        btn_frame_disc = tk.Frame(root, bg=COLOR_BG)
        btn_frame_disc.pack(pady=2)
        btn_style = {"fg": "white", "font": ("Segoe UI", 8, "bold"), "width": 16, "relief": "flat"}
        
        self.b_disc_all = tk.Button(btn_frame_disc, text=t("btn_all"), bg=COLOR_BTN_DISC, command=lambda: self.start('ALL', 'DISCORD'), **btn_style)
        self.b_disc_all.pack(side="left", padx=5)
        self.b_disc_day = tk.Button(btn_frame_disc, text=t("btn_day"), bg=COLOR_BTN_DISC, command=lambda: self.start('DAILY', 'DISCORD'), **btn_style)
        self.b_disc_day.pack(side="left", padx=5)

        btn_frame_web = tk.Frame(root, bg=COLOR_BG)
        btn_frame_web.pack(pady=5)
        self.b_web_all = tk.Button(btn_frame_web, text=t("btn_web_all"), bg=COLOR_BTN_WEB, command=lambda: self.start('ALL', 'WEB'), **btn_style)
        self.b_web_all.pack(side="left", padx=5)
        self.b_web_day = tk.Button(btn_frame_web, text=t("btn_web_day"), bg=COLOR_BTN_WEB, command=lambda: self.start('DAILY', 'WEB'), **btn_style)
        self.b_web_day.pack(side="left", padx=5)

        btn_frame_alert = tk.Frame(root, bg=COLOR_BG)
        btn_frame_alert.pack(pady=5)
        self.b_disc_last = tk.Button(btn_frame_alert, text=t("btn_last"), bg=COLOR_BTN_ALERT, command=lambda: self.start('LAST_ONE', 'DISCORD'), **btn_style)
        self.b_disc_last.pack()

        tools_frame = tk.Frame(root, bg=COLOR_BG)
        tools_frame.pack(pady=5)
        lbl_tools = tk.Label(tools_frame, text=t("lbl_tools"), bg=COLOR_BG, fg=COLOR_CREDIT)
        lbl_tools.grid(row=0, column=0, columnspan=2, pady=(0,5))
        
        btn_bkp_log = tk.Button(tools_frame, text=t("btn_backup_logs"), bg="#607D8B", fg="white", font=("Segoe UI", 8, "bold"), width=16, relief="flat", command=lambda: self.backup(LOG_PATH, "ED_Logs"))
        btn_rst_log = tk.Button(tools_frame, text=t("btn_restore_logs"), bg="#455A64", fg="white", font=("Segoe UI", 8, "bold"), width=16, relief="flat", command=lambda: self.restore(LOG_PATH))
        
        btn_bkp_bnd = tk.Button(tools_frame, text=t("btn_backup_binds"), bg="#8D6E63", fg="white", font=("Segoe UI", 8, "bold"), width=16, relief="flat", command=lambda: self.backup(BINDS_PATH, "ED_Binds"))
        btn_rst_bnd = tk.Button(tools_frame, text=t("btn_restore_binds"), bg="#5D4037", fg="white", font=("Segoe UI", 8, "bold"), width=16, relief="flat", command=lambda: self.restore(BINDS_PATH))
        
        btn_bkp_log.grid(row=1, column=0, padx=5, pady=2, sticky="ew")
        btn_rst_log.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        btn_bkp_bnd.grid(row=2, column=0, padx=5, pady=2, sticky="ew")
        btn_rst_bnd.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        log_frame = tk.Frame(root)
        log_frame.pack(padx=15, pady=(15, 5))
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_box = tk.Text(log_frame, width=53, height=8, state='disabled', font=("Consolas", 9), bg=COLOR_ENTRY_BG, fg="#00ff00", relief="flat", yscrollcommand=scrollbar.set)
        self.log_box.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.log_box.yview)

        self.lbl_credit = tk.Label(root, text="ED PvP Tracker by Cmdr Yu-gen", bg=COLOR_BG, fg=COLOR_CREDIT, font=("Segoe UI", 8))
        self.lbl_credit.pack(side="bottom", anchor="e", padx=15, pady=(0, 10))

        self.find_cmdr()
        self.log(t("status_ready"))

    def on_close(self):
        self.save_config()
        self.root.destroy()

    def backup(self, src_folder, name_prefix):
        if not os.path.exists(src_folder):
            messagebox.showerror("Error", t("err_folder_not_found").format(src_folder), parent=self.root)
            return
        save_path = filedialog.asksaveasfilename(parent=self.root, defaultextension=".zip", initialfile=f"{name_prefix}_Backup_{datetime.now().strftime('%Y%m%d')}", title=t("btn_backup_logs"))
        if save_path:
            try:
                shutil.make_archive(save_path.replace('.zip', ''), 'zip', src_folder)
                self.log(t("msg_backup_done").format(save_path))
                messagebox.showinfo("OK", t("msg_backup_done").format(save_path), parent=self.root)
            except Exception as e:
                logging.error(f"Backup Error: {traceback.format_exc()}")
                messagebox.showerror("Error", str(e), parent=self.root)

    def restore(self, dest_folder):
        zip_path = filedialog.askopenfilename(parent=self.root, filetypes=[("ZIP Files", "*.zip")], title=t("btn_restore_logs"))
        if zip_path:
            try:
                if not os.path.exists(dest_folder): os.makedirs(dest_folder)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref: zip_ref.extractall(dest_folder)
                self.log(t("msg_restore_done"))
                messagebox.showinfo("OK", t("msg_restore_done"), parent=self.root)
            except Exception as e:
                logging.error(f"Restore Error: {traceback.format_exc()}")
                messagebox.showerror("Error", str(e), parent=self.root)

    def log(self, msg):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, f"> {msg}\n")
        self.log_box.see(tk.END)
        self.log_box.config(state='disabled')

    def load_config(self):
        self.ent_url.insert(0, kos_data.get("pvp_webhook_url", ""))
        self.ent_avatar.insert(0, kos_data.get("pvp_avatar", ""))
        self.ent_exclude.insert(0, kos_data.get("pvp_exclude", ""))

    def save_config(self):
        kos_data["pvp_webhook_url"] = self.ent_url.get()
        kos_data["pvp_avatar"] = self.ent_avatar.get()
        kos_data["pvp_exclude"] = self.ent_exclude.get()
        save_db_local()

    def find_cmdr(self):
        if not os.path.exists(LOG_PATH): return
        try:
            files = sorted([f for f in os.listdir(LOG_PATH) if f.startswith("Journal") and f.endswith(".log")], key=lambda x: os.path.getmtime(os.path.join(LOG_PATH, x)), reverse=True)
            for lf in files[:20]:
                try:
                    with open(os.path.join(LOG_PATH, lf), 'r', encoding='utf-8', errors='replace') as f:
                        for line in f:
                            if '"event":"Commander"' in line or '"event":"LoadGame"' in line:
                                data = json.loads(line)
                                if "Commander" in data:
                                    self.cmdr_name = data["Commander"]
                                    if hasattr(self, 'lbl_cmdr'): self.lbl_cmdr.config(text=f"👤 CMDR: {self.cmdr_name}")
                                    return
                except: continue
        except: pass

    def start(self, mode, target):
        if target == 'DISCORD' and not self.ent_url.get().startswith("http"): 
            return messagebox.showerror("Error", "Please enter a valid Discord Webhook URL.", parent=self.root)
        self.save_config()
        ex_str = self.ent_exclude.get()
        excluded_list = [x.strip().upper() for x in ex_str.split(',') if x.strip()]
        for b in [self.b_disc_all, self.b_disc_day, self.b_disc_last, self.b_web_all, self.b_web_day]:
            b.config(state="disabled")
        threading.Thread(target=self.process, args=(mode, target, excluded_list), daemon=True).start()

    def get_link(self, name, t):
        if not name or name == "Yok": return ""
        safe_name = urllib.parse.quote(name)
        if t == 'sq': return f"https://inara.cz/elite/squadrons-search/?search={safe_name}"
        else: return f"https://inara.cz/elite/search/?search={safe_name}"

    def escape_markdown(self, text):
        if not text: return text
        special_chars = ['[', ']', '(', ')', '*', '_', '`', '~']
        for char in special_chars: text = text.replace(char, f'\\{char}')
        return text

    def get_safe_desktop_path(self):
        home = os.path.expanduser("~")
        paths_to_check = [
            os.path.join(home, "Desktop"),
            os.path.join(home, "OneDrive", "Desktop"),
            os.path.join(home, "Masaüstü"),
            os.path.join(home, "OneDrive", "Masaüstü")
        ]
        for p in paths_to_check:
            if os.path.exists(p): return p
        return os.getcwd()

    def process(self, mode, target, excluded_list):
        self.log(t("log_start"))
        kills, sq_map, power_map, ship_map = [], {}, {}, {}
        
        now = datetime.now()
        cutoff_time = now - timedelta(hours=12)
        
        try:
            if not os.path.exists(LOG_PATH): self.log("Error: Log path not found."); self.reset_btns(); return
            files = sorted([f for f in os.listdir(LOG_PATH) if f.startswith("Journal") and f.endswith(".log")], key=lambda x: os.path.getmtime(os.path.join(LOG_PATH, x)))
            
            target_files = files if mode == 'ALL' else files[-20:] 

            for i, lf in enumerate(target_files):
                if i % 10 == 0: self.log(f"{t('log_scan')} {i}/{len(target_files)}")
                try:
                    with open(os.path.join(LOG_PATH, lf), 'r', encoding='utf-8', errors='replace') as f:
                        for line in f:
                            try:
                                if '"event":"ShipTargeted"' in line:
                                    d = json.loads(line)
                                    if d.get("TargetLocked"):
                                        p_name = d.get("PilotName_Localised", "")
                                        if p_name.startswith("CMDR "): p_name = p_name[5:]
                                        if not p_name:
                                            raw = d.get("PilotName", "")
                                            if raw.startswith("$cmdr_"): p_name = raw.replace("$cmdr_", "").replace(";", "")
                                        if p_name: 
                                            if d.get("SquadronID"): sq_map[p_name.lower()] = d.get("SquadronID")
                                            if d.get("Power"): power_map[p_name.lower()] = d.get("Power")
                                            ship = d.get("Ship_Localised", d.get("Ship", ""))
                                            if ship: ship_map[p_name.lower()] = ship

                                elif '"event":"PVPKill"' in line:
                                    d = json.loads(line)
                                    dt = datetime.strptime(d.get("timestamp"), "%Y-%m-%dT%H:%M:%SZ")
                                    if mode == 'DAILY' and dt < cutoff_time: continue
                                    
                                    victim = d.get("Victim", "?")
                                    squadron = sq_map.get(victim.lower(), "Yok")
                                    if squadron.upper() in excluded_list: continue

                                    kills.append({
                                        "v": victim, 
                                        "r": RANKS.get(d.get("CombatRank",0), str(d.get("CombatRank"))), 
                                        "s": squadron, 
                                        "p": power_map.get(victim.lower(), ""), 
                                        "sh": ship_map.get(victim.lower(), "?"),
                                        "t": dt, 
                                        "ds": dt.strftime("%d-%m-%Y %H:%M"), 
                                        "ds_short": dt.strftime("%d/%m %H:%M")
                                    })
                            except: continue
                except: continue

            if not kills: self.log(t("log_none")); self.reset_btns(); return
            kills.sort(key=lambda x: x["t"], reverse=True)
            
            if mode == 'LAST_ONE' and target == 'DISCORD':
                self.send_discord_single(kills[0])
            elif target == 'DISCORD':
                top_v = Counter([k["v"] for k in kills]).most_common(10)
                top_s = Counter([k["s"] for k in kills if k["s"] != "Yok"]).most_common(10)
                self.send_discord(len(kills), kills[:10], top_v[:5], top_s[:5], mode)
            else:
                top_v = Counter([k["v"] for k in kills]).most_common(10)
                top_s = Counter([k["s"] for k in kills if k["s"] != "Yok"]).most_common(10)
                self.generate_html(len(kills), kills, top_v, top_s, mode)
            
        except Exception as e: 
            logging.error(f"PvP Tracker Process Error: {traceback.format_exc()}")
            self.log(f"Err: {e}")
        finally: self.reset_btns()

    def reset_btns(self):
        try:
            for b in [self.b_disc_all, self.b_disc_day, self.b_disc_last, self.b_web_all, self.b_web_day]:
                b.config(state="normal")
        except: pass

    def send_discord_single(self, kill_data):
        self.log(t("log_sent"))
        avatar = self.ent_avatar.get() 
        if len(avatar) < 5: avatar = DEF_AVATAR
        
        v_safe = self.escape_markdown(kill_data['v'])
        s_safe = self.escape_markdown(kill_data['s'])
        
        link_v = self.get_link(kill_data['v'], 'cmdr')
        sq_text = f"[{s_safe}]" if kill_data['s'] != "Yok" else ""
        link_s = self.get_link(kill_data['s'], 'sq') if kill_data['s'] != "Yok" else ""
        sq_display = f"**[{sq_text}]({link_s})** " if sq_text else ""
        power_text = kill_data['p'] if kill_data['p'] else "None"
        ship_text = kill_data['sh']

        embed_color = 12597547
        if kill_data['p'] in POWER_COLORS:
            try: embed_color = int(POWER_COLORS[kill_data['p']].lstrip('#'), 16)
            except: pass

        embed = {
            "title": f"🚨 {t('d_title_last')} 🚨",
            "description": f"**CMDR {self.cmdr_name}** has neutralized a hostile.",
            "color": embed_color, 
            "thumbnail": {"url": avatar},
            "fields": [
                {"name": "💀 Target", "value": f"{sq_display}**[{v_safe}]({link_v})**", "inline": True},
                {"name": "🔰 Rank", "value": f"`{kill_data['r']}`", "inline": True},
                {"name": "🚀 Ship", "value": f"`{ship_text}`", "inline": True},
                {"name": "⚡ Power", "value": f"`{power_text}`", "inline": True},
                {"name": "⏰ Time", "value": f"{kill_data['ds']}", "inline": False}
            ],
            "footer": {"text": f"ED Kill Tracker • Alert System by Cmdr Yu-gen"}
        }
        
        try:
            r = requests.post(self.ent_url.get(), json={"username": "ED Kill Tracker", "avatar_url": avatar, "embeds": [embed]})
            if r.status_code in [200, 204]:
                self.log(f"✅ {t('msg_ok')}"); messagebox.showinfo("OK", t("msg_sent"), parent=self.root)
            else:
                self.log(f"❌ Discord Error: {r.status_code}")
        except Exception as e: self.log(f"Err: {e}")

    def generate_html(self, total, kills, top_v, top_s, mode):
        self.log("Generating HTML...")
        title = t("d_title_day") if mode == 'DAILY' else t("d_title_all")
        table_title = t("d_list_full") if mode == 'ALL' else t("d_last")
        date_now = datetime.now().strftime('%d-%m-%Y %H:%M')
        
        html_pilots = ""
        for p, n in top_v:
            link = self.get_link(p, 'cmdr')
            html_pilots += f"<li><a href='{link}' target='_blank'>{p}</a> <span class='count'>{n}</span></li>"
            
        html_squads = ""
        for s, n in top_s:
            link = self.get_link(s, 'sq')
            html_squads += f"<li><a href='{link}' target='_blank'>{s}</a> <span class='count'>{n}</span></li>"
            
        html_rows = ""
        for k in kills: 
            link_v = self.get_link(k['v'], 'cmdr')
            link_s = self.get_link(k['s'], 'sq') if k['s'] != "Yok" else "#"
            s_display = f"<a href='{link_s}' target='_blank'>[{k['s']}]</a>" if k['s'] != "Yok" else "-"
            
            p_raw = k['p'] if k['p'] else "-"
            p_color = POWER_COLORS.get(p_raw, "#e0e0e0")
            p_display = f"<span style='color: {p_color}; font-weight: bold;'>{p_raw}</span>"
            
            html_rows += f"""
            <tr>
                <td>{k['ds']}</td>
                <td><a href='{link_v}' target='_blank' class='victim'>{k['v']}</a></td>
                <td>{k['r']}</td>
                <td>{k['sh']}</td>
                <td>{s_display}</td>
                <td>{p_display}</td>
            </tr>
            """

        html_content = f"""
        <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Elite Dangerous PvP Report</title><style>
        body {{ font-family: 'Segoe UI', sans-serif; background-color: #1a1a1a; color: #e0e0e0; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: #252525; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.5); }}
        h1 {{ color: #ff9800; text-align: center; border-bottom: 2px solid #ff9800; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #444; white-space: nowrap; }}
        th {{ background-color: #333; color: #ff9800; }}
        tr:hover {{ background-color: #2a2a2a; }}
        a {{ color: #ffffff; text-decoration: none; }} a:hover {{ color: #ff9800; }}
        .victim {{ font-weight: bold; color: #ffcc80; }}
        .summary {{ text-align: center; font-size: 1.5em; margin: 20px 0; font-weight: bold; color: #fff; }}
        .header-info {{ text-align: center; margin-bottom: 30px; color: #aaa; }}
        .stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }}
        .stat-box {{ background: #333; padding: 15px; border-radius: 8px; border-left: 5px solid #2196F3; }}
        h2 {{ color: #2196F3; font-size: 1.2em; margin-top: 0; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ padding: 5px 0; border-bottom: 1px solid #444; display: flex; justify-content: space-between; }}
        .count {{ background: #ff9800; color: #000; padding: 2px 8px; border-radius: 10px; font-weight: bold; font-size: 0.9em; }}
        </style></head><body><div class="container">
        <h1>{title}</h1><div class="header-info">CMDR {self.cmdr_name} | {date_now}</div>
        <div class="summary">{t('d_kill').format(total)}</div>
        <div class="stats-grid"><div class="stat-box"><h2>{t('d_top_p')}</h2><ul>{html_pilots}</ul></div>
        <div class="stat-box"><h2>{t('d_top_s')}</h2><ul>{html_squads}</ul></div></div>
        <h2>{table_title}</h2><table><thead><tr><th>Date</th><th>Pilot</th><th>Rank</th><th>Ship</th><th>Squadron</th><th>Power</th></tr></thead><tbody>{html_rows}</tbody></table></div></body></html>
        """
        
        safe_path = self.get_safe_desktop_path()
        filename = f"PvP_Report_{mode}.html"
        filepath = os.path.join(safe_path, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f: f.write(html_content)
            self.log(f"Opening report..."); webbrowser.open(f"file://{filepath}")
            messagebox.showinfo("Success", f"Report saved to:\n{filepath}", parent=self.root)
        except Exception as e: self.log(f"HTML Error: {e}")

    def send_discord(self, total, last10, top_v, top_s, mode):
        self.log(t("log_sent"))
        avatar = self.ent_avatar.get() 
        if len(avatar) < 5: avatar = DEF_AVATAR
        
        str_cmdr_list = []
        for c, n in top_v:
            c_safe = self.escape_markdown(c)
            str_cmdr_list.append(f"💀 **[{c_safe}]({self.get_link(c,'cmdr')})**: {n}")
        str_cmdr = "\n".join(str_cmdr_list) or t("d_no_data")

        str_sq_list = []
        for s, n in top_s:
            s_safe = self.escape_markdown(s)
            str_sq_list.append(f"🏴 **[{s_safe}]({self.get_link(s,'sq')})**: {n} {t('d_sq_kill')}")
        str_sq = "\n".join(str_sq_list) or t("d_no_data")

        str_last = ""
        for k in last10:
            sq_t = ""
            if k['s'] != "Yok":
                s_safe = self.escape_markdown(k['s'])
                sq_t = f"[[{s_safe}]]({self.get_link(k['s'],'sq')}) "
            
            v_safe = self.escape_markdown(k['v'])
            p_short = POWER_SHORT.get(k['p'], k['p']) if k['p'] else ""
            p_tag = f" | {p_short}" if p_short else ""
            
            str_last += f"`{k['ds_short']}` | **{sq_t}[{v_safe}]({self.get_link(k['v'],'cmdr')})** ({k['r']}) [{k['sh']}]{p_tag}\n"

        description_text = f"{t('d_desc').format(self.cmdr_name)}\n\n**{t('d_last')}**\n{str_last}"
        if len(description_text) > 4000: description_text = description_text[:4000] + "\n...(truncated)..."

        bold_total = f"**{total}**"

        embed = {
            "title": t("d_title_day") if mode == 'DAILY' else t("d_title_all"),
            "description": description_text,
            "color": 16753920 if mode == 'DAILY' else 3447003,
            "author": {"name": f"CMDR {self.cmdr_name}", "icon_url": avatar},
            "thumbnail": {"url": avatar},
            "fields": [
                {"name": t("d_sum"), "value": t("d_kill").format(bold_total), "inline": False},
                {"name": t("d_top_p"), "value": str_cmdr, "inline": True},
                {"name": t("d_top_s"), "value": str_sq, "inline": True}
            ],
            "footer": {"text": f"ED Kill Tracker by Cmdr Yu-gen • {datetime.now().strftime('%d-%m-%Y %H:%M')}"}
        }
        try:
            r = requests.post(self.ent_url.get(), json={"username": "ED Kill Tracker", "avatar_url": avatar, "embeds": [embed]})
            if r.status_code in [200, 204]:
                self.log(f"✅ {t('msg_ok')}"); messagebox.showinfo("OK", t("msg_sent"), parent=self.root)
            else:
                self.log(f"❌ Discord Error: {r.status_code}")
        except Exception as e: self.log(f"Err: {e}")

# ==========================================
# UI ÇAĞIRMA (OPEN) FONKSİYONLARI 
# ==========================================
def open_pvp_tracker():
    global pvp_tracker_window
    if pvp_tracker_window is not None and pvp_tracker_window.winfo_exists():
        pvp_tracker_window.lift()
        pvp_tracker_window.focus_force()
        return
    pvp_tracker_window = tk.Toplevel()
    PvPTrackerUI(pvp_tracker_window)

def open_logbook():
    global logbook_window
    if logbook_window is not None and logbook_window.winfo_exists():
        logbook_window.lift()
        logbook_window.focus_force()
        return

    logbook_window = tk.Toplevel()
    logbook_window.title(t("lb_title"))
    logbook_window.geometry("750x400")
    logbook_window.attributes('-topmost', True)
    
    columns = ('Tarih/Saat', 'Etkileşim', 'Hedef', 'Durum', 'Threat', 'Sistem')
    tree = ttk.Treeview(logbook_window, columns=columns, show='headings', height=15)
    
    tree.heading('Tarih/Saat', text=t("lb_date"))
    tree.column('Tarih/Saat', width=130, anchor=tk.CENTER)
    tree.heading('Etkileşim', text=t("lb_interaction"))
    tree.column('Etkileşim', width=120, anchor=tk.CENTER)
    tree.heading('Hedef', text=t("lb_target"))
    tree.column('Hedef', width=150, anchor=tk.W)
    tree.heading('Durum', text=t("lb_status"))
    tree.column('Durum', width=150, anchor=tk.CENTER)
    tree.heading('Threat', text=t("lb_threat"))
    tree.column('Threat', width=50, anchor=tk.CENTER)
    tree.heading('Sistem', text=t("lb_system"))
    tree.column('Sistem', width=120, anchor=tk.CENTER)
    
    tree.pack(pady=10, padx=10, fill='both', expand=True)
    
    for log in interaction_log:
        tree.insert('', tk.END, values=(log['time'], log['type'], log['cmdr'], log['status'], log['threat'], log['system']))

    def post_selected():
        selected = tree.selection()
        if not selected: return
        val = tree.item(selected[0], "values")
        threat_val = val[4]
        
        embed_payload = {
            "title": "🚨 TALON ORDER LOGBOOK ENTRY 🚨",
            "color": 16744192, 
            "fields": [
                {"name": "🎯 Target", "value": f"**{val[2]}**", "inline": True},
                {"name": "📍 System", "value": val[5], "inline": True},
                {"name": "⚔️ Interaction", "value": val[1], "inline": True},
                {"name": "📋 Status", "value": val[3], "inline": True},
                {"name": "🕒 Time", "value": val[0], "inline": False}
            ],
            "footer": {"text": "Talon Order Logbook"}
        }
        
        if str(threat_val) != "0": embed_payload["fields"].insert(4, {"name": "💀 Threat Lvl", "value": str(threat_val), "inline": True})
        send_webhook_thread({"embeds": [embed_payload]})
        messagebox.showinfo("OK", t("msg_sent_discord"), parent=logbook_window)

    tk.Button(logbook_window, text=t("btn_lb_send"), command=post_selected, bg="orange", font=("Arial", 10, "bold")).pack(pady=10)

def open_ui():
    global ui_window
    if ui_window is not None and ui_window.winfo_exists():
        ui_window.lift()
        ui_window.focus_force()
        return

    ui_window = tk.Toplevel()
    ui_window.title(t("set_settings"))
    ui_window.geometry("500x700")
    ui_window.attributes('-topmost', True)
    
    notebook = ttk.Notebook(ui_window)
    notebook.pack(expand=True, fill='both', padx=10, pady=10)

    tab_kos = ttk.Frame(notebook)
    tab_enemy = ttk.Frame(notebook)
    tab_squad = ttk.Frame(notebook)
    tab_settings = ttk.Frame(notebook)
    
    notebook.add(tab_kos, text=t("set_kos_cmdr"))
    notebook.add(tab_enemy, text=t("set_enemy_cmdr"))
    notebook.add(tab_squad, text=t("set_enemy_squad"))
    notebook.add(tab_settings, text=t("set_settings"))

    def sync_and_push(parent_window):
        save_db_local()
        success, msg = push_to_firebase_action()
        if not success: messagebox.showerror("Firebase Error", msg, parent=parent_window); return False
        return True

    def create_cmdr_ui(parent_tab, dict_key):
        frame = tk.Frame(parent_tab)
        frame.pack(pady=10)
        
        tk.Label(frame, text=t("cmdr_name")).grid(row=0, column=0, padx=5)
        entry_name = tk.Entry(frame, width=15)
        entry_name.grid(row=0, column=1, padx=5)
        
        tk.Label(frame, text=t("threat")).grid(row=0, column=2, padx=5)
        combo_threat = ttk.Combobox(frame, values=[1, 2, 3, 4, 5], width=3, state="readonly")
        combo_threat.current(0)
        combo_threat.grid(row=0, column=3, padx=5)
        
        listbox = tk.Listbox(parent_tab, height=15, width=45)
        listbox.pack(pady=10)
        
        def refresh_list():
            listbox.delete(0, tk.END)
            for name, lvl in kos_data[dict_key].items(): listbox.insert(tk.END, f"{name} (Lvl: {lvl})")
                
        def add_item():
            val = entry_name.get().strip().lower()
            lvl = int(combo_threat.get())
            if val:
                kos_data[dict_key][val] = lvl
                if sync_and_push(ui_window): refresh_list(); entry_name.delete(0, tk.END)
                else: del kos_data[dict_key][val]
                
        def del_item():
            sel = listbox.curselection()
            if sel:
                item_text = listbox.get(sel[0])
                name = item_text.split(" (Lvl:")[0]
                if name in kos_data[dict_key]:
                    backup_val = kos_data[dict_key][name]
                    del kos_data[dict_key][name]
                    if sync_and_push(ui_window): refresh_list()
                    else: kos_data[dict_key][name] = backup_val

        tk.Button(frame, text=t("btn_add"), command=add_item).grid(row=0, column=4, padx=5)
        tk.Button(parent_tab, text=t("btn_del_selected"), command=del_item).pack()
        refresh_list()

    create_cmdr_ui(tab_kos, "kos_cmdrs")
    create_cmdr_ui(tab_enemy, "enemy_cmdrs")

    tk.Label(tab_squad, text=t("squad_id"), font=("Arial", 9, "bold")).pack(pady=15)
    squad_frame = tk.Frame(tab_squad)
    squad_frame.pack()
    
    squad_entry = tk.Entry(squad_frame, width=15)
    squad_entry.pack(side=tk.LEFT, padx=5)
    
    squad_listbox = tk.Listbox(tab_squad, height=12, width=45)
    squad_listbox.pack(pady=10)
    
    def refresh_squads():
        squad_listbox.delete(0, tk.END)
        for s in kos_data["enemy_squads"]: squad_listbox.insert(tk.END, s.upper())
            
    def add_squad():
        val = squad_entry.get().strip().lower()
        if val and val not in kos_data["enemy_squads"]:
            kos_data["enemy_squads"].append(val)
            if sync_and_push(ui_window): refresh_squads(); squad_entry.delete(0, tk.END)
            else: kos_data["enemy_squads"].remove(val)
            
    def del_squad():
        sel = squad_listbox.curselection()
        if sel:
            val = squad_listbox.get(sel[0]).lower()
            if val in kos_data["enemy_squads"]:
                kos_data["enemy_squads"].remove(val)
                if sync_and_push(ui_window): refresh_squads()
                else: kos_data["enemy_squads"].append(val)

    tk.Button(squad_frame, text=t("btn_add"), command=add_squad).pack(side=tk.LEFT)
    tk.Button(tab_squad, text=t("btn_del_squad"), command=del_squad).pack(pady=5)
    refresh_squads()

    tk.Label(tab_settings, text=t("discord_webhook"), font=("Arial", 9, "bold")).pack(pady=(10, 2))
    web_entry = tk.Entry(tab_settings, width=50)
    web_entry.pack()
    web_entry.insert(0, kos_data.get("webhook_url", ""))
    
    ttk.Separator(tab_settings, orient='horizontal').pack(fill='x', pady=8, padx=20)
    
    tk.Label(tab_settings, text=t("lbl_fb_url"), font=("Arial", 9, "bold")).pack()
    fb_url_entry = tk.Entry(tab_settings, width=50)
    fb_url_entry.pack(pady=(0, 10))
    fb_url_entry.insert(0, kos_data.get("firebase_url", ""))
    
    tk.Label(tab_settings, text=t("read_pass"), font=("Arial", 9, "bold"), fg="blue").pack()
    read_pass_entry = tk.Entry(tab_settings, width=30, show="*")
    read_pass_entry.pack()
    read_pass_entry.insert(0, kos_data.get("read_password", ""))
    
    tk.Label(tab_settings, text=t("admin_pass"), font=("Arial", 9, "bold"), fg="red").pack(pady=(10, 0))
    admin_pass_entry = tk.Entry(tab_settings, width=30, show="*")
    admin_pass_entry.pack()
    admin_pass_entry.insert(0, kos_data.get("admin_password", ""))
    
    ttk.Separator(tab_settings, orient='horizontal').pack(fill='x', pady=8, padx=20)
    
    lang_frame = tk.Frame(tab_settings)
    lang_frame.pack(pady=5)
    tk.Label(lang_frame, text=t("language"), font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=10)
    lang_combo = ttk.Combobox(lang_frame, values=["TR", "EN"], width=5, state="readonly")
    lang_combo.pack(side=tk.LEFT)
    lang_combo.set(kos_data.get("language", "TR"))
    
    mode_frame = tk.Frame(tab_settings)
    mode_frame.pack(pady=5)
    tk.Label(mode_frame, text=t("discord_mode"), font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=10)
    
    mode_var = tk.StringVar(value=kos_data.get("post_mode", "Oto"))
    tk.Radiobutton(mode_frame, text=t("mode_auto"), variable=mode_var, value="Oto").pack(side=tk.LEFT)
    tk.Radiobutton(mode_frame, text=t("mode_manual"), variable=mode_var, value="Manuel").pack(side=tk.LEFT)
    
    sound_var = tk.BooleanVar(value=kos_data.get("sound_enabled", True))
    tk.Checkbutton(tab_settings, text=t("sound_alert"), variable=sound_var).pack(pady=2)
    
    cooldown_frame = tk.Frame(tab_settings)
    cooldown_frame.pack(pady=5)
    tk.Label(cooldown_frame, text=t("cooldown_text")).pack(side=tk.LEFT)
    cooldown_combo = ttk.Combobox(cooldown_frame, values=[1, 2, 5, 10, 15, 30], width=3, state="readonly")
    cooldown_combo.pack(side=tk.LEFT, padx=5)
    tk.Label(cooldown_frame, text=t("cooldown_min")).pack(side=tk.LEFT)
    cooldown_combo.set(str(kos_data.get("cooldown_minutes", 5)))

    def save_settings():
        kos_data["webhook_url"] = web_entry.get().strip()
        kos_data["firebase_url"] = fb_url_entry.get().strip()
        kos_data["read_password"] = read_pass_entry.get().strip()
        kos_data["admin_password"] = admin_pass_entry.get().strip()
        kos_data["post_mode"] = mode_var.get()
        kos_data["sound_enabled"] = sound_var.get()
        kos_data["cooldown_minutes"] = int(cooldown_combo.get())
        kos_data["language"] = lang_combo.get()
        
        refresh_main_ui_texts()
        
        if kos_data["admin_password"]:
            if sync_and_push(ui_window): messagebox.showinfo("OK", t("msg_saved_admin"), parent=ui_window)
            else: save_db_local()
        else:
            save_db_local()
            messagebox.showinfo("OK", t("msg_saved_local"), parent=ui_window)
            
        if edmc_post_button:
            if kos_data["post_mode"] == "Manuel": edmc_post_button.pack()
            else: edmc_post_button.pack_forget(); edmc_post_button.config(state=tk.DISABLED)
            
        ui_window.destroy()
                
    tk.Button(tab_settings, text=t("btn_save_settings"), command=save_settings, bg="lightgreen").pack(pady=10)


# ==========================================
# EDMC ANA ÇİZDİRME (PLUGIN APP) EKRANI
# ==========================================
def plugin_app(parent):
    global edmc_status_label, edmc_post_button, edmc_sync_label, logo_image, radar_btn
    global b1, b2, b3, b4, edmc_app_frame
    
    edmc_app_frame = tk.Frame(parent)
    
    logo_path = os.path.join(PLUGIN_DIR, "kosstrack.png")
    try:
        if os.path.exists(logo_path):
            logo_image = tk.PhotoImage(file=logo_path)
            tk.Label(edmc_app_frame, image=logo_image).pack(side=tk.TOP, pady=3)
    except: pass
        
    tk.Label(edmc_app_frame, text="Talon Order Suite", font=("Arial", 12, "bold"), fg="#B71C1C").pack(side=tk.TOP, pady=2)
    
    edmc_status_label = tk.Label(edmc_app_frame, text=t("status_waiting"), fg="gray", wraplength=250)
    edmc_status_label.pack(side=tk.TOP, pady=(0, 5))
    
    btn_frame = tk.Frame(edmc_app_frame)
    btn_frame.pack(side=tk.TOP, pady=2)
    
    edmc_post_button = tk.Button(btn_frame, text=t("btn_discord"), command=manual_post_action, bg="#FF9800", fg="black", font=("Arial", 9, "bold"), width=34)
    if kos_data.get("post_mode", "Oto") == "Manuel":
        edmc_post_button.pack()
        
    menu_frame = tk.Frame(edmc_app_frame)
    menu_frame.pack(side=tk.TOP, pady=5)
    
    b1 = tk.Button(menu_frame, text=t("btn_update_data"), command=manual_sync_action, bg="#A5D6A7", fg="black", font=("Arial", 9, "bold"), width=16)
    b1.grid(row=0, column=0, padx=2, pady=2)
    
    b2 = tk.Button(menu_frame, text=t("btn_logbook"), command=open_logbook, bg="#90CAF9", fg="black", font=("Arial", 9, "bold"), width=16)
    b2.grid(row=0, column=1, padx=2, pady=2)
    
    b3 = tk.Button(menu_frame, text=t("btn_settings"), command=open_ui, bg="#B39DDB", fg="black", font=("Arial", 9, "bold"), width=16)
    b3.grid(row=1, column=0, padx=2, pady=2)
    
    b4 = tk.Button(menu_frame, text=t("btn_pvp_report"), command=open_pvp_tracker, bg="#FFCC80", fg="black", font=("Arial", 9, "bold"), width=16)
    b4.grid(row=1, column=1, padx=2, pady=2)
    
    radar_frame = tk.Frame(edmc_app_frame)
    radar_frame.pack(side=tk.TOP, pady=5)
    
    def toggle_radar():
        global is_radar_active, active_overlay
        is_radar_active = not is_radar_active
        if is_radar_active:
            active_overlay = TargetOverlay(edmc_app_frame)
            radar_btn.config(text=t("btn_radar_off"), bg="#EF5350", fg="white")
        else:
            if active_overlay:
                active_overlay.destroy()
                active_overlay = None
            radar_btn.config(text=t("btn_radar_on"), bg="#81D4FA", fg="black")
            push_live_target(None) 
            
    radar_btn = tk.Button(radar_frame, text=t("btn_radar_on"), command=toggle_radar, bg="#81D4FA", fg="black", font=("Arial", 9, "bold"), width=34)
    radar_btn.pack()

    edmc_sync_label = tk.Label(edmc_app_frame, text=t("sync_waiting"), fg="gray", font=("Arial", 8))
    edmc_sync_label.pack(side=tk.TOP, pady=(5, 0))
    
    return edmc_app_frame