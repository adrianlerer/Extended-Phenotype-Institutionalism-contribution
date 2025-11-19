# Future Development: Conversational AI Extension

**Date**: November 2024  
**Idea Origin**: Adrian Lerer  
**Inspiration**: FLAISimulator (IntegridAI Suite)

---

## 🎯 Core Concept

**Extend the ABM system with conversational AI voices** to simulate realistic debates and negotiations between agents, making the abstract simulation tangible and audible.

### Inspiration: FLAISimulator

**FLAISimulator** (existing development in IntegridAI Suite repo) demonstrates multi-agent conversational dynamics. We can adapt this approach to the institutional reform ABM.

---

## 🗣️ Proposed Architecture

### 1. Voice-Enabled Agent Roles

Each agent type gets a distinct voice profile using **ElevenLabs** (or similar TTS):

**Agent Types → Voice Profiles**:

1. **Worker Agents**:
   - Voice: Diverse regional accents
   - Tone: Varies by memetic alignment (pro-formal vs pro-informal)
   - Temperature: Reflects risk aversion and income level
   
2. **Union Leaders**:
   - Voice: Strong, assertive
   - Tone: Varies by militancy (1-10 scale)
   - Temperature: High militancy = aggressive, low = cooperative
   
3. **Employers**:
   - Voice: Professional, business-like
   - Tone: Varies by coordination capacity
   - Temperature: High coordination = unified, low = fragmented
   
4. **Legislators**:
   - Voice: Political, persuasive
   - Tone: Varies by party affiliation
   - Temperature: Electoral security affects confidence level
   
5. **Judges**:
   - Voice: Formal, authoritative
   - Tone: Varies by doctrine (progressive vs conservative)
   - Temperature: High CLI = rigid, low CLI = flexible

### 2. Temperature-Driven Dialogue

**"Temperature" controls conversation intensity and conflict level**:

```python
class ConversationalTemperature:
    """
    Temperature parameters affecting dialogue dynamics
    
    Based on current simulation state:
    - CLI level (constitutional rigidity)
    - Union militancy
    - Crisis salience
    - Reform stage (proposal, voting, judicial review)
    """
    
    def calculate_temperature(self, environment_state: EnvironmentState) -> float:
        """
        Calculate conversation temperature (0.0 = calm, 1.0 = heated)
        
        Factors:
        - CLI > 0.7 → temperature +0.3
        - Union militancy > 7 → temperature +0.2
        - Crisis active → temperature +0.3
        - Reform at judicial review → temperature +0.2
        """
        temperature = 0.5  # baseline
        
        if environment_state.cli > 0.7:
            temperature += 0.3
        
        if environment_state.avg_union_militancy > 7:
            temperature += 0.2
        
        if environment_state.crisis_active:
            temperature += 0.3
        
        if environment_state.reform_proposed and environment_state.timestep % 5 == 0:
            temperature += 0.2  # Heated debate during voting
        
        return min(1.0, temperature)
```

### 3. Dialogue Generation System

**Integration with LLM + TTS**:

```python
class ConversationalSimulator:
    """
    Generate and vocalize agent debates
    
    Architecture:
    1. ABM simulation provides agent states
    2. LLM generates contextual dialogue
    3. ElevenLabs synthesizes speech
    4. Audio mixed into "parliamentary session" or "negotiation table"
    """
    
    def generate_debate(
        self,
        scenario: str,
        timestep: int,
        agents: List[BaseAgent],
        temperature: float
    ) -> List[AudioSegment]:
        """
        Generate multi-agent debate
        
        Returns:
        - List of audio segments (one per speaker)
        - Timing information for overlap/interruptions
        - Visual transcript with emotional annotations
        """
        
    def simulate_legislative_session(
        self,
        reform_proposal: ReformProposal,
        legislators: List[Legislator],
        unions: List[Union],
        employers: List[Employer]
    ) -> AudioDebate:
        """
        Simulate parliamentary debate on reform
        
        Sequence:
        1. Government minister proposes reform (formal tone)
        2. Union leaders object (temperature-dependent intensity)
        3. Business representatives support (coordination-dependent unity)
        4. Legislators debate (party-aligned positions)
        5. Vote count with reactions
        """
        
    def simulate_judicial_hearing(
        self,
        reform: ReformProposal,
        judges: List[Judge],
        union_lawyers: List[str],
        government_lawyers: List[str]
    ) -> AudioDebate:
        """
        Simulate constitutional court hearing
        
        Sequence:
        1. Court president opens session
        2. Government presents case
        3. Union lawyers present constitutional objections
        4. Judges ask questions (doctrine-dependent)
        5. Deliberation snippets
        6. Ruling announcement
        """
```

