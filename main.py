import tkinter as tk
from tkinter import messagebox
import urllib.request
import urllib.parse
import json
import sqlite3

# API key almak için: https://www.omdbapi.com/
API_KEY = "BURAYA_KENDI_API_ANAHTARINIZI_GIRIN"

def veritabani_olustur():
    conn = sqlite3.connect("filmler.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filmler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baslik TEXT,
            yil TEXT,
            imdb TEXT,
            tur TEXT,
            yonetmen TEXT,
            aciklama TEXT
        )
    """)
    conn.commit()
    conn.close()

def film_kaydet(sonuc):
    conn = sqlite3.connect("filmler.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM filmler WHERE baslik = ?", (sonuc["Başlık"],))
    if cursor.fetchone():
        conn.close()
        return
    cursor.execute("""
        INSERT INTO filmler (baslik, yil, imdb, tur, yonetmen, aciklama)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        sonuc["Başlık"],
        sonuc["Yıl"],
        sonuc["IMDB"],
        sonuc["Tür"],
        sonuc["Yönetmen"],
        sonuc["Açıklama"]
    ))
    conn.commit()
    conn.close()

def gecmis_filmleri_getir():
    conn = sqlite3.connect("filmler.db")
    cursor = conn.cursor()
    cursor.execute("SELECT baslik, yil, imdb, tur, yonetmen, aciklama FROM filmler ORDER BY id DESC LIMIT 10")
    veriler = cursor.fetchall()
    conn.close()
    return veriler

def film_ara(baslik):
    query = urllib.parse.quote(baslik)
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={query}"
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            veri = json.loads(data.decode("utf-8"))
            if veri.get("Response") == "True":
                return {
                    "Başlık": veri.get("Title", ""),
                    "Yıl": veri.get("Year", ""),
                    "IMDB": veri.get("imdbRating", ""),
                    "Tür": veri.get("Genre", ""),
                    "Yönetmen": veri.get("Director", ""),
                    "Açıklama": veri.get("Plot", "")
                }
            else:
                return None
    except Exception as e:
        print("API Hatası:", e)
        return None

def ara():
    baslik = giris.get()
    if not baslik:
        messagebox.showwarning("Uyarı", "Lütfen bir film adı giriniz.")
        return
    sonuc = film_ara(baslik)
    if sonuc:
        sonuc_metni = (
            f"🎬 {sonuc['Başlık']} ({sonuc['Yıl']})\n"
            f"⭐ IMDB: {sonuc['IMDB']}\n"
            f"🎭 Tür: {sonuc['Tür']}\n"
            f"🎬 Yönetmen: {sonuc['Yönetmen']}\n\n"
            f"{sonuc['Açıklama']}"
        )
        sonuc_label.config(state="normal")
        sonuc_label.delete("1.0", tk.END)
        sonuc_label.insert(tk.END, sonuc_metni)
        sonuc_label.config(state="disabled")
        film_kaydet(sonuc)
    else:
        messagebox.showerror("Hata", "Film bulunamadı.")

def gecmisi_goster():
    veriler = gecmis_filmleri_getir()
    gecmis_label.config(state="normal")
    gecmis_label.delete("1.0", tk.END)
    if veriler:
        for v in veriler:
            gecmis_label.insert(tk.END,
                f"🎬 {v[0]} ({v[1]})\n⭐ IMDB: {v[2]}\n🎭 Tür: {v[3]}\n🎬 Yönetmen: {v[4]}\n📖 Açıklama: {v[5]}\n\n"
            )
    else:
        gecmis_label.insert(tk.END, "Henüz geçmişte film araması yapılmadı.")
    gecmis_label.config(state="disabled")

# Program Başlangıcı
veritabani_olustur()

pencere = tk.Tk()
pencere.title("🎬 Film Arama Uygulaması")
pencere.configure(bg="#1A1A1A")
pencere.geometry("750x600")

baslik_label = tk.Label(pencere, text="🎬 Film Arama", font=("Helvetica", 20, "bold"), bg="#1A1A1A", fg="#E3E3E3")
baslik_label.pack(pady=15)

giris = tk.Entry(pencere, font=("Arial", 16), bg="#2E2E2E", fg="white", insertbackground="white", width=40)
giris.pack(pady=10)

ara_buton = tk.Button(pencere, text="🔍 Ara", font=("Arial", 14), bg="#800000", fg="white", width=15, command=ara)
ara_buton.pack(pady=5)

sonuc_label = tk.Text(pencere, font=("Arial", 13), bg="#101010", fg="white", wrap="word", height=10, width=90, bd=0, relief="flat")
sonuc_label.pack(pady=10)
sonuc_label.config(state="disabled")

gecmis_buton = tk.Button(pencere, text="📜 Geçmişi Göster", font=("Arial", 12), bg="#404040", fg="white", width=20, command=gecmisi_goster)
gecmis_buton.pack(pady=5)

gecmis_label = tk.Text(pencere, font=("Arial", 13), bg="#101010", fg="white", wrap="word", height=10, width=90, bd=0, relief="flat")
gecmis_label.pack(pady=10)
gecmis_label.config(state="disabled")

pencere.mainloop()
