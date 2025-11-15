"""
Judge Agent
===========

Judicial actors with doctrine adherence and precedent influence.
"""

from typing import Dict, Any
from dataclasses import dataclass, field
import random
from .base_agent import BaseAgent, AgentState


@dataclass
class JudgeState(AgentState):
    """State specific to Judge agents"""
    seniority: int = 5  # Years on bench
    doctrine_adherence: float = 0.7  # 0.0 (innovative) to 1.0 (precedent-bound)
    ideological_leaning: str = "centrist"  # progressive, centrist, conservative
    citation_influence: float = 0.5  # JurisRank score
    
    def __post_init__(self):
        """Initialize judge-specific beliefs"""
        super().__post_init__() if hasattr(super(), '__post_init__') else None
        self.beliefs['precedent_binding_force'] = 0.8
        self.beliefs['constitutional_rigidity'] = 0.7
        self.beliefs['social_rights_priority'] = 0.6


class Judge(BaseAgent):
    """
    Judge Agent in EPT ABM System
    
    Represents judicial actors who:
    - Apply precedents (doctrine adherence)
    - Interpret constitutional provisions
    - Protect or challenge ultraactivity
    - Influence other judges through citations
    
    Key: Doctrine adherence determines resistance to reform
    """
    
    def __init__(self, state: JudgeState):
        """Initialize Judge agent"""
        super().__init__(state)
        self.state: JudgeState = state
        
        # Judges' memetic alignment based on ideology and doctrine adherence
        ideology_scores = {
            'progressive': 0.3,
            'centrist': 0.5,
            'conservative': 0.7
        }
        base_alignment = ideology_scores.get(state.ideological_leaning, 0.5)
        
        # High doctrine adherence → lower alignment with formal reform
        self.state.memetic_alignment = base_alignment * (1.0 - 0.3 * state.doctrine_adherence)
    
    def decide_action(self, environment: Dict[str, Any]) -> str:
        """
        Decide how to rule on reform constitutionality
        
        Returns: "uphold_reform", "strike_down_reform", "narrow_interpretation"
        """
        reform_before_court = environment.get('reform_before_court', False)
        if not reform_before_court:
            return "no_case"
        
        constitutional_text_clear = environment.get('constitutional_text_clear', 0.5)
        precedent_support_reform = environment.get('precedent_support_reform', 0.3)
        public_pressure = environment.get('public_pressure', 0.5)
        
        # Calculate ruling score
        ruling_score = 0.0
        
        # Precedent weight (high doctrine adherence = follow precedent)
        ruling_score += precedent_support_reform * self.state.doctrine_adherence * 0.6
        
        # Constitutional text
        ruling_score += constitutional_text_clear * 0.3
        
        # Ideological leaning
        if self.state.ideological_leaning == 'progressive':
            ruling_score -= 0.2  # Favor workers/unions
        elif self.state.ideological_leaning == 'conservative':
            ruling_score += 0.2  # Favor business/reform
        
        # Public pressure (weak effect)
        ruling_score += (public_pressure - 0.5) * 0.1
        
        # Decision
        if ruling_score > 0.3:
            return "uphold_reform"
        elif ruling_score < -0.1:
            return "strike_down_reform"
        else:
            return "narrow_interpretation"  # Compromise
    
    def update_beliefs(self, observations: Dict[str, Any]):
        """Update beliefs based on judicial outcomes and citations"""
        if 'ruling_cited' in observations:
            # Being cited increases influence
            self.state.citation_influence = min(1.0, self.state.citation_influence + 0.05)
        
        if 'ruling_reversed' in observations:
            # Being reversed decreases confidence in doctrine
            self.state.beliefs['precedent_binding_force'] *= 0.9
        
        if 'social_unrest' in observations:
            unrest_level = observations['social_unrest']
            # High unrest may increase social rights priority
            self.state.beliefs['social_rights_priority'] = (
                0.7 * self.state.beliefs['social_rights_priority'] +
                0.3 * unrest_level
            )
    
    def interact(self, other_agent: BaseAgent) -> Dict[str, Any]:
        """Interact with other agents"""
        if other_agent.get_type() == "Judge":
            # Citation and influence
            other_state: JudgeState = other_agent.state
            
            # Senior judges influence junior judges
            if self.state.seniority > other_state.seniority:
                influence = self.state.citation_influence * 0.3
                return {
                    'interaction_type': 'precedent_influence',
                    'influence_strength': influence
                }
            else:
                return {
                    'interaction_type': 'citation_exchange',
                    'influence_strength': 0.1
                }
        
        elif other_agent.get_type() == "Union":
            # Receive amicus briefs
            return {
                'interaction_type': 'amicus_brief_received',
                'weight': 0.1 * (1.0 - self.state.doctrine_adherence)  # Innovative judges more receptive
            }
        
        elif other_agent.get_type() == "Employer":
            # Receive amicus briefs
            return {
                'interaction_type': 'amicus_brief_received',
                'weight': 0.1 * (1.0 - self.state.doctrine_adherence)
            }
        
        else:
            return {'interaction_type': 'none'}
