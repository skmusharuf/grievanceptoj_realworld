#!/usr/bin/env python
"""
GrievanceHub - Complete Application Entry Point
Runs both Flask Backend and Frontend Server
Usage: python run.py
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def get_project_root():
    """Get the root directory of the project"""
    return Path(__file__).parent

def run_backend():
    """Start Flask backend"""
    print("\n" + "="*60)
    print("Starting Flask Backend Server...")
    print("="*60)
    
    backend_dir = get_project_root() / "backend"
    
    # Check if backend directory exists
    if not backend_dir.exists():
        print(f"ERROR: Backend directory not found at {backend_dir}")
        return None
    
    # Create virtual environment if it doesn't exist
    venv_path = backend_dir / "venv"
    if not venv_path.exists():
        print(f"Creating virtual environment at {venv_path}...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    
    # Determine python executable in venv
    if sys.platform == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    # Install requirements
    requirements_file = backend_dir / "requirements.txt"
    if requirements_file.exists():
        print(f"Installing backend dependencies...")
        subprocess.run([str(python_exe), "-m", "pip", "install", "-q", "-r", str(requirements_file)], check=False)
    
    # Run the backend
    run_py = backend_dir / "run.py"
    if not run_py.exists():
        print(f"ERROR: Backend run.py not found at {run_py}")
        return None
    
    # Start backend in a subprocess
    backend_process = subprocess.Popen(
        [str(python_exe), str(run_py)],
        cwd=str(backend_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print(f"Backend process started (PID: {backend_process.pid})")
    print("Backend running at http://localhost:5000")
    
    return backend_process

def run_frontend():
    """Start Frontend server"""
    print("\n" + "="*60)
    print("Starting Frontend Server...")
    print("="*60)
    
    frontend_dir = get_project_root() / "frontend"
    
    if not frontend_dir.exists():
        print(f"ERROR: Frontend directory not found at {frontend_dir}")
        return None
    
    # Wait a bit for backend to start
    time.sleep(2)
    
    # Start frontend server (using Python's http.server)
    if sys.platform == "win32":
        # Windows
        frontend_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8000", "--directory", str(frontend_dir)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    else:
        # Unix/Linux/Mac
        frontend_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8000", "--directory", str(frontend_dir)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
    print(f"Frontend process started (PID: {frontend_process.pid})")
    print("Frontend running at http://localhost:8000")
    
    return frontend_process

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║          GRIEVANCEHUB - COMPLETE APPLICATION              ║")
    print("║                                                           ║")
    print("║  Backend (Flask + SQLAlchemy):  http://localhost:5000    ║")
    print("║  Frontend (Vanilla HTML/CSS):   http://localhost:8000    ║")
    print("║                                                           ║")
    print("║  Press CTRL+C to stop the server                          ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print("="*60 + "\n")

def main():
    """Main entry point"""
    print_banner()
    
    # Start backend
    backend_process = run_backend()
    if not backend_process:
        print("ERROR: Could not start backend. Please check your setup.")
        sys.exit(1)
    
    # Start frontend
    frontend_process = run_frontend()
    if not frontend_process:
        print("ERROR: Could not start frontend.")
        backend_process.terminate()
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✓ Both servers are running!")
    print("="*60)
    print("\nOpening browser in 3 seconds...")
    time.sleep(3)
    
    try:
        webbrowser.open('http://localhost:8000')
    except:
        print("Could not open browser automatically.")
    
    print("\n" + "="*60)
    print("APPLICATION READY")
    print("="*60)
    print("\nAccess the application at: http://localhost:8000")
    print("API available at: http://localhost:5000/api")
    print("\nTo stop the server, press CTRL+C")
    print("="*60 + "\n")
    
    try:
        # Keep both processes running
        while True:
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("WARNING: Backend process has terminated")
            if frontend_process.poll() is not None:
                print("WARNING: Frontend process has terminated")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\nShutting down servers...")
        
        # Terminate both processes
        try:
            backend_process.terminate()
            frontend_process.terminate()
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
            frontend_process.kill()
        
        print("Servers stopped successfully.")
        print("="*60)
        sys.exit(0)

if __name__ == "__main__":
    main()
