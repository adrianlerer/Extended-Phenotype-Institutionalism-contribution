"""
Employer Agent
==============

Business entities with coordination capacity parameter (1-10).
"""

from typing import Dict, Any
from dataclasses import dataclass, field
import random
from .base_agent import BaseAgent, AgentState


@dataclass
class EmployerState(AgentState):
    """State specific to Employer agents"""
    coordination_capacity: int = 5  # 1 (fragmented) to 10 (highly coordinated)
    firm_size: str = "medium"  # small, medium, large
    sector: str = "manufacturing"
    lobbying_budget: float = 0.5  # 0.0 to 1.0
    
    def __post_init__(self):
        """Initialize employer-specific beliefs"""
        super().__post_init__() if hasattr(super(), '__post_init__') else None
        self.beliefs['reform_benefit'] = 0.7  # Employers generally favor reform
        self.beliefs['union_strength'] = 0.5
        self.beliefs['enforcement_effectiveness'] = 0.4


class Employer(BaseAgent):
    """
    Employer Agent in EPT ABM System
    
    Represents business interests that:
    - Support labor market reforms
    - Oppose ultraactivity and rigid regulations
    - Lobby for formal institution changes
    - Coordinate with other employers through business associations
    
    Key parameter: COORDINATION CAPACITY (1-10)
    - Low (1-3): Fragmented, weak collective action
    - Medium (4-7): Moderate coordination through associations
    - High (8-10): Strong unified business lobbying
    """
    
    def __init__(self, state: EmployerState):
        """Initialize Employer agent"""
        super().__init__(state)
        self.state: EmployerState = state
        
        # Employers generally pro-formal institutions
        self.state.memetic_alignment = 0.5 + (state.coordination_capacity / 20.0)
    
    def decide_action(self, environment: Dict[str, Any]) -> str:
        """
        Decide employer's strategic response
        
        Actions:
        - "lobby_reform": Push for labor market reforms
        - "coordinate": Build business coalitions
        - "negotiate": Bargain with unions
        - "litigate": Challenge regulations in court
        - "comply": Accept status quo
        """
        reform_opportunity = environment.get('reform_opportunity', False)
        union_strength = environment.get('union_strength', 0.5)
        government_pro_business = environment.get('government_pro_business', 0.5)
        
        self.state.beliefs['union_strength'] = union_strength
        
        # High coordination → more aggressive reform push
        if self.state.coordination_capacity >= 7:
            if reform_opportunity:
                return "lobby_reform"
            elif union_strength < 0.4:
                return "litigate"  # Weak unions, challenge regulations
            else:
                return "coordinate"  # Build coalition
        
        # Medium coordination → selective action
        elif self.state.coordination_capacity >= 4:
            if reform_opportunity and government_pro_business > 0.6:
                return "lobby_reform"
            else:
                return "negotiate"
        
        # Low coordination → passive
        else:
            if union_strength > 0.7:
                return "comply"  # Too weak to resist
            else:
                return "negotiate"
    
    def update_beliefs(self, observations: Dict[str, Any]):
        """Update beliefs based on lobbying and negotiation outcomes"""
        if 'reform_outcome' in observations:
            success = observations['reform_outcome']
            self.state.beliefs['reform_benefit'] = (
                0.7 * self.state.beliefs['reform_benefit'] +
                0.3 * (1.0 if success else 0.3)
            )
        
        if 'union_mobilization' in observations:
            self.state.beliefs['union_strength'] = (
                0.6 * self.state.beliefs['union_strength'] +
                0.4 * observations['union_mobilization']
            )
    
    def interact(self, other_agent: BaseAgent) -> Dict[str, Any]:
        """Interact with other agents"""
        if other_agent.get_type() == "Employer":
            # Coordinate with other employers
            other_state: EmployerState = other_agent.state
            
            avg_coordination = (self.state.coordination_capacity + other_state.coordination_capacity) / 2
            
            if avg_coordination >= 6:
                # Form business association
                if other_state.agent_id not in self.state.network_connections:
                    self.state.network_connections.append(other_state.agent_id)
                
                return {
                    'interaction_type': 'business_coalition',
                    'coordination': avg_coordination / 10.0
                }
            else:
                return {
                    'interaction_type': 'information_sharing',
                    'coordination': avg_coordination / 10.0
                }
        
        elif other_agent.get_type() == "Legislator":
            # Lobby legislator
            influence = (
                self.state.lobbying_budget * 0.7 +
                (self.state.coordination_capacity / 10.0) * 0.3
            )
            
            return {
                'interaction_type': 'lobbying',
                'influence_strength': influence,
                'position': 'pro_reform'
            }
        
        elif other_agent.get_type() == "Union":
            # Negotiate or resist
            if self.state.coordination_capacity <= 4:
                return {
                    'interaction_type': 'collective_bargaining',
                    'cooperative': True
                }
            else:
                return {
                    'interaction_type': 'resistance',
                    'strength': self.state.coordination_capacity / 10.0
                }
        
        else:
            return {'interaction_type': 'none'}
