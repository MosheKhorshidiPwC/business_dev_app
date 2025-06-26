import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional
import uuid

from data_manager import DataManager
from business_matcher import BusinessMatcher
from connection_manager import ConnectionManager
from logger import BusinessLogger

# Configure Streamlit page
st.set_page_config(
    page_title="Business Development Tool",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()
if 'business_matcher' not in st.session_state:
    st.session_state.business_matcher = BusinessMatcher()
if 'connection_manager' not in st.session_state:
    st.session_state.connection_manager = ConnectionManager()
if 'logger' not in st.session_state:
    st.session_state.logger = BusinessLogger()
if 'show_delete_confirmation' not in st.session_state:
    st.session_state.show_delete_confirmation = False
if 'company_to_delete' not in st.session_state:
    st.session_state.company_to_delete = None

def show_delete_confirmation_dialog():
    """Show confirmation dialog for company deletion."""
    company = st.session_state.company_to_delete
    
    if company:
        # Create a prominent confirmation section
        st.error("🚨 COMPANY DELETION CONFIRMATION")
        
        with st.container():
            st.markdown("---")
            st.warning(f"⚠️ You are about to delete **{company['name']}**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**This action will:**")
                st.write("• Delete the company permanently")
                st.write("• Remove all associated contacts")
                st.write("• Mark related business needs as inactive")
            with col2:
                st.write("**Company Details:**")
                st.write(f"• Name: {company['name']}")
                st.write(f"• Sector: {company.get('sector', 'N/A')}")
                st.write(f"• Location: {company.get('location', 'N/A')}")
            
            st.error("⚠️ **THIS ACTION CANNOT BE UNDONE**")
            st.markdown("---")
            
            # Reason input
            deletion_reason = st.text_area(
                "Please provide a reason for deletion (required):",
                placeholder="e.g., Duplicate entry, Company closed, Data cleanup, etc.",
                help="This will be logged for audit purposes",
                key="deletion_reason_input"
            )
            
            # User name input
            user_name = st.text_input(
                "Your name (optional):",
                placeholder="Enter your name for audit trail",
                help="This helps track who performed the deletion",
                key="deletion_user_input"
            )
            
            if not user_name:
                user_name = "System User"
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("❌ Cancel", use_container_width=True, key="cancel_deletion"):
                    st.session_state.show_delete_confirmation = False
                    st.session_state.company_to_delete = None
                    st.rerun()
            
            with col2:
                pass  # Empty column for spacing
            
            with col3:
                if st.button("🗑️ Delete Company", type="primary", use_container_width=True, key="confirm_deletion"):
                    if deletion_reason.strip():
                        # Log the deletion before performing it
                        st.session_state.logger.log_company_deletion(
                            company, 
                            deletion_reason.strip(), 
                            user_name
                        )
                        
                        # Perform the deletion
                        if st.session_state.data_manager.delete_company(company['name']):
                            st.success(f"Company '{company['name']}' has been deleted successfully!")
                            st.session_state.show_delete_confirmation = False
                            st.session_state.company_to_delete = None
                            st.rerun()
                        else:
                            st.error("Failed to delete company. Please try again.")
                    else:
                        st.error("Please provide a reason for deletion.")
            
            st.markdown("---")

def create_sample_connections():
    """Create sample connections to demonstrate the Connection Management functionality."""
    # Get existing business needs
    business_needs = st.session_state.data_manager.get_business_needs()
    
    if not business_needs:
        st.error("Please load sample data first (Companies and Business Needs are required)")
        return False
    
    # Sample connections with realistic scenarios
    sample_connections = [
        {
            'id': str(uuid.uuid4()),
            'business_need_id': business_needs[0]['id'] if len(business_needs) > 0 else str(uuid.uuid4()),
            'from_entity': 'TechStart Inc.',
            'to_entity': 'Top VC',
            'match_score': 0.85,
            'status': 'contacted',
            'created_date': (datetime.now() - timedelta(days=5)).isoformat(),
            'updated_date': (datetime.now() - timedelta(days=2)).isoformat(),
            'notes': f"[{(datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d %H:%M')}] High match score! Top VC specializes in tech startups seeking Series A.\n[{(datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M')}] Sent initial pitch deck to their investment team. Waiting for response."
        },
        {
            'id': str(uuid.uuid4()),
            'business_need_id': business_needs[1]['id'] if len(business_needs) > 1 else str(uuid.uuid4()),
            'from_entity': 'GreenEnergy Solutions',
            'to_entity': 'Amos Company',
            'match_score': 0.72,
            'status': 'responded',
            'created_date': (datetime.now() - timedelta(days=7)).isoformat(),
            'updated_date': (datetime.now() - timedelta(days=1)).isoformat(),
            'notes': f"[{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M')}] Matched based on B2B SaaS expertise for energy sector.\n[{(datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d %H:%M')}] Initial contact made through LinkedIn.\n[{(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M')}] Great response! They're interested in exploring energy management software partnerships. Scheduling call for this week."
        },
        {
            'id': str(uuid.uuid4()),
            'business_need_id': business_needs[0]['id'] if len(business_needs) > 0 else str(uuid.uuid4()),
            'from_entity': 'TechStart Inc.',
            'to_entity': 'Sivan Company',
            'match_score': 0.68,
            'status': 'connected',
            'created_date': (datetime.now() - timedelta(days=14)).isoformat(),
            'updated_date': (datetime.now() - timedelta(days=3)).isoformat(),
            'notes': f"[{(datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d %H:%M')}] Healthcare tech + AI marketing = interesting synergy for health/fitness customer acquisition.\n[{(datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d %H:%M')}] Excellent first call - they need better customer acquisition tools.\n[{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M')}] Pilot program agreed! Testing our AI marketing platform for their fitness app.\n[{(datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d %H:%M')}] SUCCESS! Connection established - they became a paying customer and strategic partner."
        },
        {
            'id': str(uuid.uuid4()),
            'business_need_id': business_needs[1]['id'] if len(business_needs) > 1 else str(uuid.uuid4()),
            'from_entity': 'GreenEnergy Solutions',
            'to_entity': 'FinanceFlow',
            'match_score': 0.58,
            'status': 'initiated',
            'created_date': datetime.now().isoformat(),
            'updated_date': datetime.now().isoformat(),
            'notes': f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] New potential match identified. FinanceFlow's payment solutions could help our customers finance renewable energy installations. Researching their partnership program."
        },
        {
            'id': str(uuid.uuid4()),
            'business_need_id': business_needs[0]['id'] if len(business_needs) > 0 else str(uuid.uuid4()),
            'from_entity': 'TechStart Inc.',
            'to_entity': 'Noa Company',
            'match_score': 0.45,
            'status': 'closed',
            'created_date': (datetime.now() - timedelta(days=21)).isoformat(),
            'updated_date': (datetime.now() - timedelta(days=12)).isoformat(),
            'notes': f"[{(datetime.now() - timedelta(days=21)).strftime('%Y-%m-%d %H:%M')}] Explored potential B2C application of our B2B platform.\n[{(datetime.now() - timedelta(days=18)).strftime('%Y-%m-%d %H:%M')}] Interesting discussions but different target markets.\n[{(datetime.now() - timedelta(days=12)).strftime('%Y-%m-%d %H:%M')}] Decided not to pursue - focus mismatch between B2B and B2C. Maintaining friendly relationship for future opportunities."
        }
    ]
    
    # Add connections to the database
    for connection in sample_connections:
        st.session_state.data_manager.add_connection(connection)
    
    return True

