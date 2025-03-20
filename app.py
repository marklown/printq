import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jelcijeiflasdf'

def get_db_connection():
  conn = sqlite3.connect('database.db')
  conn.row_factory = sqlite3.Row
  return conn

def get_job(job_id):
  conn = get_db_connection()
  job = conn.execute('SELECT * FROM jobs WHERE id = ?',
                      (job_id,)).fetchone()
  conn.close()
  if job is None:
      abort(404)
  return job


@app.route('/')
def index():
  conn = get_db_connection()
  jobs = conn.execute('SELECT * FROM jobs').fetchall()
  conn.close()
  return render_template('index.html', jobs=jobs)

@app.route('/completed')
def completed():
  conn = get_db_connection()
  jobs = conn.execute('SELECT * FROM jobs WHERE completed = ?', (True,)).fetchall()
  conn.close()
  return render_template('completed.html', jobs=jobs)

@app.route('/deleted')
def deleted():
  conn = get_db_connection()
  jobs = conn.execute('SELECT * FROM jobs WHERE deleted = ?', (True,)).fetchall()
  conn.close()
  return render_template('deleted.html', jobs=jobs)

@app.route('/add', methods=('GET', 'POST'))
def add():
  if request.method == 'POST':
    job = request.form['job']
    color = request.form['color']
    submitted_by = request.form['submitted_by']
    comments = request.form['comments']

    if not job or not color or not submitted_by:
      flash('Missing required fields')
    else:
      conn = get_db_connection()
      conn.execute('INSERT INTO jobs (job, color, submitted_by, comments) VALUES (?, ?, ?, ?)',
                   (job, color, submitted_by, comments)
      )
      conn.commit()
      conn.close()
      return redirect(url_for('index'))

  return render_template('add.html')

@app.route('/edit/<int:job_id>', methods=('GET', 'POST'))
def edit(job_id):
  job = get_job(job_id)

  if request.method == 'POST':
    job = request.form['job']
    color = request.form['color']
    submitted_by = request.form['submitted_by']
    comments = request.form['comments']

    if not job or not color or not submitted_by:
      flash('Missing required fields')
    else:
      conn = get_db_connection()
      conn.execute('UPDATE jobs SET job=?, color=?, submitted_by=?, comments=? WHERE id=?',
                   (job, color, submitted_by, comments, job_id)
      )
      conn.commit()
      conn.close()
      return redirect(url_for('index'))

  return render_template('edit.html', job=job)

@app.route('/complete/<int:job_id>', methods=['POST'])
def complete(job_id):
  conn = get_db_connection()
  conn.execute('UPDATE jobs SET completed = ?, completed_on = CURRENT_TIMESTAMP WHERE id = ?',
               (True, job_id)
  )
  conn.commit()
  conn.close()
  return redirect(url_for('index'))

@app.route('/delete/<int:job_id>', methods=['POST'])
def delete(job_id):
  conn = get_db_connection()
  conn.execute('UPDATE jobs SET deleted = ?, deleted_on = CURRENT_TIMESTAMP WHERE id = ?',
               (True, job_id)
  )
  conn.commit()
  conn.close()
  return redirect(url_for('index'))

@app.route('/revert/<int:job_id>', methods=['POST'])
def revert(job_id):
  conn = get_db_connection()
  conn.execute('UPDATE jobs SET deleted = ?, completed = ? WHERE id = ?',
               (False, False, job_id)
  )
  conn.commit()
  conn.close()
  return redirect(url_for('index'))


if __name__ == '__main__':
  app.run(host="127.0.0.1", port=8080, debug=True, threaded=False)