---

## 🎬 Use Cases

### Use Case 1: Policy Simulation Preview

**Scenario**: Government planning reform

**Process**:
1. Configure simulation parameters (CLI, union militancy, etc.)
2. Run simulation silently to get outcomes
3. Generate "replay" of key moments with voices
4. Present to cabinet with audio-visual debate

**Output**:
- 5-10 minute audio drama of parliamentary session
- Key objections vocalized by simulated union leaders
- Judicial hearing preview if CLI high
- Final vote announcement

**Value**: Decision-makers can **hear** the opposition, not just read statistics.

### Use Case 2: Training Simulations

**Scenario**: Train negotiators for labor reform

**Process**:
1. Set up counterfactual scenarios
2. Generate debates with different temperature levels
3. Compare calm negotiation vs heated confrontation
4. Train team on de-escalation tactics

**Output**:
- Multiple audio tracks showing negotiation dynamics
- Temperature dial showing escalation points
- Transcripts with emotional annotations

**Value**: Experiential learning through realistic simulations.

### Use Case 3: Public Communication

**Scenario**: Explain complex institutional dynamics to public

**Process**:
1. Run Uruguay 1991 vs Argentina 1990-2024 scenarios
2. Generate contrasting debates
3. Publish as podcast episodes

**Output**:
- "Why Uruguay succeeded: A simulated debate" (15 min audio)
- "Argentina's chronic lock-in: Voices from 23 failed reforms" (20 min audio)

**Value**: Make ABM results accessible to non-technical audiences.

### Use Case 4: Academic Presentations

**Scenario**: Conference presentation on ABM results

**Process**:
1. Run simulation live on stage
2. Play audio snippets at key timesteps
3. Show how temperature correlates with outcomes

**Output**:
- Live demo with real-time voice generation
- Interactive Q&A with simulated agents
- Conference attendees can "ask" virtual union leader questions

**Value**: Memorable, engaging academic presentations.

---

## 🔧 Technical Implementation

### Phase 1: Voice Profile Library (Week 1-2)

**Task**: Create distinct voice profiles for each agent type

```python
# Voice profiles using ElevenLabs API
VOICE_PROFILES = {
    'union_leader_militant': {
        'voice_id': 'xyz123',
        'stability': 0.5,
        'similarity_boost': 0.75,
        'style': 0.8  # High emotion
    },
    'union_leader_cooperative': {
        'voice_id': 'abc456',
        'stability': 0.7,
        'similarity_boost': 0.65,
        'style': 0.4  # Moderate emotion
    },
    'employer_coordinated': {
        'voice_id': 'def789',
        'stability': 0.8,
        'similarity_boost': 0.7,
        'style': 0.3  # Professional
    },
    # ... etc for all agent types
}
```

### Phase 2: Dialogue Generation (Week 3-4)

**Task**: LLM integration for contextual dialogue

