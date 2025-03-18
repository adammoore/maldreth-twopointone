-- MaLDReTH Database Schema
-- This schema defines the structure for the SQLite database used by the MaLDReTH application.

-- Drop existing tables if they exist
DROP TABLE IF EXISTS tools;
DROP TABLE IF EXISTS tool_categories;
DROP TABLE IF EXISTS connections;
DROP TABLE IF EXISTS stages;

-- Create stages table for research data lifecycle stages
CREATE TABLE stages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    order_index INTEGER NOT NULL
);

-- Create tool_categories table for categorizing tools within each stage
CREATE TABLE tool_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stage_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (stage_id) REFERENCES stages (id) ON DELETE CASCADE
);

-- Create tools table for individual research tools
CREATE TABLE tools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    url TEXT,
    source TEXT, -- 'open' or 'closed'
    interoperable BOOLEAN DEFAULT 0,
    scope TEXT, -- 'Generic' or 'Disciplinary'
    FOREIGN KEY (category_id) REFERENCES tool_categories (id) ON DELETE CASCADE
);

-- Create connections table for relationships between stages
CREATE TABLE connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_stage_id INTEGER NOT NULL,
    to_stage_id INTEGER NOT NULL,
    connection_type TEXT NOT NULL, -- 'normal' or 'alternative'
    FOREIGN KEY (from_stage_id) REFERENCES stages (id) ON DELETE CASCADE,
    FOREIGN KEY (to_stage_id) REFERENCES stages (id) ON DELETE CASCADE
);

-- Initial data for stages
INSERT INTO stages (name, description, order_index) VALUES 
('Conceptualise', 'To formulate the initial research idea or hypothesis, and define the scope of the research project and the data component/requirements of that project.', 1),
('Plan', 'To establish a structured strategic framework for management of the research project, outlining aims, objectives, methodologies, and resources required for data collection, management and analysis.', 2),
('Fund', 'To identify and acquire financial resources to support the research project, including data collection, management, analysis, sharing, publishing and preservation.', 3),
('Collect', 'To use predefined procedures, methodologies and instruments to acquire and store data that is reliable, fit for purpose and of sufficient quality to test the research hypothesis.', 4),
('Process', 'To make new and existing data analysis-ready. This may involve standardised pre-processing, cleaning, reformatting, structuring, filtering, and performing quality control checks on data.', 5),
('Analyse', 'To derive insights, knowledge, and understanding from processed data.', 6),
('Store', 'To record data using technological media appropriate for processing and analysis whilst maintaining data integrity and security.', 7),
('Publish', 'To release research data in published form for use by others with appropriate metadata for citation.', 8),
('Preserve', 'To ensure the safety, integrity, and accessibility of data for as long as necessary.', 9),
('Share', 'To make data available and accessible to humans and/or machines.', 10),
('Access', 'To control and manage data access by designated users and reusers.', 11),
('Transform', 'To create new data from the original, for example by migration into a different format or by creating a subset.', 12);

-- Initial connections between stages
INSERT INTO connections (from_stage_id, to_stage_id, connection_type) VALUES 
(1, 2, 'normal'),  -- Conceptualise -> Plan
(2, 4, 'normal'),  -- Plan -> Collect
(4, 5, 'normal'),  -- Collect -> Process
(5, 6, 'normal'),  -- Process -> Analyse
(6, 7, 'normal'),  -- Analyse -> Store
(7, 8, 'normal'),  -- Store -> Publish
(8, 9, 'normal'),  -- Publish -> Preserve
(9, 10, 'normal'), -- Preserve -> Share
(10, 11, 'normal'), -- Share -> Access
(11, 12, 'normal'), -- Access -> Transform
(12, 1, 'normal'); -- Transform -> Conceptualise

-- Alternative connections
INSERT INTO connections (from_stage_id, to_stage_id, connection_type) VALUES 
(6, 4, 'alternative'),  -- Analyse -> Collect
(5, 4, 'alternative'),  -- Process -> Collect
(7, 5, 'alternative');  -- Store -> Process

-- Initial tool categories for Conceptualise stage
INSERT INTO tool_categories (stage_id, name, description) VALUES
(1, 'Mind mapping, concept mapping and knowledge modelling', 'Tools that define the entities of research and their relationships'),
(1, 'Diagramming and flowchart', 'Tools that detail the research workflow'),
(1, 'Wireframing and prototyping', 'Tools that visualise and demonstate the research workflow');

-- Initial tool categories for Plan stage
INSERT INTO tool_categories (stage_id, name, description) VALUES
(2, 'Data management planning (DMP)', 'Tools focused on enabling preparation and submission of data management plans'),
(2, 'Project planning', 'Tools designed to enable project planning'),
(2, 'Combined DMP/project', 'Tools which combine project planning with the ability to prepare data management plans');

-- Initial tool categories for Collect stage
INSERT INTO tool_categories (stage_id, name, description) VALUES
(4, 'Quantitative data collection tool', 'Tools that collect quantitative data'),
(4, 'Qualitative data collection (e.g. Survey tool)', 'Tools that collect qualitative data'),
(4, 'Harvesting tool (e.g. WebScrapers)', 'Tools that harvest data from various sources');

-- Initial tools for Conceptualise stage
INSERT INTO tools (category_id, name, description, url, source, interoperable, scope) VALUES
(1, 'Miro', 'Collaborative online whiteboard platform', 'https://miro.com', 'closed', 1, 'Generic'),
(1, 'Meister Labs', 'Mind mapping and task management', 'https://www.meisterlabs.com', 'closed', 1, 'Generic'),
(1, 'XMind', 'Mind mapping and brainstorming tool', 'https://www.xmind.net', 'closed', 1, 'Generic'),
(2, 'Lucidchart', 'Diagramming and visualization tool', 'https://www.lucidchart.com', 'closed', 1, 'Generic'),
(2, 'Draw.io', 'Free online diagram software', 'https://www.diagrams.net', 'open', 1, 'Generic'),
(2, 'Creately', 'Visual collaboration tool', 'https://creately.com', 'closed', 1, 'Generic'),
(3, 'Balsamiq', 'Rapid wireframing tool', 'https://balsamiq.com', 'closed', 1, 'Generic'),
(3, 'Figma', 'Collaborative interface design tool', 'https://www.figma.com', 'closed', 1, 'Generic');

-- Initial tools for Plan stage
INSERT INTO tools (category_id, name, description, url, source, interoperable, scope) VALUES
(4, 'DMP Tool', 'Data management planning tool', 'https://dmptool.org', 'open', 1, 'Generic'),
(4, 'DMP Online', 'Online data management planning tool', 'https://dmponline.dcc.ac.uk', 'open', 1, 'Generic'),
(4, 'RDMO', 'Research Data Management Organiser', 'https://rdmorganiser.github.io', 'open', 1, 'Generic'),
(5, 'Trello', 'List-making application for project management', 'https://trello.com', 'closed', 1, 'Generic'),
(5, 'Asana', 'Work management platform', 'https://asana.com', 'closed', 1, 'Generic'),
(5, 'Microsoft Project', 'Project management software', 'https://www.microsoft.com/en-us/microsoft-365/project/project-management-software', 'closed', 1, 'Generic'),
(6, 'Data Stewardship Wizard', 'Smart data management planning tool', 'https://ds-wizard.org', 'open', 1, 'Generic'),
(6, 'Redbox Research Data', 'Research data management platform', 'https://www.redboxresearchdata.com.au', 'open', 1, 'Generic'),
(6, 'Argos', 'Research data management tool', 'https://argos.openaire.eu', 'open', 1, 'Generic');
