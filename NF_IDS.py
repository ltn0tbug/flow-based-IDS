from model import RNN_DNN
from config import Config, v92ipfix, features, fea2sca
import numpy as np
import json
import pandas as pd
import torch

config = Config()
pre_model = RNN_DNN(config.model_config)

checkpoint = torch.load(config.root_checkpoint_dir + f"{config.version}.pt", map_location=config.device)
pre_model.load_state_dict(checkpoint['model_state_dict'])

pre_model.eval()
hidden = torch.zeros(config.model_config.n_layer,1,config.model_config.hidd_size1).to(config.device)

def GetSeqPredict(f_seq):
    global hidden
    y_pred, hidden = pre_model(f_seq.float(), hidden)
    return y_pred.view(-1).tolist()

def Json2Tensor(js2j):

    feature_map = [{feature:j[v92ipfix[feature]] for feature in features} for j in js2j]

    df = pd.DataFrame.from_records(feature_map)

    # Require Null pre-processing
    assert df.isnull().values.any()==False
    bad_ip_idx = df['IPV4_SRC_ADDR'].str.contains("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",regex=True)
    bad_ip_idx = bad_ip_idx[bad_ip_idx==False].index.tolist()
    df.drop(bad_ip_idx,axis=0,inplace=True)
    bad_ip_idx = df['IPV4_DST_ADDR'].str.contains("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",regex=True)
    bad_ip_idx = bad_ip_idx[bad_ip_idx==False].index.tolist()
    df.drop(bad_ip_idx,axis=0,inplace=True)

    for feature in features:
      df[feature] = df[feature].transform(fea2sca[feature])

    return torch.from_numpy(df.to_numpy(dtype=np.float64)).view(1,-1,len(features))


def GetPredict(raw_data):
    js2j = raw_data
    if isinstance(js2j, str):
        js2j = json.loads(js2j)
    
    in_tensor = None
    if isinstance(js2j, list):
        in_tensor = Json2Tensor(js2j)
    elif isinstance(js2j, dict):
        in_tensor = Json2Tensor([js2j])
    else:
        raise Exception("Invalid data")
    
    predict = GetSeqPredict(in_tensor)
    return predict

if __name__ == '__main__':
    data = """{
      "destination_ipv4_prefix_length": 0,
      "source_ipv4_prefix_length": 0,
      "protocol_identifier": 1,
      "packet_delta_count": 1,
      "bgp_destination_as_number": 0,
      "flow_start_sys_up_time": 18374487,
      "egress_interface": 8189,
      "octet_delta_count": 98,
      "type": "netflow_flow",
      "bgp_source_as_number": 0,
      "ip_next_hop_ipv4_address": "0.0.0.0",
      "destination_ipv4_address": "10.0.0.4",
      "source_ipv4_address": "10.0.0.1",
      "exporter": {
        "uptime_millis": 18375492,
        "engine_type": 15,
        "address": "192.168.142.138:34700",
        "engine_id": 15,
        "version": 5,
        "sampling_interval": 0,
        "timestamp": "2022-07-08T07:55:39.666Z"
      },
      "tcp_control_bits": 0,
      "ip_class_of_service": 0,
      "ingress_interface": 7682,
      "flow_end_sys_up_time": 18374487,
      "destination_transport_port": 0,
      "source_transport_port": 0,
      "flow_duration_milliseconds": 10,
      "post_packet_delta_count": 10,
      "post_octet_delta_count": 10,
      "ixia_l7_app_id": 0
    }
"""
    print(GetPredict(data))
