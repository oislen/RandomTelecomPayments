
**Table of Contents**

- [New Hire Tasks](#new-hire-tasks)
  - [0. Onboarding](#0-onboarding)
  - [1. Feature Engineering](#1-feature-engineering)
  - [2. Network Analysis](#2-network-analysis)
  - [3. Anomaly Detection](#3-anomaly-detection)
  - [4. Predictive Modelling](#4-predictive-modelling)

# New Hire Tasks

## 0. Onboarding

Before starting the tasks below, review the following documentation to understand the project structure, data model, and development workflow:

* [`CLAUDE.md`](../CLAUDE.md) — full project overview, repository structure, development setup, running instructions, coding conventions, and common agent tasks
* [`README.md`](../README.md) — public-facing project documentation
* [`doc/data_dictionary.csv`](data_dictionary.csv) — column-level descriptions for the generated dataset
* [`doc/entity_relationship_diagram.jpg`](entity_relationship_diagram.jpg) — visual data model

## 1. Feature Engineering

Engineer features / attributes for modelling and reporting purposes. The features should be representative of the relationships between users, devices, ips, cards and transactions.

## 2. Network Analysis

Create device, ip and card networks to identify users groups / clusters.

## 3. Anomaly Detection

Using the engineered features from 1. and the user networks from 2. create an anomaly detection system to identify abnormal customer behaviour.

## 4. Predictive Modelling

Using the engineered features from 1. and the user networks from 2. create a model to classify fraudulent users.