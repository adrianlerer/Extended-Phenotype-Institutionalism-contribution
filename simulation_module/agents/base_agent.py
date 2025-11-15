"""
Base Agent Class
================

Foundation for all ABM agents in the EPT simulation system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from dataclasses import dataclass, field
import uuid


@dataclass
class AgentState:
    """Base state for all agents"""
    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    beliefs: Dict[str, float] = field(default_factory=dict)
    resources: float = 1.0
    network_connections: List[str] = field(default_factory=list)
    memetic_alignment: float = 0.5  # 0.0 = anti-formal, 1.0 = pro-formal
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary"""
        return {
            'agent_id': self.agent_id,
            'beliefs': self.beliefs,
            'resources': self.resources,
            'network_size': len(self.network_connections),
            'memetic_alignment': self.memetic_alignment
        }


class BaseAgent(ABC):
    """
    Abstract base class for all agents in EPT ABM system
    
    All agents share:
    - Unique ID
    - State variables (beliefs, resources, connections)
    - Memetic alignment (position on informal/formal spectrum)
    - Decision rules (abstract methods)
    - Interaction protocols
    """
    
    def __init__(self, state: AgentState):
        """Initialize agent with state"""
        self.state = state
        self.history: List[Dict[str, Any]] = []
    
    @abstractmethod
    def decide_action(self, environment: Dict[str, Any]) -> str:
        """
        Decide what action to take given current environment
        
        Args:
            environment: Dict with current state of simulation
        
        Returns:
            Action string (e.g., "support_reform", "oppose_reform", "neutral")
        """
        pass
    
    @abstractmethod
    def update_beliefs(self, observations: Dict[str, Any]):
        """
        Update beliefs based on observations
        
        Args:
            observations: Dict with observed outcomes from environment
        """
        pass
    
    @abstractmethod
    def interact(self, other_agent: 'BaseAgent') -> Dict[str, Any]:
        """
        Interact with another agent
        
        Args:
            other_agent: Another agent to interact with
        
        Returns:
            Dict describing interaction outcome
        """
        pass
    
    def get_memetic_fitness(self, institution_type: str) -> float:
        """
        Calculate agent's fitness under given institution type
        
        Args:
            institution_type: "formal" or "informal"
        
        Returns:
            Fitness score (0.0 to 1.0)
        """
        if institution_type == "formal":
            return self.state.memetic_alignment
        else:  # informal
            return 1.0 - self.state.memetic_alignment
    
    def record_state(self, timestep: int):
        """Record current state to history"""
        self.history.append({
            'timestep': timestep,
            'state': self.state.to_dict()
        })
    
    def get_type(self) -> str:
        """Return agent type as string"""
        return self.__class__.__name__
