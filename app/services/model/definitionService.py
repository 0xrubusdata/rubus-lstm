import torch.nn as nn

class LSTMModel(nn.Module):
    # Your LSTMModel class from the script
    def __init__(self, input_size, hidden_layer_size, num_layers, output_size=1, dropout=0.2):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size
        self.linear_1 = nn.Linear(input_size, hidden_layer_size)
        self.relu = nn.ReLU()
        self.lstm = nn.LSTM(hidden_layer_size, hidden_size=hidden_layer_size, num_layers=num_layers, batch_first=True)
        self.dropout = nn.Dropout(dropout)
        self.linear_2 = nn.Linear(num_layers * hidden_layer_size, output_size)

    def forward(self, x):
        batchsize = x.shape[0]
        x = self.linear_1(x)
        x = self.relu(x)
        lstm_out, (h_n, c_n) = self.lstm(x)
        x = h_n.permute(1, 0, 2).reshape(batchsize, -1)
        x = self.dropout(x)
        return self.linear_2(x)[:, -1]

class DefinitionService:
    @staticmethod
    def define_lstm_model(input_size, hidden_layer_size, num_layers, dropout):
        return LSTMModel(input_size, hidden_layer_size, num_layers, dropout=dropout)

definition_service = DefinitionService()