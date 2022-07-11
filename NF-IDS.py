from model import RNN_DNN
from config import Config
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import torch
import numpy as np

config = Config()
pre_model = RNN_DNN(in_size=config.feature_size, out_size=config.out_size, n_layer=config.n_layer, hidd_size1=config.hidd_size1, hidd_size2=config.hidd_size2)
pre_model.eval()
hidden = torch.zeros(config.n_layer,1,config.hidd_size1).to(config.device)

def GetSeqPredict(f_seq):
    global hidden
    print(hidden)
    y_pred, hidden = pre_model(f_seq.float(), hidden)
    return torch.round(y_pred.view(-1)).int().tolist()

path_to_dataset = "NF-ToN-IoT.csv"
data = pd.read_csv(path_to_dataset, nrows =100)
df = pd.DataFrame(data)
features = ['IPV4_SRC_ADDR', 'L4_SRC_PORT', 'IPV4_DST_ADDR', 'L4_DST_PORT', 'PROTOCOL', 'L7_PROTO', 'IN_BYTES', 'OUT_BYTES', 'IN_PKTS', 'OUT_PKTS', 'TCP_FLAGS', 'FLOW_DURATION_MILLISECONDS', 'Label']
# Require Null pre-processing
assert df.isnull().values.any()==False
bad_ip_idx = df['IPV4_SRC_ADDR'].str.contains("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",regex=True)
bad_ip_idx = bad_ip_idx[bad_ip_idx==False].index.tolist()
df.drop(bad_ip_idx,axis=0,inplace=True)
bad_ip_idx = df['IPV4_DST_ADDR'].str.contains("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",regex=True)
bad_ip_idx = bad_ip_idx[bad_ip_idx==False].index.tolist()
df.drop(bad_ip_idx,axis=0,inplace=True)
ip2int = lambda ip: np.int64(sum([int(x) << 8*i for i,x in enumerate(reversed(ip.split('.')))]))
df["IPV4_SRC_ADDR"] = df["IPV4_SRC_ADDR"].transform(ip2int)
df["IPV4_DST_ADDR"] = df["IPV4_DST_ADDR"].transform(ip2int)
#df = df.drop(['IPV4_SRC_ADDR', 'IPV4_DST_ADDR', 'Attack'],axis=1)
df = df[features]
scaler = MinMaxScaler()
df = scaler.fit_transform(df)
x = torch.from_numpy((df[:,:-1].astype(np.float64)))
n_samples = x.shape[0]
x = torch.reshape(x[:-(n_samples%config.seq_length)], (-1, config.seq_length, config.feature_size))
print(GetSeqPredict(x[:64]))