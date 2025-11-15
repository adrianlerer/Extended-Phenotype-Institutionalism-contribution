"""
Legislator Agent
================

Politicians with reform incentives and electoral constraints.
"""

from typing import Dict, Any
from dataclasses import dataclass, field
import random
from .base_agent import BaseAgent, AgentState


@dataclass
class LegislatorState(AgentState):
    """State specific to Legislator agents"""
    party_affiliation: str = "centrist"  # left, center-left, centrist, center-right, right
    electoral_security: float = 0.5  # 0.0 (vulnerable) to 1.0 (safe seat)
    reform_commitment: float = 0.5  # Commitment to pushing reforms
    union_ties: float = 0.5  # Connection to unions
    business_ties: float = 0.5  # Connection to employers
    
    def __post_init__(self):
        """Initialize legislator-specific beliefs"""
        super().__post_init__() if hasattr(super(), '__post_init__') else None
        self.beliefs['reform_electoral_benefit'] = 0.5
        self.beliefs['union_retaliation_risk'] = 0.6
        self.beliefs['business_support_gain'] = 0.5


class Legislator(BaseAgent):
    """
    Legislator Agent in EPT ABM System
    
    Represents politicians who must balance:
    - Electoral incentives (reelection)
    - Ideological commitments
    - Interest group pressures (unions vs employers)
    - Crisis urgency
    
    Decision: Support or oppose labor market reforms
    """
    
    def __init__(self, state: LegislatorState):
        """Initialize Legislator agent"""
        super().__init__(state)
        self.state: LegislatorState = state
        
        # Set memetic alignment based on party
        party_alignments = {
            'left': 0.2,
            'center-left': 0.4,
            'centrist': 0.5,
            'center-right': 0.7,
            'right': 0.8
        }
        self.state.memetic_alignment = party_alignments.get(state.party_affiliation, 0.5)
    
    def decide_action(self, environment: Dict[str, Any]) -> str:
        """
        Decide whether to support reform
        
        Returns: "support_reform", "oppose_reform", "abstain"
        """
        crisis_active = environment.get('crisis_active', False)
        union_mobilization = environment.get('union_mobilization', 0.5)
        business_pressure = environment.get('business_pressure', 0.5)
        public_support_reform = environment.get('public_support_reform', 0.5)
        
        # Calculate expected electoral utility
        support_score = 0.0
        
        # Crisis increases reform urgency
        if crisis_active:
            support_score += 0.3
        
        # Business pressure
        support_score += business_pressure * self.state.business_ties * 0.4
        
        # Union opposition
        support_score -= union_mobilization * self.state.union_ties * 0.5
        
        # Public opinion
        support_score += (public_support_reform - 0.5) * 0.3
        
        # Electoral security: vulnerable legislators avoid risky votes
        if self.state.electoral_security < 0.4:
            support_score *= 0.5  # Cautious
        
        # Party ideology
        if self.state.party_affiliation in ['left', 'center-left']:
            support_score -= 0.2
        elif self.state.party_affiliation in ['center-right', 'right']:
            support_score += 0.2
        
        # Decision
        if support_score > 0.2:
            return "support_reform"
        elif support_score < -0.2:
            return "oppose_reform"
        else:
            return "abstain"
    
    def update_beliefs(self, observations: Dict[str, Any]):
        """Update beliefs based on political outcomes"""
        if 'reform_passed' in observations:
            passed = observations['reform_passed']
            electoral_impact = observations.get('electoral_impact', 0.0)
            
            self.state.beliefs['reform_electoral_benefit'] = (
                0.7 * self.state.beliefs['reform_electoral_benefit'] +
                0.3 * electoral_impact
            )
        
        if 'union_retaliation' in observations:
            retaliation = observations['union_retaliation']
            self.state.beliefs['union_retaliation_risk'] = (
                0.6 * self.state.beliefs['union_retaliation_risk'] +
                0.4 * retaliation
            )
    
    def interact(self, other_agent: BaseAgent) -> Dict[str, Any]:
        """Interact with interest groups"""
        if other_agent.get_type() == "Union":
            # Receive union lobbying
            return {
                'interaction_type': 'lobbying_received',
                'receptiveness': self.state.union_ties
            }
        
        elif other_agent.get_type() == "Employer":
            # Receive business lobbying
            return {
                'interaction_type': 'lobbying_received',
                'receptiveness': self.state.business_ties
            }
        
        elif other_agent.get_type() == "Legislator":
            # Form legislative coalitions
            other_state: LegislatorState = other_agent.state
            
            # Similar party affiliation → coalition
            if self.state.party_affiliation == other_state.party_affiliation:
                return {
                    'interaction_type': 'coalition',
                    'strength': 0.8
                }
            else:
                return {
                    'interaction_type': 'negotiation',
                    'strength': 0.3
                }
        
        else:
            return {'interaction_type': 'none'}
