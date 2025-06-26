from typing import Dict, List, Optional
from datetime import datetime, timedelta
import uuid

class ConnectionManager:
    """Manages business connections, email templates, and follow-ups."""
    
    def __init__(self):
        self.email_templates = {
            'initial_outreach': {
                'subject': 'Introduction - {from_company} & {to_company}',
                'body': """Dear {contact_name},

I hope this email finds you well. My name is {sender_name} from {from_company}.

{introduction_reason}

{value_proposition}

I believe there could be valuable synergies between our organizations. Would you be open to a brief conversation to explore potential collaboration opportunities?

I'd be happy to schedule a 15-20 minute call at your convenience.

Best regards,
{sender_name}
{sender_title}
{from_company}
{sender_contact}"""
            },
            'follow_up_1': {
                'subject': 'Re: Introduction - {from_company} & {to_company}',
                'body': """Hi {contact_name},

I wanted to follow up on my previous email regarding potential collaboration between {from_company} and {to_company}.

{follow_up_reason}

If now isn't the right time, I'd appreciate any guidance on when might be better or who else might be the right person to connect with.

Thank you for your time.

Best regards,
{sender_name}"""
            },
            'follow_up_2': {
                'subject': 'Final follow-up - {from_company} collaboration opportunity',
                'body': """Hi {contact_name},

This is my final follow-up regarding the potential collaboration opportunity between {from_company} and {to_company}.

I understand you're likely very busy, and I don't want to be persistent. If there's interest in the future, please feel free to reach out.

Thank you for your time and consideration.

Best regards,
{sender_name}"""
            },
            'introduction_email': {
                'subject': 'Introduction: {party1_name} <> {party2_name}',
                'body': """Hi {party1_name} and {party2_name},

I'm pleased to introduce you both as I believe there could be valuable synergies between your organizations.

{party1_name} - {party1_description}

{party2_name} - {party2_description}

{connection_reason}

I'll let you both take it from here. Wishing you a productive conversation!

Best regards,
{introducer_name}"""
            }
        }
        
        self.connection_stages = [
            'initiated',
            'contacted',
            'responded',
            'meeting_scheduled',
            'meeting_completed',
            'connected',
            'closed'
        ]
    
    def generate_email(self, template_type: str, **kwargs) -> Dict[str, str]:
        """
        Generate an email from a template.
        
        Args:
            template_type: Type of email template
            **kwargs: Variables to substitute in the template
        
        Returns:
            Dictionary with 'subject' and 'body' keys
        """
        if template_type not in self.email_templates:
            raise ValueError(f"Template type '{template_type}' not found")
        
        template = self.email_templates[template_type]
        
        try:
            subject = template['subject'].format(**kwargs)
            body = template['body'].format(**kwargs)
            
            return {
                'subject': subject,
                'body': body,
                'template_type': template_type,
                'generated_at': datetime.now().isoformat()
            }
        except KeyError as e:
            raise ValueError(f"Missing required parameter: {e}")
    
    def generate_initial_outreach_email(self, business_need: Dict, target_company: Dict, 
                                      sender_info: Dict, target_contact: Dict = None) -> Dict[str, str]:
        """Generate an initial outreach email for a business connection."""
        
        # Create introduction reason based on business need
        introduction_reason = self._create_introduction_reason(business_need)
        
        # Create value proposition
        value_proposition = self._create_value_proposition(business_need, target_company)
        
        # Prepare email variables
        email_vars = {
            'contact_name': target_contact.get('name', 'there') if target_contact else 'there',
            'sender_name': sender_info.get('name', ''),
            'sender_title': sender_info.get('title', ''),
            'sender_contact': sender_info.get('email', ''),
            'from_company': business_need['company_name'],
            'to_company': target_company['name'],
            'introduction_reason': introduction_reason,
            'value_proposition': value_proposition
        }
        
        return self.generate_email('initial_outreach', **email_vars)
    
    def generate_follow_up_email(self, connection: Dict, follow_up_number: int = 1) -> Dict[str, str]:
        """Generate a follow-up email for an existing connection."""
        
        template_type = f'follow_up_{follow_up_number}'
        if template_type not in self.email_templates:
            template_type = 'follow_up_2'  # Use final follow-up as default
        
        # Create follow-up reason
        follow_up_reason = self._create_follow_up_reason(connection, follow_up_number)
        
        email_vars = {
            'contact_name': connection.get('contact_name', 'there'),
            'sender_name': connection.get('sender_name', ''),
            'from_company': connection['from_entity'],
            'to_company': connection['to_entity'],
            'follow_up_reason': follow_up_reason
        }
        
        return self.generate_email(template_type, **email_vars)
    
    def generate_introduction_email(self, connection: Dict, party1_info: Dict, party2_info: Dict,
                                  introducer_info: Dict) -> Dict[str, str]:
        """Generate an introduction email connecting two parties."""
        
        connection_reason = self._create_connection_reason(connection)
        
        email_vars = {
            'party1_name': party1_info.get('name', ''),
            'party2_name': party2_info.get('name', ''),
            'party1_description': party1_info.get('description', ''),
            'party2_description': party2_info.get('description', ''),
            'connection_reason': connection_reason,
            'introducer_name': introducer_info.get('name', '')
        }
        
        return self.generate_email('introduction_email', **email_vars)
    
    def _create_introduction_reason(self, business_need: Dict) -> str:
        """Create an introduction reason based on the business need."""
        need_type = business_need.get('type', '')
        looking_for = business_need.get('looking_for', '')
        
        reasons = {
            'Pre-sale action': 'We are currently in our pre-sales process and exploring strategic partnerships.',
            'New customer acquisition': 'We are expanding our customer base and believe your company could benefit from our solutions.',
            'Proactive customer contact': 'We are reaching out to existing clients to explore additional collaboration opportunities.',
            'Significant business event': f"Following recent developments in our business, we are seeking {looking_for.lower()} partnerships.",
            'Professional management': 'As part of our ongoing business development efforts, we are connecting with industry leaders.',
            'Low communication frequency': 'We wanted to reconnect and explore current collaboration opportunities.'
        }
        
        return reasons.get(need_type, f'We are currently looking for {looking_for.lower()} partnerships and believe your company could be a great fit.')
    
    def _create_value_proposition(self, business_need: Dict, target_company: Dict) -> str:
        """Create a value proposition based on the business need and target company."""
        looking_for = business_need.get('looking_for', '').lower()
        target_sectors = business_need.get('target_sectors', [])
        company_sector = target_company.get('sector', '')
        
        propositions = {
            'investor': f"We are seeking investment to scale our operations in the {', '.join(target_sectors).lower()} sector(s). Your expertise in {company_sector.lower()} could provide valuable strategic guidance.",
            'customer': f"Our solutions could help streamline your operations in {company_sector.lower()} and drive significant value for your business.",
            'supplier': f"We believe your capabilities in {company_sector.lower()} could perfectly complement our business needs and help us serve our customers better.",
            'partner': f"A strategic partnership between our companies could create mutual value and help us both expand in the {company_sector.lower()} market.",
            'service provider': f"Your expertise in {company_sector.lower()} could help us enhance our service offerings and operational efficiency."
        }
        
        return propositions.get(looking_for, f"We believe there could be valuable synergies between our organizations in the {company_sector.lower()} space.")
    
    def _create_follow_up_reason(self, connection: Dict, follow_up_number: int) -> str:
        """Create a follow-up reason based on the connection and follow-up number."""
        if follow_up_number == 1:
            return "I wanted to check if you had a chance to review my previous message about potential collaboration opportunities."
        elif follow_up_number == 2:
            return "I realize you must be very busy, but I wanted to reach out one more time as I believe this opportunity could be mutually beneficial."
        else:
            return "I wanted to make one final attempt to connect, as I believe there could be significant value in exploring this opportunity together."
    
    def _create_connection_reason(self, connection: Dict) -> str:
        """Create a connection reason for introduction emails."""
        return f"Based on my understanding of both your businesses, I believe there could be valuable synergies worth exploring. The match score for this connection is {connection.get('match_score', 0):.0%}."
    
    def schedule_follow_up(self, connection_id: str, days_from_now: int = 7) -> Dict:
        """Schedule a follow-up for a connection."""
        follow_up_date = datetime.now() + timedelta(days=days_from_now)
        
        return {
            'id': str(uuid.uuid4()),
            'connection_id': connection_id,
            'scheduled_date': follow_up_date.isoformat(),
            'status': 'scheduled',
            'type': 'follow_up',
            'created_date': datetime.now().isoformat()
        }
    
    def get_connection_stage_next_actions(self, current_stage: str) -> List[str]:
        """Get suggested next actions for a connection stage."""
        actions = {
            'initiated': [
                'Send initial outreach email',
                'Research contact information',
                'Prepare company overview'
            ],
            'contacted': [
                'Wait for response (3-5 business days)',
                'Prepare for potential meeting',
                'Research their recent news/updates'
            ],
            'responded': [
                'Schedule introductory call',
                'Prepare meeting agenda',
                'Send calendar invite'
            ],
            'meeting_scheduled': [
                'Prepare presentation materials',
                'Research attendees',
                'Confirm meeting details'
            ],
            'meeting_completed': [
                'Send follow-up summary',
                'Share relevant documents',
                'Schedule next steps'
            ],
            'connected': [
                'Monitor relationship progress',
                'Schedule regular check-ins',
                'Track mutual value creation'
            ],
            'closed': [
                'Document lessons learned',
                'Update contact information',
                'Consider future opportunities'
            ]
        }
        
        return actions.get(current_stage, ['Review connection status'])
    
    def get_email_template_variables(self, template_type: str) -> List[str]:
        """Get the list of variables required for a specific email template."""
        if template_type not in self.email_templates:
            return []
        
        template = self.email_templates[template_type]
        import re
        
        variables = set()
        for text in [template['subject'], template['body']]:
            variables.update(re.findall(r'\{(\w+)\}', text))
        
        return sorted(list(variables))
    
    def validate_email_template_data(self, template_type: str, data: Dict) -> List[str]:
        """Validate that all required variables are provided for an email template."""
        required_vars = self.get_email_template_variables(template_type)
        missing_vars = [var for var in required_vars if var not in data or not data[var]]
        
        return missing_vars
    
    def get_connection_statistics(self, connections: List[Dict]) -> Dict:
        """Get statistics about connections."""
        if not connections:
            return {
                'total': 0,
                'by_status': {},
                'success_rate': 0,
                'average_score': 0
            }
        
        total = len(connections)
        by_status = {}
        successful = 0
        total_score = 0
        
        for conn in connections:
            status = conn.get('status', 'unknown')
            by_status[status] = by_status.get(status, 0) + 1
            
            if status in ['connected', 'meeting_completed']:
                successful += 1
            
            score = conn.get('match_score', 0)
            if isinstance(score, (int, float)):
                total_score += score
        
        return {
            'total': total,
            'by_status': by_status,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'average_score': (total_score / total * 100) if total > 0 else 0
        } 