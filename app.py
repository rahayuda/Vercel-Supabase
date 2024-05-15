from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client

app = Flask(__name__)

# Supabase connection details
url: str = "https://uexkziqpqgvudhyjhupk.supabase.co"
key: str = "vgBAZs0lBJlm1Gw4"
supabase: Client = create_client(url, key)

@app.route('/')
def index():
    response = supabase.table('mahasiswa').select('*').execute()
    results = response.data
    return render_template('index.html', results=results)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        supabase.table('mahasiswa').insert({'nim': nim, 'nama': nama}).execute()
        return redirect(url_for('index'))
    return render_template('insert.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    id = request.args.get('id')
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        supabase.table('mahasiswa').update({'nim': nim, 'nama': nama}).eq('id', id).execute()
        return redirect(url_for('index'))
    result = supabase.table('mahasiswa').select('*').eq('id', id).execute().data[0]
    return render_template('update.html', result=result)

@app.route('/delete')
def delete():
    id = request.args.get('id')
    supabase.table('mahasiswa').delete().eq('id', id).execute()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8083)
