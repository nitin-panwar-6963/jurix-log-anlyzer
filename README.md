<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=250&color=0:0f172a,100:06b6d4&text=JurixAI%20SRE%20Kernel%20v2.0&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=40"/>

<h3>🛡️ AI-Powered Incident Response & Self-Triage CI/CD Intelligence Platform</h3>

<p>
Transforming Jenkins Failures into AI-Generated Root Cause Analysis, Automated Incident Reports, and Instant Remediation Playbooks.
</p>

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=22&duration=3500&pause=1000&color=00D9FF&center=true&vCenter=true&width=900&lines=AI-Powered+Root+Cause+Analysis;Automated+Incident+Response;Jenkins+Failure+Detection;Kubernetes+Native+Deployment;Enterprise+AIOps+Platform" />

<br>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge\&logo=flask)
![Jenkins](https://img.shields.io/badge/Jenkins-CI/CD-D24939?style=for-the-badge\&logo=jenkins\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?style=for-the-badge\&logo=kubernetes\&logoColor=white)
![Gemini](https://img.shields.io/badge/Google-Gemini_AI-4285F4?style=for-the-badge\&logo=google)
![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)

</div>

---

# 🚀 Overview

**JurixAI SRE Kernel v2.0** is an AI-driven AIOps and Site Reliability Engineering platform designed to automate incident triage, root cause analysis, reporting, and alerting across modern CI/CD environments.

Instead of manually analyzing thousands of lines of Jenkins console output, JurixAI automatically:

✅ Captures pipeline failures
✅ Sends logs through a secure webhook gateway
✅ Generates AI-powered Root Cause Analysis (RCA)
✅ Creates enterprise-grade PDF reports
✅ Delivers remediation guidance to stakeholders

---

# ⚡ Execution Pipeline

```text
🚨 Jenkins Pipeline Failure
            │
            ▼
📡 Bash Log Collector
            │
            ▼
🌐 Flask Webhook Gateway
            │
            ▼
🤖 Google Gemini AI Engine
            │
            ▼
🔍 Root Cause Analysis
            │
            ▼
📄 Automated PDF Report
            │
            ▼
📧 SMTP Notification Service
            │
            ▼
🛡️ SRE Team Response
```

---

# 🎯 Key Features

### 🤖 AI-Powered Root Cause Analysis

Utilizes Google Gemini AI to identify deployment, infrastructure, networking, and application failures.

### 📄 Automated Incident Reporting

Generates structured PDF reports containing RCA findings and remediation steps.

### 🚨 Real-Time Failure Detection

Captures Jenkins failures directly through native webhook integration.

### 📧 Intelligent Notification Engine

Sends detailed email alerts with attached reports to stakeholders.

### ☸️ Kubernetes Native

Built for containerized deployments using Docker and Kubernetes.

### 🔒 Secure Secret Management

Sensitive credentials are isolated through Kubernetes Secrets.

---

# 🏗️ Architecture

```text
                  Jenkins Pipeline
                         │
                         ▼
                 Failure Detection
                         │
                         ▼
                 Webhook Gateway
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
 Google Gemini AI                 PDF Generator
        │                                 │
        └────────────────┬────────────────┘
                         ▼
                 SMTP Alert Engine
                         │
                         ▼
                    Admin Inbox
```

---

# 📂 Project Structure

```bash
JurixAI-SRE-Kernel/
│
├── k8s/
│   ├── Namespace.yml
│   ├── Secret.yml
│   ├── deployment.yml
│   ├── Service.yml
│   └── ingress.yml
│
├── templates/
│   └── index.html
│
├── static/
│   └── css/
│       └── style.css
│
├── app.py
├── Dockerfile
├── requirements.txt
└── Jenkinsfile
```

---

# 🛠️ Technology Stack

| Layer         | Technology        |
| ------------- | ----------------- |
| Backend       | Python, Flask     |
| AI Engine     | Google Gemini API |
| CI/CD         | Jenkins           |
| Containers    | Docker            |
| Orchestration | Kubernetes (Kind) |
| Reporting     | ReportLab         |
| Notifications | SMTP              |
| Frontend      | HTML, CSS         |

---

# ☸️ Kubernetes Deployment

```bash
# Create Cluster
kind create cluster --name jurixai-cluster

# Create Namespace
kubectl apply -f k8s/Namespace.yml

# Create Secrets
kubectl apply -f k8s/Secret.yml

# Deploy Application
kubectl apply -f k8s/deployment.yml

# Expose Service
kubectl apply -f k8s/Service.yml

# Verify
kubectl get all -n jurixai-sre
```

---

# 🚨 Jenkins Integration

The included Jenkinsfile automatically executes a failure hook whenever the pipeline enters a failed state.

```groovy
post {
    failure {
        // Capture Logs
        // Send Webhook
        // Generate RCA
        // Dispatch Alert
    }
}
```

---

# 👨‍💻 Team Syntax Squad

### 🛡️ Nitin Panwar

Project Lead & System Infrastructure Architect

### 📑 Gunjan Kumari

Documentation & Presentation Lead

### 🎤 Ditya

Pitch & Communication Specialist

### ⚙️ Tushar Singh

Backend Support Engineer

---

<div align="center">

## 🌟 From Failure Detection to Automated Resolution

### Built by Developers. Designed for Reliability.

⭐ Star the repository if you found this project useful.

</div>
