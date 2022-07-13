import torch
import numpy as np

IP_MAX = BYTES_MAX = PKTS_MAX = FLOW_DURATION = 4294967295
PORT_MAX = PROTO_7_MAX = 65535

PROTO_MAX = TCP_FLAG_MAX = 256
PROTO_MAP = {'HOPOPT': 0, 'ICMP': 1, 'IGMP': 2, 'GGP': 3, 'IPV4': 4, 'ST': 5, 'TCP': 6, 'CBT': 7, 'EGP': 8, 'IGP': 9, 'BBN-RCC-MON': 10, 'NVP-II': 11, 'PUP': 12, 'ARGUS (DEPRECATED)': 13, 'EMCON': 14, 'XNET': 15, 'CHAOS': 16, 'UDP': 17, 'MUX': 18, 'DCN-MEAS': 19, 'HMP': 20, 'PRM': 21, 'XNS-IDP': 22, 'TRUNK-1': 23, 'TRUNK-2': 24, 'LEAF-1': 25, 'LEAF-2': 26, 'RDP': 27, 'IRTP': 28, 'ISO-TP4': 29, 'NETBLT': 30, 'MFE-NSP': 31, 'MERIT-INP': 32, 'DCCP': 33, '3PC': 34, 'IDPR': 35, 'XTP': 36, 'DDP': 37, 'IDPR-CMTP': 38, 'TP++': 39, 'IL': 40, 'IPV6': 41, 'SDRP': 42, 'IPV6-ROUTE': 43, 'IPV6-FRAG': 44, 'IDRP': 45, 'RSVP': 46, 'GRE': 47, 'DSR': 48, 'BNA': 49, 'ESP': 50, 'AH': 51, 'I-NLSP': 52, 'SWIPE': 53, 'NARP': 54, 'MOBILE': 55, 'TLSP': 56, 'SKIP': 57, 'IPV6-ICMP': 58, 'IPV6-NONXT': 59, 'IPV6-OPTS': 60, '': 145, 'CFTP': 62, 'SAT-EXPAK': 64, 'KRYPTOLAN': 65, 'RVD': 66, 'IPPC': 67, 'SAT-MON': 69, 'VISA': 70, 'IPCV': 71, 'CPNX': 72, 'CPHB': 73, 'WSN': 74, 'PVP': 75, 'BR-SAT-MON': 76, 'SUN-ND': 77, 'WB-MON': 78, 'WB-EXPAK': 79, 'ISO-IP': 80, 'VMTP': 81, 'SECURE-VMTP': 82, 'VINES': 83, 'TTP': 84, 'IPTM': 85, 'NSFNET-IGP': 86, 'DGP': 87, 'TCF': 88, 'EIGRP': 89, 'OSPFIGP': 90, 'SPRITE-RPC': 91, 'LARP': 92, 'MTP': 93, 'AX.25': 94, 'IPIP': 95, 'MICP (DEPRECATED)': 96, 'SCC-SP': 97, 'ETHERIP': 98, 'ENCAP': 99, 'GMTP': 101, 'IFMP': 102, 'PNNI': 103, 'PIM': 104, 'ARIS': 105, 'SCPS': 106, 'QNX': 107, 'A/N': 108, 'IPCOMP': 109, 'SNP': 110, 'COMPAQ-PEER': 111, 'IPX-IN-IP': 112, 'VRRP': 113, 'PGM': 114, 'L2TP': 116, 'DDX': 117, 'IATP': 118, 'STP': 119, 'SRP': 120, 'UTI': 121, 'SMP': 122, 'SM (DEPRECATED)': 123, 'PTP': 124, 'ISIS OVER IPV4': 125, 'FIRE': 126, 'CRTP': 127, 'CRUDP': 128, 'SSCOPMCE': 129, 'IPLT': 130, 'SPS': 131, 'PIPE': 132, 'SCTP': 133, 'FC': 134, 'RSVP-E2E-IGNORE': 135, 'MOBILITY HEADER': 136, 'UDPLITE': 137, 'MPLS-IN-IP': 138, 'MANET': 139, 'HIP': 140, 'SHIM6': 141, 'WESP': 142, 'ROHC': 143, 'ETHERNET': 144}

v92ipfix = {
    "IPV4_SRC_ADDR":"source_ipv4_address",
    "IPV4_DST_ADDR":"destination_ipv4_address",
    "L4_SRC_PORT":"source_transport_port",
    "L4_DST_PORT":"destination_transport_port",
    "PROTOCOL":"protocol_identifier",
    "L7_PROTO":"ixia_l7_app_id",
    "IN_BYTES":"octet_delta_count",
    "OUT_BYTES":"post_octet_delta_count",
    "IN_PKTS":"packet_delta_count",
    "OUT_PKTS":"post_packet_delta_count",
    "TCP_FLAGS":"tcp_control_bits",
    "FLOW_DURATION_MILLISECONDS":"flow_duration_milliseconds",
}

features = ['IPV4_SRC_ADDR', 'L4_SRC_PORT', 'IPV4_DST_ADDR', 'L4_DST_PORT', 'PROTOCOL', 'L7_PROTO', 'IN_BYTES', 'OUT_BYTES', 'IN_PKTS', 'OUT_PKTS', 'TCP_FLAGS', 'FLOW_DURATION_MILLISECONDS']

class ModelConfig():
  def __init__(self):
    self.n_layer = 2
    self.hidd_size1 = 128
    self.hidd_size2 = 32

class TrainConfig():  
  def __init__(self):
    self.epoch = 20
    self.lr = 1e-2
    self.batch_size = 25

class Config():
  def __init__(self):
    self.feature_size = 12
    self.out_size = 1
    self.seq_length = 64
    
    self.num_round = 100
    self.num_client = 10

    self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    self.model_config = ModelConfig()
    self.model_config.feature_size = self.feature_size
    self.model_config.out_size = self.out_size
    self.model_config.device = self.device

    self.train_config = TrainConfig()
    self.train_config.device = self.device
    self.batch_size = self.train_config.batch_size
    self.train_config.n_layer =  self.model_config.n_layer
    self.train_config.hidd_size1 = self.model_config.hidd_size1

    self.root_checkpoint_dir = "./checkpoint/"

    self.version = "RNN_DNN_v1.0"

fea2sca = {
  'IPV4_SRC_ADDR': lambda ip: np.float64(sum([int(x) << 8*i for i,x in enumerate(reversed(ip.split('.')))]))/IP_MAX,
  'IPV4_DST_ADDR': lambda ip: np.float64(sum([int(x) << 8*i for i,x in enumerate(reversed(ip.split('.')))]))/IP_MAX,
  'L4_SRC_PORT': lambda port: np.float64(port)/PORT_MAX,
  'L4_DST_PORT': lambda port: np.float64(port)/PORT_MAX,
  'PROTOCOL': lambda proto: np.float64(proto)/PROTO_MAX,
  'L7_PROTO': lambda l7_proto:  np.float64(l7_proto)/PROTO_7_MAX,
  'IN_BYTES': lambda in_b: np.float64(in_b)/BYTES_MAX,
  'OUT_BYTES': lambda out_b: np.float64(out_b)/BYTES_MAX,
  'IN_PKTS': lambda in_p: np.float64(in_p)/PKTS_MAX,
  'OUT_PKTS': lambda out_p: np.float64(out_p)/PKTS_MAX,
  'TCP_FLAGS': lambda tcp_f: np.float64(tcp_f)/TCP_FLAG_MAX,
  'FLOW_DURATION_MILLISECONDS': lambda flow_duration: np.float64(flow_duration)/FLOW_DURATION,
}

