import os
import shutil
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, send_file, current_app, redirect, url_for, flash
import sys
from pathlib import Path

backup_bp = Blueprint('backup', __name__, url_prefix='/backups')

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

def get_db_path():
    """Returns the absolute path to the database file."""
    # From app.py logic
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        return os.path.join(application_path, 'pos.db')
    else:
        return os.path.join(os.getcwd(), 'instance', 'pos.db')

def get_backup_dir():
    """Returns the backup directory path, creating it if needed."""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.getcwd()
    
    backup_path = os.path.join(base_path, 'backups')
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
    return backup_path

@backup_bp.route('/')
def index():
    """Render the backup management page."""
    backups = []
    backup_dir = get_backup_dir()
    
    if os.path.exists(backup_dir):
        for filename in os.listdir(backup_dir):
            if filename.endswith('.db'):
                filepath = os.path.join(backup_dir, filename)
                stat = os.stat(filepath)
                backups.append({
                    'name': filename,
                    'size': f"{stat.st_size / 1024:.2f} KB",
                    'created_at': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
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

    if file and file.filename.endswith('.db'):
        try:
            safe_filename = sanitize_filename(file.filename)
            backup_dir = get_backup_dir()
            file.save(os.path.join(backup_dir, safe_filename))
            return jsonify({'success': True, 'message': 'Backup uploaded successfully.'})
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid filename'}), 400
    else:
        return jsonify({'success': False, 'message': 'Invalid file type. Must be .db'}), 400


