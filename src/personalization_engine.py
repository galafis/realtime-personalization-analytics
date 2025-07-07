"""
Real-Time Customer Personalization Engine
Advanced ML-powered personalization using GCP and streaming analytics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Optional
import random
from dataclasses import dataclass
import uuid

@dataclass
class CustomerProfile:
    """Customer profile for personalization"""
    customer_id: str
    age: int
    income: float
    segment: str
    preferences: Dict[str, float]
    behavior_score: float
    last_interaction: datetime
    
@dataclass
class PersonalizationRecommendation:
    """Personalization recommendation result"""
    customer_id: str
    recommendation_type: str
    content: str
    confidence_score: float
    expected_engagement: float
    timestamp: datetime

class RealTimePersonalizationEngine:
    """Real-time personalization engine using ML and streaming data"""
    
    def __init__(self, seed: int = 42):
        """Initialize personalization engine"""
        np.random.seed(seed)
        random.seed(seed)
        
        # Product categories and their characteristics
        self.product_categories = {
            'financial_services': {
                'products': ['Credit Card', 'Personal Loan', 'Investment', 'Insurance'],
                'engagement_factors': ['income', 'age', 'credit_score']
            },
            'digital_banking': {
                'products': ['Mobile App', 'Online Banking', 'Digital Wallet', 'API Services'],
                'engagement_factors': ['tech_savviness', 'transaction_frequency']
            },
            'investment_products': {
                'products': ['Stocks', 'Bonds', 'Mutual Funds', 'Crypto', 'Real Estate'],
                'engagement_factors': ['risk_tolerance', 'income', 'age']
            }
        }
        
        # Content types for recommendations
        self.content_types = [
            'product_recommendation', 'educational_content', 'promotional_offer',
            'risk_assessment', 'portfolio_optimization', 'market_insights'
        ]
        
        # Behavioral patterns
        self.behavior_patterns = {
            'conservative': {'risk_tolerance': 0.2, 'engagement_threshold': 0.7},
            'moderate': {'risk_tolerance': 0.5, 'engagement_threshold': 0.5},
            'aggressive': {'risk_tolerance': 0.8, 'engagement_threshold': 0.3}
        }
    
    def generate_customer_profiles(self, num_customers: int = 5000) -> List[CustomerProfile]:
        """Generate customer profiles for personalization"""
        profiles = []
        
        for i in range(num_customers):
            # Basic demographics
            age = max(18, min(80, np.random.normal(45, 15)))
            income = max(1000, np.random.lognormal(10, 0.8))
            
            # Determine segment based on income and age
            if income > 100000 and age > 35:
                segment = 'Premium'
            elif income > 50000:
                segment = 'Gold'
            elif income > 25000:
                segment = 'Silver'
            else:
                segment = 'Bronze'
            
            # Generate preferences (0-1 scale for different categories)
            preferences = {
                'financial_services': np.random.beta(2, 2),
                'digital_banking': np.random.beta(3, 2) if age < 50 else np.random.beta(1, 3),
                'investment_products': np.random.beta(2, 3) if income > 30000 else np.random.beta(1, 4),
                'risk_tolerance': np.random.beta(2, 2),
                'tech_savviness': np.random.beta(3, 2) if age < 40 else np.random.beta(1, 3),
                'price_sensitivity': np.random.beta(2, 2),
                'brand_loyalty': np.random.beta(2, 2)
            }
            
            # Calculate behavior score based on preferences and demographics
            behavior_score = (
                preferences['digital_banking'] * 0.3 +
                preferences['financial_services'] * 0.3 +
                (1 - preferences['price_sensitivity']) * 0.2 +
                preferences['brand_loyalty'] * 0.2
            )
            
            profile = CustomerProfile(
                customer_id=f'CUST_{i+1:06d}',
                age=int(age),
                income=income,
                segment=segment,
                preferences=preferences,
                behavior_score=behavior_score,
                last_interaction=datetime.now() - timedelta(days=np.random.randint(0, 30))
            )
            
            profiles.append(profile)
        
        return profiles
    
    def generate_interaction_events(self, profiles: List[CustomerProfile], 
                                  days_back: int = 30) -> pd.DataFrame:
        """Generate customer interaction events"""
        events = []
        
        for profile in profiles:
            # Number of interactions based on behavior score and segment
            segment_multiplier = {'Premium': 3.0, 'Gold': 2.0, 'Silver': 1.5, 'Bronze': 1.0}
            num_interactions = int(
                np.random.poisson(10) * 
                segment_multiplier[profile.segment] * 
                profile.behavior_score
            )
            
            for _ in range(num_interactions):
                event_time = datetime.now() - timedelta(
                    days=np.random.randint(0, days_back),
                    hours=np.random.randint(0, 24),
                    minutes=np.random.randint(0, 60)
                )
                
                # Choose interaction type based on preferences
                interaction_types = ['page_view', 'click', 'purchase', 'inquiry', 'download']
                interaction_weights = [0.4, 0.3, 0.1, 0.15, 0.05]
                
                interaction_type = np.random.choice(interaction_types, p=interaction_weights)
                
                # Choose content category based on preferences
                category_prefs = {k: v for k, v in profile.preferences.items() 
                                if k in self.product_categories}
                category = max(category_prefs, key=category_prefs.get)
                
                # Generate engagement metrics
                engagement_duration = max(1, np.random.exponential(30))  # seconds
                engagement_score = min(1.0, profile.behavior_score + np.random.normal(0, 0.1))
                
                event = {
                    'event_id': str(uuid.uuid4()),
                    'customer_id': profile.customer_id,
                    'timestamp': event_time,
                    'interaction_type': interaction_type,
                    'content_category': category,
                    'engagement_duration': round(engagement_duration, 2),
                    'engagement_score': round(engagement_score, 3),
                    'device_type': np.random.choice(['mobile', 'desktop', 'tablet'], p=[0.6, 0.3, 0.1]),
                    'channel': np.random.choice(['web', 'mobile_app', 'email', 'sms'], p=[0.4, 0.4, 0.15, 0.05])
                }
                
                events.append(event)
        
        return pd.DataFrame(events)
    
    def calculate_real_time_scores(self, profile: CustomerProfile, 
                                 recent_interactions: pd.DataFrame) -> Dict[str, float]:
        """Calculate real-time personalization scores"""
        scores = {}
        
        # Base scores from profile preferences
        for category in self.product_categories:
            base_score = profile.preferences.get(category, 0.5)
            
            # Adjust based on recent interactions
            recent_category_interactions = recent_interactions[
                recent_interactions['content_category'] == category
            ]
            
            if len(recent_category_interactions) > 0:
                recent_engagement = recent_category_interactions['engagement_score'].mean()
                interaction_frequency = len(recent_category_interactions) / 30  # per day
                
                # Boost score based on recent positive engagement
                engagement_boost = (recent_engagement - 0.5) * 0.3
                frequency_boost = min(0.2, interaction_frequency * 0.1)
                
                adjusted_score = base_score + engagement_boost + frequency_boost
            else:
                adjusted_score = base_score
            
            scores[category] = max(0, min(1, adjusted_score))
        
        return scores
    
    def generate_recommendations(self, profile: CustomerProfile,
                               real_time_scores: Dict[str, float],
                               num_recommendations: int = 5) -> List[PersonalizationRecommendation]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Sort categories by score
        sorted_categories = sorted(real_time_scores.items(), key=lambda x: x[1], reverse=True)
        
        for i, (category, score) in enumerate(sorted_categories[:num_recommendations]):
            # Choose recommendation type based on customer segment and score
            if profile.segment in ['Premium', 'Gold'] and score > 0.7:
                rec_type = 'premium_product_recommendation'
                confidence = score * 0.9
            elif score > 0.6:
                rec_type = 'product_recommendation'
                confidence = score * 0.8
            elif score > 0.4:
                rec_type = 'educational_content'
                confidence = score * 0.7
            else:
                rec_type = 'promotional_offer'
                confidence = score * 0.6
            
            # Generate content based on category and type
            if category == 'financial_services':
                products = self.product_categories[category]['products']
                content = f"Recommended: {np.random.choice(products)} tailored for {profile.segment} customers"
            elif category == 'digital_banking':
                content = f"Enhance your digital banking experience with our latest {category} features"
            else:
                content = f"Explore {category} opportunities matching your profile"
            
            # Calculate expected engagement based on historical patterns
            expected_engagement = min(0.95, score * profile.behavior_score * 1.2)
            
            recommendation = PersonalizationRecommendation(
                customer_id=profile.customer_id,
                recommendation_type=rec_type,
                content=content,
                confidence_score=round(confidence, 3),
                expected_engagement=round(expected_engagement, 3),
                timestamp=datetime.now()
            )
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def simulate_real_time_pipeline(self, profiles: List[CustomerProfile],
                                  interactions_df: pd.DataFrame) -> pd.DataFrame:
        """Simulate real-time personalization pipeline"""
        all_recommendations = []
        
        for profile in profiles:
            # Get recent interactions for this customer
            customer_interactions = interactions_df[
                interactions_df['customer_id'] == profile.customer_id
            ].sort_values('timestamp', ascending=False).head(50)  # Last 50 interactions
            
            # Calculate real-time scores
            real_time_scores = self.calculate_real_time_scores(profile, customer_interactions)
            
            # Generate recommendations
            recommendations = self.generate_recommendations(profile, real_time_scores)
            
            # Convert to dict for DataFrame
            for rec in recommendations:
                rec_dict = {
                    'customer_id': rec.customer_id,
                    'recommendation_type': rec.recommendation_type,
                    'content': rec.content,
                    'confidence_score': rec.confidence_score,
                    'expected_engagement': rec.expected_engagement,
                    'timestamp': rec.timestamp,
                    'customer_segment': profile.segment,
                    'customer_behavior_score': profile.behavior_score
                }
                all_recommendations.append(rec_dict)
        
        return pd.DataFrame(all_recommendations)
    
    def generate_ab_test_data(self, recommendations_df: pd.DataFrame) -> pd.DataFrame:
        """Generate A/B test data for recommendation effectiveness"""
        ab_test_data = []
        
        for _, rec in recommendations_df.iterrows():
            # Simulate A/B test variants
            variants = ['control', 'variant_a', 'variant_b']
            
            for variant in variants:
                # Simulate different engagement rates for variants
                base_engagement = rec['expected_engagement']
                
                if variant == 'control':
                    actual_engagement = base_engagement * np.random.normal(0.8, 0.1)
                elif variant == 'variant_a':
                    actual_engagement = base_engagement * np.random.normal(1.0, 0.1)
                else:  # variant_b
                    actual_engagement = base_engagement * np.random.normal(1.2, 0.15)
                
                actual_engagement = max(0, min(1, actual_engagement))
                
                # Simulate conversion (binary outcome)
                conversion_probability = actual_engagement * 0.3  # 30% max conversion rate
                converted = np.random.random() < conversion_probability
                
                ab_record = {
                    'test_id': f"TEST_{rec['customer_id']}_{variant}",
                    'customer_id': rec['customer_id'],
                    'variant': variant,
                    'recommendation_type': rec['recommendation_type'],
                    'expected_engagement': rec['expected_engagement'],
                    'actual_engagement': round(actual_engagement, 3),
                    'converted': converted,
                    'timestamp': rec['timestamp']
                }
                
                ab_test_data.append(ab_record)
        
        return pd.DataFrame(ab_test_data)

if __name__ == "__main__":
    # Generate sample data
    engine = RealTimePersonalizationEngine()
    
    print("Generating customer profiles...")
    profiles = engine.generate_customer_profiles(1000)
    
    print("Generating interaction events...")
    interactions = engine.generate_interaction_events(profiles)
    
    print("Generating recommendations...")
    recommendations = engine.simulate_real_time_pipeline(profiles, interactions)
    
    print("Generating A/B test data...")
    ab_test_data = engine.generate_ab_test_data(recommendations)
    
    # Save data
    profiles_df = pd.DataFrame([{
        'customer_id': p.customer_id,
        'age': p.age,
        'income': p.income,
        'segment': p.segment,
        'behavior_score': p.behavior_score,
        'last_interaction': p.last_interaction,
        **{f'pref_{k}': v for k, v in p.preferences.items()}
    } for p in profiles])
    
    # Create data directory
    import os
    os.makedirs('../data', exist_ok=True)
    
    # Save datasets
    profiles_df.to_csv('../data/customer_profiles.csv', index=False)
    interactions.to_csv('../data/interactions.csv', index=False)
    recommendations.to_csv('../data/recommendations.csv', index=False)
    ab_test_data.to_csv('../data/ab_test_results.csv', index=False)
    
    print(f"\n=== Dataset Summary ===")
    print(f"Customer Profiles: {len(profiles_df)} records")
    print(f"Interactions: {len(interactions)} records")
    print(f"Recommendations: {len(recommendations)} records")
    print(f"A/B Test Data: {len(ab_test_data)} records")

