IHLP Term Project <br/>
**Topic: Federated Learning System for Distributed AI/ML model training** <br/><br/>

**File Structure**:<br/><br/>
FederatedLearningSys/<br/>
|-- client/<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- client1.py<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- client2.py<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- client3.py<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- houston-weather.csv<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- michigan-weather.csv<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- seattle-weather.csv<br/>
|-- k8s/<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- nodePort.yaml<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- sev.yaml<br/>
|-- server/<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- Dockerfile<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- requirements.txt<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-- server.py<br/>
|-- .gitignore<br/>
|-- README.md<br/>

<br/>
Since our objective was to build a higly scalable Federated Learning System, we have taken the Dockerization approach. By creating a Docker container of our server, we can implmenet the server-side code on Kubernetes Engine, and configure the Kubernetes Engine to manage the scaling of the server in response to increasing or decreasing requests from the client.
<br/><br/>

**Steps to run the server using Kubernetes**: <br/>
- Make sure your system/server has following softwares installed:
  - Docker
  - Kubernetes
  - kubectl (command line tool for managing Kubernetes)<br/>
- Step 1:
  - RUN "kubectl apply -f k8s/sev.yaml"
  - RUN "kubectl apply -f k8s/nodePort.yaml"
- Step 2:
  - Connect the server on localhost:
    - http://localhost:30001/get_model
    - http://localhost:30001/submit_updates
    - http://localhost:30001/aggregate
  - Connect the server with IP Address/DNS:
    - http://<your-dns>:30001/get_model
    - http://<your-dns>:30001/submit_updates
    - http://<your-dns>:30001/aggregate
<br/><br/>

**Steps to run the server on your local system**: <br/>
- Make sure your system/server has following softwares installed:
  - Python
<br/>
- Step 1:
  - RUN "pip install -r server/requirements.txt"
  - RUN "python server/server.py"
- Step 2:
  - Connect the server on localhost:
    - http://localhost:30001/get_model
    - http://localhost:30001/submit_updates
    - http://localhost:30001/aggregate
  - Connect the server with IP Address/DNS:
    - http://<your-dns>:30001/get_model
    - http://<your-dns>:30001/submit_updates
    - http://<your-dns>:30001/aggregate