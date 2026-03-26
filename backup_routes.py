import os
import shutil
import sqlite3
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, send_file, current_app, redirect, url_for, flash
import sys
from pathlib import Path

backup_bp = Blueprint('backup', __name__, url_prefix='/backups')

def validate_sqlite_db(filepath):
    """Validate if file is a valid SQLite database."""
    try:
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()
        # Run integrity check
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        conn.close()
        return result[0] == 'ok'
    except Exception:
        return False

def sanitize_filename(filename):
    """Remove path traversal characters from filename"""
    # Only allow alphanumeric, underscore, hyphen, dot
    import re
    safe_name = re.sub(r'[^\w\-.]', '', filename)
    # Remove leading dots to prevent hidden files
    safe_name = safe_name.lstrip('.')
    if not safe_name:
        raise ValueError("Invalid filename")
    return safe_name

def get_data_dir():
    """Returns the same stable data directory as app.py."""
    if getattr(sys, 'frozen', False):
        base = os.environ.get('APPDATA', os.path.expanduser('~'))
        data_dir = os.path.join(base, 'MiTiendaPoS')
    else:
        data_dir = os.path.join(os.getcwd(), 'instance')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def get_db_path():
    """Returns the absolute path to the database file."""
    return os.path.join(get_data_dir(), 'pos.db')

def get_backup_dir():
    """Returns the backup directory path, creating it if needed."""
    backup_path = os.path.join(get_data_dir(), 'backups')
    os.makedirs(backup_path, exist_ok=True)
    return backup_path

@backup_bp.route('/')
def index():
    """Render the backup management page."""
    backups = []
    backup_dir = get_backup_dir()

    if os.path.exists(backup_dir):
        # Cleanup old backups - keep only last 10
        all_files = []
        for filename in os.listdir(backup_dir):
            if filename.endswith('.db'):
                filepath = os.path.join(backup_dir, filename)
                stat = os.stat(filepath)
                all_files.append({
                    'name': filename,
                    'path': filepath,
                    'ctime': stat.st_ctime,
                    'size': stat.st_size
                })

        # Sort by creation time, delete oldest if more than 10
        all_files.sort(key=lambda x: x['ctime'], reverse=True)

        if len(all_files) > 10:
            for old_file in all_files[10:]:
                try:
                    os.remove(old_file['path'])
                except Exception:
                    pass

        # List valid backups
        for file_info in all_files[:10]:
            filepath = file_info['path']

            # Verify file still exists (might have been deleted externally)
            if not os.path.exists(filepath):
                continue

            is_valid = validate_sqlite_db(filepath)
            status = '[OK]' if is_valid else '[CORRUPTO]'

            backups.append({
                'name': file_info['name'],
                'size': f"{file_info['size'] / 1024:.2f} KB",
                'created_at': datetime.fromtimestamp(file_info['ctime']).strftime('%Y-%m-%d %H:%M:%S'),
                'status': status
            })

    # Sort by creation time desc
    backups.sort(key=lambda x: x['created_at'], reverse=True)
    return render_template('backups.html', backups=backups)

@backup_bp.route('/create', methods=['POST'])
def create_backup():
    """Create a new backup of the current database."""
    try:
        db_path = get_db_path()
        if not os.path.exists(db_path):
            return jsonify({'success': False, 'message': 'Database file not found.'}), 404
            
        backup_dir = get_backup_dir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        shutil.copy2(db_path, backup_path)
        return jsonify({'success': True, 'message': 'Backup created successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@backup_bp.route('/restore/<filename>', methods=['POST'])
def restore_backup(filename):
    """Restore the database from a backup file."""
    try:
        safe_filename = sanitize_filename(filename)
        backup_dir = get_backup_dir()
        backup_path = os.path.join(backup_dir, safe_filename)
        db_path = get_db_path()

        if not os.path.exists(backup_path):
            return jsonify({'success': False, 'message': 'Backup file not found.'}), 404

        # Validate backup integrity BEFORE restoring
        if not validate_sqlite_db(backup_path):
            return jsonify({'success': False, 'message': 'Backup file is corrupted. Cannot restore.'}), 400

        # Create a temp safety backup just in case
        safety_path = db_path + ".safety"
        if os.path.exists(db_path):
            shutil.copy2(db_path, safety_path)

        shutil.copy2(backup_path, db_path)

        return jsonify({'success': True, 'message': 'Database restored successfully. Please restart the application if you encounter issues.'})
    except ValueError as e:
        return jsonify({'success': False, 'message': 'Invalid filename'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@backup_bp.route('/download/<filename>')
def download_backup(filename):
    """Download a backup file."""
    try:
        safe_filename = sanitize_filename(filename)
        backup_dir = get_backup_dir()
        backup_path = os.path.join(backup_dir, safe_filename)
        if not os.path.exists(backup_path):
            return jsonify({'error': 'File not found'}), 404
        return send_file(backup_path, as_attachment=True)
    except ValueError:
        return jsonify({'error': 'Invalid filename'}), 400

@backup_bp.route('/delete/<filename>', methods=['DELETE'])
def delete_backup(filename):
    """Delete a backup file."""
    try:
        safe_filename = sanitize_filename(filename)
        backup_dir = get_backup_dir()
        filepath = os.path.join(backup_dir, safe_filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True, 'message': 'Backup deleted successfully.'})
        return jsonify({'success': False, 'message': 'File not found.'}), 404
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid filename'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@backup_bp.route('/upload', methods=['POST'])
def upload_backup():
    """Upload an external backup file."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400

    if not file.filename.endswith('.db'):
        return jsonify({'success': False, 'message': 'Invalid file type. Must be .db'}), 400

    # Check file size (max 100MB)
    if file.content_length and file.content_length > 100 * 1024 * 1024:
        return jsonify({'success': False, 'message': 'File too large. Maximum 100MB.'}), 400

    try:
        safe_filename = sanitize_filename(file.filename)
        backup_dir = get_backup_dir()
        temp_path = os.path.join(backup_dir, f"{safe_filename}.tmp")

        # Save to temp file first
        file.save(temp_path)

        # Validate before keeping
        if not validate_sqlite_db(temp_path):
            os.remove(temp_path)
            return jsonify({'success': False, 'message': 'Invalid SQLite database file.'}), 400

        # Move to final location
        final_path = os.path.join(backup_dir, safe_filename)
        os.rename(temp_path, final_path)

        return jsonify({'success': True, 'message': 'Backup uploaded successfully.'})
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid filename'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


