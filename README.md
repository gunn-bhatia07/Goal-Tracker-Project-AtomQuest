# Goal Tracking System (In-House Performance Portal)

## Overview

The Goal Tracking System is a web-based application built using Streamlit, Python, and SQLite. It is designed to streamline employee goal setting, tracking, and performance evaluation within an organization. The system replaces manual tracking methods such as spreadsheets and emails with a centralized digital platform.

It supports role-based access for Employees and Managers, enabling structured goal management and quarterly performance tracking.

---

## Problem Statement

Many organizations face challenges in performance management due to:

- Lack of centralized goal tracking
- Limited visibility into employee progress
- Manual and inconsistent review processes
- Difficulty in maintaining accountability across teams

This system addresses these issues by providing a structured and transparent goal management workflow.

---

## Features

### Employee Module

- Create and manage up to 8 goals per cycle
- Define goal title, target, and weightage
- Track progress across four quarters (Q1 to Q4)
- Update status for each quarter:
  - Not Started
  - On Track
  - Completed
- View all assigned goals in a structured dashboard

---

### Manager Module

- View team members and their assigned goals
- Approve, return, or review employee goals
- Add manager comments for feedback
- Monitor team performance and progress
- View quarterly overview of team activity
- Access performance metrics and KPIs

---

### Analytics and KPIs

- Total goals per employee
- Approved and pending goals count
- Team size overview
- Approval rate across team
- Quarterly progress summary

---

### User Interface

- Clean and professional blue-themed design
- KPI dashboard cards for quick insights
- Sidebar-based authentication system
- Card-based layout for better readability
- Structured tables for performance tracking

---

## Technology Stack

- Frontend: Streamlit
- Backend: Python
- Database: SQLite
- Libraries:
  - pandas
  - streamlit

---

## Project Structure