```python
class DialogueGenerator:
    """
    Generate agent dialogue based on simulation state
    
    Uses LLM (GPT-4, Claude, or similar) with prompt engineering
    """
    
    def generate_agent_statement(
        self,
        agent: BaseAgent,
        context: SimulationContext,
        temperature: float
    ) -> str:
        """
        Generate statement for agent
        
        Prompt structure:
        - Agent type and state variables
        - Current simulation context (reform stage, CLI, etc.)
        - Conversation temperature
        - Historical actions in current scenario
        
        Returns: Natural language statement reflecting agent's position
        """
        
        prompt = f"""
        You are a {agent.get_type()} in a labor market reform debate.
        
        Your characteristics:
        {self._format_agent_state(agent)}
        
        Current situation:
        {self._format_context(context)}
        
        Conversation temperature: {temperature} (0=calm, 1=heated)
        
        Generate a statement reflecting your position on the proposed reform.
        """
        
        # Call LLM API
        response = self.llm_client.generate(
            prompt=prompt,
            max_tokens=200,
            temperature=temperature  # LLM temperature matches simulation temperature
        )
        
        return response
```

### Phase 3: Audio Synthesis (Week 5-6)

**Task**: Convert text to speech with emotional tone

```python
class VoiceSynthesizer:
    """
    Synthesize speech using ElevenLabs API
    """
    
    def synthesize_statement(
        self,
        text: str,
        voice_profile: dict,
        temperature: float
    ) -> AudioSegment:
        """
        Convert text to speech
        
        Adjusts voice parameters based on temperature:
        - High temperature → faster pace, higher pitch variation
        - Low temperature → slower pace, more measured tone
        """
        
        # Adjust voice settings for temperature
        settings = voice_profile.copy()
        settings['stability'] *= (1.0 - temperature * 0.3)  # Less stable when heated
        settings['style'] = max(0.0, min(1.0, settings['style'] + temperature * 0.2))
        
        # Call ElevenLabs API
        audio = elevenlabs.generate(
            text=text,
            voice=settings['voice_id'],
            model="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=settings['stability'],
                similarity_boost=settings['similarity_boost'],
                style=settings['style']
            )
        )
        
        return AudioSegment.from_file(io.BytesIO(audio))
```

### Phase 4: Multi-Agent Orchestration (Week 7-8)

**Task**: Coordinate multiple speakers in debate format

```python
class DebateOrchestrator:
    """
    Orchestrate multi-agent debates with turn-taking
    """
    
    def create_debate_sequence(
        self,
        agents: List[BaseAgent],
        debate_topic: str,
        temperature: float,
        max_turns: int = 10
    ) -> List[AudioSegment]:
        """
        Create turn-based debate
        
        Logic:
        - High temperature → more interruptions, overlapping speech
        - Low temperature → orderly turn-taking
        - Agent decision rules determine who speaks when
        """
        
        audio_segments = []
        
        for turn in range(max_turns):
            # Select next speaker based on agent state and temperature
            speaker = self._select_next_speaker(agents, temperature)
            
            # Generate dialogue
            statement = self.dialogue_gen.generate_agent_statement(
                agent=speaker,
                context=self._get_current_context(),
                temperature=temperature
            )
            
            # Synthesize audio
            audio = self.voice_synth.synthesize_statement(
                text=statement,
                voice_profile=self._get_voice_profile(speaker),
                temperature=temperature
            )
            
            audio_segments.append({
                'speaker': speaker.get_type(),
                'audio': audio,
                'text': statement,
                'timestamp': turn * 10  # seconds
            })
        
        return audio_segments
    
    def mix_debate_audio(
        self,
        segments: List[dict],
        add_background: bool = True
    ) -> AudioSegment:
        """
        Mix all audio segments into single track
        
        Features:
        - Background ambience (parliament, courtroom, etc.)
        - Cross-fade between speakers
        - Interrupt effects for high-temperature moments
        """
        
        mixed_audio = AudioSegment.silent(duration=0)
        
        for segment in segments:
            # Add silence/cross-fade
            mixed_audio += AudioSegment.silent(duration=500)
            
            # Add speaker audio
            mixed_audio += segment['audio']
        
        if add_background:
            # Add subtle background (parliamentary murmurs, etc.)
            background = self._generate_background_ambience()
            mixed_audio = mixed_audio.overlay(background, gain_during_overlay=-20)
        
        return mixed_audio
```

