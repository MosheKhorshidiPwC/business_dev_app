import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import uuid
from faker import Faker

class DataManager:
    """Manages all data operations for the business development tool."""
    
    def __init__(self, data_file: str = "business_data.json"):
        self.data_file = data_file
        self.data = self._load_data()
        self.fake = Faker()
    
    def _load_data(self) -> Dict:
        """Load data from JSON file or create empty structure."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        
        return {
            'companies': [],
            'contacts': [],
            'business_needs': [],
            'connections': [],
            'settings': {}
        }
    
    def _save_data(self):
        """Save data to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    # Company methods
    def add_company(self, company_data: Dict):
        """Add a new company."""
        self.data['companies'].append(company_data)
        self._save_data()
    
    def get_companies(self) -> List[Dict]:
        """Get all companies."""
        return self.data['companies']
    
    def get_company_by_id(self, company_id: str) -> Optional[Dict]:
        """Get a company by ID."""
        return next((c for c in self.data['companies'] if c['id'] == company_id), None)
    
    def get_company_by_name(self, name: str) -> Optional[Dict]:
        """Get a company by name."""
        return next((c for c in self.data['companies'] if c['name'] == name), None)
    
    def delete_company(self, company_name: str) -> bool:
        """Delete a company by name."""
        initial_count = len(self.data['companies'])
        self.data['companies'] = [c for c in self.data['companies'] if c['name'] != company_name]
        
        # Also delete associated contacts
        self.data['contacts'] = [c for c in self.data['contacts'] if c['company_name'] != company_name]
        
        # Update business needs to mark them as inactive if they reference this company
        for need in self.data['business_needs']:
            if need['company_name'] == company_name:
                need['status'] = 'inactive'
        
        if len(self.data['companies']) < initial_count:
            self._save_data()
            return True
        return False
    
    # Contact methods
    def add_contact(self, contact_data: Dict):
        """Add a new contact."""
        self.data['contacts'].append(contact_data)
        self._save_data()
    
    def get_contacts(self) -> List[Dict]:
        """Get all contacts."""
        return self.data['contacts']
    
    def get_contacts_by_company(self, company_name: str) -> List[Dict]:
        """Get contacts for a specific company."""
        return [c for c in self.data['contacts'] if c['company_name'] == company_name]
    
    def delete_contact(self, contact_id: str) -> bool:
        """Delete a contact by ID."""
        initial_count = len(self.data['contacts'])
        self.data['contacts'] = [c for c in self.data['contacts'] if c['id'] != contact_id]
        
        if len(self.data['contacts']) < initial_count:
            self._save_data()
            return True
        return False
    
    # Business need methods
    def add_business_need(self, business_need_data: Dict):
        """Add a new business need."""
        self.data['business_needs'].append(business_need_data)
        self._save_data()
    
    def get_business_needs(self) -> List[Dict]:
        """Get all business needs."""
        return self.data['business_needs']
    
    def get_business_need_by_id(self, need_id: str) -> Optional[Dict]:
        """Get a business need by ID."""
        return next((n for n in self.data['business_needs'] if n['id'] == need_id), None)
    
    def update_business_need_status(self, need_id: str, status: str):
        """Update business need status."""
        need = self.get_business_need_by_id(need_id)
        if need:
            need['status'] = status
            self._save_data()
    
    def delete_business_need(self, need_id: str) -> bool:
        """Delete a business need by ID."""
        initial_count = len(self.data['business_needs'])
        self.data['business_needs'] = [n for n in self.data['business_needs'] if n['id'] != need_id]
        
        # Also delete associated connections
        self.data['connections'] = [c for c in self.data['connections'] if c.get('business_need_id') != need_id]
        
        if len(self.data['business_needs']) < initial_count:
            self._save_data()
            return True
        return False
    
    # Connection methods
    def add_connection(self, connection_data: Dict):
        """Add a new connection."""
        self.data['connections'].append(connection_data)
        self._save_data()
    
    def get_connections(self) -> List[Dict]:
        """Get all connections."""
        return self.data['connections']
    
    def get_connection_by_id(self, connection_id: str) -> Optional[Dict]:
        """Get a connection by ID."""
        return next((c for c in self.data['connections'] if c['id'] == connection_id), None)
    
    def update_connection_status(self, connection_id: str, status: str):
        """Update connection status."""
        connection = self.get_connection_by_id(connection_id)
        if connection:
            connection['status'] = status
            connection['updated_date'] = datetime.now().isoformat()
            self._save_data()
    
    def update_connection_notes(self, connection_id: str, notes: str):
        """Update connection notes."""
        connection = self.get_connection_by_id(connection_id)
        if connection:
            connection['notes'] = notes
            connection['updated_date'] = datetime.now().isoformat()
            self._save_data()
    
    def delete_connection(self, connection_id: str) -> bool:
        """Delete a connection by ID."""
        initial_count = len(self.data['connections'])
        self.data['connections'] = [c for c in self.data['connections'] if c['id'] != connection_id]
        
        if len(self.data['connections']) < initial_count:
            self._save_data()
            return True
        return False
    
    # Data management methods
    def clear_all_data(self):
        """Clear all data."""
        self.data = {
            'companies': [],
            'contacts': [],
            'business_needs': [],
            'connections': [],
            'settings': {}
        }
        self._save_data()
    
    def load_sample_data(self):
        """Load sample data for testing."""
        # Sample companies
        sample_companies = [
            {
                'id': str(uuid.uuid4()),
                'name': 'TechStart Inc.',
                'sector': 'Technology',
                'size': '11-50',
                'website': 'https://techstart.example.com',
                'location': 'San Francisco, CA',
                'founded_year': 2020,
                'description': 'AI-powered marketing automation platform',
                'tags': ['startup', 'b2b', 'saas', 'ai'],
                'created_date': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'GreenEnergy Solutions',
                'sector': 'Manufacturing',
                'size': '51-200',
                'website': 'https://greenenergy.example.com',
                'location': 'Austin, TX',
                'founded_year': 2018,
                'description': 'Renewable energy equipment manufacturer',
                'tags': ['green', 'renewable', 'manufacturing'],
                'created_date': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'FinanceFlow',
                'sector': 'Finance',
                'size': '201-1000',
                'website': 'https://financeflow.example.com',
                'location': 'New York, NY',
                'founded_year': 2015,
                'description': 'Digital banking and payment solutions',
                'tags': ['fintech', 'banking', 'payments'],
                'created_date': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'HealthTech Innovations',
                'sector': 'Healthcare',
                'size': '11-50',
                'website': 'https://healthtech.example.com',
                'location': 'Boston, MA',
                'founded_year': 2021,
                'description': 'Telemedicine and health monitoring platform',
                'tags': ['healthcare', 'telemedicine', 'monitoring'],
                'created_date': datetime.now().isoformat()
            }
        ]
        
        # Sample contacts
        sample_contacts = [
            {
                'id': str(uuid.uuid4()),
                'name': 'John Smith',
                'email': 'john.smith@techstart.example.com',
                'company_name': 'TechStart Inc.',
                'position': 'CEO',
                'phone': '+1-555-0101',
                'linkedin': 'https://linkedin.com/in/johnsmith',
                'role_type': 'Decision Maker',
                'notes': 'Founder and CEO, very interested in partnerships',
                'created_date': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Sarah Johnson',
                'email': 'sarah.johnson@greenenergy.example.com',
                'company_name': 'GreenEnergy Solutions',
                'position': 'VP Sales',
                'phone': '+1-555-0102',
                'linkedin': 'https://linkedin.com/in/sarahjohnson',
                'role_type': 'Decision Maker',
                'notes': 'Leads sales efforts, looking for new markets',
                'created_date': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Michael Chen',
                'email': 'michael.chen@financeflow.example.com',
                'company_name': 'FinanceFlow',
                'position': 'CTO',
                'phone': '+1-555-0103',
                'linkedin': 'https://linkedin.com/in/michaelchen',
                'role_type': 'Technical',
                'notes': 'Technical leader, interested in API integrations',
                'created_date': datetime.now().isoformat()
            }
        ]
        
        # Sample business needs
        sample_business_needs = [
            {
                'id': str(uuid.uuid4()),
                'title': 'Seeking Series A Investment',
                'company_name': 'TechStart Inc.',
                'type': 'Significant business event',
                'priority': 'High',
                'looking_for': 'Investor',
                'target_sectors': ['Technology', 'Finance'],
                'budget_range': '$500K+',
                'timeline': '3-6 months',
                'description': 'Looking for Series A funding to scale our AI marketing platform. Need investors with experience in B2B SaaS.',
                'status': 'active',
                'created_date': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'title': 'Partnership for Energy Storage',
                'company_name': 'GreenEnergy Solutions',
                'type': 'Proactive customer contact',
                'priority': 'Medium',
                'looking_for': 'Partner',
                'target_sectors': ['Technology', 'Manufacturing'],
                'budget_range': '$100K-500K',
                'timeline': '6-12 months',
                'description': 'Seeking technology partners for advanced energy storage solutions. Looking for companies with battery technology expertise.',
                'status': 'active',
                'created_date': datetime.now().isoformat()
            }
        ]
        
        # Sample connections - showing different stages of the connection process
        sample_connections = [
            {
                'id': str(uuid.uuid4()),
                'business_need_id': sample_business_needs[0]['id'],  # Series A Investment need
                'from_entity': 'TechStart Inc.',
                'to_entity': 'FinanceFlow',
                'match_score': 0.75,
                'status': 'contacted',
                'created_date': (datetime.now() - timedelta(days=5)).isoformat(),
                'updated_date': (datetime.now() - timedelta(days=2)).isoformat(),
                'notes': f"[{(datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d %H:%M')}] Initial match created based on sector compatibility and company size.\n[{(datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M')}] Sent initial outreach email to Michael Chen. Waiting for response."
            },
            {
                'id': str(uuid.uuid4()),
                'business_need_id': sample_business_needs[1]['id'],  # Energy Storage Partnership
                'from_entity': 'GreenEnergy Solutions',
                'to_entity': 'TechStart Inc.',
                'match_score': 0.68,
                'status': 'responded',
                'created_date': (datetime.now() - timedelta(days=7)).isoformat(),
                'updated_date': (datetime.now() - timedelta(days=1)).isoformat(),
                'notes': f"[{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M')}] Auto-matched based on complementary technologies.\n[{(datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d %H:%M')}] Initial contact made through LinkedIn.\n[{(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M')}] Positive response received! John Smith is interested in exploring energy storage AI applications. Scheduling call for next week."
            },
            {
                'id': str(uuid.uuid4()),
                'business_need_id': sample_business_needs[0]['id'],  # Series A Investment need
                'from_entity': 'TechStart Inc.',
                'to_entity': 'HealthTech Innovations',
                'match_score': 0.82,
                'status': 'connected',
                'created_date': (datetime.now() - timedelta(days=14)).isoformat(),
                'updated_date': (datetime.now() - timedelta(days=3)).isoformat(),
                'notes': f"[{(datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d %H:%M')}] High match score due to similar sector and startup stage.\n[{(datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d %H:%M')}] Great initial call - they've been through Series A recently.\n[{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M')}] Introduced to their lead investor, Alexandra Rodriguez at MedTech Ventures.\n[{(datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d %H:%M')}] Connection established! Alexandra is reviewing our pitch deck."
            },
            {
                'id': str(uuid.uuid4()),
                'business_need_id': sample_business_needs[1]['id'],  # Energy Storage Partnership
                'from_entity': 'GreenEnergy Solutions',
                'to_entity': 'FinanceFlow',
                'match_score': 0.45,
                'status': 'initiated',
                'created_date': datetime.now().isoformat(),
                'updated_date': datetime.now().isoformat(),
                'notes': f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Recently identified potential match. FinanceFlow's payment solutions could complement our renewable energy customer financing needs. Research phase - need to identify best contact person."
            },
            {
                'id': str(uuid.uuid4()),
                'business_need_id': sample_business_needs[0]['id'],  # Series A Investment need
                'from_entity': 'TechStart Inc.',
                'to_entity': 'GreenEnergy Solutions',
                'match_score': 0.52,
                'status': 'closed',
                'created_date': (datetime.now() - timedelta(days=21)).isoformat(),
                'updated_date': (datetime.now() - timedelta(days=12)).isoformat(),
                'notes': f"[{(datetime.now() - timedelta(days=21)).strftime('%Y-%m-%d %H:%M')}] Explored potential corporate investment opportunity.\n[{(datetime.now() - timedelta(days=18)).strftime('%Y-%m-%d %H:%M')}] Had promising discussions about AI applications in renewable energy.\n[{(datetime.now() - timedelta(days=12)).strftime('%Y-%m-%d %H:%M')}] Decided to focus on technology partnership rather than investment. Connection closed for Series A purpose but keeping relationship warm for future collaboration."
            }
        ]
        
        # Load sample data
        self.data['companies'].extend(sample_companies)
        self.data['contacts'].extend(sample_contacts)
        self.data['business_needs'].extend(sample_business_needs)
        self.data['connections'].extend(sample_connections)
        
        self._save_data()
    
    def export_to_excel(self, filename: str = None):
        """Export data to Excel file (future implementation)."""
        if not filename:
            filename = f"business_data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # Future: Implement Excel export using openpyxl
        pass
    
    def import_from_excel(self, filename: str):
        """Import data from Excel file (future implementation)."""
        # Future: Implement Excel import using openpyxl
        pass 