# ZVM Auditor

ZVM Auditor is a template designed to emit audit-level logs from the Zerto ZVM API. It captures tasks and events from the Zerto Virtual Manager (ZVM) and forwards them to other systems for further analysis, monitoring, and compliance purposes.

This is just a template, by default it just sends the logs to the python logging interface. But if you want to send them to another system like splunk or datadog or elasticsearch you could use this as a starting point.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Features

- **Real-time Audit Logs**: Capture and forward tasks and events from the Zerto ZVM on a configurable interval
- **Flexible Integration**: Add integrations to whatever 3rd party system you need
- **Configurable**: Customize the log output and destinations to suit your environment.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/zvm-auditor.git
    ```
2. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Edit `zvm_auditor.py` to match your ZVM API and destination systems.

## Usage

Run the auditor with the following command:

```bash
python zvm_auditor.py

## License

This project is licensed under the GNU General Public License v3.0.

zvm-auditor - Emitter template for ZVM audit logs
Copyright (C) 2024 Justin Paul

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