---

## 📊 Integration with Existing ABM System

### Minimal Changes to Core System

**Good news**: Current ABM architecture already supports this extension with minimal modification.

**Required hooks**:

```python
# Add to SimulationEnvironment class
class SimulationEnvironment:
    """Enhanced with conversational AI support"""
    
    def __init__(self, ..., enable_conversation: bool = False):
        # ... existing init code ...
        
        if enable_conversation:
            self.conversation_recorder = ConversationRecorder()
            self.key_moments = []  # Track important timesteps
    
    def step(self):
        """Enhanced timestep with conversation recording"""
        
        # ... existing step logic ...
        
        if self.enable_conversation and self._is_key_moment():
            # Record this moment for voice generation
            self.key_moments.append({
                'timestep': self.state.timestep,
                'type': self._get_moment_type(),  # 'proposal', 'vote', 'ruling'
                'agents': self._get_active_agents(),
                'temperature': self._calculate_temperature()
            })
    
    def generate_audio_replay(self) -> AudioDebate:
        """Generate audio replay of simulation"""
        
        orchestrator = DebateOrchestrator()
        
        audio_segments = []
        for moment in self.key_moments:
            segment = orchestrator.create_debate_sequence(
                agents=moment['agents'],
                debate_topic=moment['type'],
                temperature=moment['temperature']
            )
            audio_segments.extend(segment)
        
        return orchestrator.mix_debate_audio(audio_segments)
```

---

## 🎨 User Interface Concepts

### Option 1: Interactive Dashboard

**Streamlit app with voice controls**:

```python
import streamlit as st

st.title("ABM Conversational Simulator")

# Scenario selection
scenario = st.selectbox("Select scenario", ["Uruguay 1991", "Argentina chronic lock-in"])

# Temperature slider
temperature = st.slider("Conversation temperature", 0.0, 1.0, 0.5)

# Run simulation
if st.button("Run simulation with voices"):
    with st.spinner("Running simulation..."):
        # Run ABM
        results = run_scenario(scenario)
        
        # Generate audio
        audio = generate_audio_replay(results, temperature)
        
        # Display
        st.audio(audio)
        st.write("Transcript:")
        st.write(audio.transcript)
```

### Option 2: Command-Line Tool

```bash
# Generate audio replay
python conversational_abm.py \
    --scenario uruguay_1991 \
    --temperature 0.7 \
    --output uruguay_debate.mp3 \
    --format podcast

# Output: 15-minute audio file with debate highlights
```

### Option 3: API Endpoint

```python
# FastAPI endpoint
@app.post("/api/v1/simulate/voice")
def simulate_with_voice(request: VoiceSimulationRequest):
    """
    Run simulation and generate audio debate
    
    POST body:
    {
        "scenario": "uruguay_1991",
        "temperature": 0.7,
        "language": "es",  # Spanish
        "duration_limit": 600  # 10 minutes max
    }
    
    Returns:
    {
        "audio_url": "https://...",
        "transcript": "...",
        "key_moments": [...]
    }
    """
```

---

## 💰 Cost Considerations

### ElevenLabs API Pricing (Estimated)

**Assumptions**:
- 10-minute debate = ~1,500 words
- 5 different voices
- ElevenLabs: $0.18 per 1,000 characters

**Cost per simulation**:
- Text: ~10,000 characters
- Cost: ~$1.80 per audio replay

**Optimization strategies**:
1. Cache frequently used statements
2. Pre-generate common responses
3. Offer tiered service (text-only free, audio premium)

### LLM API Pricing (Estimated)

**GPT-4 Turbo**:
- Input: ~2,000 tokens per agent statement
- Output: ~200 tokens
- Cost: ~$0.02 per statement

**For 10-agent debate** (50 statements):
- Cost: ~$1.00

**Total cost per audio replay**: ~$3-5

---

## 🚀 Development Timeline

