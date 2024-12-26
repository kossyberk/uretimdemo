import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime

urunler = {}

def urun_ekle():
    ad = entry_ad.get()
    uzunluk = entry_uzunluk.get()
    kilo = entry_kilo.get()
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not ad:
        messagebox.showwarning("Uyarı", "Lütfen ürün adını girin!")
        return

    try:
        uzunluk = float(uzunluk)
        kilo = float(kilo)
    except ValueError:
        messagebox.showerror("Hata", "Uzunluk ve kilo değerleri sayısal olmalıdır!")
        return

    if ad in urunler:
        urunler[ad]["uzunluklar"].append(uzunluk)
        urunler[ad]["kilolar"].append(kilo)
        urunler[ad]["tarihler"].append(tarih)
    else:
        urunler[ad] = {
            "uzunluklar": [uzunluk],
            "kilolar": [kilo],
            "tarihler": [tarih]
        }

    messagebox.showinfo("Başarılı", f"{ad} başarıyla eklendi.")
    entry_ad.delete(0, tk.END)
    entry_uzunluk.delete(0, tk.END)
    entry_kilo.delete(0, tk.END)

def urunleri_goster():
    liste_penceresi = tk.Toplevel(root)
    liste_penceresi.title("Ürün Listesi")
    liste_penceresi.geometry("600x400")
    
    tree = ttk.Treeview(liste_penceresi, columns=("ad", "uzunluk", "kilo", "tarih"), show="headings")
    tree.heading("ad", text="Ürün Adı")
    tree.heading("uzunluk", text="Uzunluk (m)")
    tree.heading("kilo", text="Kilo (kg)")
    tree.heading("tarih", text="Üretim Tarihi")
    tree.pack(fill=tk.BOTH, expand=True)

    for ad, bilgiler in urunler.items():
        for uzunluk, kilo, tarih in zip(bilgiler["uzunluklar"], bilgiler["kilolar"], bilgiler["tarihler"]):
            tree.insert("", tk.END, values=(ad, uzunluk, kilo, tarih))

def grafik_goster():
    def urun_sec_ve_grafik_ciz():
        secili_item = tree.selection()
        if not secili_item:
            messagebox.showwarning("Uyarı", "Lütfen bir ürün seçin!")
            return
        urun_adi = tree.item(secili_item[0])['values'][0]
        urun = urunler[urun_adi]

        # uzunluk grafik
        plt.figure(figsize=(6, 5))
        plt.plot(urun["tarihler"], urun["uzunluklar"], linestyle='-', marker='o', label='Uzunluk (m)', color='blue')
        plt.xlabel("Üretim Zamanı")
        plt.ylabel("Uzunluk (m)")
        plt.title(f"{urun_adi} - Uzunluk Grafiği")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # kilo grafik
        plt.figure(figsize=(10, 5))
        plt.plot(urun["tarihler"], urun["kilolar"], linestyle='-', marker='o', label='Kilo (kg)', color='green')
        plt.xlabel("Üretim Zamanı")
        plt.ylabel("Kilo (kg)")
        plt.title(f"{urun_adi} - Kilo Grafiği")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    grafik_penceresi = tk.Toplevel(root)
    grafik_penceresi.title("Ürün Seç ve Grafik Göster")
    grafik_penceresi.geometry("400x300")

    tree = ttk.Treeview(grafik_penceresi, columns=("ad", "girdi_sayisi"), show="headings")
    tree.heading("ad", text="Ürün Adı")
    tree.heading("girdi_sayisi", text="Girdi Sayısı")
    tree.pack(fill=tk.BOTH, expand=True)

    for ad, bilgiler in urunler.items():
        tree.insert("", tk.END, values=(ad, len(bilgiler["tarihler"])))

    tk.Button(grafik_penceresi, text="Grafik Göster", command=urun_sec_ve_grafik_ciz).pack(pady=10)

# Ana ekrsn
root = tk.Tk()
root.title("Üretim Giriş Uygulaması")
root.geometry("400x300")


tk.Label(root, text="Ürün Adı:").pack()
entry_ad = tk.Entry(root)
entry_ad.pack()

tk.Label(root, text="Ürün Uzunluğu (m):").pack()
entry_uzunluk = tk.Entry(root)
entry_uzunluk.pack()

tk.Label(root, text="Ürün Kilosu (kg):").pack()
entry_kilo = tk.Entry(root)
entry_kilo.pack()

# Buttonlar
tk.Button(root, text="Ürün Ekle", command=urun_ekle).pack(pady=5)
tk.Button(root, text="Ürünler", command=urunleri_goster).pack(pady=5)
tk.Button(root, text="Grafik", command=grafik_goster).pack(pady=5)

root.mainloop()