def main():
    st.title("🤝 Business Development Tool")
    st.sidebar.title("Navigation")
    
    # Show delete confirmation dialog if needed (takes priority over other pages)
    if st.session_state.show_delete_confirmation:
        show_delete_confirmation_dialog()
        return  # Don't show other pages while confirming deletion
    
    # Sidebar navigation
    pages = {
        "Dashboard": dashboard_page,
        "Companies": companies_page,
        "Contacts": contacts_page,
        "Business Needs": business_needs_page,
        "Matching & Connections": matching_page,
        "Connection Management": connection_management_page,
        "Analytics": analytics_page,
        "Settings": settings_page
    }
    
    selected_page = st.sidebar.selectbox("Select Page", list(pages.keys()))
    
    # Display selected page
    pages[selected_page]()

def dashboard_page():
    st.header("📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get current data
    companies = st.session_state.data_manager.get_companies()
    contacts = st.session_state.data_manager.get_contacts()
    business_needs = st.session_state.data_manager.get_business_needs()
    connections = st.session_state.data_manager.get_connections()
    
    with col1:
        st.metric("Total Companies", len(companies))
    with col2:
        st.metric("Total Contacts", len(contacts))
    with col3:
        st.metric("Active Business Needs", len([n for n in business_needs if n['status'] == 'active']))
    with col4:
        st.metric("Total Connections", len(connections))
    
    # Recent activity
    st.subheader("Recent Activity")
    if connections:
        recent_connections = sorted(connections, key=lambda x: x['created_date'], reverse=True)[:5]
        for conn in recent_connections:
            st.write(f"📞 {conn['from_entity']} → {conn['to_entity']} ({conn['status']})")
    else:
        st.info("No recent connections found. Start by adding companies and creating business needs!")
    
    # Quick actions
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add New Company"):
            st.session_state.quick_action = "add_company"
            st.rerun()
    
    with col2:
        if st.button("🎯 Create Business Need"):
            st.session_state.quick_action = "add_business_need"
            st.rerun()
    
    with col3:
        if st.button("🔍 Find Matches"):
            st.session_state.quick_action = "find_matches"
            st.rerun()

def companies_page():
    st.header("🏢 Companies Management")
    
    tab1, tab2 = st.tabs(["View Companies", "Add Company"])
    
    with tab1:
        companies = st.session_state.data_manager.get_companies()
        
        if companies:
            # Dataframe in expander
            with st.expander("Companies"):
                df = pd.DataFrame(companies)
                st.table(df)
            
            # Company selection and actions outside expander
            selected_company_name = st.selectbox("Select company for details/actions", ["No Selection"] + [c['name'] for c in companies])
            
            if selected_company_name and selected_company_name != "No Selection":
                company = next((c for c in companies if c['name'] == selected_company_name), None)
                if company:
                    # Display company details
                    st.subheader("Company Details")
                    
                    # Basic information in columns
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Company Size", company.get('size', 'N/A'))
                    with col2:
                        st.metric("Founded", company.get('founded_year', 'N/A'))
                    with col3:
                        st.metric("Sector", company.get('sector', 'N/A'))
                    
                    # Contact and location info
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**📍 Location:**", company.get('location', 'Not specified'))
                        if company.get('website'):
                            st.write("**🌐 Website:**", f"[{company['website']}]({company['website']})")
                        else:
                            st.write("**🌐 Website:** Not specified")
                    
                    with col1:
                        if company.get('description'):
                            st.write("**📝 Description:**")
                            st.write(company['description'])
                        else:
                            st.write("**📝 Description:** No description available")
                    
                    # Tags display
                    if company.get('tags'):
                        st.write("**🏷️ Tags:**")
                        tag_cols = st.columns(min(len(company['tags']), 4))
                        for i, tag in enumerate(company['tags']):
                            with tag_cols[i % 4]:
                                st.markdown(f"`{tag}`")
                    else:
                        st.write("**🏷️ Tags:** No tags")
                    
                    # Created date
                    if company.get('created_date'):
                        try:
                            created_date = datetime.fromisoformat(company['created_date'].replace('Z', '+00:00'))
                            st.caption(f"Added to system: {created_date.strftime('%B %d, %Y at %H:%M')}")
                        except:
                            st.caption(f"Added to system: {company['created_date']}")
                    
                    st.divider()
                    
                    # Delete button and warning
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if st.button("🗑️ Delete Company", type="secondary"):
                            st.session_state.company_to_delete = company
                            st.session_state.show_delete_confirmation = True
                            st.rerun()
                    with col1:
                        st.warning("⚠️ This will also delete all associated contacts and mark related business needs as inactive.")
        else:
            st.info("No companies found. Add your first company below!")

    with tab2:
        with st.form("add_company_form"):
            st.subheader("Add New Company")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Company Name*", key="company_name")
                sector = st.selectbox("Sector", [
                    "Technology", "Finance", "Healthcare", "Manufacturing", 
                    "Retail", "Education", "Real Estate", "Other"
                ])
                size = st.selectbox("Company Size", [
                    "1-10", "11-50", "51-200", "201-1000", "1000+"
                ])
                website = st.text_input("Website")
            
            with col2:
                location = st.text_input("Location")
                founded_year = st.number_input("Founded Year", min_value=1800, max_value=2024, value=2020)
                description = st.text_area("Description")
                tags = st.text_input("Tags (comma-separated)", help="e.g., startup, b2b, saas")
            
            submitted = st.form_submit_button("Add Company")
            
            if submitted and name:
                company_data = {
                    'id': str(uuid.uuid4()),
                    'name': name,
                    'sector': sector,
                    'size': size,
                    'website': website,
                    'location': location,
                    'founded_year': founded_year,
                    'description': description,
                    'tags': [tag.strip() for tag in tags.split(',') if tag.strip()],
                    'created_date': datetime.now().isoformat()
                }
                
                # Log company creation
                st.session_state.logger.log_company_creation(company_data, "Company created via web interface")
                
                # Add company to database
                st.success(f"Company '{name}' added successfully!")
                st.session_state.data_manager.add_company(company_data)
                st.rerun()
                

def contacts_page():
    st.header("👥 Contacts Management")
    
    tab1, tab2 = st.tabs(["View Contacts", "Add Contact"])
    
    with tab1:
        contacts = st.session_state.data_manager.get_contacts()
        if contacts:
            df = pd.DataFrame(contacts)
            st.table(df)
        else:
            st.info("No contacts found. Add your first contact below!")
    
    with tab2:
        companies = st.session_state.data_manager.get_companies()
        
        if not companies:
            st.warning("Please add companies first before adding contacts.")
            return
        
        with st.form("add_contact_form"):
            st.subheader("Add New Contact")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name*")
                email = st.text_input("Email*")
                company_name = st.selectbox("Company", [c['name'] for c in companies])
                position = st.text_input("Position")
            
            with col2:
                phone = st.text_input("Phone")
                linkedin = st.text_input("LinkedIn Profile")
                role_type = st.selectbox("Role Type", [
                    "Decision Maker", "Influencer", "User", "Technical", "Financial"
                ])
                notes = st.text_area("Notes")
            
            submitted = st.form_submit_button("Add Contact")
            
            if submitted and name and email:
                contact_data = {
                    'id': str(uuid.uuid4()),
                    'name': name,
                    'email': email,
                    'company_name': company_name,
                    'position': position,
                    'phone': phone,
                    'linkedin': linkedin,
                    'role_type': role_type,
                    'notes': notes,
                    'created_date': datetime.now().isoformat()
                }
                
                st.session_state.data_manager.add_contact(contact_data)
                st.success(f"Contact '{name}' added successfully!")
                st.rerun()

def business_needs_page():
    st.header("🎯 Business Needs Management")
    
    tab1, tab2 = st.tabs(["View Business Needs", "Create Business Need"])
    
    with tab1:
        business_needs = st.session_state.data_manager.get_business_needs()
        if business_needs:
            for need in business_needs:
                with st.expander(f"{need['title']} - {need['type']} ({need['status']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Company:** {need['company_name']}")
                        st.write(f"**Type:** {need['type']}")
                        st.write(f"**Priority:** {need['priority']}")
                    with col2:
                        st.write(f"**Status:** {need['status']}")
                        st.write(f"**Created:** {need['created_date'][:10]}")
                    st.write(f"**Description:** {need['description']}")
        else:
            st.info("No business needs found. Create your first business need below!")
    
    with tab2:
        companies = st.session_state.data_manager.get_companies()
        
        if not companies:
            st.warning("Please add companies first before creating business needs.")
            return
        
        with st.form("add_business_need_form"):
            st.subheader("Create New Business Need")
            
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Title*")
                company_name = st.selectbox("Company", [c['name'] for c in companies])
                need_type = st.selectbox("Type", [
                    "Pre-sale action", "New customer acquisition", 
                    "Proactive customer contact", "Significant business event",
                    "Professional management", "Low communication frequency"
                ])
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            
            with col2:
                looking_for = st.selectbox("Looking For", [
                    "Investor", "Customer", "Supplier", "Partner", 
                    "Service Provider", "Mentor", "Other"
                ])
                target_sectors = st.multiselect("Target Sectors", [
                    "Technology", "Finance", "Healthcare", "Manufacturing", 
                    "Retail", "Education", "Real Estate", "Other"
                ])
                budget_range = st.selectbox("Budget Range", [
                    "$0-10K", "$10K-50K", "$50K-100K", "$100K-500K", "$500K+"
                ])
                timeline = st.selectbox("Timeline", [
                    "Immediate", "1-3 months", "3-6 months", "6-12 months", "12+ months"
                ])
            
            description = st.text_area("Description*")
            
            submitted = st.form_submit_button("Create Business Need")
            
            if submitted and title and description:
                business_need_data = {
                    'id': str(uuid.uuid4()),
                    'title': title,
                    'company_name': company_name,
                    'type': need_type,
                    'priority': priority,
                    'looking_for': looking_for,
                    'target_sectors': target_sectors,
                    'budget_range': budget_range,
                    'timeline': timeline,
                    'description': description,
                    'status': 'active',
                    'created_date': datetime.now().isoformat()
                }
                
                st.session_state.data_manager.add_business_need(business_need_data)
                st.success(f"Business need '{title}' created successfully!")
                st.rerun()

def matching_page():
    st.header("🔍 Matching & Connections")
    
    business_needs = st.session_state.data_manager.get_business_needs()
    active_needs = [n for n in business_needs if n['status'] == 'active']
    
    if not active_needs:
        st.warning("No active business needs found. Please create some business needs first.")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Select Business Need")
        selected_need = st.selectbox(
            "Choose a business need to find matches:",
            [""] + [f"{need['title']} ({need['company_name']})" for need in active_needs]
        )
    
    if selected_need:
        # Find the selected business need
        need = next((n for n in active_needs if f"{n['title']} ({n['company_name']})" == selected_need), None)
        
        if need:
            with col2:
                st.subheader("Business Need Details")
                st.write(f"**Company:** {need['company_name']}")
                st.write(f"**Looking for:** {need['looking_for']}")
                st.write(f"**Target Sectors:** {', '.join(need['target_sectors'])}")
                st.write(f"**Budget:** {need['budget_range']}")
                st.write(f"**Timeline:** {need['timeline']}")
            
            # Find matches
            if st.button("🔍 Find Matches"):
                with st.spinner("Finding matches..."):
                    # Get companies for matching
                    companies = st.session_state.data_manager.get_companies()
                    matches = st.session_state.business_matcher.find_matches(need, companies)
                
                if matches:
                    st.subheader("Potential Matches")
                    
                    for match in matches:
                        with st.expander(f"Match: {match['company']['name']} (Score: {match['score']:.0%})"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.write(f"**Company:** {match['company']['name']}")
                                st.write(f"**Sector:** {match['company']['sector']}")
                                st.write(f"**Size:** {match['company']['size']}")
                                
                            with col2:
                                st.write(f"**Match Score:** {match['score']:.0%}")
                                st.write(f"**Reasons:** {', '.join(match['reasons'])}")
                                
                            with col3:
                                if st.button(f"Initiate Connection", key=f"connect_{match['company']['id']}"):
                                    connection_data = {
                                        'id': str(uuid.uuid4()),
                                        'business_need_id': need['id'],
                                        'from_entity': need['company_name'],
                                        'to_entity': match['company']['name'],
                                        'match_score': match['score'],
                                        'status': 'initiated',
                                        'created_date': datetime.now().isoformat(),
                                        'notes': f"Auto-matched based on: {', '.join(match['reasons'])}"
                                    }
                                    st.session_state.data_manager.add_connection(connection_data)
                                    st.success("Connection initiated!")
                                    st.rerun()
                else:
                    st.info("No matches found for this business need.")

def connection_management_page():
    st.header("📞 Connection Management")
    
    connections = st.session_state.data_manager.get_connections()
    
    if not connections:
        st.info("No connections found. You can create sample connections to see the functionality!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔗 Create Sample Connections", type="primary"):
                if create_sample_connections():
                    st.success("Sample connections created successfully!")
                    st.rerun()
        
        with col2:
            st.info("💡 Or go to 'Matching & Connections' to create real matches from your business needs")
        
        return
    
    # Filter connections by status
    status_filter = st.selectbox("Filter by Status", ["All", "initiated", "contacted", "responded", "connected", "closed"])
    
    filtered_connections = connections
    if status_filter != "All":
        filtered_connections = [c for c in connections if c['status'] == status_filter]
    
    for connection in filtered_connections:
        with st.expander(f"{connection['from_entity']} → {connection['to_entity']} ({connection['status']})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**From:** {connection['from_entity']}")
                st.write(f"**To:** {connection['to_entity']}")
                st.write(f"**Match Score:** {connection.get('match_score', 0):.0%}")
            
            with col2:
                st.write(f"**Status:** {connection['status']}")
                st.write(f"**Created:** {connection['created_date'][:10]}")
                
            with col3:
                new_status = st.selectbox(
                    "Update Status",
                    ["initiated", "contacted", "responded", "connected", "closed"],
                    index=["initiated", "contacted", "responded", "connected", "closed"].index(connection['status']),
                    key=f"status_{connection['id']}"
                )
                
                if st.button("Update", key=f"update_{connection['id']}"):
                    st.session_state.data_manager.update_connection_status(connection['id'], new_status)
                    st.success("Status updated!")
                    st.rerun()
            
            st.write(f"**Notes:** {connection.get('notes', 'No notes')}")
            
            # Add notes
            new_note = st.text_area("Add Note", key=f"note_{connection['id']}")
            if st.button("Add Note", key=f"add_note_{connection['id']}") and new_note:
                current_notes = connection.get('notes', '')
                updated_notes = f"{current_notes}\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {new_note}"
                st.session_state.data_manager.update_connection_notes(connection['id'], updated_notes)
                st.success("Note added!")
                st.rerun()

def analytics_page():
    st.header("📈 Analytics & Reports")
    
    companies = st.session_state.data_manager.get_companies()
    connections = st.session_state.data_manager.get_connections()
    business_needs = st.session_state.data_manager.get_business_needs()
    
    if not companies and not connections:
        st.info("No data available for analytics. Add some companies and create connections first!")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Company sectors pie chart
        if companies:
            st.subheader("Companies by Sector")
            sector_counts = {}
            for company in companies:
                sector = company.get('sector', 'Unknown')
                sector_counts[sector] = sector_counts.get(sector, 0) + 1
            
            fig_pie = px.pie(
                values=list(sector_counts.values()),
                names=list(sector_counts.keys()),
                title="Company Distribution by Sector"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Connection status chart
        if connections:
            st.subheader("Connections by Status")
            status_counts = {}
            for connection in connections:
                status = connection.get('status', 'Unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            fig_bar = px.bar(
                x=list(status_counts.keys()),
                y=list(status_counts.values()),
                title="Connection Status Distribution"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Connections over time
    if connections:
        st.subheader("Connections Over Time")
        connection_dates = [datetime.fromisoformat(c['created_date']).date() for c in connections]
        date_counts = {}
        for date in connection_dates:
            date_counts[date] = date_counts.get(date, 0) + 1
        
        if date_counts:
            fig_line = px.line(
                x=list(date_counts.keys()),
                y=list(date_counts.values()),
                title="Connections Created Over Time"
            )
            st.plotly_chart(fig_line, use_container_width=True)
    
    # Success metrics
    if connections:
        st.subheader("Success Metrics")
        
        total_connections = len(connections)
        successful_connections = len([c for c in connections if c['status'] == 'connected'])
        success_rate = (successful_connections / total_connections * 100) if total_connections > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Connections", total_connections)
        with col2:
            st.metric("Successful Connections", successful_connections)
        with col3:
            st.metric("Success Rate", f"{success_rate:.1f}%")

def settings_page():
    st.header("⚙️ Settings")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Data Export", "Sample Data", "Configuration", "Audit Logs"])
    
    with tab1:
        st.subheader("Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Export Companies to CSV"):
                companies = st.session_state.data_manager.get_companies()
                if companies:
                    df = pd.DataFrame(companies)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download Companies CSV",
                        data=csv,
                        file_name=f"companies_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No companies to export")
        
        with col2:
            if st.button("Export Connections to CSV"):
                connections = st.session_state.data_manager.get_connections()
                if connections:
                    df = pd.DataFrame(connections)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download Connections CSV",
                        data=csv,
                        file_name=f"connections_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No connections to export")
    
    with tab2:
        st.subheader("Sample Data")
        st.write("Load sample data to test the application")
        
        if st.button("Load Sample Data"):
            st.session_state.data_manager.load_sample_data()
            st.success("Sample data loaded successfully!")
            st.rerun()
        
        if st.button("Clear All Data"):
            if st.checkbox("I understand this will delete all data"):
                st.session_state.data_manager.clear_all_data()
                st.success("All data cleared!")
                st.rerun()
    
    with tab3:
        st.subheader("Configuration")
        st.info("Future: Configure API keys, email templates, matching algorithms, etc.")
    
    with tab4:
        st.subheader("📋 Audit Logs")
        st.write("View all system operations and changes for audit purposes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Refresh Logs"):
                st.rerun()
        
        with col2:
            search_term = st.text_input("🔍 Search logs", placeholder="Enter search term...")
        
        st.divider()
        
        if search_term:
            st.subheader(f"Search Results for: '{search_term}'")
            search_results = st.session_state.logger.search_logs(search_term)
            if search_results and "No matching entries found" not in search_results:
                st.text(search_results)
            else:
                st.info("No matching log entries found.")
        else:
            st.subheader("Recent Operations (Last 50 lines)")
            recent_logs = st.session_state.logger.get_recent_logs(50)
            if recent_logs:
                st.text(recent_logs)
            else:
                st.info("No log entries found.")
        
        st.divider()
        
        # Download logs option
        if st.button("💾 Download Full Log File"):
            try:
                with open("business_operations.log", "r", encoding='utf-8') as f:
                    log_content = f.read()
                
                st.download_button(
                    label="Download Log File",
                    data=log_content,
                    file_name=f"business_operations_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
                    mime="text/plain"
                )
            except FileNotFoundError:
                st.warning("No log file found yet. Perform some operations first.")

if __name__ == "__main__":
    main() 