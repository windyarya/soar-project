from flask import Flask, request, jsonify, send_file
import os
import shelve
import json
import subprocess

app = Flask(__name__)
lists_directory = '/var/ossec/etc/lists/'

def create_cdb(json_data, output_cdb, output_readable):
    temp_directory = '/tmp/flask_cdb_temp/'

    # Membuat direktori sementara jika belum ada
    os.makedirs(temp_directory, exist_ok=True)

    temp_cdb_path = os.path.join(temp_directory, output_cdb)
    temp_readable_path = os.path.join(temp_directory, output_readable)

    with shelve.open(temp_cdb_path, writeback=True) as cdb_writer:
        for key, value in json_data.items():
            value = value if value is not None else ""
            cdb_writer[key] = value

    with open(temp_readable_path, 'w') as readable_file:
        for key in json_data.keys():
            readable_file.write(f"{key}:\n")

    # Menyalin file CDB ke direktori tujuan
    subprocess.run(['cp', temp_cdb_path, os.path.join(lists_directory, output_cdb)])

    # Menyalin file readable ke direktori tujuan
    subprocess.run(['cp', temp_readable_path, os.path.join(lists_directory, output_readable)])

    # Menghapus direktori sementara
    subprocess.run(['rm', '-r', temp_directory])

@app.route('/create_cdb', methods=['POST'])
def create_cdb_api():
    try:
        data = request.get_json()
        json_data = data.get('json_data')
        output_cdb_file = data.get('output_cdb_file', 'ip-blocked.cdb')
        output_readable_file = data.get('output_readable_file', 'ip-blocked')

        create_cdb(json_data, output_cdb_file, output_readable_file)

        response = {'status': 'success', 'message': 'CDB file created or updated successfully'}
        return jsonify(response), 200
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500

@app.route('/download_cdb', methods=['GET'])
def download_cdb_api():
    try:
        output_cdb_file = request.args.get('file_name', 'ip-blocked.cdb')
        cdb_path = os.path.join(lists_directory, output_cdb_file)

        if not os.path.exists(cdb_path):
            response = {'status': 'error', 'message': 'File not found'}
            return jsonify(response), 404

        return send_file(cdb_path, as_attachment=True)

    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500

@app.route('/download_readable', methods=['GET'])
def download_readable_api():
    try:
        output_readable_file = request.args.get('file_name', '')
        readable_path = os.path.join(lists_directory, output_readable_file)

        if not os.path.exists(readable_path):
            response = {'status': 'error', 'message': 'Readable file not found'}
            return jsonify(response), 404

        return send_file(readable_path, as_attachment=True)

    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500

if __name__ == '__main__':
    # Ganti host dan port sesuai kebutuhan
    app.run(host='10.15.41.26', port=5000, debug=True)