### Phase 1: Prototype (2-3 weeks)
- [ ] Voice profile library (5 agent types)
- [ ] Basic dialogue generation (LLM integration)
- [ ] Single-agent speech synthesis
- [ ] Simple turn-taking logic

**Deliverable**: Single debate between 2 agents (union vs employer)

### Phase 2: Multi-Agent (3-4 weeks)
- [ ] Full 5-agent type support
- [ ] Temperature-driven dialogue
- [ ] Audio mixing and orchestration
- [ ] Transcript generation with timing

**Deliverable**: Complete legislative session simulation

### Phase 3: Integration (2-3 weeks)
- [ ] Integrate with existing ABM system
- [ ] Key moment detection
- [ ] Replay generation from simulation history
- [ ] Export formats (MP3, podcast RSS)

**Deliverable**: Full ABM → Audio pipeline

### Phase 4: UI & Distribution (2-3 weeks)
- [ ] Streamlit dashboard
- [ ] API endpoints
- [ ] Documentation and examples
- [ ] Demo videos

**Deliverable**: Production-ready conversational ABM

**Total timeline**: 10-12 weeks (2.5-3 months)

---

## 📚 Related Work / Inspiration

### FLAISimulator (IntegridAI Suite)

**Repository**: Check IntegridAI Suite repo for FLAISimulator implementation

**Key learnings to adapt**:
- Multi-agent conversation management
- Turn-taking algorithms
- Audio mixing techniques
- Real-time interaction patterns

### Academic References

- **Scherer et al. (2019)**. "Vocal emotion expression in conversational agents"
- **Nass & Lee (2001)**. "Does computer-synthesized speech manifest personality?"
- **Epstein (2006)**. "Generative social science" (ABM + narrative)

---

## 🎯 Success Metrics

**Technical**:
- Audio generation time: <30 seconds for 10-minute debate
- Voice quality: >4.0/5.0 naturalness rating
- Dialogue coherence: >80% contextually appropriate statements

**User Experience**:
- Engagement: Users listen to >70% of generated audio
- Comprehension: >80% correctly identify agent positions after listening
- Usefulness: >70% say audio helps understand simulation results

**Commercial**:
- Government pilots: 3+ agencies testing system
- Consulting adoption: McKinsey/BCG interest
- Academic citations: 10+ papers citing conversational ABM

---

## 💡 Extension Ideas

### Idea 1: Multilingual Support

Generate debates in Spanish, Portuguese, English based on jurisdiction.

### Idea 2: Historical Recreation

Use ElevenLabs voice cloning to simulate actual historical figures (with disclaimers).

### Idea 3: Interactive Negotiation

User plays role of government minister, AI agents respond in real-time.

### Idea 4: Podcast Series

"Simulated Reforms" - monthly podcast exploring different scenarios with AI debates.

---

## 📧 Next Steps

**Tomorrow**:
1. Review FLAISimulator code in IntegridAI Suite repo
2. Test ElevenLabs API with sample agent statements
3. Prototype single union leader voice generation

**This Week**:
1. Design voice profile library
2. Create dialogue generation prompts
3. Build basic 2-agent conversation

**This Month**:
1. Full prototype with 5 agent types
2. Temperature-driven dialogue system
3. Integration plan with existing ABM

---

## 🔗 Resources

**APIs to evaluate**:
- ElevenLabs: https://elevenlabs.io
- Azure Speech Services: https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/
- Google Text-to-Speech: https://cloud.google.com/text-to-speech

**Audio processing**:
- pydub: Audio manipulation
- librosa: Audio analysis
- soundfile: Audio I/O

**LLM integration**:
- OpenAI GPT-4
- Anthropic Claude
- Open-source alternatives (Llama, Mixtral)

---

**This extension would make the ABM system uniquely engaging and accessible, bridging the gap between technical simulation and human understanding through natural conversation.**

---

**Author**: Adrian Lerer  
**Date**: November 2024  
**Status**: Concept document for future development
