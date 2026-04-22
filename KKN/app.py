from flask import Flask, render_template, request, redirect, session
from models.db import supabase

app = Flask(__name__)
app.secret_key = "kkn_secret"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        data = supabase.table("admin").select("*").eq("username", username).eq("password", password).execute()

        if data.data:
            session['login'] = True
            return redirect('/dashboard')

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if not session.get("login"):
        return redirect("/login")

    peng = supabase.table("pengumuman").select("*").execute()
    surat = supabase.table("surat").select("*").execute()

    return render_template("dashboard.html",
        pengumuman=len(peng.data),
        surat=len(surat.data)
                          )
  
@app.route('/pengumuman')
def pengumuman():
    data = supabase.table("pengumuman").select("*").execute()
    return render_template("pengumuman.html", data=data.data)


@app.route('/tambah_pengumuman', methods=['POST'])
def tambah_pengumuman():
    supabase.table("pengumuman").insert({
        "judul": request.form['judul'],
        "isi": request.form['isi']
    }).execute()

    return redirect('/pengumuman')

@app.route('/layanan', methods=['GET','POST'])
def layanan():
    if request.method == 'POST':
        supabase.table("surat").insert({
            "nama": request.form['nama'],
            "jenis_surat": request.form['jenis'],
            "keterangan": request.form['keterangan']
        }).execute()

    return render_template("layanan.html")

@app.route('/galeri', methods=['GET','POST'])
def galeri():
    if request.method == 'POST':
        supabase.table("galeri").insert({
            "gambar": request.form['gambar'],
            "keterangan": request.form['keterangan']
        }).execute()

    data = supabase.table("galeri").select("*").execute()
    return render_template("galeri.html", data=data.data)

@app.route('/map')
def map():
    return render_template("map.html")
