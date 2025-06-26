import json
import os
from datetime import datetime
from typing import Dict, Optional

class BusinessLogger:
    """Handles logging of all business operations for audit trail."""
    
    def __init__(self, log_file: str = "business_operations.log"):
        self.log_file = log_file
        self.ensure_log_file_exists()
    
    def ensure_log_file_exists(self):
        """Create log file if it doesn't exist."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("=== Business Development Tool - Operations Log ===\n")
                f.write(f"Log started: {datetime.now().isoformat()}\n\n")
    
    def log_company_creation(self, company_data: Dict, user_note: str = ""):
        """Log company creation event."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": "COMPANY_CREATED",
            "company_id": company_data.get('id', 'N/A'),
            "company_name": company_data.get('name', 'N/A'),
            "sector": company_data.get('sector', 'N/A'),
            "size": company_data.get('size', 'N/A'),
            "location": company_data.get('location', 'N/A'),
            "user_note": user_note,
            "details": {
                "website": company_data.get('website', ''),
                "founded_year": company_data.get('founded_year', ''),
                "description": company_data.get('description', ''),
                "tags": company_data.get('tags', [])
            }
        }
        
        self._write_log_entry(log_entry)
    
    def log_company_deletion(self, company_data: Dict, deletion_reason: str, user_name: str = "System User"):
        """Log company deletion event."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": "COMPANY_DELETED",
            "company_id": company_data.get('id', 'N/A'),
            "company_name": company_data.get('name', 'N/A'),
            "sector": company_data.get('sector', 'N/A'),
            "deleted_by": user_name,
            "deletion_reason": deletion_reason,
            "original_data": company_data
        }
        
        self._write_log_entry(log_entry)
    
    def log_contact_creation(self, contact_data: Dict, user_note: str = ""):
        """Log contact creation event."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": "CONTACT_CREATED",
            "contact_id": contact_data.get('id', 'N/A'),
            "contact_name": contact_data.get('name', 'N/A'),
            "company_name": contact_data.get('company_name', 'N/A'),
            "position": contact_data.get('position', 'N/A'),
            "email": contact_data.get('email', 'N/A'),
            "user_note": user_note
        }
        
        self._write_log_entry(log_entry)
    
    def log_business_need_creation(self, need_data: Dict, user_note: str = ""):
        """Log business need creation event."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": "BUSINESS_NEED_CREATED",
            "need_id": need_data.get('id', 'N/A'),
            "title": need_data.get('title', 'N/A'),
            "company_name": need_data.get('company_name', 'N/A'),
            "type": need_data.get('type', 'N/A'),
            "looking_for": need_data.get('looking_for', 'N/A'),
            "priority": need_data.get('priority', 'N/A'),
            "user_note": user_note
        }
        
        self._write_log_entry(log_entry)
    
    def log_connection_creation(self, connection_data: Dict, user_note: str = ""):
        """Log connection creation event."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": "CONNECTION_CREATED",
            "connection_id": connection_data.get('id', 'N/A'),
            "from_entity": connection_data.get('from_entity', 'N/A'),
            "to_entity": connection_data.get('to_entity', 'N/A'),
            "match_score": connection_data.get('match_score', 0),
            "user_note": user_note
        }
        
        self._write_log_entry(log_entry)
    
    def _write_log_entry(self, log_entry: Dict):
        """Write a log entry to the log file."""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                timestamp = log_entry['timestamp']
                operation = log_entry['operation']
                
                # Write readable log entry
                f.write(f"\n{'='*60}\n")
                f.write(f"[{timestamp}] {operation}\n")
                f.write(f"{'='*60}\n")
                
                # Write details based on operation type
                if operation == "COMPANY_CREATED":
                    f.write(f"Company Name: {log_entry['company_name']}\n")
                    f.write(f"Company ID: {log_entry['company_id']}\n")
                    f.write(f"Sector: {log_entry['sector']}\n")
                    f.write(f"Size: {log_entry['size']}\n")
                    f.write(f"Location: {log_entry['location']}\n")
                    if log_entry['user_note']:
                        f.write(f"Note: {log_entry['user_note']}\n")
                    
                elif operation == "COMPANY_DELETED":
                    f.write(f"Company Name: {log_entry['company_name']}\n")
                    f.write(f"Company ID: {log_entry['company_id']}\n")
                    f.write(f"Deleted By: {log_entry['deleted_by']}\n")
                    f.write(f"Deletion Reason: {log_entry['deletion_reason']}\n")
                    f.write(f"Original Sector: {log_entry['sector']}\n")
                
                elif operation in ["CONTACT_CREATED", "BUSINESS_NEED_CREATED", "CONNECTION_CREATED"]:
                    for key, value in log_entry.items():
                        if key not in ['timestamp', 'operation']:
                            f.write(f"{key.replace('_', ' ').title()}: {value}\n")
                
                # Write JSON for detailed record
                f.write(f"\nJSON Record:\n{json.dumps(log_entry, indent=2, ensure_ascii=False)}\n")
                f.write(f"\n")
                
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def get_recent_logs(self, lines: int = 20) -> str:
        """Get recent log entries."""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
                return ''.join(recent_lines)
        except Exception as e:
            return f"Error reading log file: {e}"
    
    def search_logs(self, search_term: str) -> str:
        """Search for specific terms in logs."""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                matching_lines = [line for line in lines if search_term.lower() in line.lower()]
                return '\n'.join(matching_lines) if matching_lines else "No matching entries found."
        except Exception as e:
            return f"Error searching log file: {e}" 