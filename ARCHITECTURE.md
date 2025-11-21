# 🏗️ AI Museum Curator - Architecture Documentation

## System Overview

AI Museum Curator is a multi-agent system that generates museum-quality exhibitions using coordinated AI agents, custom tools, and quality evaluation loops.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUT                               │
│                      (Exhibition Topic)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   TOPIC INTAKE AGENT                             │
│  - Validates topic                                               │
│  - Enriches with context                                         │
│  - Generates exhibition title                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PARALLEL RESEARCH PHASE                        │
│                                                                   │
│  ┌──────────────────────┐      ┌──────────────────────┐        │
│  │  RESEARCH AGENT      │      │ VISUAL CONTEXT AGENT │        │
│  │  - Google Search     │      │ - Prepare visual     │        │
│  │  - Fact extraction   │      │   references         │        │
│  │  - Summarization     │      │ - Image search       │        │
│  └──────────────────────┘      └──────────────────────┘        │
│                                                                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               EXHIBIT GENERATOR AGENT                            │
│  - Creates 6-8 exhibits                                          │
│  - Detailed descriptions                                         │
│  - Historical context                                            │
│  - Cultural significance                                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              EXHIBITION DESIGNER AGENT                           │
│  - Organizes exhibits into 3-4 themed rooms                     │
│  - Creates room narratives                                       │
│  - Designs visitor flow                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   NARRATIVE AGENT                                │
│  - Writes curator's introduction                                │
│  - Creates room narratives                                       │
│  - Develops educational storyline                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              VISUAL CONTEXT ENHANCEMENT                          │
│  - Enhances visual references                                    │
│  - Adds search URLs                                              │
│  - Contextualizes imagery                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  TIMELINE GENERATION                             │
│  - Extracts dates from exhibits                                 │
│  - Creates chronological timeline                                │
│  - Formats timeline events                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   EVALUATOR AGENT                                │
│  - Validates structure                                           │
│  - Scores content quality                                        │
│  - Checks cultural sensitivity                                   │
│  - Calculates overall score                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────┴────────┐
                    │  Score >= 0.75? │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                   YES               NO
                    │                 │
                    │                 ▼
                    │    ┌─────────────────────────┐
                    │    │     LOOP AGENT          │
                    │    │  - Refine exhibition    │
                    │    │  - Enhance content      │
                    │    │  - Add exhibits         │
                    │    └──────────┬──────────────┘
                    │               │
                    │               │ (Max 2 loops)
                    │               │
                    └───────────────┴──────────────┐
                                                   │
                                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MEMORY BANK AGENT                              │
│  - Stores in SQLite database                                     │
│  - Saves JSON file                                               │
│  - Records metadata                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXHIBITION OUTPUT                             │
│  - Complete exhibition JSON                                      │
│  - Quality metrics                                               │
│  - Agent statistics                                              │
│  - Exhibition ID                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Details

### 1. Topic Intake Agent
**Purpose**: Validate and enrich user input

**Inputs**: Raw topic string

**Outputs**: 
- Enriched topic data
- Exhibition title
- Category classification
- Time period
- Key themes

**Processing**:
1. Validates topic is suitable
2. Uses Gemini to generate context
3. Extracts structured information
4. Prepares for research phase

### 2. Research Agent
**Purpose**: Conduct research and gather facts

**Inputs**: Topic data

**Outputs**:
- Search results
- Extracted facts
- Research summary
- Quality score

**Processing**:
1. Generates 5 research queries
2. Executes Google searches
3. Extracts facts from results
4. Synthesizes findings with Gemini
5. Validates fact consistency

**Tools Used**:
- Google Search Tool
- Fact Consistency Checker

### 3. Visual Context Agent (Parallel)
**Purpose**: Prepare visual references

**Inputs**: Topic data

**Outputs**:
- Visual reference preparation
- Image search queries

**Processing**:
1. Runs in parallel with Research Agent
2. Prepares visual context
3. Generates image search queries

### 4. Exhibit Generator Agent
**Purpose**: Create individual exhibits

**Inputs**: Research data

**Outputs**: 6-8 detailed exhibits

**Processing**:
1. Uses research summary and facts
2. Generates exhibits with Gemini
3. Structures as JSON
4. Includes descriptions, facts, visual refs

**Exhibit Structure**:
```json
{
  "name": "Exhibit Title",
  "description": "Detailed description",
  "time_period": "1400-1500 CE",
  "cultural_significance": "Why it matters",
  "facts": ["Fact 1", "Fact 2"],
  "visual_refs": ["Image description"],
  "tags": ["tag1", "tag2"]
}
```

### 5. Exhibition Designer Agent
**Purpose**: Organize exhibits into rooms

**Inputs**: Exhibits and topic data

**Outputs**: Exhibition structure with 3-4 rooms

**Processing**:
1. Determines optimal room count
2. Generates room themes
3. Assigns exhibits to rooms
4. Creates room descriptions

**Room Structure**:
```json
{
  "title": "Room Title",
  "theme": "Room Theme",
  "description": "Room description",
  "narrative": "Room narrative",
  "exhibits": [...]
}
```

### 6. Narrative Agent
**Purpose**: Create storytelling content

**Inputs**: Exhibition structure

**Outputs**: Exhibition with narratives

