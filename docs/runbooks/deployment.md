# Deployment Runbook

## Prerequisites
- kubectl access
- Helm installed
- Access to container registry

## Deployment Steps
1. Build container:
   ```bash
   docker build -t your-registry/flask-app:tag .