"""
Union Agent
===========

Organized labor with militancy parameter controlling strategic behavior.
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field
import random
from .base_agent import BaseAgent, AgentState


@dataclass
class UnionState(AgentState):
    """State specific to Union agents"""
    militancy: int = 5  # 1 (cooperative) to 10 (confrontational)
    member_count: int = 100
    strike_capacity: float = 0.5  # 0.0 to 1.0
    political_connections: float = 0.5  # Influence with legislators
    
    def __post_init__(self):
        """Initialize union-specific beliefs"""
        super().__post_init__() if hasattr(super(), '__post_init__') else None
        self.beliefs['ultraactivity_value'] = 0.8  # High value for ultraactivity
        self.beliefs['reform_threat'] = 0.5
        self.beliefs['mobilization_success'] = 0.6


class Union(BaseAgent):
    """
    Union Agent in EPT ABM System
    
    Represents organized labor unions that:
    - Mobilize workers against reforms
    - Defend ultraactivity and informal practices
    - Coordinate collective action
    - Lobby legislators and judges
    
    Key parameter: MILITANCY (1-10)
    - Low militancy (1-3): Cooperative, negotiate with employers
    - Medium militancy (4-7): Strategic, selective mobilization
    - High militancy (8-10): Confrontational, resist all changes
    """
    
    def __init__(self, state: UnionState):
        """Initialize Union agent"""
        super().__init__(state)
        self.state: UnionState = state
        
        # Set memetic alignment based on militancy
        # High militancy → strong informal preference
        self.state.memetic_alignment = max(0.1, 1.0 - (state.militancy / 12.0))
    
    def decide_action(self, environment: Dict[str, Any]) -> str:
        """
        Decide union's strategic response to environment
        
        Actions:
        - "strike": Mobilize strike action
        - "negotiate": Engage in collective bargaining
        - "lobby": Influence legislators/judges
        - "mobilize": Organize workers
        - "neutral": No action
        """
        # Extract environment
        reform_proposed = environment.get('reform_proposed', False)
        reform_targets_ultraactivity = environment.get('reform_targets_ultraactivity', False)
        crisis_active = environment.get('crisis_active', False)
        government_support = environment.get('government_support', 0.5)
        
        # Calculate threat level
        threat_level = 0.0
        if reform_proposed:
            threat_level += 0.5
        if reform_targets_ultraactivity:
            threat_level += 0.5 * self.state.beliefs['ultraactivity_value']
        
        self.state.beliefs['reform_threat'] = threat_level
        
        # Decision logic based on militancy
        if threat_level > 0.7:
            if self.state.militancy >= 7:
                # High militancy: immediate strike
                return "strike"
            elif self.state.militancy >= 4:
                # Medium militancy: mobilize first, strike if needed
                return "mobilize"
            else:
                # Low militancy: try to negotiate
                return "negotiate"
        
        elif threat_level > 0.3:
            if self.state.militancy >= 6:
                return "lobby"
            else:
                return "negotiate"
        
        else:
            # Low threat: routine organizing
            return "organize"
    
    def update_beliefs(self, observations: Dict[str, Any]):
        """
        Update beliefs based on mobilization outcomes
        
        Unions learn from:
        - Success/failure of strikes
        - Legislative outcomes
        - Judicial rulings
        - Member feedback
        """
        # Update mobilization success belief
        if 'mobilization_outcome' in observations:
            outcome = observations['mobilization_outcome']
            self.state.beliefs['mobilization_success'] = (
                0.7 * self.state.beliefs['mobilization_success'] +
                0.3 * outcome
            )
        
        # Update reform threat perception
        if 'reform_passed' in observations:
            if observations['reform_passed']:
                # Reform passed despite opposition
                self.state.beliefs['reform_threat'] += 0.2
                self.state.militancy = min(10, self.state.militancy + 1)
            else:
                # Successfully blocked reform
                self.state.beliefs['reform_threat'] -= 0.1
        
        # Update ultraactivity value based on judicial rulings
        if 'judicial_ruling_ultraactivity' in observations:
            ruling_favorable = observations['judicial_ruling_ultraactivity']
            if ruling_favorable:
                self.state.beliefs['ultraactivity_value'] = min(1.0, self.state.beliefs['ultraactivity_value'] + 0.1)
            else:
                self.state.beliefs['ultraactivity_value'] = max(0.0, self.state.beliefs['ultraactivity_value'] - 0.2)
    
    def interact(self, other_agent: BaseAgent) -> Dict[str, Any]:
        """
        Interact with other agents
        
        Unions can:
        - Mobilize workers
        - Coordinate with other unions
        - Lobby legislators
        - Pressure judges through amicus briefs
        - Negotiate with employers
        """
        if other_agent.get_type() == "Worker":
            # Mobilize worker (handled in worker.interact)
            return {
                'interaction_type': 'mobilization',
                'militancy': self.state.militancy,
                'influence': self.state.militancy / 10.0
            }
        
        elif other_agent.get_type() == "Union":
            # Coordinate with other union
            other_state: UnionState = other_agent.state
            
            # Share information and coordinate strategy
            avg_militancy = (self.state.militancy + other_state.militancy) / 2
            coordination_strength = 1.0 - abs(self.state.militancy - other_state.militancy) / 10.0
            
            # Form coalition if militancy is similar
            if coordination_strength > 0.7:
                if other_state.agent_id not in self.state.network_connections:
                    self.state.network_connections.append(other_state.agent_id)
                
                return {
                    'interaction_type': 'coalition',
                    'coordination_strength': coordination_strength,
                    'combined_strike_capacity': (self.state.strike_capacity + other_state.strike_capacity) / 2
                }
            else:
                return {
                    'interaction_type': 'information_sharing',
                    'coordination_strength': coordination_strength
                }
        
        elif other_agent.get_type() == "Legislator":
            # Lobby legislator
            from .legislator import Legislator
            legislator: Legislator = other_agent
            
            # Influence depends on political connections and member count
            influence_strength = (
                self.state.political_connections * 0.6 +
                min(1.0, self.state.member_count / 1000.0) * 0.4
            )
            
            return {
                'interaction_type': 'lobbying',
                'influence_strength': influence_strength,
                'position': 'anti_reform' if self.state.militancy > 5 else 'negotiate_reform'
            }
        
        elif other_agent.get_type() == "Judge":
            # Submit amicus brief or public pressure
            influence_strength = self.state.political_connections * 0.3
            
            return {
                'interaction_type': 'amicus_brief',
                'influence_strength': influence_strength,
                'position': 'defend_ultraactivity'
            }
        
        elif other_agent.get_type() == "Employer":
            # Negotiate or confront
            if self.state.militancy <= 4:
                return {
                    'interaction_type': 'collective_bargaining',
                    'cooperative': True
                }
            else:
                return {
                    'interaction_type': 'confrontation',
                    'strike_threat': self.state.strike_capacity
                }
        
        else:
            return {
                'interaction_type': 'none',
                'influence': 0.0
            }
    
    def calculate_strike_power(self, environment: Dict[str, Any]) -> float:
        """
        Calculate effective strike power in current environment
        
        Returns:
            Strike power (0.0 to 1.0)
        """
        base_power = self.state.strike_capacity
        
        # Modifiers
        member_modifier = min(1.0, self.state.member_count / 500.0)
        militancy_modifier = self.state.militancy / 10.0
        crisis_penalty = 0.7 if environment.get('crisis_active', False) else 1.0
        
        # Network effects: more connected unions have more power
        network_bonus = min(0.3, len(self.state.network_connections) * 0.05)
        
        total_power = base_power * member_modifier * militancy_modifier * crisis_penalty + network_bonus
        return min(1.0, total_power)