**Processing**:
1. Generates curator's introduction (4 paragraphs)
2. Creates room narratives (2-3 sentences each)
3. Ensures educational tone
4. Maintains engagement

### 7. Evaluator Agent
**Purpose**: Assess exhibition quality

**Inputs**: Complete exhibition

**Outputs**: Evaluation report with scores

**Processing**:
1. Validates structure completeness
2. Evaluates narrative quality
3. Checks factual quality
4. Assesses cultural sensitivity
5. Calculates overall score

**Metrics**:
- Overall Quality Score (composite)
- Completeness Score
- Narrative Quality
- Factual Quality
- Cultural Sensitivity

**Tools Used**:
- Fact Consistency Checker
- Exhibit Formatter

### 8. Loop Agent
**Purpose**: Refine exhibitions below threshold

**Inputs**: Exhibition + evaluation

**Outputs**: Refined exhibition

**Processing**:
1. Checks if score >= 0.75
2. If below, applies refinements:
   - Enhances curator notes
   - Adds missing exhibits
   - Improves descriptions
3. Maximum 2 refinement loops
4. Re-evaluates after each loop

### 9. Memory Bank Agent
**Purpose**: Store exhibitions persistently

**Inputs**: Exhibition + evaluation

**Outputs**: Storage confirmation + ID

**Processing**:
1. Stores in SQLite database
2. Saves JSON file
3. Records metadata
4. Returns exhibition ID

**Database Schema**:
```sql
CREATE TABLE exhibitions (
    id INTEGER PRIMARY KEY,
    topic TEXT,
    title TEXT,
    created_at TEXT,
    quality_score REAL,
    data TEXT
)
```

## Custom Tools

### Google Search Tool
- Executes web searches
- Extracts snippets and links
- Returns structured results

### Fact Consistency Checker
- Validates fact quality
- Checks for dates and details
- Assesses cultural sensitivity
- Returns quality scores

### Timeline Generator
- Extracts dates from exhibits
- Creates chronological timeline
- Formats timeline events

### Exhibit Formatter
- Standardizes exhibit structure
- Validates completeness
- Ensures consistency

## Data Flow

```
Topic String
    ↓
Topic Data (Dict)
    ↓
Research Data (Dict with facts, summary)
    ↓
Exhibits (List[Dict])
    ↓
Exhibition Structure (Dict with rooms)
    ↓
Exhibition with Narrative (Dict)
    ↓
Exhibition with Visuals (Dict)
    ↓
Exhibition with Timeline (Dict)
    ↓
Evaluation Report (Dict with scores)
    ↓
Refined Exhibition (if needed)
    ↓
Storage Result (Dict with ID)
```

## Quality Assurance

### Success Rate Tracking
- Each agent tracks executions and successes
- Overall system success rate calculated
- Target: 95-99% success rate

### Error Handling
- Try-catch blocks in all agents
- Graceful degradation
- Fallback mechanisms
- Detailed error logging

### Evaluation Thresholds
- Accuracy: 85%
- Narrative: 80%
- Cultural Sensitivity: 90%
- Completeness: 85%
- Overall: 75%

## Observability

### Logging
- JSONL structured logs
- Agent start/complete/error events
- Performance metrics
- Exhibition metadata

### Metrics
- Quality scores
- Agent success rates
- Execution durations
- System statistics

### Tracing
- Agent execution flow
- Input/output tracking
- Error propagation
- Performance bottlenecks

## Scalability Considerations

### Parallel Processing
- Research and Visual Context agents run concurrently
- ThreadPoolExecutor for parallel execution
- Can be extended to more parallel agents

### Caching
- Research results can be cached
- Exhibit templates can be reused
- Database for historical data

### Performance
- Gemini 1.5 Flash for speed
- Configurable token limits
- Optimized prompts
- Efficient data structures

## Configuration

All system parameters in `config.py`:

```python
# Model Configuration
MODEL_NAME = "gemini-1.5-flash"
TEMPERATURE = 0.7
MAX_TOKENS = 8192

# Agent Configuration
MAX_RESEARCH_RESULTS = 10
MAX_EXHIBITS_PER_ROOM = 5
MIN_QUALITY_SCORE = 0.75
MAX_REFINEMENT_LOOPS = 2

# Evaluation Thresholds
ACCURACY_THRESHOLD = 0.85
NARRATIVE_THRESHOLD = 0.80
CULTURAL_SENSITIVITY_THRESHOLD = 0.90
COMPLETENESS_THRESHOLD = 0.85

# Success Rate Target
TARGET_SUCCESS_RATE = 0.97
```

## Deployment

### Streamlit Application
- Beautiful museum-inspired UI
- Real-time generation
- Metrics visualization
- Export functionality
- Exhibition history

### CLI Interface
- `run.py` for command-line usage
- Batch processing support
- JSON output

### API Potential
- Can be wrapped in FastAPI
- RESTful endpoints
- Async processing
- Webhook notifications

## Future Enhancements

1. **Image Generation**: Integrate DALL-E or Stable Diffusion
2. **3D Visualization**: VR/AR exhibition walkthroughs
3. **Multi-language**: Support for multiple languages
4. **Collaborative Curation**: Multiple users editing
5. **Advanced Search**: Semantic search across exhibitions
6. **Export Formats**: PDF, HTML, PowerPoint
7. **Social Sharing**: Share exhibitions on social media
8. **Analytics**: Visitor engagement tracking
