## Getting Started

Follow these steps to get started with the project.

### Prerequisites

Make sure you have Python and pip installed on your system. You can check if they are installed by running the following commands:

```bash
python --version
pip --version
```

If they are not installed, you can download Python from the official Python website, and pip is usually installed automatically along with Python.

### Installation
First, make sure the requirements are installed. To do this, run:

```bash
pip install -r requirements.txt
```

### Running the Application
Once the requirements are installed, you can start the application using uvicorn. Run the following command
```bash
uvicorn app:app --host 0.0.0.0
```

This will start the application and it will be available at http://localhost:8000 or at the address you specify in the host and port.