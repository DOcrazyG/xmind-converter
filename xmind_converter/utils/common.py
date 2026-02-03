"""Common utility functions"""

import os
import tempfile
import zipfile


def ensure_directory(directory):
    """Ensure directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_file_extension(file_path):
    """Get file extension"""
    return os.path.splitext(file_path)[1].lower()


def is_xmind_file(file_path):
    """Check if it's an XMind file"""
    if not os.path.exists(file_path):
        return False
    return zipfile.is_zipfile(file_path)


def safe_filename(filename):
    """Generate safe filename"""
    import re
    # Remove or replace unsafe characters
    safe_name = re.sub(r'[<>:\\