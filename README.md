# Investnest

InvestNest is a full-stack web application designed to help users manage their investment portfolios. The application allows users to create, manage, and track their investment portfolios while providing real-time data integration, user-friendly reports, and robust authentication mechanisms.

# Table of Contents

# Description

InvestNest is a comprehensive investment portfolio management system that provides users with the tools to monitor and manage their investments. It integrates with real-time market data sources to keep portfolio values updated and includes powerful reporting and analytics features.

# User Experience

InvestNest is built with user experience at its core, providing intuitive navigation, clear feedback, and robust security features. Users can easily manage their portfolios, view detailed performance metrics, and customize their experience with personalized settings.

# Agile Methodology and Planning

## Epics

A total of 6 epics were designed for the project, with the project delivery focused on Epic 3. Each of Epics 1, 2, and 3 was executed in individual sprints. Epics 4, 5, and 6 are not planned for execution at this stage and are considered future expansions.

### Epic 1: Project Setup and Initial Configuration

#### User Stories

### Epic 2: User Authentication and Authorization

#### User Stories

### Epic 3: Portfolio Management (Project Delivery)

#### User Stories

### Epic 4: Real-Time Data Integration

#### User Stories

### Epic 5: Reporting and Analytics

#### User Stories

### Epic 6: User Notifications

#### User Stories

## MoSCoW Methodology

The first three epics and their stories are essential for the project delivery, providing all necessary features and expected standards. Therefore, most of these tasks are classified as 'Must Have' or 'Should Have.'

User stories are broken down into tasks, where each task is categorized as 'Must Have,' 'Should Have,' 'Could Have,' or 'Won’t Have.' Each task is also assigned a story point weight of 1, 2, or 4, reflecting the effort required to complete it.

The story point weight and MoSCoW priority of each task for the three sprints (Epics 1, 2, and 3) were carefully planned to allow flexibility in execution. 'Must Haves' do not exceed 60% of the sprint's total story points. The details for each sprint are provided below:

### Sprint/Epic 1

**Story Point / MoSCoW** | **Must Have** | **Should Have** | **Could Have**
:-----:|:-----:|:-----:|:-----:
**1** | 10 | 0 | 0
**2** | 10 | 4 | 0
**4** | 1 | 2 | 2
**Total** | 34 | 16 | 8

- Total story points: 58
- Total 'Must Have': 34
- Must Have proportion: 58.62%

[Sprint 1 story point weight graph](https://github.com/users/catapam/projects/2/insights/4)

### Sprint/Epic 2

**Story Point / MoSCoW** | **Must Have** | **Should Have** | **Could Have**
:-----:|:-----:|:-----:|:-----:
**1** | 4 | 3 | 0
**2** | 9 | 5 | 7
**4** | 0 | 0 | 2
**Total** | 22 | 13 | 22

- Total story points: 57
- Total 'Must Have': 22
- Must Have proportion: 38.59%

[Sprint 2 story point weight graph](https://github.com/users/catapam/projects/2/insights/5)

### Sprint/Epic 3

**Story Point / MoSCoW** | **Must Have** | **Should Have** | **Could Have**
:-----:|:-----:|:-----:|:-----:
**1** | 4 | 1 | 0
**2** | 12 | 6 | 9
**4** | 1 | 1 | 4
**Total** | 32 | 17 | 34

- Total story points: 83
- Total 'Must Have': 32
- Must Have proportion: 38.55%

[Sprint 3 story point weight graph](https://github.com/users/catapam/projects/2/insights/6)

## Sprint Length

Based on the total story points, Sprints 1 and 2 were set to last 2 weeks each, while Sprint 3 was extended by an additional week, making it 3 weeks long.

## Reviews

Tasks and tickets were reviewed weekly. New tickets, such as bug reports, were incorporated into the planning, which sometimes resulted in the removal of tasks from sprints or adjustments to their MoSCoW priorities.

# Design

InvestNest's design prioritizes a clean, user-friendly interface that supports easy navigation and data visibility. The application is structured to guide users through their investment management journey, offering clear and concise feedback at every step.

Key design principles include:
- **User-Centric Design**: Ensures that the application is intuitive and easy to use.
- **Responsive Design**: The application is fully responsive and works seamlessly across different devices.
- **Security**: Emphasis on robust security measures, including secure authentication and role-based access control.

## Color scheme

## Typography

## Wireframes

# Features

## Existing Features

* **Portfolio Management**: Allows users to create, update, and delete portfolios and assets, with real-time data updates.
* **Real-Time Data Integration**: Fetches and displays up-to-date market prices for all assets in a user’s portfolio.
* **User Authentication and Authorization**: Secure login, registration, and role-based access control.
* **Reporting and Analytics**: Detailed performance metrics and visualizations to help users track their investments.

## Future Features

* **Advanced Analytics**: Introduce more advanced analytics, such as risk assessments and forecasting tools.
* **Automated Alerts**: Implement automated alerts for significant portfolio changes.
* **Portfolio Sharing**: Allow users to share their portfolios with others securely.
* **Multi-Currency Support**: Enable tracking and reporting of investments in multiple currencies.

# How to Use

1. **Register/Login**: Users must register or log in to manage their portfolios.
2. **Create Portfolio**: After logging in, users can create a new investment portfolio.
3. **Add Assets**: Users can add various assets (stocks, bonds, etc.) to their portfolios.
4. **Monitor Performance**: View the portfolio dashboard to monitor investment performance.
5. **Manage Settings**: Customize user settings and notifications from the profile section.

# Technology Used

## Languages

* Python
* Django
* Sql
* HTML
* CSS
* JavaScript

## Frameworks, Libraries, and Tools

* **Django**: The main web framework used for building the application.
* **PostgreSQL**: The relational database used to store user and portfolio data.
* **Bootstrap**: For responsive design and styling.
* **Chart.js**: For data visualizations in the performance dashboard.
* **Heroku**: For application deployment.
* **Git**: For version control.

# Deployment

To deploy the application on Heroku:

1. Visit the Heroku website, log in, or create a new account.
2. On the dashboard, click "New" and select "Create new app."
3. Enter a unique app name and choose a region.
4. Click "Create app."
5. Navigate to the "Settings" tab and find "Config Vars."
6. Click "Reveal Config Vars," add "PORT" as a key with the value "8000," and click "Add."
7. Scroll down to the "Buildpacks" section, click "Add buildpack," and select "Python."
8. Repeat step 7 to add "Node.js," ensuring "Python" is listed first.
9. Scroll to the top and select the "Deploy" tab.
10. Choose GitHub as the deployment method, then search for your repository and click "Connect."
11. Scroll down and either "Enable Automatic Deploys" to update the code each time it is pushed to GitHub, or choose "Manual Deploy" for manual updates.

# Testing

## Automated testing

## Manual testing

# Bugs

# Future optimizations

# Credits

## Code

## Content

# Acknowledgements