import torch.nn as nn

class RNN_DNN(nn.Module):
  def __init__(self, config):
    super(RNN_DNN,self).__init__()
    self.gru = nn.GRU(input_size=config.feature_size, hidden_size=config.hidd_size1, num_layers=config.n_layer,batch_first=True)
    self.fc1 = nn.Linear(in_features=config.hidd_size1, out_features=config.hidd_size2)
    self.relu = nn.ReLU()
    self.fc2 = nn.Linear(in_features=config.hidd_size2, out_features=config.out_size)
    self.sig = nn.Sigmoid()
  
  def forward(self, x, hid):
    self.gru.flatten_parameters()

    out, hid = self.gru(x, hid)
    out = self.fc1(out)
    out = self.relu(out)
    out = self.fc2(out)
    predict = self.sig(out)
    return predict, hid
  
  def initialize_model_weights_(self):
    for m in self.modules():
      if type(m) in [nn.GRU, nn.LSTM, nn.RNN]:
        for name, param in m.named_parameters():
          if 'weight_ih' in name:
            nn.init.xavier_uniform_(param.data)
          elif 'weight_hh' in name:
            nn.init.orthogonal_(param.data)
          elif 'bias' in name:
            param.data.fill_(0)
      elif isinstance(m, nn.Linear):
        nn.init.xavier_uniform_(m.weight)
        if m.bias is not None:
          nn.init.constant_(m.bias, 0)