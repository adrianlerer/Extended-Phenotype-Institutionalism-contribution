"""
SimulationEnvironment - Core ABM Engine
========================================

Complete simulation environment managing agent populations, timestep logic,
reform processing, and institutional evolution.

Integration with EPT Theory:
- CLI (Constitutional Lock-In Index) tracking
- MFD (Memetic Fitness Differential) calculation
- Agent-based institutional dynamics
- Historical validation scenarios
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import random
import numpy as np
from collections import defaultdict

# Import agent classes
from .agents.base_agent import BaseAgent
from .agents.worker import Worker, WorkerState
from .agents.union import Union, UnionState
from .agents.employer import Employer, EmployerState
from .agents.legislator import Legislator, LegislatorState
from .agents.judge import Judge, JudgeState


@dataclass
class EnvironmentState:
    """Complete state of simulation environment"""
    timestep: int = 0
    
    # TRIPLE CAPTURE DECOMPOSITION (Critical Correction 2025-11-15)
    # See: CRITICAL_CORRECTION_TRIPLE_CAPTURE.md
    cli_memetic: float = 0.5      # Cultural norms component (0.0 to 1.0)
    cli_corporate: float = 0.5     # Interest group veto power (0.0 to 1.0)
    cli_oligarchic: float = 0.5    # Judicial/political control (0.0 to 1.0)
    
    # Empirically calibrated weights (from validation data)
    alpha: float = 0.40  # Weight for memetic capture (slowest to change)
    beta: float = 0.35   # Weight for corporate capture (moderate speed)
    gamma: float = 0.25  # Weight for oligarchic capture (fastest to change)
    
    # Aggregate CLI (calculated from components)
    @property
    def cli(self) -> float:
        """Calculate aggregate CLI from triple capture components"""
        return (
            self.alpha * self.cli_memetic +
            self.beta * self.cli_corporate +
            self.gamma * self.cli_oligarchic
        )
    
    mfd: float = 1.0  # Memetic Fitness Differential
    
    # Constitutional parameters (0.0 to 1.0 each) - LEGACY
    # NOTE: These map to oligarchic capture but kept for backwards compatibility
    constitutional_rigidity: float = 0.5
    ultraactivity_protection: float = 0.5
    judicial_review_strength: float = 0.5
    
    # Economic/social state
    gdp_per_capita: float = 10000.0
    unemployment_rate: float = 0.08
    informal_employment_rate: float = 0.35
    
    # Political state
    crisis_active: bool = False
    crisis_salience: float = 0.0  # 0.0 to 1.0
    government_reform_appetite: float = 0.5
    
    # Reform tracking
    reform_proposed: bool = False
    reform_targets_ultraactivity: bool = False
    reform_passed: bool = False
    reforms_attempted: int = 0
    reforms_succeeded: int = 0
    
    # Agent aggregates
    avg_worker_compliance: float = 0.5
    avg_union_militancy: float = 5.0
    avg_employer_coordination: float = 5.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary"""
        return {
            'timestep': self.timestep,
            # Triple Capture Components
            'cli_memetic': round(self.cli_memetic, 3),
            'cli_corporate': round(self.cli_corporate, 3),
            'cli_oligarchic': round(self.cli_oligarchic, 3),
            # Aggregate CLI
            'cli': round(self.cli, 3),
            'mfd': round(self.mfd, 2),
            # Legacy constitutional parameters
            'constitutional_rigidity': round(self.constitutional_rigidity, 3),
            'ultraactivity_protection': round(self.ultraactivity_protection, 3),
            'judicial_review_strength': round(self.judicial_review_strength, 3),
            # Economic/social state
            'gdp_per_capita': round(self.gdp_per_capita, 2),
            'unemployment_rate': round(self.unemployment_rate, 3),
            'informal_employment_rate': round(self.informal_employment_rate, 3),
            # Political state
            'crisis_active': self.crisis_active,
            'crisis_salience': round(self.crisis_salience, 3),
            # Reform tracking
            'reforms_attempted': self.reforms_attempted,
            'reforms_succeeded': self.reforms_succeeded,
            'reform_success_rate': round(self.reforms_succeeded / max(1, self.reforms_attempted), 3)
        }


