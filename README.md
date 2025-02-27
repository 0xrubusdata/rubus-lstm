# Rubus LSTM

# ![0xRubusLstm](./public/agents/0xRubusLstm.png)

This project aims to develop an AI trading agent capable of analyzing financial assets, predicting future prices, and making informed trading decisions.

## Project Overview

The agent will use machine learning techniques, specifically Long Short-Term Memory (LSTM) networks, to analyze historical price data and technical indicators. The agent will be composed of two main components:

1.  **Data Collection and Training Agent:** Responsible for collecting data, training the LSTM model, and generating trading strategies.
2.  **Validation and Optimization Agent:** Responsible for evaluating the performance of the trained model and suggesting improvements.

## Development Plan

### Phase 1: Minimum Viable Product (MVP)

* **Objective:** Create a basic agent capable of analyzing a single cryptocurrency asset using a predefined technical pattern (e.g., Swing Failure Pattern - SFP).
* **Tasks:**
    * Set up a Python backend with an API for data access and model training.
    * Implement data collection using the CCXT library for a specific cryptocurrency exchange.
    * Develop a module to detect the SFP pattern using a chosen technical analysis library (e.g., Pandas TA).
    * Train an LSTM model to predict price movements based on the detected pattern.
    * Create a simple frontend to visualize the predicted prices and the detected pattern.
    * Implement an agent able to define cron task regarding the asset and the pattern he has to find.
    * Implement an agent able to train the LSTM model.
    * Implement vectorial memory to persist training data and results.
* **Deliverables:**
    * A functional backend API.
    * A basic frontend application.
    * A trained LSTM model for a single cryptocurrency asset and pattern.
    * One agent for data collection and training.
    * Vectorial memory functionnalities.

### Phase 2: расширение возможностей

* **Objective:** Extend the agent's capabilities to analyze multiple cryptocurrency assets and technical patterns.
* **Tasks:**
    * Refactor the code to support multiple cryptocurrency assets and exchanges.
    * Implement additional technical patterns using the chosen library or other.
    * Enhance the frontend to visualize multiple assets and patterns.
    * Implement the validation and optimization agent to evaluate and improve the model's performance.
    * Implement an agent able to validate the training and ask for training modification if needed.
* **Deliverables:**
    * An enhanced backend API supporting multiple assets and patterns.
    * An improved frontend application.
    * A more robust and accurate AI trading agent.
    * One agent for validation and optimisation.

### Phase 3: Abstraction and Optimization

* **Objective:** Improve the agent's flexibility and performance by abstracting technical analysis libraries and optimizing trading strategies.
* **Tasks:**
    * Abstract the technical analysis library to allow easy switching between libraries (e.g., TA-Lib, FinTA).
    * Implement reinforcement learning to enable the agent to create and optimize trading strategies.
    * Integrate risk management mechanisms into the agent's decision-making process.
    * Enhance the Vectorial memory to keep a track of each training and evaluation.
* **Deliverables:**
    * A highly flexible and optimized AI trading agent.
    * A comprehensive evaluation report.

## Technologies

* Python
* TensorFlow/PyTorch
* CCXT
* Pandas TA/TA-Lib/FinTA
* Vectorial Database.
* Langchain / LlamaIndex

## Getting Started

1.  Clone the repository.
2.  Install the required dependencies.
3.  Configure the API keys for the chosen cryptocurrency exchange.
4.  Run the backend API.
5.  Run the frontend application.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.
