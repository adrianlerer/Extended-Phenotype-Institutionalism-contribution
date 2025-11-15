"""
Worker Agent
============

Individual workers with compliance preferences and economic constraints.
"""

from typing import Dict, Any
from dataclasses import dataclass, field
import random
from .base_agent import BaseAgent, AgentState


@dataclass
class WorkerState(AgentState):
    """State specific to Worker agents"""
    employment_status: str = "employed"  # employed, unemployed, informal
    income_level: float = 1.0  # Relative income (0.0 to 2.0)
    risk_aversion: float = 0.5  # 0.0 = risk-loving, 1.0 = risk-averse
    compliance_cost: float = 0.3  # Cost to comply with formal rules
    
    def __post_init__(self):
        """Initialize worker-specific beliefs"""
        super().__post_init__() if hasattr(super(), '__post_init__') else None
        self.beliefs['formal_institutions_benefit'] = 0.5
        self.beliefs['informal_institutions_benefit'] = 0.5
        self.beliefs['enforcement_probability'] = 0.3


class Worker(BaseAgent):
    """
    Worker Agent in EPT ABM System
    
    Represents individual workers who must decide whether to:
    - Comply with formal labor regulations
    - Participate in informal practices
    - Support or oppose reforms
    
    Decision factors:
    - Income level and economic security
    - Risk aversion
    - Compliance costs
    - Perceived benefits of formal vs informal institutions
    """
    
    def __init__(self, state: WorkerState):
        """Initialize Worker agent"""
        super().__init__(state)
        self.state: WorkerState = state
    
    def decide_action(self, environment: Dict[str, Any]) -> str:
        """
        Decide whether to comply with formal rules or use informal practices
        
        Logic:
        - High compliance cost + low enforcement → prefer informal
        - High income + low risk aversion → prefer formal (can afford compliance)
        - Crisis situation → may switch preferences
        """
        # Extract environment variables
        enforcement_level = environment.get('enforcement_level', 0.3)
        formal_benefits = environment.get('formal_benefits', 0.5)
        informal_benefits = environment.get('informal_benefits', 0.5)
        crisis_active = environment.get('crisis_active', False)
        
        # Calculate expected utility of formal compliance
        formal_utility = (
            formal_benefits * self.state.beliefs['formal_institutions_benefit'] -
            self.state.compliance_cost +
            (enforcement_level * 0.5)  # Benefit from legal protection
        )
        
        # Calculate expected utility of informal practices
        informal_utility = (
            informal_benefits * self.state.beliefs['informal_institutions_benefit'] -
            (enforcement_level * self.state.risk_aversion * 0.5)  # Risk of sanction
        )
        
        # Crisis modifier: increases risk aversion
        if crisis_active:
            informal_utility -= self.state.risk_aversion * 0.3
        
        # Decision with some randomness
        if formal_utility > informal_utility + random.gauss(0, 0.1):
            return "comply_formal"
        else:
            return "use_informal"
    
    def update_beliefs(self, observations: Dict[str, Any]):
        """
        Update beliefs based on observed outcomes
        
        Workers learn from:
        - Personal experiences with formal/informal institutions
        - Peer experiences (network effects)
        - Enforcement actions
        """
        # Update enforcement probability belief
        if 'enforcement_observed' in observations:
            self.state.beliefs['enforcement_probability'] = (
                0.7 * self.state.beliefs['enforcement_probability'] +
                0.3 * observations['enforcement_observed']
            )
        
        # Update benefit beliefs based on outcomes
        if 'formal_outcome' in observations:
            outcome = observations['formal_outcome']
            self.state.beliefs['formal_institutions_benefit'] = (
                0.8 * self.state.beliefs['formal_institutions_benefit'] +
                0.2 * outcome
            )
        
        if 'informal_outcome' in observations:
            outcome = observations['informal_outcome']
            self.state.beliefs['informal_institutions_benefit'] = (
                0.8 * self.state.beliefs['informal_institutions_benefit'] +
                0.2 * outcome
            )
        
        # Update memetic alignment
        belief_diff = (
            self.state.beliefs['formal_institutions_benefit'] -
            self.state.beliefs['informal_institutions_benefit']
        )
        self.state.memetic_alignment = 0.5 + 0.5 * belief_diff
        self.state.memetic_alignment = max(0.0, min(1.0, self.state.memetic_alignment))
    
    def interact(self, other_agent: BaseAgent) -> Dict[str, Any]:
        """
        Interact with another agent
        
        Workers can:
        - Share information with other workers (peer effects)
        - Receive influence from unions
        - Respond to employer incentives
        """
        if other_agent.get_type() == "Worker":
            # Peer influence: workers share beliefs
            other_state: WorkerState = other_agent.state
            
            # Average beliefs (social learning)
            for belief_name in ['formal_institutions_benefit', 'informal_institutions_benefit']:
                self.state.beliefs[belief_name] = (
                    0.8 * self.state.beliefs[belief_name] +
                    0.2 * other_state.beliefs[belief_name]
                )
            
            return {
                'interaction_type': 'peer_learning',
                'influence': 0.2
            }
        
        elif other_agent.get_type() == "Union":
            # Union mobilizes worker
            from .union import Union, UnionState
            union: Union = other_agent
            union_state: UnionState = union.state
            
            # Union increases informal preference if militancy is high
            influence = union_state.militancy / 10.0
            self.state.beliefs['informal_institutions_benefit'] += influence * 0.1
            self.state.beliefs['informal_institutions_benefit'] = min(1.0, self.state.beliefs['informal_institutions_benefit'])
            
            # Join union network
            if union_state.agent_id not in self.state.network_connections:
                self.state.network_connections.append(union_state.agent_id)
            
            return {
                'interaction_type': 'union_mobilization',
                'influence': influence
            }
        
        else:
            # Minimal interaction with other agent types
            return {
                'interaction_type': 'minimal',
                'influence': 0.0
            }