@dataclass
class ReformProposal:
    """Represents a reform attempt"""
    proposal_id: str
    timestep: int
    targets_ultraactivity: bool
    targets_constitutional: bool
    expected_cli_reduction: float
    political_cost: float
    sponsors: List[str] = field(default_factory=list)
    
    # Voting results
    legislative_votes_for: int = 0
    legislative_votes_against: int = 0
    legislative_passed: bool = False
    judicial_review_passed: bool = False
    final_passed: bool = False


class SimulationEnvironment:
    """
    Core ABM Simulation Environment
    
    Manages:
    - Agent populations (workers, unions, employers, legislators, judges)
    - Timestep execution logic
    - Reform proposal and processing
    - CLI/MFD calculation and tracking
    - Institutional evolution
    - History recording
    
    Timestep Logic:
    1. Check for crisis events (stochastic)
    2. Propose reforms (if conditions met)
    3. Agents decide actions
    4. Agents interact (network effects)
    5. Process reform (legislative + judicial)
    6. Update environment state
    7. Record history
    """
    
    def __init__(
        self,
        n_workers: int = 100,
        n_unions: int = 5,
        n_employers: int = 20,
        n_legislators: int = 50,
        n_judges: int = 9,
        initial_cli: float = 0.5,
        initial_mfd: float = 1.0,
        # Triple Capture Components (optional - if None, uses initial_cli for all)
        initial_cli_memetic: Optional[float] = None,
        initial_cli_corporate: Optional[float] = None,
        initial_cli_oligarchic: Optional[float] = None,
        union_militancy_range: Tuple[int, int] = (4, 7),
        employer_coordination_range: Tuple[int, int] = (4, 7),
        crisis_probability: float = 0.05,
        reform_proposal_interval: int = 20,
        random_seed: Optional[int] = None
    ):
        """
        Initialize simulation environment
        
        Args:
            n_workers: Number of worker agents
            n_unions: Number of union agents
            n_employers: Number of employer agents
            n_legislators: Number of legislator agents
            n_judges: Number of judge agents
            initial_cli: Starting CLI value
            initial_mfd: Starting MFD value
            union_militancy_range: (min, max) militancy for unions
            employer_coordination_range: (min, max) coordination for employers
            crisis_probability: Probability of crisis per timestep
            reform_proposal_interval: Timesteps between reform proposals
            random_seed: Random seed for reproducibility
        """
        if random_seed is not None:
            random.seed(random_seed)
            np.random.seed(random_seed)
        
        # Initialize state with triple capture decomposition
        # If components provided, use them; otherwise use initial_cli for all
        self.state = EnvironmentState(
            cli_memetic=initial_cli_memetic if initial_cli_memetic is not None else initial_cli,
            cli_corporate=initial_cli_corporate if initial_cli_corporate is not None else initial_cli,
            cli_oligarchic=initial_cli_oligarchic if initial_cli_oligarchic is not None else initial_cli,
            mfd=initial_mfd
        )
        
        # Legacy constitutional parameters (map to oligarchic)
        self.state.constitutional_rigidity = initial_cli * 0.35 / 0.35
        self.state.ultraactivity_protection = initial_cli * 0.40 / 0.40
        self.state.judicial_review_strength = initial_cli * 0.25 / 0.25
        
        # Simulation parameters
        self.crisis_probability = crisis_probability
        self.reform_proposal_interval = reform_proposal_interval
        
        # Agent populations
        self.workers: List[Worker] = []
        self.unions: List[Union] = []
        self.employers: List[Employer] = []
        self.legislators: List[Legislator] = []
        self.judges: List[Judge] = []
        
        # Create agents
        self._create_worker_population(n_workers)
        self._create_union_population(n_unions, union_militancy_range)
        self._create_employer_population(n_employers, employer_coordination_range)
        self._create_legislator_population(n_legislators)
        self._create_judge_population(n_judges)
        
        # History tracking
        self.history: List[Dict[str, Any]] = []
        self.reform_history: List[ReformProposal] = []
        
        # Current reform
        self.current_reform: Optional[ReformProposal] = None
        
    def _create_worker_population(self, n: int):
        """Create worker agents with heterogeneous parameters"""
        for i in range(n):
            state = WorkerState(
                income_level=np.random.lognormal(0, 0.5),
                risk_aversion=np.random.beta(2, 2),
                compliance_cost=np.random.uniform(0.1, 0.5),
                memetic_alignment=np.random.beta(2, 2)
            )
            self.workers.append(Worker(state))
    
    def _create_union_population(self, n: int, militancy_range: Tuple[int, int]):
        """Create union agents with specified militancy range"""
        for i in range(n):
            militancy = random.randint(militancy_range[0], militancy_range[1])
            state = UnionState(
                militancy=militancy,
                member_count=random.randint(50, 500),
                strike_capacity=np.random.beta(2, 2),
                political_connections=np.random.beta(2, 2)
            )
            self.unions.append(Union(state))
    
    def _create_employer_population(self, n: int, coordination_range: Tuple[int, int]):
        """Create employer agents with specified coordination range"""
        for i in range(n):
            coordination = random.randint(coordination_range[0], coordination_range[1])
            state = EmployerState(
                coordination_capacity=coordination,
                firm_size=random.choice(['small', 'medium', 'large']),
                sector=random.choice(['manufacturing', 'services', 'agriculture']),
                lobbying_budget=np.random.beta(2, 2)
            )
            self.employers.append(Employer(state))
    
    def _create_legislator_population(self, n: int):
        """Create legislator agents with party affiliations"""
        for i in range(n):
            state = LegislatorState(
                party_affiliation=random.choice(['left', 'center', 'right']),
                electoral_security=np.random.beta(3, 3),
                ideology_flexibility=np.random.beta(2, 2),
                union_connections=np.random.beta(2, 2),
                business_connections=np.random.beta(2, 2)
            )
            self.legislators.append(Legislator(state))
    
    def _create_judge_population(self, n: int):
        """Create judge agents with doctrine preferences"""
        for i in range(n):
            state = JudgeState(
                doctrine=random.choice(['progressive', 'conservative', 'moderate']),
                precedent_weight=np.random.beta(3, 2),
                constitutional_interpretation=random.choice(['strict', 'flexible']),
                labor_rights_priority=np.random.beta(2, 2)
            )
            self.judges.append(Judge(state))
    
    def step(self):
        """
        Execute one timestep of simulation
        
        Complete sequence:
        1. Crisis check (stochastic events)
        2. Reform proposal (periodic)
        3. Agent decisions
        4. Agent interactions
        5. Reform processing (if proposed)
        6. State updates (CLI, MFD, aggregates)
        7. History recording
        """
        self.state.timestep += 1
        
        # 1. Check for crisis events
        self._check_crisis_events()
        
        # 2. Propose reform if interval reached
        if self.state.timestep % self.reform_proposal_interval == 0:
            if self.state.government_reform_appetite > 0.5 or self.state.crisis_active:
                self._propose_reform()
        
        # 3. Agents decide actions
        environment_dict = self._get_environment_dict()
        for agent_list in [self.workers, self.unions, self.employers, self.legislators, self.judges]:
            for agent in agent_list:
                action = agent.decide_action(environment_dict)
                # Actions are stored in agent state for interaction phase
        
        # 4. Agent interactions (network effects)
        self._execute_agent_interactions()
        
        # 5. Process reform if one is active
        if self.current_reform is not None:
            self._process_reform()
        
        # 6. Update environment state
        self._update_environment_state()
        
        # 7. Record history
        self._record_history()
    
    def _check_crisis_events(self):
        """Check for economic/political crisis (stochastic)"""
        if random.random() < self.crisis_probability:
            self.state.crisis_active = True
            self.state.crisis_salience = np.random.beta(3, 1)  # Skewed toward high salience
            self.state.government_reform_appetite += 0.3
            self.state.government_reform_appetite = min(1.0, self.state.government_reform_appetite)
        else:
            # Crisis decay
            if self.state.crisis_active:
                self.state.crisis_salience *= 0.9
                if self.state.crisis_salience < 0.1:
                    self.state.crisis_active = False
    
    def _propose_reform(self):
        """Propose a labor market reform"""
        # Reform targeting decision
        targets_ultraactivity = random.random() < 0.7  # 70% of reforms target ultraactivity
        targets_constitutional = random.random() < 0.3  # 30% target constitutional provisions
        
        expected_cli_reduction = 0.0
        if targets_ultraactivity:
            expected_cli_reduction += 0.15 * self.state.ultraactivity_protection
        if targets_constitutional:
            expected_cli_reduction += 0.10 * self.state.constitutional_rigidity
        
        reform = ReformProposal(
            proposal_id=f"reform_{self.state.timestep}",
            timestep=self.state.timestep,
            targets_ultraactivity=targets_ultraactivity,
            targets_constitutional=targets_constitutional,
            expected_cli_reduction=expected_cli_reduction,
            political_cost=np.random.beta(2, 2)
        )
        
        self.current_reform = reform
        self.state.reform_proposed = True
        self.state.reform_targets_ultraactivity = targets_ultraactivity
        self.state.reforms_attempted += 1
    
    def _execute_agent_interactions(self):
        """Execute agent-to-agent interactions (network effects)"""
        # Union-Worker interactions
        for union in self.unions:
            # Each union interacts with subset of workers
            worker_sample = random.sample(self.workers, min(20, len(self.workers)))
            for worker in worker_sample:
                union.interact(worker)
                worker.interact(union)
        
        # Union-Legislator lobbying
        for union in self.unions:
            legislator_sample = random.sample(self.legislators, min(5, len(self.legislators)))
            for legislator in legislator_sample:
                union.interact(legislator)
        
        # Employer-Legislator lobbying
        for employer in self.employers:
            legislator_sample = random.sample(self.legislators, min(5, len(self.legislators)))
            for legislator in legislator_sample:
                employer.interact(legislator)
        
        # Worker-Worker peer effects
        for _ in range(len(self.workers) // 4):
            w1, w2 = random.sample(self.workers, 2)
            w1.interact(w2)
    
    def _process_reform(self):
        """
        Process reform through legislative and judicial channels
        
        Sequence:
        1. Legislative vote
        2. If passes: Judicial review (if CLI high)
        3. If both pass: Reform succeeds, CLI reduces
        """
        reform = self.current_reform
        
        # Legislative voting
        votes_for = 0
        votes_against = 0
        
        for legislator in self.legislators:
            # Legislator vote depends on:
            # - Party affiliation
            # - Union/business connections
            # - Electoral security
            # - Crisis pressure
            
            vote_prob = self._calculate_legislator_vote_probability(legislator, reform)
            
            if random.random() < vote_prob:
                votes_for += 1
            else:
                votes_against += 1
        
        reform.legislative_votes_for = votes_for
        reform.legislative_votes_against = votes_against
        reform.legislative_passed = votes_for > votes_against
        
        # Judicial review (if legislative passed and CLI > 0.4)
        if reform.legislative_passed:
            if self.state.cli > 0.4:
                # Judicial review more likely to block with high CLI
                judicial_block_probability = self.state.cli * 0.8
                
                # Judges vote on constitutionality
                judges_uphold = 0
                judges_strike = 0
                
                for judge in self.judges:
                    uphold_prob = self._calculate_judge_uphold_probability(judge, reform)
                    if random.random() < uphold_prob:
                        judges_strike += 1
                    else:
                        judges_uphold += 1
                
                reform.judicial_review_passed = judges_strike < (len(self.judges) // 2 + 1)
            else:
                # Low CLI: judicial review not triggered or passes easily
                reform.judicial_review_passed = True
            
            # Final outcome
            reform.final_passed = reform.legislative_passed and reform.judicial_review_passed
        else:
            reform.final_passed = False
        
        # Apply reform effects if passed
        if reform.final_passed:
            self.state.reforms_succeeded += 1
            self.state.reform_passed = True
            
            # Update triple capture components (differential speed)
            self.update_cli_components('success')
            
            # Legacy: Reduce CLI components (for backwards compatibility)
            if reform.targets_ultraactivity:
                self.state.ultraactivity_protection *= 0.7
            if reform.targets_constitutional:
                self.state.constitutional_rigidity *= 0.9
            
            # Recalculate CLI
            self._recalculate_cli()
        else:
            self.state.reform_passed = False
            
            # Failed reform strengthens lock-in (entrenchment)
            self.update_cli_components('failure')
        
        # Store in history and clear current
        self.reform_history.append(reform)
        self.current_reform = None
        self.state.reform_proposed = False
        self.state.reform_targets_ultraactivity = False
    
    def _calculate_legislator_vote_probability(
        self, 
        legislator: Legislator, 
        reform: ReformProposal
    ) -> float:
        """Calculate probability legislator votes for reform"""
        state: LegislatorState = legislator.state
        
        # Base probability by party
        base_prob = {
            'left': 0.2,
            'center': 0.5,
            'right': 0.7
        }[state.party_affiliation]
        
        # Modifiers
        crisis_boost = 0.3 if self.state.crisis_active else 0.0
        union_pressure = -0.2 * state.union_ties * (self.state.avg_union_militancy / 10.0)
        business_pressure = 0.2 * state.business_ties
        electoral_security_modifier = state.electoral_security * 0.2  # Secure legislators more willing
        
        vote_prob = base_prob + crisis_boost + union_pressure + business_pressure + electoral_security_modifier
        return np.clip(vote_prob, 0.0, 1.0)
    
    def _calculate_judge_uphold_probability(
        self,
        judge: Judge,
        reform: ReformProposal
    ) -> float:
        """Calculate probability judge upholds reform (doesn't strike down)"""
        state: JudgeState = judge.state
        
        # Base probability by doctrine
        base_prob = {
            'progressive': 0.3,   # Progressive judges protect labor rights
            'moderate': 0.5,
            'conservative': 0.7   # Conservative judges defer to legislature
        }[state.doctrine]
        
        # Modifiers
        if reform.targets_ultraactivity:
            # Labor rights priority matters
            base_prob -= state.labor_rights_priority * 0.3
        
        # Precedent weight: high precedent weight → less likely to uphold change
        precedent_modifier = -state.precedent_weight * 0.2
        
        uphold_prob = base_prob + precedent_modifier
        return np.clip(uphold_prob, 0.0, 1.0)
    
    def _recalculate_cli(self):
        """
        Recalculate CLI from triple capture components
        
        NOTE: cli property auto-calculates from cli_memetic, cli_corporate, cli_oligarchic
        This method now syncs legacy constitutional parameters with oligarchic component
        """
        # Update legacy parameters from oligarchic capture
        # (For backwards compatibility with scenarios using old formulation)
        self.state.constitutional_rigidity = self.state.cli_oligarchic
        self.state.ultraactivity_protection = self.state.cli_oligarchic
        self.state.judicial_review_strength = self.state.cli_oligarchic
    
    def update_cli_components(self, reform_outcome: str):
        """
        Update triple capture components based on reform outcome
        
        Components change at different speeds:
        - Memetic: Slowest (cultural inertia, System 1 heuristics)
        - Corporate: Moderate (strategic adaptation, organizational inertia)
        - Oligarchic: Fastest (appointments, precedents)
        
        Args:
            reform_outcome: 'success' or 'failure'
        """
        if reform_outcome == 'success':
            # Successful reform weakens all capture mechanisms
            # But at different rates reflecting their inertia
            self.state.cli_memetic *= 0.98      # 2% reduction (very slow cultural shift)
            self.state.cli_corporate *= 0.92    # 8% reduction (moderate adaptation)
            self.state.cli_oligarchic *= 0.85   # 15% reduction (fast precedent change)
            
        else:  # failure
            # Failed reform strengthens capture (entrenchment effect)
            # Memetic especially: "reform is impossible" becomes common sense
            self.state.cli_memetic *= 1.02      # 2% increase (narrative reinforcement)
            self.state.cli_corporate *= 1.03    # 3% increase (emboldens veto players)
            self.state.cli_oligarchic *= 1.01   # 1% increase (precedent confirmation)
        
        # Enforce bounds [0.0, 1.0]
        self.state.cli_memetic = np.clip(self.state.cli_memetic, 0.0, 1.0)
        self.state.cli_corporate = np.clip(self.state.cli_corporate, 0.0, 1.0)
        self.state.cli_oligarchic = np.clip(self.state.cli_oligarchic, 0.0, 1.0)
        
        # Sync legacy parameters
        self._recalculate_cli()
    
    def _update_environment_state(self):
        """Update aggregate state variables"""
        # Agent aggregates
        if self.workers:
            compliances = [1.0 if w.decide_action(self._get_environment_dict()) == "comply_formal" else 0.0 
                          for w in random.sample(self.workers, min(50, len(self.workers)))]
            self.state.avg_worker_compliance = np.mean(compliances)
        
        if self.unions:
            self.state.avg_union_militancy = np.mean([u.state.militancy for u in self.unions])
        
        if self.employers:
            self.state.avg_employer_coordination = np.mean([e.state.coordination_capacity for e in self.employers])
        
        # Economic variables (simplified dynamics)
        self.state.informal_employment_rate = 0.35 + 0.1 * (1.0 - self.state.avg_worker_compliance)
        self.state.unemployment_rate = max(0.03, 0.08 - 0.02 * (1.0 - self.state.cli))
        
        # MFD calculation (simplified)
        # MFD = (r_informal × e_informal × a_informal) / (r_formal × e_formal × a_formal)
        r_informal = self.state.informal_employment_rate
        r_formal = 1.0 - r_informal
        e_informal = self.state.avg_union_militancy / 10.0
        e_formal = max(0.1, 1.0 - e_informal)
        a_informal = self.state.cli  # High CLI → informal practices attractive
        a_formal = max(0.1, 1.0 - a_informal)
        
        self.state.mfd = (r_informal * e_informal * a_informal) / (r_formal * e_formal * a_formal)
    
    def _get_environment_dict(self) -> Dict[str, Any]:
        """Get environment state as dictionary for agent decision-making"""
        return {
            'timestep': self.state.timestep,
            'cli': self.state.cli,
            'mfd': self.state.mfd,
            'crisis_active': self.state.crisis_active,
            'crisis_salience': self.state.crisis_salience,
            'reform_proposed': self.state.reform_proposed,
            'reform_targets_ultraactivity': self.state.reform_targets_ultraactivity,
            'enforcement_level': 1.0 - self.state.cli,
            'formal_benefits': 0.5 + 0.2 * (1.0 - self.state.cli),
            'informal_benefits': 0.5 + 0.2 * self.state.cli,
            'government_support': self.state.government_reform_appetite,
            'unemployment_rate': self.state.unemployment_rate,
            'informal_employment_rate': self.state.informal_employment_rate
        }
    
    def _record_history(self):
        """Record current state to history"""
        self.history.append(self.state.to_dict())
    
    def run(self, n_timesteps: int):
        """
        Run simulation for n timesteps
        
        Args:
            n_timesteps: Number of timesteps to simulate
        """
        for _ in range(n_timesteps):
            self.step()
    
    def get_results(self) -> Dict[str, Any]:
        """
        Get simulation results
        
        Returns:
            Dictionary with:
            - history: Full timestep history
            - reform_history: All reform attempts
            - final_state: Final environment state
            - summary_stats: Summary statistics
        """
        return {
            'history': self.history,
            'reform_history': [
                {
                    'proposal_id': r.proposal_id,
                    'timestep': r.timestep,
                    'targets_ultraactivity': r.targets_ultraactivity,
                    'legislative_passed': r.legislative_passed,
                    'judicial_review_passed': r.judicial_review_passed,
                    'final_passed': r.final_passed
                }
                for r in self.reform_history
            ],
            'final_state': self.state.to_dict(),
            'summary_stats': {
                'total_timesteps': self.state.timestep,
                'reforms_attempted': self.state.reforms_attempted,
                'reforms_succeeded': self.state.reforms_succeeded,
                'reform_success_rate': self.state.reforms_succeeded / max(1, self.state.reforms_attempted),
                'final_cli': self.state.cli,
                'final_mfd': self.state.mfd,
                'cli_trajectory': [h['cli'] for h in self.history],
                'mfd_trajectory': [h['mfd'] for h in self.history]
            }
        }
tory]
            }
        }
