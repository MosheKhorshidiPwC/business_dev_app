# Business Development Tool

A Streamlit-based prototype for business development and connection management. This tool helps identify business needs, match companies for potential partnerships, and manage the connection process.

## Features

### 🏢 Company Management
- Add and manage company profiles
- Track company details (sector, size, location, tags)
- View company databases with filtering

### 👥 Contact Management
- Manage contacts within companies
- Track contact roles and information
- Associate contacts with companies

### 🎯 Business Needs Management
- Create and track business needs
- Categorize needs by type (pre-sale, customer acquisition, etc.)
- Set priority levels and timelines
- Define target sectors and budget ranges

### 🔍 Intelligent Matching
- AI-powered matching algorithm
- Sector-based compatibility scoring
- Budget and company size matching
- Tag and keyword matching
- Multi-factor scoring system

### 📞 Connection Management
- Track connection status through pipeline stages
- Add notes and updates to connections
- Monitor communication history
- Automated email template generation (future)

### 📈 Analytics & Reporting
- Dashboard with key metrics
- Company distribution analytics
- Connection success tracking
- Timeline analysis
- Export capabilities

## Installation

1. Clone or download the repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Quick Start

1. **Load Sample Data**: Go to Settings → Sample Data → "Load Sample Data" to get started with example companies and business needs.

2. **Add Companies**: Navigate to the Companies page to add your own companies with details like sector, size, and tags.

3. **Create Business Needs**: Define what type of connections you're looking for in the Business Needs section.

4. **Find Matches**: Use the Matching & Connections page to find potential matches for your business needs.

5. **Manage Connections**: Track and update the status of your business connections.

## Application Structure

```
business_dev_app/
├── app.py                  # Main Streamlit application
├── data_manager.py         # Data storage and management
├── business_matcher.py     # Matching algorithm logic
├── connection_manager.py   # Connection and email management
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── business_data.json     # Data storage file (created automatically)
```

## Data Model

### Companies
- Basic information (name, sector, size, location)
- Descriptive data (description, tags, founded year)
- Contact information (website)

### Contacts
- Personal information (name, email, phone)
- Professional data (position, company, role type)
- Social links (LinkedIn)

### Business Needs
- Identification (title, company, type)
- Requirements (looking for, target sectors, budget)
- Timeline and priority
- Current status

### Connections
- Relationship mapping (from/to entities)
- Match scoring and reasoning
- Status tracking and notes
- Timeline information

## Matching Algorithm

The matching system uses a weighted scoring approach:

- **Sector Matching (40%)**: Exact, related, or complementary sector matches
- **Entity Type Matching (30%)**: Investor, customer, supplier, partner matching
- **Size/Budget Matching (15%)**: Company size vs budget range compatibility
- **Keyword Matching (15%)**: Tags and description analysis

## Future Enhancements

### Planned Features
- Excel integration for data import/export
- Email automation and templates
- External data source integration (web scraping)
- Advanced analytics and reporting
- API integrations for company data
- Automated follow-up scheduling
- Custom matching algorithm weights

### Database Migration
The current prototype uses JSON file storage. Future versions will support:
- Excel Web integration
- PostgreSQL/MySQL databases
- Cloud storage solutions
- Real-time data synchronization

## Usage Examples

### Creating a Business Need
1. Go to "Business Needs" → "Create Business Need"
2. Fill in the details:
   - Title: "Seeking Series A Investment"
   - Company: Select your company
   - Type: "Significant business event"
   - Looking for: "Investor"
   - Target sectors: ["Technology", "Finance"]
   - Budget range: "$500K+"

### Finding Matches
1. Navigate to "Matching & Connections"
2. Select your business need
3. Click "Find Matches"
4. Review the scored matches
5. Click "Initiate Connection" for relevant matches

### Managing Connections
1. Go to "Connection Management"
2. Update connection status as you progress
3. Add notes about interactions
4. Track success rates in Analytics

## Support

This is a prototype application. For questions or feature requests, please refer to the application documentation or contact the development team.

## License

This project is for internal use and evaluation purposes. 