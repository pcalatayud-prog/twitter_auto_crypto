# Documentation

This folder contains documentation for the Bitcoin Twitter Bot project.

## Contents

- `workflow.drawio` - Workflow diagram showing the application's process flow

## Viewing the Workflow Diagram

The workflow diagram is created using draw.io (diagrams.net). You can view and edit this file in the following ways:

1. Online at [diagrams.net](https://app.diagrams.net/) - Use the "Open Existing Diagram" option and upload the workflow.drawio file
2. Desktop app - Download the [diagrams.net desktop application](https://github.com/jgraph/drawio-desktop/releases) and open the file
3. VS Code extension - Install the [Draw.io Integration extension](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) for VS Code

## Workflow Description

The diagram illustrates the core workflow of the Bitcoin Twitter Bot:

1. Application starts and initializes the Twitter client
2. CryptoTracker is initialized to track Bitcoin data
3. A random message type is selected (standard or detailed)
4. Bitcoin data is fetched from CoinMarketCap and Yahoo Finance
5. The appropriate report is generated based on the selected message type
6. The tweet is posted to Twitter
7. The application ends

The diagram also shows the external API dependencies:
- CoinMarketCap API for current price and metrics
- Yahoo Finance API for historical data
- Twitter API for posting tweets