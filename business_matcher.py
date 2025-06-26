from typing import Dict, List, Tuple
import re
from datetime import datetime

class BusinessMatcher:
    """Handles matching logic for finding relevant business connections."""
    
    def __init__(self):
        self.sector_weights = {
            'exact_match': 1.0,
            'related': 0.7,
            'complementary': 0.5
        }
        
        # Define sector relationships
        self.sector_relationships = {
            'Technology': {
                'related': ['Finance', 'Healthcare'],
                'complementary': ['Manufacturing', 'Education']
            },
            'Finance': {
                'related': ['Technology', 'Real Estate'],
                'complementary': ['Healthcare', 'Retail']
            },
            'Healthcare': {
                'related': ['Technology', 'Education'],
                'complementary': ['Finance', 'Manufacturing']
            },
            'Manufacturing': {
                'related': ['Technology', 'Retail'],
                'complementary': ['Finance', 'Healthcare']
            },
            'Retail': {
                'related': ['Technology', 'Manufacturing'],
                'complementary': ['Finance', 'Education']
            },
            'Education': {
                'related': ['Technology', 'Healthcare'],
                'complementary': ['Finance', 'Retail']
            },
            'Real Estate': {
                'related': ['Finance', 'Technology'],
                'complementary': ['Retail', 'Manufacturing']
            }
        }
    
    def find_matches(self, business_need: Dict, companies: List[Dict] = None) -> List[Dict]:
        """
        Find matching companies for a business need.
        
        Args:
            business_need: The business need to match
            companies: List of companies to search (optional, will get from data manager if not provided)
        
        Returns:
            List of match dictionaries with company data and match scores
        """
        if companies is None:
            # In a real implementation, this would get companies from data manager
            # For now, we'll simulate with some sample companies
            companies = self._get_sample_companies()
        
        matches = []
        
        for company in companies:
            # Skip the company that created the business need
            if company['name'] == business_need['company_name']:
                continue
            
            match_score, reasons = self._calculate_match_score(business_need, company)
            
            if match_score > 0.3:  # Minimum threshold
                matches.append({
                    'company': company,
                    'score': match_score,
                    'reasons': reasons
                })
        
        # Sort by match score descending
        matches.sort(key=lambda x: x['score'], reverse=True)
        
        return matches[:10]  # Return top 10 matches
    
    def _calculate_match_score(self, business_need: Dict, company: Dict) -> Tuple[float, List[str]]:
        """Calculate match score between a business need and a company."""
        score = 0.0
        reasons = []
        
        # Sector matching
        sector_score, sector_reason = self._match_sectors(
            business_need.get('target_sectors', []), 
            company.get('sector', '')
        )
        score += sector_score * 0.4  # 40% weight
        if sector_reason:
            reasons.append(sector_reason)
        
        # Looking for type matching
        looking_for_score, looking_for_reason = self._match_looking_for(
            business_need.get('looking_for', ''), 
            company
        )
        score += looking_for_score * 0.3  # 30% weight
        if looking_for_reason:
            reasons.append(looking_for_reason)
        
        # Company size matching
        size_score, size_reason = self._match_company_size(
            business_need.get('budget_range', ''), 
            company.get('size', '')
        )
        score += size_score * 0.15  # 15% weight
        if size_reason:
            reasons.append(size_reason)
        
        # Tag matching
        tag_score, tag_reason = self._match_tags(
            business_need.get('description', ''), 
            company.get('tags', [])
        )
        score += tag_score * 0.15  # 15% weight
        if tag_reason:
            reasons.append(tag_reason)
        
        return min(score, 1.0), reasons
    
    def _match_sectors(self, target_sectors: List[str], company_sector: str) -> Tuple[float, str]:
        """Match target sectors with company sector."""
        if not target_sectors or not company_sector:
            return 0.0, ""
        
        # Exact match
        if company_sector in target_sectors:
            return self.sector_weights['exact_match'], f"Exact sector match ({company_sector})"
        
        # Related sector match
        for target_sector in target_sectors:
            if target_sector in self.sector_relationships:
                related = self.sector_relationships[target_sector].get('related', [])
                if company_sector in related:
                    return self.sector_weights['related'], f"Related sector ({company_sector} ↔ {target_sector})"
        
        # Complementary sector match
        for target_sector in target_sectors:
            if target_sector in self.sector_relationships:
                complementary = self.sector_relationships[target_sector].get('complementary', [])
                if company_sector in complementary:
                    return self.sector_weights['complementary'], f"Complementary sector ({company_sector} ↔ {target_sector})"
        
        return 0.0, ""
    
    def _match_looking_for(self, looking_for: str, company: Dict) -> Tuple[float, str]:
        """Match what the business need is looking for with company characteristics."""
        if not looking_for:
            return 0.0, ""
        
        company_size = company.get('size', '')
        company_tags = company.get('tags', [])
        company_description = company.get('description', '').lower()
        
        score = 0.0
        reason = ""
        
        if looking_for.lower() == 'investor':
            # Look for investment-related characteristics
            if 'finance' in company.get('sector', '').lower():
                score = 0.8
                reason = "Financial sector company (potential investor)"
            elif any(tag in ['investment', 'fund', 'venture', 'capital'] for tag in company_tags):
                score = 0.9
                reason = "Investment-related tags"
            elif company_size in ['201-1000', '1000+']:
                score = 0.5
                reason = "Large company (potential corporate investor)"
        
        elif looking_for.lower() == 'customer':
            # Look for potential customer characteristics
            if company_size in ['51-200', '201-1000', '1000+']:
                score = 0.7
                reason = "Good size for potential customer"
            elif 'b2b' in company_tags:
                score = 0.6
                reason = "B2B company (potential customer)"
        
        elif looking_for.lower() == 'supplier':
            # Look for supplier characteristics
            if 'manufacturing' in company.get('sector', '').lower():
                score = 0.8
                reason = "Manufacturing sector (potential supplier)"
            elif any(tag in ['supplier', 'manufacturing', 'b2b'] for tag in company_tags):
                score = 0.7
                reason = "Supplier-related characteristics"
        
        elif looking_for.lower() == 'partner':
            # Look for partnership characteristics
            if company_size in ['11-50', '51-200']:
                score = 0.6
                reason = "Similar size for partnership"
            elif any(tag in ['startup', 'innovation', 'tech'] for tag in company_tags):
                score = 0.7
                reason = "Innovation-focused (good partner)"
        
        return score, reason
    
    def _match_company_size(self, budget_range: str, company_size: str) -> Tuple[float, str]:
        """Match budget range with company size."""
        if not budget_range or not company_size:
            return 0.0, ""
        
        # Simple heuristic: larger budgets match with larger companies
        budget_score = {
            '$0-10K': 0.2,
            '$10K-50K': 0.4,
            '$50K-100K': 0.6,
            '$100K-500K': 0.8,
            '$500K+': 1.0
        }.get(budget_range, 0.0)
        
        size_score = {
            '1-10': 0.2,
            '11-50': 0.4,
            '51-200': 0.6,
            '201-1000': 0.8,
            '1000+': 1.0
        }.get(company_size, 0.0)
        
        # Match score based on how close budget and size are
        diff = abs(budget_score - size_score)
        score = max(0, 1.0 - diff)
        
        if score > 0.7:
            return score, f"Good budget-size match ({budget_range} ↔ {company_size})"
        elif score > 0.4:
            return score, f"Moderate budget-size match"
        else:
            return 0.0, ""
    
    def _match_tags(self, description: str, company_tags: List[str]) -> Tuple[float, str]:
        """Match business need description with company tags."""
        if not description or not company_tags:
            return 0.0, ""
        
        description_lower = description.lower()
        matched_tags = []
        
        for tag in company_tags:
            if tag.lower() in description_lower:
                matched_tags.append(tag)
        
        if matched_tags:
            score = min(len(matched_tags) * 0.2, 0.8)  # Max 0.8, 0.2 per tag
            return score, f"Keyword match: {', '.join(matched_tags)}"
        
        return 0.0, ""
    
    def _get_sample_companies(self) -> List[Dict]:
        """Get sample companies for testing (replace with actual data manager call)."""
        return [
            {
                'id': '1',
                'name': 'VentureCapital Partners',
                'sector': 'Finance',
                'size': '201-1000',
                'tags': ['investment', 'fund', 'venture', 'capital'],
                'description': 'Early stage venture capital fund focusing on technology startups'
            },
            {
                'id': '2',
                'name': 'TechSolutions Corp',
                'sector': 'Technology',
                'size': '51-200',
                'tags': ['b2b', 'saas', 'enterprise'],
                'description': 'Enterprise software solutions for businesses'
            },
            {
                'id': '3',
                'name': 'GreenManufacturing Inc',
                'sector': 'Manufacturing',
                'size': '201-1000',
                'tags': ['green', 'sustainable', 'manufacturing'],
                'description': 'Sustainable manufacturing equipment and solutions'
            },
            {
                'id': '4',
                'name': 'HealthTech Startup',
                'sector': 'Healthcare',
                'size': '11-50',
                'tags': ['startup', 'healthcare', 'innovation'],
                'description': 'Innovative healthcare technology solutions'
            },
            {
                'id': '5',
                'name': 'EnergyStorage Systems',
                'sector': 'Technology',
                'size': '51-200',
                'tags': ['energy', 'battery', 'storage', 'tech'],
                'description': 'Advanced battery technology and energy storage systems'
            }
        ]
    
    def get_match_explanation(self, business_need: Dict, company: Dict) -> str:
        """Get a detailed explanation of why a company matches a business need."""
        score, reasons = self._calculate_match_score(business_need, company)
        
        explanation = f"Match Score: {score:.1%}\n\n"
        explanation += "Matching Factors:\n"
        
        for reason in reasons:
            explanation += f"• {reason}\n"
        
        if not reasons:
            explanation += "• No significant matching factors found\n"
        
        return explanation 