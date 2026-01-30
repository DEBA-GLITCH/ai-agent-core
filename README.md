# AI Agent Core

A minimal, production-style AI agent framework built from scratch without agent libraries.

This project demonstrates how to build a real AI agent with:
- Planning
- Validation
- Tool execution
- Structured tool inputs
- Execution memory

## Features
- Schema-enforced planning
- Automatic retry & correction
- Tool abstraction (calculator, file reader)
- Deterministic execution
- Short-term memory (cache-based)

## Architecture
User → Planner → Validator → Tool Executor → Memory

## Tools
- calculator: executes math expressions
- file_reader: reads local text files

## Memory
- Execution-level cache
- Prevents redundant tool calls
- Reset on each run (by design)

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
