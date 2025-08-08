# Infrastructure

This folder contains the main infrastructure elements of the project.

## Set up
1. Enable all the needed apis: cloud run, cloud build, artifact registry etc.
2. Set-up CI/CD using github actions
  1. Create a cicd service account with the following rights:
    - Artifact Registry Admin
    - Cloud Run Invoker
    - WIF user
    - Token creator
  2. Set-up Workload Identity Federation - used for sa impersonation runs from actions
    - Enable the api if need
    - Follow the steps in the interface for creating a pool and a provider
    - For GitHub specifically, add in prover assertion: assertions.repository and cell condition to your repo name <user>/<repo>
  3. Grant access using your pre-created service account to this workpool setting again the repository name assertion
  4. Add workload and sa address to your repo actions secrets


## Deployment files
Add a tree here
