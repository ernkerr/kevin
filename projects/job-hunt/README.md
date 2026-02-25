# Job Hunt Project

This project contains the structure and docs for the Job Hunt sub-agent suite (Research Scout, Assessment Coach, Tutor, and Mock Interview Conductor).

## Vault
- Obsidian vault: `obsidian/Job Hunt Second Brain`
  - `Research/`: interview market research
  - `Skills/`: personal skill inventory + knowledge gaps
  - `Interview Logs/`: transcripts, Whisper summaries, takeaways
  - `Projects/`: practice builds, repo references, idea lists
  - `Meta/`: operating docs, agent configs, templates

## Agents
1. Research Scout — small model with web access for startup interview trends
2. Assessment Coach — higher-intelligence model for contextual correction and gap tracking
3. Tutor — project-based learning coach tied to real repos
4. Mock Interview Conductor — async interview drills + retention checks

## Next Steps
- Add Obsidian note templates (Research report, Skill entry, Interview log, Project brief)
- Define shared state files for agents (JSON/YAML)
- Spawn agents via sessions once configs are ready
