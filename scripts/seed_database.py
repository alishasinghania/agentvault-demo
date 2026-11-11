#!/usr/bin/env python3
"""Create ./data/meridian.db with sample Meridian Corp tables."""

import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.config import DATABASE_PATH


def main():
    os.makedirs(os.path.dirname(os.path.abspath(DATABASE_PATH)) or ".", exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            department TEXT,
            salary INTEGER,
            hire_date TEXT
        );
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            name TEXT,
            budget INTEGER,
            lead_id INTEGER,
            status TEXT
        );
        CREATE TABLE IF NOT EXISTS assignments (
            employee_id INTEGER,
            project_id INTEGER,
            role TEXT
        );
        DELETE FROM employees;
        DELETE FROM projects;
        DELETE FROM assignments;
        INSERT INTO employees VALUES
            (1, 'Ada Lovelace', 'ada@meridian.com', 'Engineering', 180000, '2020-01-15'),
            (2, 'Grace Hopper', 'grace@meridian.com', 'Engineering', 175000, '2019-06-01'),
            (3, 'Alan Turing', 'alan@meridian.com', 'Research', 190000, '2021-03-20'),
            (4, 'Katherine Johnson', 'kathy@meridian.com', 'HR', 120000, '2018-11-02');
        INSERT INTO projects VALUES
            (1, 'AgentVault', 500000, 1, 'active'),
            (2, 'Apollo', 250000, 2, 'active');
        INSERT INTO assignments VALUES
            (1, 1, 'lead'),
            (2, 1, 'engineer'),
            (3, 2, 'researcher');
        """
    )
    conn.commit()
    conn.close()
    print(f"Seeded database at {DATABASE_PATH}")


if __name__ == "__main__":
    main()
