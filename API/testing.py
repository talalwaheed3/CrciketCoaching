import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template_string
from werkzeug.utils import secure_filename
from werkzeug.serving import run_simple
import socket
import threading
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration - NO RESTRICTIONS
UPLOAD_FOLDER = 'shared_files'
# NO MAX FILE SIZE - Remove all size restrictions
# NO ALLOWED EXTENSIONS - Accept any file type

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Remove MAX_CONTENT_LENGTH to allow unlimited file size
# app.config['MAX_CONTENT_LENGTH'] = None

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_local_ip():
    """Get local IP address"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def allowed_file(filename):
    """Accept ANY file - No restrictions"""
    return True  # Accept all files regardless of extension

def get_file_size(file_path):
    """Get file size in human readable format"""
    try:
        size = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    except:
        return "Unknown"

def get_file_info(filename):
    """Get file information"""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        try:
            stat = os.stat(file_path)
            return {
                'name': filename,
                'size': get_file_size(file_path),
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'path': file_path
            }
        except:
            return {
                'name': filename,
                'size': "Unknown",
                'modified': "Unknown",
                'path': file_path
            }
    return None

# HTML Template for Web Interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cross-Platform File Sharing API</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; color: #333; }
        .section { margin-bottom: 30px; }
        .upload-area { border: 2px dashed #007bff; padding: 40px; text-align: center; border-radius: 10px; margin-bottom: 20px; }
        .upload-area.dragover { background: #e3f2fd; border-color: #1976d2; }
        input[type="file"] { display: none; }
        .upload-btn { background: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        .upload-btn:hover { background: #0056b3; }
        .file-list { margin-top: 20px; }
        .file-item { display: flex; justify-content: space-between; align-items: center; padding: 10px; border-bottom: 1px solid #eee; }
        .file-info { flex: 1; }
        .file-name { font-weight: bold; color: #333; word-break: break-all; }
        .file-details { color: #666; font-size: 14px; }
        .download-btn { background: #28a745; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; font-size: 14px; }
        .download-btn:hover { background: #218838; }
        .delete-btn { background: #dc3545; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; margin-left: 10px; font-size: 14px; }
        .delete-btn:hover { background: #c82333; }
        .progress { width: 100%; height: 20px; background: #f0f0f0; border-radius: 10px; overflow: hidden; margin: 10px 0; }
        .progress-bar { height: 100%; background: #007bff; transition: width 0.3s ease; }
        .info-box { background: #e9ecef; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .status { margin-top: 10px; padding: 10px; border-radius: 5px; }
        .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .status.info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .api-info { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .api-info h3 { margin-bottom: 10px; color: #495057; }
        .api-info code { background: #e9ecef; padding: 2px 6px; border-radius: 3px; }
        .stats { display: flex; justify-content: space-around; margin-bottom: 20px; }
        .stat-item { text-align: center; padding: 15px; background: #f8f9fa; border-radius: 5px; }
        .stat-number { font-size: 24px; font-weight: bold; color: #007bff; }
        .stat-label { color: #6c757d; margin-top: 5px; }
        .no-restrictions { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center; }
        .upload-progress { display: none; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗂️ Cross-Platform File Sharing API</h1>
            <p>Share files between Mac and Windows seamlessly</p>
        </div>

        <div class="no-restrictions">
            <strong>✅ NO RESTRICTIONS:</strong> Any file type • Any file size • No timeout
        </div>

        <div class="info-box">
            <strong>🌐 Server Info:</strong><br>
            Local IP: <code>{{ local_ip }}</code><br>
            Port: <code>{{ port }}</code><br>
            Access URL: <code>http://{{ local_ip }}:{{ port }}</code>
        </div>

        <div class="stats">
            <div class="stat-item">
                <div class="stat-number" id="file-count">{{ file_count }}</div>
                <div class="stat-label">Files Shared</div>
            </div>
            <div class="stat-item">
                <div class="stat-number" id="total-size">{{ total_size }}</div>
                <div class="stat-label">Total Size</div>
            </div>
        </div>

        <div class="section">
            <h2>📤 Upload Files (Any Type, Any Size)</h2>
            <div class="upload-area" id="upload-area">
                <p>Drag & drop files here or click to select</p>
                <p style="color: #666; font-size: 14px;">Accepts ANY file type (.txt, .py, .exe, .dmg, .iso, etc.)</p>
                <input type="file" id="file-input" multiple>
                <button class="upload-btn" onclick="document.getElementById('file-input').click()">
                    Choose Files
                </button>
            </div>
            <div class="upload-progress" id="upload-progress">
                <div class="progress">
                    <div class="progress-bar" id="progress-bar"></div>
                </div>
                <div id="progress-text">Uploading...</div>
            </div>
            <div id="upload-status"></div>
        </div>

        <div class="section">
            <h2>📁 Shared Files</h2>
            <div class="file-list" id="file-list">
                {% for file in files %}
                <div class="file-item">
                    <div class="file-info">
                        <div class="file-name">{{ file.name }}</div>
                        <div class="file-details">{{ file.size }} • Modified: {{ file.modified }}</div>
                    </div>
                    <div>
                        <a href="/download/{{ file.name }}" class="download-btn">Download</a>
                        <button class="delete-btn" onclick="deleteFile('{{ file.name }}')">Delete</button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="api-info">
            <h3>🔧 API Endpoints</h3>
            <p><strong>Upload:</strong> <code>POST /upload</code> - Accepts ANY file type</p>
            <p><strong>Download:</strong> <code>GET /download/&lt;filename&gt;</code></p>
            <p><strong>List Files:</strong> <code>GET /api/files</code></p>
            <p><strong>Delete:</strong> <code>DELETE /api/files/&lt;filename&gt;</code></p>
            <p><strong>Server Info:</strong> <code>GET /api/info</code></p>
        </div>
    </div>

    <script>
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');
        const uploadStatus = document.getElementById('upload-status');
        const uploadProgress = document.getElementById('upload-progress');
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');

        // Drag and drop functionality
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            uploadFiles(files);
        });

        fileInput.addEventListener('change', (e) => {
            uploadFiles(e.target.files);
        });

        function uploadFiles(files) {
            const formData = new FormData();
            
            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }

            uploadProgress.style.display = 'block';
            showStatus('Uploading files... This may take a while for large files.', 'info');

            // Create XMLHttpRequest for progress tracking
            const xhr = new XMLHttpRequest();
            
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const percentage = (e.loaded / e.total) * 100;
                    progressBar.style.width = percentage + '%';
                    progressText.textContent = `Uploading... ${percentage.toFixed(1)}%`;
                }
            });

            xhr.addEventListener('load', () => {
                uploadProgress.style.display = 'none';
                
                if (xhr.status === 200) {
                    try {
                        const data = JSON.parse(xhr.responseText);
                        if (data.success) {
                            showStatus(`Successfully uploaded ${data.uploaded_files.length} files`, 'success');
                            setTimeout(() => location.reload(), 2000);
                        } else {
                            showStatus(`Error: ${data.message}`, 'error');
                        }
                    } catch (e) {
                        showStatus('Upload completed but response parsing failed', 'error');
                    }
                } else {
                    showStatus(`Upload failed with status: ${xhr.status}`, 'error');
                }
            });

            xhr.addEventListener('error', () => {
                uploadProgress.style.display = 'none';
                showStatus('Upload failed due to network error', 'error');
            });

            xhr.open('POST', '/upload');
            xhr.send(formData);
        }

        function deleteFile(filename) {
            if (confirm(`Are you sure you want to delete "${filename}"?`)) {
                fetch(`/api/files/${encodeURIComponent(filename)}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showStatus(`Successfully deleted "${filename}"`, 'success');
                        setTimeout(() => location.reload(), 1000);
                    } else {
                        showStatus(`Error: ${data.message}`, 'error');
                    }
                })
                .catch(error => {
                    showStatus(`Error: ${error.message}`, 'error');
                });
            }
        }

        function showStatus(message, type) {
            uploadStatus.innerHTML = `<div class="status ${type}">${message}</div>`;
            if (type === 'success') {
                setTimeout(() => {
                    uploadStatus.innerHTML = '';
                }, 5000);
            }
        }

        // Auto-refresh file list every 30 seconds
        setInterval(() => {
            fetch('/api/files')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('file-count').textContent = data.files.length;
                    }
                })
                .catch(error => {
                    console.log('Auto-refresh failed:', error);
                });
        }, 30000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main web interface"""
    try:
        # Get all files in upload directory
        files = []
        total_size = 0
        
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    file_info = get_file_info(filename)
                    if file_info:
                        files.append(file_info)
                        try:
                            total_size += os.path.getsize(file_path)
                        except:
                            pass
        
        # Format total size
        total_size_str = "0 B"
        if total_size > 0:
            temp_size = total_size
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if temp_size < 1024.0:
                    total_size_str = f"{temp_size:.1f} {unit}"
                    break
                temp_size /= 1024.0
        
        return render_template_string(HTML_TEMPLATE, 
                                    files=files, 
                                    file_count=len(files),
                                    total_size=total_size_str,
                                    local_ip=get_local_ip(),
                                    port=5000)
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads - Accept ANY file type"""
    try:
        if 'files' not in request.files:
            return jsonify({'success': False, 'message': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        uploaded_files = []
        errors = []
        
        for file in files:
            if file.filename == '':
                errors.append('Empty filename')
                continue
            
            # Accept ANY file - no restrictions
            if file:
                filename = secure_filename(file.filename)
                
                # If secure_filename removes everything, use original filename
                if not filename:
                    filename = file.filename.replace('/', '_').replace('\\', '_')
                
                # Handle duplicate filenames
                counter = 1
                base_name, ext = os.path.splitext(filename)
                original_filename = filename
                
                while os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
                    filename = f"{base_name}_{counter}{ext}"
                    counter += 1
                
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                
                try:
                    file.save(file_path)
                    
                    uploaded_files.append({
                        'original_name': file.filename,
                        'saved_name': filename,
                        'size': get_file_size(file_path),
                        'path': file_path
                    })
                    
                    logger.info(f"File uploaded: {filename} (Original: {file.filename})")
                except Exception as save_error:
                    errors.append(f'Failed to save {file.filename}: {str(save_error)}')
            else:
                errors.append(f'Invalid file: {file.filename}')
        
        if uploaded_files:
            return jsonify({
                'success': True,
                'message': f'Successfully uploaded {len(uploaded_files)} files',
                'uploaded_files': uploaded_files,
                'errors': errors
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No files were uploaded',
                'errors': errors
            }), 400
            
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download a specific file"""
    try:
        # Don't use secure_filename for download to preserve original names
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'message': 'File not found'}), 404
        
        # Check if it's actually a file and not a directory
        if not os.path.isfile(file_path):
            return jsonify({'success': False, 'message': 'Not a file'}), 404
        
        logger.info(f"File downloaded: {filename}")
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
        
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/files', methods=['GET'])
def list_files():
    """Get list of all files"""
    try:
        files = []
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    file_info = get_file_info(filename)
                    if file_info:
                        files.append(file_info)
        
        return jsonify({'success': True, 'files': files})
        
    except Exception as e:
        logger.error(f"List files error: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/files/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete a specific file"""
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'message': 'File not found'}), 404
        
        if not os.path.isfile(file_path):
            return jsonify({'success': False, 'message': 'Not a file'}), 404
        
        os.remove(file_path)
        logger.info(f"File deleted: {filename}")
        return jsonify({'success': True, 'message': f'File "{filename}" deleted successfully'})
        
    except Exception as e:
        logger.error(f"Delete error: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/info')
def server_info():
    """Get server information"""
    try:
        return jsonify({
            'success': True,
            'server_info': {
                'local_ip': get_local_ip(),
                'port': 5000,
                'upload_folder': UPLOAD_FOLDER,
                'restrictions': {
                    'max_file_size': 'UNLIMITED',
                    'allowed_extensions': 'ALL TYPES',
                    'timeout': 'NONE'
                }
            }
        })
    except Exception as e:
        logger.error(f"Server info error: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'success': False, 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({'success': False, 'message': 'Internal server error'}), 500

def print_server_info():
    """Print server startup information"""
    local_ip = get_local_ip()
    print("\n" + "="*70)
    print("🚀 UNLIMITED CROSS-PLATFORM FILE SHARING API")
    print("="*70)
    print(f"📂 Upload Directory: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"🌐 Local IP: {local_ip}")
    print(f"🔌 Port: 8000")
    print(f"📏 Max File Size: ♾️  UNLIMITED")
    print(f"📁 Allowed Extensions: ✅ ALL TYPES (.txt, .py, .exe, .dmg, .iso, etc.)")
    print(f"⏱️  Timeout: ❌ NONE")
    print("\n🔗 ACCESS URLS:")
    print(f"   Local: http://127.0.0.1:8000")
    print(f"   Network: http://{local_ip}:8000")
    print("\n📡 API ENDPOINTS:")
    print(f"   Upload: POST http://{local_ip}:8000/upload")
    print(f"   Download: GET http://{local_ip}:8000/download/<filename>")
    print(f"   List Files: GET http://{local_ip}:8000/api/files")
    print(f"   Delete: DELETE http://{local_ip}:8000/api/files/<filename>")
    print(f"   Server Info: GET http://{local_ip}:8000/api/info")
    print("\n💡 USAGE:")
    print("   1. Share the Network URL with your friend")
    print("   2. Upload ANY file type, ANY size")
    print("   3. No restrictions whatsoever")
    print("   4. Files saved in 'shared_files' directory")
    print("\n✅ FEATURES:")
    print("   • Accept ANY file extension")
    print("   • No file size limits")
    print("   • No timeout restrictions")
    print("   • Progress tracking for uploads")
    print("   • Cross-platform compatibility")
    print("   • Web interface + API access")
    print("\n⚠️  SECURITY NOTE:")
    print("   This server has NO restrictions - use responsibly!")
    print("   Only for trusted local network sharing.")
    print("="*70)


if __name__ == '__main__':
    try:
        print_server_info()
        
        # Run the server with no restrictions
        run_simple(
            hostname='0.0.0.0',  # Listen on all interfaces
            port=8000,
            application=app,
            use_reloader=False,
            use_debugger=False,
            threaded=True,
            request_handler=None,
            passthrough_errors=False
        )
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {str(e)}")
        logger.error(f"Server startup error: {str(e)}")