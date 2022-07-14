# NF_IDS Deployment
## Setup
- Setup virtual environment
```
vscode@Ubuntu:~/project/flow-based-IDS$ pip -m venv .env
vscode@Ubuntu:~/project/flow-based-IDS$ source .env/bin/activate
(.env) vscode@Ubuntu:~/project/flow-based-IDS$
```
- Install requirement
```
(.env) vscode@Ubuntu:~/project/flow-based-IDS$ pip install torch==1.5.1+cpu torchvision==0.6.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
(.env) vscode@Ubuntu:~/project/flow-based-IDS$ pip install -r requirements.txt
```
## Deploy NF_IDS server

```
(.env) vscode@Ubuntu:~/project/flow-based-IDS$ export FLASK_APP=main.py
(.env) vscode@Ubuntu:~/project/flow-based-IDS$ flask run
```
## Example query
- Request

```
(.env) vscode@Ubuntu:~/project/flow-based-IDS$ curl -X POST http://127.0.0.1:5000/predict -H 'Content-Type: application/json' -d '{"destination_ipv4_prefix_length": 0,"source_ipv4_prefix_length": 0,"protocol_identifier": 1,"packet_delta_count": 1,"octet_delta_count": 98,"tcp_control_bits": 0,"destination_ipv4_address":"10.0.0.4","source_ipv4_address":"10.0.0.1","destination_transport_port": 0,"source_transport_port": 0,"flow_duration_milliseconds": 10,"post_packet_delta_count": 10,"post_octet_delta_count": 10,"ixia_l7_app_id": 0}'
```
- Response
```
{
  "predict0": 0.13789403438568115
}
```